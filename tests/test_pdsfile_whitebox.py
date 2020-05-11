import pdsfile
import pytest
import settings

PDS_DATA_DIR = settings.PDS_DATA_DIR
TESTFILE_PATH = settings.TESTFILE_PATH

################################################################################
# PdsFile Whitebox test
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
        print(target_pdsfile.abspath)
        assert target_pdsfile.exists == False

    def test_absolute_or_logical_path_2(self):
        """absolute_or_logical_path: get logical path."""
        target_pdsfile = pdsfile.PdsFile.new_virtual('volumes')
        expected = 'volumes'
        assert target_pdsfile.absolute_or_logical_path == expected
