import os
import pdsfile
import pdsviewable
import pytest

from tests.helper import instantiate_target_pdsfile

PDS_DATA_DIR = os.environ['PDS_DATA_DIR']

################################################################################
# Whitebox test for functions & properties in PdsFile class
################################################################################
class TestPdsFileWhiteBox:
    def test_exists_1(self):
        # Note: line 1015, the path will never be hit.
        target_pdsfile = pdsfile.PdsFile.new_virtual('volumes')
        assert target_pdsfile.exists == True

    def test_exists_2(self):
        # Note: line 1016, find the case where self.abspath is None &
        # self.is_virtual is False
        target_pdsfile = pdsfile.PdsFile()
        assert target_pdsfile.is_virtual == False
        target_pdsfile.abspath = None
        assert target_pdsfile.exists == False

    def test_isdir_1(self):
        # Note: similar to test_exists_1
        target_pdsfile = pdsfile.PdsFile.new_virtual('volumes')
        expected = 'volumes'
        assert target_pdsfile.isdir == True

    def test_isdir_2(self):
        # Note: similar to test_exists_2
        target_pdsfile = pdsfile.PdsFile()
        assert target_pdsfile.is_virtual == False
        target_pdsfile.abspath = None
        assert target_pdsfile.isdir == False

    def test_absolute_or_logical_path(self):
        """absolute_or_logical_path: get logical path."""
        target_pdsfile = pdsfile.PdsFile.new_virtual('volumes')
        expected = 'volumes'
        assert target_pdsfile.absolute_or_logical_path == expected
