import os
import pdsfile
import pytest
import settings
import sys

PDS_DATA_DIR = settings.PDS_DATA_DIR
TESTFILE_PATH = settings.TESTFILE_PATH

################################################################################
# Whitebox test
################################################################################
class TestWhiteBox:
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
