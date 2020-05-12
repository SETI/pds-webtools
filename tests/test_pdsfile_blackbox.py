import pdsfile
import pdsviewable
import pytest
import settings

from tests.helper import instantiate_target_pdsfile

PDS_DATA_DIR = settings.PDS_DATA_DIR
TESTFILE_PATH = settings.TESTFILE_PATH

################################################################################
# PdsFile Blackbox test
################################################################################
class TestPdsFileBlackBox:
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
            ('volumes/COISS_0xxx', '')
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
        """islabel: test on one label and one non label files."""
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

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COVIMS_0xxx/COVIMS_0001/data/' \
            '1999010T054026_1999010T060958/v1294638283_1.lbl',
            'PDS3 label'),
            ('previews/COVIMS_0xxx/COVIMS_0001/data/' \
            '1999010T054026_1999010T060958/v1294638283_1_thumb.png',
            'Thumbnail preview image')
        ]
    )
    def test_description(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.description == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COVIMS_8xxx/COVIMS_8001/data/' \
            'VIMS_2017_251_GAMCRU_I_TAU_10KM.lbl', 'LABEL'),
            ('volumes/COVIMS_8xxx/COVIMS_8001/data/' \
            'VIMS_2017_251_GAMCRU_I_TAU_10KM.tab', 'TABLE'),
            ('volumes/COVIMS_8xxx', 'VOLDIR'),
            ('volumes/COVIMS_0xxx/COVIMS_0001', 'VOLUME'),
            ('metadata/COVIMS_0xxx/COVIMS_0001/COVIMS_0001_index.tab',
            'INDEX'),
            ('previews/COVIMS_0xxx', 'BROWDIR'),
            ('previews/COVIMS_0xxx/COVIMS_0001', 'BROWDIR'),
            ('previews/COVIMS_0xxx/COVIMS_0001/data' \
            '1999010T054026_1999010T060958/v1294638283_1_thumb.png', 'BROWSE'),
            ('metadata/COVIMS_0xxx/COVIMS_0001', 'INDEXDIR')
        ]
    )
    def test_icon_type(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.icon_type == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/EBROCC_xxxx/EBROCC_0001/DATA/ESO1M/ES1_EPD.tab',
            'ES1_EPD.lbl'),
            ('volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/' \
            'HDAC1999_007_16_31.dat',
            'HDAC1999_007_16_31.lbl'),
            ('previews/COISS_3xxx/COISS_3002/data/maps/' \
            'SE_400K_0_108_SMN_thumb.png',
            '')
        ]
    )
    def test_label_basename(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.label_basename == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R.IMG',
            PDS_DATA_DIR + 'volumes/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R.LBL'),
            ('volumes/GO_0xxx/GO_0017/J0/OPNAV', ''),
            ('metadata/GO_0xxx/GO_0017/GO_0017_index.tab',
            PDS_DATA_DIR + 'metadata/GO_0xxx/GO_0017/GO_0017_index.lbl'),
            ('previews/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R_med.jpg', '')
        ]
    )
    def test_label_abspath(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.label_abspath == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/HSTIx_xxxx/HSTI1_1556/DATA/VISIT_01/IB4W01I5Q.lbl',
            [
                'HST WFC3 images of the Pluto system    2010-04-24 to 2010-09-06',
                'VOLUME'
            ]),
            ('previews/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R_med.jpg',
            [
                'Galileo Jupiter images 1996-06-03 to 1996-12-14T' \
                ' (SC clock 03464059-03740374)',
                'VOLUME'
            ]),
            ('metadata/COVIMS_0xxx/COVIMS_0001',
            [
                'Cassini VIMS near IR image cubes 1999-01-10 to 2000-09-18 ' \
                '(SC clock 1294638283-1347975444)',
                'VOLUME'
            ])

        ]
    )
    def test__volume_info(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile._volume_info[0] == expected[0]
        assert target_pdsfile._volume_info[1] == expected[1]

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/HSTNx_xxxx/HSTN0_7176/DATA/VISIT_01/N4BI01L4Q.lbl',
            'hst-07176-nicmos-n4bi01l4q'),
            ('volumes/HSTJx_xxxx/HSTJ0_9296/DATA/VISIT_B1/J8M3B1021.lbl',
            'hst-09296-acs-j8m3b1021'),
            ('volumes/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R.lbl',
            'go-ssi-c0346405900')
        ]
    )
    def test_opus_id(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.opus_id == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/HSTJx_xxxx/HSTJ0_9296/DATA/VISIT_B1/J8M3B1021.asc', False),
            ('previews/HSTJx_xxxx/HSTJ0_9296/DATA/VISIT_B1/J8M3B1021_thumb.jpg',
            True)
        ]
    )
    def test_is_viewable(self, input_path, expected):
        """is_viewable: test on one image and one non image files."""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.is_viewable == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('previews/HSTOx_xxxx/HSTO0_7308/DATA/VISIT_05/O43B05C1Q_small.jpg',
            'O43B05C1Q_small.jpg'),
            ('volumes/HSTOx_xxxx/HSTO0_7308/DATA/VISIT_05/O43B05C1Q.lbl', '')
        ]
    )
    def test_alt(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.alt == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('previews/HSTOx_xxxx/HSTO0_7308/DATA/VISIT_05/O43B05C1Q_small.jpg',
            pdsviewable.PdsViewSet),
            ('volumes/HSTOx_xxxx/HSTO0_7308/DATA/VISIT_05/O43B05C1Q.lbl', None)
        ]
    )
    def test_viewset(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        if expected is not None:
            assert isinstance(target_pdsfile.viewset, expected)

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/HSTUx_xxxx/HSTU0_5167/DATA/VISIT_04', True),
            ('volumes/NHSP_xxxx/NHSP_1000/DATA/CK/MERGED_NHPC_2006_V011.LBL',
            False)
        ]
    )
    def test_isdir(self, input_path, expected):
        """isdir: test on one directory and one label file."""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.isdir == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/' \
            'lor_0003103486_0x630_eng.lbl', []),
            ('volumes/NHxxLO_xxxx/NHLALO_1001',
            [
                'aareadme.txt', 'calib', 'catalog', 'data',
                'document', 'index', 'voldesc.cat'
            ])
        ]
    )
    def test_childnames(self, input_path, expected):
        """childnames: test on one directory and one label file."""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.childnames == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('metadata/NHxxMV_xxxx/NHLAMV_1001/NHLAMV_1001_index.tab', True),
            ('volumes/NHxxMV_xxxx/NHLAMV_1001/index/index.tab', True),
            ('volumes/NHxxMV_xxxx/NHLAMV_1001/data/20060321_000526/' \
            'mc0_0005261846_0x536_eng_1.lbl', False)
        ]
    )
    def test_is_index(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.is_index == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COUVIS_0xxx/COUVIS_0058/DATA/D2017_001/' \
            'EUV2017_001_03_49.LBL',
            [
                PDS_DATA_DIR + 'volumes/COUVIS_0xxx/COUVIS_0058/CALIB/' \
                'VERSION_5/D2017_001/EUV2017_001_03_49_CAL_5.DAT',
                PDS_DATA_DIR + 'volumes/COUVIS_0xxx/COUVIS_0058/DATA/' \
                'D2017_001/EUV2017_001_03_49.LBL',
                PDS_DATA_DIR + 'volumes/COUVIS_0xxx/COUVIS_0058/DATA/' \
                'D2017_001/EUV2017_001_03_49.DAT',
                PDS_DATA_DIR + 'volumes/COUVIS_0xxx/COUVIS_0058/CALIB/' \
                'VERSION_5/D2017_001/EUV2017_001_03_49_CAL_5.LBL',
                PDS_DATA_DIR + 'volumes/COUVIS_0xxx/COUVIS_0058/CALIB/' \
                'VERSION_4/D2017_001/EUV2017_001_03_49_CAL_4.LBL',
                PDS_DATA_DIR + 'volumes/COUVIS_0xxx/COUVIS_0058/CALIB/' \
                'VERSION_4/D2017_001/EUV2017_001_03_49_CAL_4.DAT'
            ]),
            ('volumes/COUVIS_0xxx/COUVIS_0058/DATA',
            [
                PDS_DATA_DIR + 'volumes/COUVIS_0xxx/COUVIS_0058/DATA',
                PDS_DATA_DIR + 'volumes/COUVIS_0xxx/COUVIS_0058/CALIB/VERSION_5',
                PDS_DATA_DIR + 'volumes/COUVIS_0xxx/COUVIS_0058/CALIB/VERSION_4',
            ]),
        ]
    )
    def test_associated_abspaths(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        target_associated_abspaths = target_pdsfile.associated_abspaths(
            'volumes')
        for path in expected:
            assert path in target_associated_abspaths

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/' \
            'FUV1999_007_16_57.DAT',
            [
                'volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/' \
                'FUV1999_007_16_57.DAT',
                'volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/' \
                'FUV1999_007_16_57.LBL',
                'volumes/COUVIS_0xxx/COUVIS_0001/CALIB/VERSION_3/D1999_007/' \
                'FUV1999_007_16_57_CAL_3.DAT',
                'volumes/COUVIS_0xxx/COUVIS_0001/CALIB/VERSION_3/D1999_007/' \
                'FUV1999_007_16_57_CAL_3.LBL'
            ]),
            # Check if the last "/" is ignored
            ('volumes/COUVIS_0xxx/COUVIS_0001/DATA/',
            [
                'volumes/COUVIS_0xxx/COUVIS_0001/DATA',
                'volumes/COUVIS_0xxx/COUVIS_0001/CALIB/VERSION_3'
            ]),
        ]
    )
    def test_associated_logical_paths(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        target_associated_logical_paths = target_pdsfile.associated_logical_paths(
            'volumes')
        for path in expected:
            assert path in target_associated_logical_paths
