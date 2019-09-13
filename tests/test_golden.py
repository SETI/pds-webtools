import os

from contextlib import closing
import pytest
import sqlite3

from pdsfile import preload, PdsFile, use_pickles
from tests.golden_files import FILES
from tests.golden_attributes import ATTRIBUTES, get_attribute_as_string

_PICKLES = int(os.getenv('PDS_WEBTOOLS_USE_PICKLES', '0'))
_USE_PICKLES = _PICKLES == 1
_TEST_DIR = os.getenv('PDS_WEBTOOLS_TEST_DIR')


@pytest.fixture(scope='module')
def db_connection():
    use_pickles(status=_USE_PICKLES)
    preload(os.path.join(_TEST_DIR, 'holdings'))
    with closing(sqlite3.connect('tests/golden.db')) as conn:
        yield conn

@pytest.mark.parametrize('file, key',
                         [(file, attr)
                          for file in FILES
                          for attr in ATTRIBUTES])
def test_golden_stuff(db_connection, file, key):
    abspath = os.path.abspath(os.path.join(_TEST_DIR, file))
    pdsfile = PdsFile.from_abspath(abspath)
    with closing(db_connection.cursor()) as c:
        calculated = get_attribute_as_string(pdsfile, key)
        expected = list(c.execute(
                'SELECT value FROM golden WHERE pickles=? AND file=? AND key=?',
                (_PICKLES, file, key)))[0][0]
        assert expected == calculated, repr((_PICKLES, file, key,
                                             expected, calculated))

        if False:
            # Now see if it has a cached value
            cached_key = '_%s_filled' % key
            if hasattr(pdsfile, cached_key):
                cached = get_attribute_as_string(pdsfile, cached_key)
                assert expected == cached, \
                    repr(('PICKLES' if _USE_PICKLES else 'NO-PICKLES',
                          file, cached_key))


def test_other_stuff():
    assert not _USE_PICKLES
