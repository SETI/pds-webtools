import pdsgroup

import pytest

from pdsfile.pds3file.tests.helper import get_pdsfiles

##########################################################################################
# Whitebox test for functions & properties in PdsGroup class
##########################################################################################
class TestPdsGroupWhiteBox:
    @pytest.mark.parametrize(
        'input_paths,expected',
        [
            (['volumes/COISS_0xxx'], 'volumes'),

        ]
    )
    def test_parent_logical_path(self, input_paths, expected):
        pdsfiles = get_pdsfiles(input_paths)
        target_pdsgroup = pdsgroup.PdsGroup(pdsfiles=pdsfiles)
        res = target_pdsgroup.parent_logical_path
        assert res == expected
