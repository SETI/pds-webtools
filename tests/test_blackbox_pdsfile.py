import os
import pdsfile
import pytest
import settings
import sys

PDS_DATA_DIR = settings.PDS_DATA_DIR
TESTFILE_PATH = settings.TESTFILE_PATH

def instantiate_target_pdsfile(path, is_abspath=True):
    if is_abspath:
        TESTFILE_PATH = PDS_DATA_DIR + path
        target_pdsfile = pdsfile.PdsFile.from_abspath(TESTFILE_PATH)
    else:
        TESTFILE_PATH = path
        target_pdsfile = pdsfile.PdsFile.from_logical_path(TESTFILE_PATH)
    return target_pdsfile

################################################################################
# Blackbox test
################################################################################
class TestBlackBox:
    def test_exists_1(self):
        target_pdsfile = instantiate_target_pdsfile(
            '/volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.DAT')
        assert target_pdsfile.exists == True

    def test_exists_2(self):
        target_pdsfile = instantiate_target_pdsfile(
            '/volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.IMG')
        assert target_pdsfile.exists == False

    def test_islabel_1(self):
        target_pdsfile = instantiate_target_pdsfile(
            '/volumes/COCIRS_1xxx/COCIRS_1001/DATA/TSDR/NAV_DATA/TAR10013100.lbl')
        assert target_pdsfile.islabel == True

    def test_islabel_2(self):
        target_pdsfile = instantiate_target_pdsfile(
            '/volumes/COCIRS_5xxx/COCIRS_5401/DATA/GEODATA/GEO0401130240_699.tab')
        assert target_pdsfile.islabel == False

    def test_absolute_or_logical_path_1(self):
        file_path = '/diagrams/COCIRS_5xxx/COCIRS_5401/BROWSE/TARGETS/' \
            'IMG0401130240_FP1_thumb.jpg'
        expected = PDS_DATA_DIR + file_path
        target_pdsfile = instantiate_target_pdsfile(file_path)
        assert target_pdsfile.absolute_or_logical_path == expected

    def test_absolute_or_logical_path_2(self):
        expected = 'volumes'
        target_pdsfile = pdsfile.PdsFile.new_virtual('volumes')
        assert target_pdsfile.absolute_or_logical_path == expected

    def test_html_path(self):
        file_path = '/diagrams/COCIRS_6xxx/COCIRS_6004/BROWSE/SATURN/' \
            'POI1004010000_FP1_small.jpg'
        target_pdsfile = instantiate_target_pdsfile(file_path)
        expected = 'holdings' + file_path
        assert target_pdsfile.html_path == expected
