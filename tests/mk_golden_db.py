import getopt
import os
import sys

import sqlite3

from pdsfile import preload, PdsFile, use_pickles
from tests.golden_attributes import ATTRIBUTES, get_attribute_as_string
from tests.golden_files import FILES

_PICKLES = int(os.getenv('PDS_WEBTOOLS_USE_PICKLES', '0'))
_USE_PICKLES = _PICKLES == 1
_TEST_DIR = os.getenv('PDS_WEBTOOLS_TEST_DIR', None)

def mk_database(c):
    use_pickles(status=_USE_PICKLES)
    preload(os.path.join(_TEST_DIR, 'holdings'))
    with open('golden_cache_errors.txt', 'a') as f:
        for file in FILES:
            abspath = os.path.abspath(os.path.join(_TEST_DIR, file))
            pdsfile = PdsFile.from_abspath(abspath)
            for k in sorted(ATTRIBUTES):
                r = get_attribute_as_string(pdsfile, k)
                sql = '''INSERT INTO golden(pickles, file, key, value)
			 VALUES (?,?,?,?);'''
                c.execute(sql, (_PICKLES, file, k, r))

                cached_k = '_%s_filled' % k
                if hasattr(pdsfile, cached_k):
                    cached_r = get_attribute_as_string(pdsfile, k)
                    if r == cached_r:
                        pass
                    else:
                        f.write('%s: %s=%s; %s=%s' %
                                (file, k, r, cached_k, cached_r))


def make_db():
    exists = os.path.exists('tests/golden.db')
    conn = sqlite3.connect('tests/golden.db')
    c = conn.cursor()
    if not exists:
        c.execute('''CREATE TABLE golden (
                         pickles boolean NOT NULL,
                         file text NOT NULL,
                         key text NOT NULL,
                         value text NOT NULL);''')
        c.execute(
            'CREATE INDEX golden_pickles_file_key '
            'ON golden(pickles, file, key)')
        conn.commit()
    
    mk_database(c)
    conn.commit()


    # os.system('touch tests/golden.db')
