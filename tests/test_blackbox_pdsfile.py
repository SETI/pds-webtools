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
    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.DAT',
            True),
            ('volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.IMG',
            False)
        ]
    )
    def test_exists(self, input_path, expected):
        """exists: test on one existing and one non exising file."""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.exists == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('diagrams/COCIRS_5xxx/COCIRS_5401/BROWSE/TARGETS/' \
            'IMG0401130240_FP1_thumb.jpg', 'COCIRS_5401/BROWSE/TARGETS/' \
            'IMG0401130240_FP1_thumb.jpg'),
            ('volumes/COISS_0xxx/COISS_0001', 'COISS_0001'),
            ('volumes/COISS_0xxx', ''),
        ]
    )
    def test_filespec(self, input_path, expected):
        """filespec: test on a file and one directory."""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.filespec == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COCIRS_1xxx/COCIRS_1001/DATA/TSDR/NAV_DATA/TAR10013100.lbl',
            True),
            ('volumes/COCIRS_5xxx/COCIRS_5401/DATA/GEODATA/GEO0401130240_699.tab',
            False)
        ]
    )
    def test_islabel(self, input_path, expected):
        """islabel: test on one label and one non label file."""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.islabel == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('diagrams/COCIRS_5xxx/COCIRS_5401/BROWSE/TARGETS/' \
            'IMG0401130240_FP1_thumb.jpg',
            PDS_DATA_DIR + 'diagrams/COCIRS_5xxx/COCIRS_5401/BROWSE/TARGETS/' \
            'IMG0401130240_FP1_thumb.jpg'),
            ('volumes', PDS_DATA_DIR + 'volumes')
        ]
    )
    def test_absolute_or_logical_path(self, input_path, expected):
        """absolute_or_logical_path: get abspath."""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        expected = PDS_DATA_DIR + input_path if expected is None else expected
        assert target_pdsfile.absolute_or_logical_path == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('diagrams/COCIRS_6xxx/COCIRS_6004/BROWSE/SATURN/' \
            'POI1004010000_FP1_small.jpg',
            'holdings/diagrams/COCIRS_6xxx/COCIRS_6004/BROWSE/SATURN/' \
            'POI1004010000_FP1_small.jpg'),
            ('volumes/COISS_1xxx/COISS_1001',
            'holdings/volumes/COISS_1xxx/COISS_1001')
        ]
    )
    def test_html_path(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        expected = 'holdings/' + input_path if expected is None else expected
        assert target_pdsfile.html_path == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COISS_3xxx/COISS_3002/data/maps/SE_400K_90S_0_SMN.lbl',
            '.lbl'),
            ('volumes/COISS_3xxx/COISS_3002/data/maps/', '')
        ]
    )
    def test_extension(self, input_path, expected):
        """extension: test on one file and one directory."""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        try:
            dot_idx = input_path.rindex('.')
        except ValueError:
            dot_idx = None

        if expected is None:
            expected = input_path[dot_idx:] if dot_idx else ''
        assert target_pdsfile.extension == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COISS_3xxx/COISS_3002/data',
            'volumes/COISS_3xxx/COISS_3002'),
            ('volumes/COISS_2xxx/COISS_2002/data/1460960653_1461048959/' \
            'N1460960868_1.IMG',
            'volumes/COISS_2xxx/COISS_2002/data/1460960653_1461048959')
        ]
    )
    def test_parent_logical_path(self, input_path, expected):
        """parent_logical_path: test on one file and one directory."""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        input_path = input_path[:-1] if input_path[-1] == '/' else input_path
        try:
            slash_idx = input_path.rindex('/')
        except ValueError:
            slash_idx = None

        if expected is None:
            expected = input_path[:slash_idx] if slash_idx else ''
        assert target_pdsfile.parent_logical_path == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/' \
            'HDAC1999_007_16_31_thumb.png',
            'HDAC1999_007_16_31'),
            ('volumes/COUVIS_8xxx/COUVIS_8001/data/' \
            'UVIS_HSP_2017_228_BETORI_I_TAU10KM.lbl',
            'UVIS_HSP_2017_228_BETORI_I_TAU10KM'),
            ('volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/' \
            'Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_CAL.tab',
            'RSS_2005_123_K34_E_CAL')
        ]
    )
    def test_anchor(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.anchor == expected
