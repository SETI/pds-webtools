import os
import pdsfile
import pdsviewable
import pytest

from tests.helper import instantiate_target_pdsfile

PDS_DATA_DIR = os.environ['PDS_DATA_DIR']
PDS_PDSDATA_PATH = PDS_DATA_DIR[:PDS_DATA_DIR.index('holdings')]
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
            ('diagrams/COCIRS_5xxx/COCIRS_5401/BROWSE/TARGETS/IMG0401130240_FP1_thumb.jpg',
             'COCIRS_5401/BROWSE/TARGETS/IMG0401130240_FP1_thumb.jpg'),
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
            ('diagrams/COCIRS_5xxx/COCIRS_5401/BROWSE/TARGETS/IMG0401130240_FP1_thumb.jpg',
             PDS_DATA_DIR + 'diagrams/COCIRS_5xxx/COCIRS_5401/BROWSE/TARGETS/IMG0401130240_FP1_thumb.jpg'),
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
            ('diagrams/COCIRS_6xxx/COCIRS_6004/BROWSE/SATURN/POI1004010000_FP1_small.jpg',
             'holdings/diagrams/COCIRS_6xxx/COCIRS_6004/BROWSE/SATURN/POI1004010000_FP1_small.jpg'),
            ('volumes/COISS_1xxx/COISS_1001', 'holdings/volumes/COISS_1xxx/COISS_1001')
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
            ('volumes/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460960868_1.IMG',
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
            ('previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
             'HDAC1999_007_16_31'),
            ('volumes/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2017_228_BETORI_I_TAU10KM.lbl',
             'UVIS_HSP_2017_228_BETORI_I_TAU10KM'),
            ('volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_CAL.tab',
             'RSS_2005_123_K34_E_CAL')
        ]
    )
    def test_anchor(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.anchor == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COVIMS_0xxx/COVIMS_0001/data/1999010T054026_1999010T060958/v1294638283_1.lbl',
             'PDS3 label'),
            ('previews/COVIMS_0xxx/COVIMS_0001/data/1999010T054026_1999010T060958/v1294638283_1_thumb.png',
             'Thumbnail preview image')
        ]
    )
    def test_description(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.description == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COVIMS_8xxx/COVIMS_8001/data/VIMS_2017_251_GAMCRU_I_TAU_10KM.lbl', 'LABEL'),
            ('volumes/COVIMS_8xxx/COVIMS_8001/data/VIMS_2017_251_GAMCRU_I_TAU_10KM.tab', 'TABLE'),
            ('volumes/COVIMS_8xxx', 'VOLDIR'),
            ('volumes/COVIMS_0xxx/COVIMS_0001', 'VOLUME'),
            ('metadata/COVIMS_0xxx/COVIMS_0001/COVIMS_0001_index.tab', 'INDEX'),
            ('previews/COVIMS_0xxx', 'BROWDIR'),
            ('previews/COVIMS_0xxx/COVIMS_0001', 'BROWDIR'),
            ('previews/COVIMS_0xxx/COVIMS_0001/data1999010T054026_1999010T060958/v1294638283_1_thumb.png',
             'BROWSE'),
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
            ('volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31.dat',
             'HDAC1999_007_16_31.lbl'),
            ('previews/COISS_3xxx/COISS_3002/data/maps/SE_400K_0_108_SMN_thumb.png', '')
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
                'Galileo Jupiter images 1996-06-03 to 1996-12-14T (SC clock 03464059-03740374)',
                'VOLUME'
             ]),
            ('metadata/COVIMS_0xxx/COVIMS_0001',
             [
                'Cassini VIMS near IR image cubes 1999-01-10 to 2000-09-18 (SC clock 1294638283-1347975444)',
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
            ('volumes/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/'
             + 'lor_0003103486_0x630_eng.lbl', []),
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
            ('volumes/NHxxMV_xxxx/NHLAMV_1001/data/20060321_000526/mc0_0005261846_0x536_eng_1.lbl',
             False)
        ]
    )
    def test_is_index(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.is_index == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COUVIS_0xxx/COUVIS_0058/DATA/D2017_001/EUV2017_001_03_49.LBL',
             [
                PDS_DATA_DIR + 'volumes/COUVIS_0xxx/COUVIS_0058/CALIB/VERSION_5/D2017_001/EUV2017_001_03_49_CAL_5.DAT',
                PDS_DATA_DIR + 'volumes/COUVIS_0xxx/COUVIS_0058/DATA/D2017_001/EUV2017_001_03_49.LBL',
                PDS_DATA_DIR + 'volumes/COUVIS_0xxx/COUVIS_0058/DATA/D2017_001/EUV2017_001_03_49.DAT',
                PDS_DATA_DIR + 'volumes/COUVIS_0xxx/COUVIS_0058/CALIB/VERSION_5/D2017_001/EUV2017_001_03_49_CAL_5.LBL',
                PDS_DATA_DIR + 'volumes/COUVIS_0xxx/COUVIS_0058/CALIB/VERSION_4/D2017_001/EUV2017_001_03_49_CAL_4.LBL',
                PDS_DATA_DIR + 'volumes/COUVIS_0xxx/COUVIS_0058/CALIB/VERSION_4/D2017_001/EUV2017_001_03_49_CAL_4.DAT'
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
            ('volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/FUV1999_007_16_57.DAT',
             [
                'volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/FUV1999_007_16_57.DAT',
                'volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/FUV1999_007_16_57.LBL',
                'volumes/COUVIS_0xxx/COUVIS_0001/CALIB/VERSION_3/D1999_007/FUV1999_007_16_57_CAL_3.DAT',
                'volumes/COUVIS_0xxx/COUVIS_0001/CALIB/VERSION_3/D1999_007/FUV1999_007_16_57_CAL_3.LBL'
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

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/FUV1999_007_16_57.DAT',
             'volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/FUV1999_007_16_57.DAT'),
        ]
    )
    def test_associated_parallel(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        target_associated_parallel = target_pdsfile.associated_parallel()
        assert target_associated_parallel.logical_path == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('previews/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_small.jpg',
             pdsviewable.PdsViewSet),
            ('previews/VGISS_5xxx/VGISS_5101/DATA/C13854XX',
             pdsviewable.PdsViewSet),
            ('volumes/VGISS_5xxx/VGISS_5101/DATA/C13854XX',
             pdsviewable.PdsViewSet),
        ]
    )
    def test_viewset_lookup(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        if expected is not None:
            assert isinstance(target_pdsfile.viewset_lookup(), expected)

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('metadata/VGISS_8xxx/VGISS_8201/VGISS_8201_inventory.tab',
             PDS_DATA_DIR + 'metadata/VGISS_8xxx/VGISS_8201'),
            ('metadata/VGISS_6xxx/VGISS_6101',
             PDS_DATA_DIR + 'metadata/VGISS_6xxx/VGISS_6101'),
            ('volumes/VGISS_7xxx/VGISS_7201/DATA/C24476XX/C2447654_RAW.lbl',
             PDS_DATA_DIR + 'volumes/VGISS_7xxx/VGISS_7201')
        ]
    )
    def test_volume_abspath(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.volume_abspath() == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/HSTOx_xxxx/HSTO0_7308/DATA/VISIT_05/O43B05C1Q.asc',
             PDS_DATA_DIR + 'volumes/HSTOx_xxxx'),
            ('previews/HSTNx_xxxx/HSTN0_7176/DATA/VISIT_01/N4BI01L4Q_thumb.jpg',
             PDS_DATA_DIR + 'previews/HSTNx_xxxx')
        ]
    )
    def test_volset_abspath(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.volset_abspath() == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274/EUV2004_274_01_39.lbl',
             (PDS_DATA_DIR + 'checksums-volumes/COUVIS_0xxx_v1/COUVIS_0009_md5.txt', 81)),
            ('metadata/VGISS_5xxx/VGISS_5101/VGISS_5101_supplemental_index.tab',
             (PDS_DATA_DIR + 'checksums-metadata/VGISS_5xxx/VGISS_5101_metadata_md5.txt', 78))
        ]
    )
    def test_checksum_path_and_lskip(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.checksum_path_and_lskip() == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab',
             (PDS_DATA_DIR + 'archives-metadata/HSTUx_xxxx/HSTU0_5167_metadata.tar.gz', 68)),
            ('volumes/EBROCC_xxxx/EBROCC_0001/DATA/ESO1M/ES1_EPD.lbl',
             (PDS_DATA_DIR + 'archives-volumes/EBROCC_xxxx/EBROCC_0001.tar.gz', 68))
        ]
    )
    def test_archive_path_and_lskip(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.archive_path_and_lskip() == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_RAW.lbl',
             (PDS_PDSDATA_PATH + 'shelves/info/volumes/VGISS_5xxx/VGISS_5101_info.shelf', 78)),
            ('metadata/NHxxLO_xxxx/NHLALO_1001/NHLALO_1001_inventory.tab',
             (PDS_PDSDATA_PATH + 'shelves/info/metadata/NHxxLO_xxxx/NHLALO_1001_info.shelf', 81))
        ]
    )
    def test_shelf_path_and_lskip(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.shelf_path_and_lskip() == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COCIRS_5xxx/COCIRS_5401/DATA/GEODATA/GEO0401130240_699.lbl',
             ('GEO0401130240_699', '', '.lbl')),
            ('diagrams/COCIRS_6xxx/COCIRS_6004/BROWSE/SATURN/POI1004010000_FP1_small.jpg',
             ('POI1004010000_FP1', '_small', '.jpg'))
        ]
    )
    def test_split_basename(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.split_basename() == expected

    @pytest.mark.parametrize(
        'input_path,basenames,expected',
        [
            ('volumes/COCIRS_0xxx/COCIRS_0410',
             ['COCIRS_0xxx_v3', 'COCIRS_0xxx', 'COCIRS_0xxx_v2'],
             #  Sort by version number
             ['COCIRS_0xxx', 'COCIRS_0xxx_v3', 'COCIRS_0xxx_v2']),
        ]
    )
    def test_sort_basenames(self, input_path, basenames, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.sort_basenames(basenames=basenames) == expected

    @pytest.mark.parametrize(
        'input_path,logical_paths,expected',
        [
            ('previews/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274',
             [
                'previews/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274/EUV2004_274_09_50_small.png',
                'previews/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274/EUV2004_274_01_39_thumb.png',
                'previews/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274/EUV2004_274_07_10_full.png',
                'previews/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274/EUV2004_274_02_25_med.png',
             ],
             #  Sort by logical_path
             [
                'previews/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274/EUV2004_274_01_39_thumb.png',
                'previews/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274/EUV2004_274_02_25_med.png',
                'previews/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274/EUV2004_274_07_10_full.png',
                'previews/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274/EUV2004_274_09_50_small.png',
             ]),
        ]
    )
    def test_sort_logical_paths(self, input_path, logical_paths, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.sort_logical_paths(logical_paths=logical_paths)
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COVIMS_8xxx/COVIMS_8001/data/VIMS_2017_251_GAMCRU_I_TAU_10KM.tab',
             True),
            (PDS_DATA_DIR + 'metadata/COVIMS_0xxx/COVIMS_0001',
             False),
        ]
    )
    def test_is_logical_path(self, input_path, expected):
        res = pdsfile.is_logical_path(path=input_path)
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            (PDS_DATA_DIR + 'volumes/COUVIS_0xxx/COUVIS_0058/DATA/D2017_001/EUV2017_001_03_49.dat',
             'volumes/COUVIS_0xxx/COUVIS_0058/DATA/D2017_001/EUV2017_001_03_49.dat'),
            ('volumes/COUVIS_0xxx/COUVIS_0058/DATA/D2017_001/EUV2017_001_03_49.dat',
             'volumes/COUVIS_0xxx/COUVIS_0058/DATA/D2017_001/EUV2017_001_03_49.dat'),
        ]
    )
    def test_logical_path_from_abspath(self, input_path, expected):
        try:
            res = pdsfile.logical_path_from_abspath(abspath=input_path)
            assert res == expected
        except ValueError as err:
            assert True # Not an absolute path

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COISS_0xxx/COISS_0001/data/wacfm/bit_wght/13302/133020.lbl',
             True)
        ]
    )
    def test_from_logical_path(self, input_path, expected):
        res = pdsfile.PdsFile.from_logical_path(path=input_path)
        assert isinstance(res, pdsfile.PdsFile)
        assert res.exists == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COISS_0xxx/COISS_0001/data/wacfm/bit_wght/13302/133020.lbl',
             True),
            (PDS_DATA_DIR + 'volumes/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1.lbl',
             True),
        ]
    )
    def test_from_abspath(self, input_path, expected):
        try:
            res = pdsfile.PdsFile.from_abspath(abspath=input_path)
            assert isinstance(res, pdsfile.PdsFile)
            assert res.exists == expected
        except ValueError as err:
            assert True # Not an absolute path

    @pytest.mark.parametrize(
        'input_path,relative_path,expected',
        [
            ('previews/COUVIS_0xxx_v1/COUVIS_0009/DATA',
             '/D2004_274/EUV2004_274_01_39_thumb.png',
             True),
            ('volumes/COUVIS_0xxx/COUVIS_0001',
             '/DATA/D1999_007/FUV1999_007_16_57.LBL',
             True),
            ('volumes/COUVIS_0xxx/COUVIS_0001',
             '/DATAx/D1999_007/FUV1999_007_16_57.LBL',
             False),
        ]
    )
    def test_from_relative_path(self, input_path, relative_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.from_relative_path(path=relative_path)
        assert isinstance(res, pdsfile.PdsFile)
        assert res.exists == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('holdings/volumes/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274/EUV2004_274_01_39.dat',
             True),
            ('COVIMS_0xxx/COVIMS_0001/data/1999010T054026_1999010T060958',
             True),
            ('metadata/HSTOx_xxxx/HSTO0_7308',
             True),

        ]
    )
    def test_from_path(self, input_path, expected):
        res = pdsfile.PdsFile.from_path(path=input_path)
        print(res.abspath)
        assert isinstance(res, pdsfile.PdsFile)
        assert res.exists == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COVIMS_0xxx/COVIMS_0001/data/1999010T054026_1999010T060958/v1294638283_1.lbl',
             ''),
            ('volumes/HSTOx_xxxx/HSTO0_7308/DATA/VISIT_05/O43B05C1Q.lbl',
             ''),
        ]
    )
    # Need to find a better way to test this one.
    def test_opus_products(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.opus_products()
        for key in res:
            for files in res[key]:
                for pdsf in files:
                    assert pdsf.exists == True

    @pytest.mark.parametrize(
        'input_path,selection,expected',
        [
            # ['O43B05C1Q', 'O43B05C3Q', 'O43B06BTQ', 'O43B06BVQ', 'O43B09B3Q', 'O43B09B5Q', 'O43B11D7Q', 'O43B11D8Q', 'O43B12XAQ', 'O43B13S4Q', 'O43B13S6Q', 'O43B13S8Q', 'O43B13SAQ', 'O43B14SFQ', 'O43B14SIQ', 'O43B15XEQ', 'O43B20010', 'O43B20X9Q', 'O43B21010', 'O43B21020', 'O43B22010', 'O43B22LXQ', 'O43B22MBQ', 'O43B2AXBQ', 'O43B2AXCQ', 'O43B2QXCQ', 'O43B2RXEQ', 'O43B2SXGQ', 'O43B2SXIQ', 'O43B2TXKQ', 'O43B2TXMQ', 'O43B2XCLQ', 'O43B2XCMQ', 'O43B4ASKQ', 'O43B5HXGQ', 'O43B5HXIQ', 'O43BA1BNQ', 'O43BA1BPQ', 'O43BA2H4Q', 'O43BA2H6Q', 'O43BA3M4Q', 'O43BA3M6Q', 'O43BA4DUQ', 'O43BA4DWQ', 'O43BA5C5Q', 'O43BA5C7Q', 'O43BA6BXQ', 'O43BA6BZQ', 'O43BA9B7Q', 'O43BA9B9Q', 'O43BB9BBQ', 'O43BC9BDQ', 'O43BD9BFQ', 'O43BD9BHQ', 'O43BE9BJQ']
            ('metadata/HSTOx_xxxx/HSTO0_7308/HSTO0_7308_index.tab',
             'O43B06BTQ', 2),
            ('metadata/HSTOx_xxxx/HSTO0_7308/HSTO0_7308_index.tab',
             'O43BB9BBQ', 50),
            ('metadata/HSTOx_xxxx/HSTO0_7308/HSTO0_7308_index.tab',
             'XXX/YYY/ZZZ', ''),
        ]
    )
    # Need to find a better way to test this one.
    def test_find_selected_row_number(self, input_path, selection, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        try:
            res = target_pdsfile.find_selected_row_number(selection=selection)
            assert res == expected
        except IOError:
            assert True # Index row is not found

    @pytest.mark.parametrize(
        'input_path,selection,expected',
        [
            # childnames: ['U2NO0401T', 'U2NO0402T', 'U2NO0403T', 'U2NO0404T']
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab',
             'U2NO0404T', 3),
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab',
             '', -1),
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab',
             'AAAAAAA', -1),

        ]
    )
    # Need to find a better way to test this one.
    def test_find_row_number_at_or_below(self, input_path, selection, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.find_row_number_at_or_below(selection=selection)
        assert res == expected


    @pytest.mark.parametrize(
        'input_path,selection,expected',
        [
            # childnames: ['U2NO0401T', 'U2NO0402T', 'U2NO0403T', 'U2NO0404T']
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab',
             None, None),
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab',
             'U2NO0401T', 'U2NO0401T'),
        ]
    )
    # Need to find a better way to test this one.
    def test_cache_child_row_pdsfiles(self, input_path, selection, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.cache_child_row_pdsfiles(selection=selection)
        if expected is None:
            assert res == expected
        else:
            assert res.basename == expected

    @pytest.mark.parametrize(
        'input_path,selection,expected',
        [
            # ['O43B05C1Q', 'O43B05C3Q', 'O43B06BTQ', 'O43B06BVQ', 'O43B09B3Q', 'O43B09B5Q', 'O43B11D7Q', 'O43B11D8Q', 'O43B12XAQ', 'O43B13S4Q', 'O43B13S6Q', 'O43B13S8Q', 'O43B13SAQ', 'O43B14SFQ', 'O43B14SIQ', 'O43B15XEQ', 'O43B20010', 'O43B20X9Q', 'O43B21010', 'O43B21020', 'O43B22010', 'O43B22LXQ', 'O43B22MBQ', 'O43B2AXBQ', 'O43B2AXCQ', 'O43B2QXCQ', 'O43B2RXEQ', 'O43B2SXGQ', 'O43B2SXIQ', 'O43B2TXKQ', 'O43B2TXMQ', 'O43B2XCLQ', 'O43B2XCMQ', 'O43B4ASKQ', 'O43B5HXGQ', 'O43B5HXIQ', 'O43BA1BNQ', 'O43BA1BPQ', 'O43BA2H4Q', 'O43BA2H6Q', 'O43BA3M4Q', 'O43BA3M6Q', 'O43BA4DUQ', 'O43BA4DWQ', 'O43BA5C5Q', 'O43BA5C7Q', 'O43BA6BXQ', 'O43BA6BZQ', 'O43BA9B7Q', 'O43BA9B9Q', 'O43BB9BBQ', 'O43BC9BDQ', 'O43BD9BFQ', 'O43BD9BHQ', 'O43BE9BJQ']
            ('metadata/HSTOx_xxxx/HSTO0_7308/HSTO0_7308_index.tab',
             'O43BA4DUQ', 'O43BA4DUQ'),
            ('metadata/HSTOx_xxxx/HSTO0_7308/HSTO0_7308_index.tab',
             'O43BA2H4Q', 'O43BA2H4Q'),
            ('metadata/HSTOx_xxxx/HSTO0_7308/HSTO0_7308_index.tab',
             'XXX/YYY/ZZZ', None),
        ]
    )
    # Need to find a better way to test this one.
    def test_row_pdsfile(self, input_path, selection, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        try:
            res = target_pdsfile.row_pdsfile(selection=selection)
            assert res.basename == expected
            assert isinstance(res, pdsfile.PdsFile)
        except IOError:
            assert True # Index row is not found

    @pytest.mark.parametrize(
        'input_path,selection,expected',
        [
            # childnames: ['U2NO0401T', 'U2NO0402T', 'U2NO0403T', 'U2NO0404T']
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab',
             'U2NO0403T', 'U2NO0403T'),
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab',
             'U2NO0401T', 'U2NO0401T'),
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab',
             'XXX/YYY/ZZZ', 'U2NO0404T'),
        ]
    )
    def test_nearest_row_pdsfile(self, input_path, selection, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.nearest_row_pdsfile(selection=selection)
        assert isinstance(res, pdsfile.PdsFile)
        assert res.basename == expected

    @pytest.mark.parametrize(
        'input_path,selection,expected',
        [
            # selections will be ones we have in test directory
            ('metadata/HSTOx_xxxx/HSTO0_7308/HSTO0_7308_index.tab', 'O43B05C1Q',
             PDS_DATA_DIR + 'volumes/HSTOx_xxxx/HSTO0_7308/DATA/VISIT_05/O43B05C1Q.lbl'),
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab', 'U2NO0404T',
             PDS_DATA_DIR + 'volumes/HSTUx_xxxx/HSTU0_5167/DATA/VISIT_04/U2NO0404T.lbl'),
        ]
    )
    def test_data_pdsfile_for_index_and_selection(
            self, input_path, selection, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.data_pdsfile_for_index_and_selection(
            selection=selection)
        assert isinstance(res, pdsfile.PdsFile)
        assert res.exists == True
        assert res.abspath == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COISS_0xxx/COISS_0001/data', None),
            ('previews/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274', None),
        ]
    )
    def test_group_children(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.group_children()
        for group in res:
            assert isinstance(group, pdsfile.PdsGroup)

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COCIRS_0xxx_v3/COCIRS_0401/DATA/TSDR/NAV_DATA/TAR04012400.LBL',
             PDS_DATA_DIR + 'volumes/COCIRS_0xxx_v3/COCIRS_0401/DATA/TSDR/NAV_DATA'),
            ('volumes/COCIRS_1xxx/COCIRS_1001/DATA/TSDR/NAV_DATA/TAR10013100.DAT',
             PDS_DATA_DIR + 'volumes/COCIRS_1xxx/COCIRS_1001/DATA/TSDR/NAV_DATA'),
        ]
    )
    def test_parent(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.parent()
        assert isinstance(res, pdsfile.PdsFile)
        assert res.abspath == expected

    @pytest.mark.parametrize(
        'input_path,basename,expected',
        [
            ('volumes/COCIRS_6xxx/COCIRS_6004/DATA/GEODATA/',
             'GEO1004021018_699.lbl',
             PDS_DATA_DIR + 'volumes/COCIRS_6xxx/COCIRS_6004/DATA/GEODATA/GEO1004021018_699.lbl'),
            ('metadata/COISS_1xxx/COISS_1001',
             'COISS_1001_inventory.tab',
             PDS_DATA_DIR + 'metadata/COISS_1xxx/COISS_1001/COISS_1001_inventory.tab'),
        ]
    )
    def test_child(self, input_path, basename, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.child(basename=basename)
        assert isinstance(res, pdsfile.PdsFile)
        assert res.abspath == expected

    @pytest.mark.parametrize(
        'input_path,interiors,expected',
        [
            (PDS_DATA_DIR + 'volumes/COISS_1xxx/COISS_1001',
             ['data/1294561143_1295221348/W1294561202_1.lbl'],
             PDS_DATA_DIR + 'volumes/COISS_1xxx/COISS_1001'),
            (PDS_DATA_DIR + 'volumes/COUVIS_0xxx/COUVIS_0001',
             ['DATA/D1999_007/HDAC1999_007_16_31.DAT'],
             PDS_DATA_DIR + 'volumes/COUVIS_0xxx/COUVIS_0001'),
        ]
    )
    def test_load_opus_ids_for_volume_interiors(
            self, input_path, interiors, expected):
        pdsfile.PdsFile.load_opus_ids_for_volume_interiors(
            volume_abspath=input_path, interiors=interiors)

        abspath = input_path + '/' + interiors[0]
        print(abspath)
        target_pdsfile = pdsfile.PdsFile.from_abspath(abspath)
        opus_id = target_pdsfile.opus_id
        print(target_pdsfile.abspath)
        assert opus_id in pdsfile.PdsFile.OPUS_ID_ABSPATHS
        assert abspath in pdsfile.PdsFile.OPUS_ID_ABSPATHS[opus_id]
        assert expected in pdsfile.PdsFile.OPUS_ID_VOLUMES_LOADED

    @pytest.mark.parametrize(
        'input_suffix,expected',
        [
            ('_v2.1.3', (20103, 'Version 2.1.3 (superseded)', '2.1.3')),
        ]
    )
    def test_version_info(self, input_suffix, expected):
        res = pdsfile.PdsFile.version_info(suffix=input_suffix)
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_CAL.lbl',
             True),
            (PDS_DATA_DIR + 'volumes/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1.lbl',
             True),
        ]
    )
    def test__from_absolute_or_logical_path(self, input_path, expected):
        res = pdsfile.PdsFile._from_absolute_or_logical_path(path=input_path)
        assert isinstance(res, pdsfile.PdsFile)
        assert res.exists == expected

    @pytest.mark.parametrize(
        'filespec,expected',
        [
            ('COISS_0001', True),
            ('COISS_1001/data/1294561143_1295221348/W1294561261_1_thumb.jpg',
             True),
        ]
    )
    def test_from_filespec(self, filespec, expected):
        res = pdsfile.PdsFile.from_filespec(filespec=filespec)
        print(res.abspath)
        assert isinstance(res, pdsfile.PdsFile)
        assert res.exists == expected

    @pytest.mark.parametrize(
        'opus_id,expected',
        [
            ('hst-07176-nicmos-n4bi01l4q',
             'volumes/HSTNx_xxxx/HSTN0_7176/DATA/VISIT_01/N4BI01L4Q.LBL'),
        ]
    )
    def test_from_opus_id(self, opus_id, expected):
        res = pdsfile.PdsFile.from_opus_id(opus_id=opus_id)
        print(res.logical_path)
        assert isinstance(res, pdsfile.PdsFile)
        assert res.logical_path == expected
