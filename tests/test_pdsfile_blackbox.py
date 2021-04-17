import datetime
import os
import pdsfile
import pdsgroup
import pdsgrouptable
import pdsviewable
import pytest
import re
import sys

from tests.helper import *

PDS_DATA_DIR = os.environ['PDS_DATA_DIR']
PDS_PDSDATA_PATH = PDS_DATA_DIR[:PDS_DATA_DIR.index('holdings')]
################################################################################
# Blackbox test for functions & properties in PdsFile class
################################################################################
class TestPdsFileBlackBox:
    ############################################################################
    # Local implementations of basic filesystem operations
    ############################################################################
    @pytest.mark.parametrize(
        'input_path,expected',
        [
            (PDS_DATA_DIR + '/volumes/COISS_2xxx',
             [
                'COISS_2090', 'COISS_2025', 'COISS_2055', 'COISS_2058',
                'COISS_2086', 'COISS_2105', 'COISS_2067', 'COISS_2017',
                'COISS_2049', 'COISS_2011', 'COISS_2026', 'COISS_2039',
                'COISS_2073', 'COISS_2044', 'COISS_2062', 'COISS_2037',
                'COISS_2114', 'COISS_2110', 'COISS_2072', 'COISS_2002',
                'COISS_2108', 'COISS_2093', 'COISS_2030', 'COISS_2081',
                'COISS_2040', 'COISS_2007', 'COISS_2098', 'COISS_2077',
                'COISS_2115', 'COISS_2029', 'COISS_2050', 'COISS_2111',
                'COISS_2059', 'COISS_2005', 'COISS_2032', 'COISS_2045',
                'COISS_2035', 'COISS_2084', 'COISS_2109', 'COISS_2096',
                'COISS_2019', 'COISS_2083', 'COISS_2008', 'COISS_2095',
                'COISS_2020', 'COISS_2023', 'COISS_2014', 'COISS_2100',
                'COISS_2041', 'COISS_2076', 'COISS_2012', 'COISS_2089',
                'COISS_2103', 'COISS_2061', 'COISS_2107', 'COISS_2024',
                'COISS_2013', 'COISS_2046', 'COISS_2071', 'COISS_2053',
                'COISS_2092', 'COISS_2038', 'COISS_2080', 'COISS_2068',
                'COISS_2018', 'COISS_2036', 'COISS_2060', 'COISS_2057',
                'COISS_2116', 'COISS_2004', 'COISS_2074', 'COISS_2033',
                'COISS_2043', 'COISS_2079', 'COISS_2113', 'COISS_2001',
                'COISS_2052', 'COISS_2065', 'COISS_2016', 'COISS_2021',
                'COISS_2102', 'COISS_2064', 'COISS_2099', 'COISS_2106',
                'COISS_2085', 'COISS_2078', 'COISS_2097', 'COISS_2056',
                'COISS_2066', 'COISS_2051', 'COISS_2101', 'COISS_2063',
                'COISS_2082', 'COISS_2094', 'COISS_2034', 'COISS_2009',
                'COISS_2088', 'COISS_2006', 'COISS_2022', 'COISS_2015',
                'COISS_2028', 'COISS_2091', 'COISS_2031', 'COISS_2104',
                'COISS_2010', 'COISS_2027', 'COISS_2003', 'COISS_2054',
                'COISS_2048', 'COISS_2087', 'COISS_2112', 'COISS_2070',
                'COISS_2075', 'COISS_2042', 'COISS_2069', 'COISS_2047'
            ]
           ),
        ]
    )
    def test_os_listdir(self, input_path, expected):
        res = pdsfile.PdsFile.os_listdir(abspath=input_path)
        assert len(res) == len(expected)
        assert res.sort() == expected.sort()

    ############################################################################
    # Test for DEFAULT FILE SORT ORDER
    ############################################################################
    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31.DAT',
             True),
            ('volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31.DAT',
             False),
        ]
    )
    def test_sort_labels_after(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        target_pdsfile.sort_labels_after(labels_after=expected)
        assert target_pdsfile.SORT_ORDER['labels_after'] == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31.DAT',
             True),
            ('volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31.DAT',
             False),
        ]
    )
    def test_sort_dirs_first(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        target_pdsfile.sort_dirs_first(dirs_first=expected)
        assert target_pdsfile.SORT_ORDER['dirs_first'] == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31.DAT',
             True),
            ('volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31.DAT',
             False),
        ]
    )
    def test_sort_dirs_last(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        target_pdsfile.sort_dirs_last(dirs_last=expected)
        assert target_pdsfile.SORT_ORDER['dirs_last'] == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31.DAT',
             True),
            ('volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31.DAT',
             False),
        ]
    )
    def test_sort_info_first(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        target_pdsfile.sort_info_first(info_first=expected)
        assert target_pdsfile.SORT_ORDER['info_first'] == expected

    ############################################################################
    # Test for properties
    ############################################################################
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
             PDS_DATA_DIR + '/diagrams/COCIRS_5xxx/COCIRS_5401/BROWSE/TARGETS/IMG0401130240_FP1_thumb.jpg'),
            ('volumes', PDS_DATA_DIR + '/volumes')
        ]
    )
    def test_absolute_or_logical_path(self, input_path, expected):
        """absolute_or_logical_path: get abspath."""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        if expected is None:
            expected = PDS_DATA_DIR + '/' + input_path
        assert target_pdsfile.absolute_or_logical_path == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('diagrams/COCIRS_6xxx/COCIRS_6004/BROWSE/SATURN/POI1004010000_FP1_small.jpg',
             '/holdings/diagrams/COCIRS_6xxx/COCIRS_6004/BROWSE/SATURN/POI1004010000_FP1_small.jpg'),
            ('volumes/COISS_1xxx/COISS_1001', '/holdings/volumes/COISS_1xxx/COISS_1001')
        ]
    )
    def test_html_path(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        expected = '/holdings/' + input_path if expected is None else expected
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
            ('volumes/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2017_228_BETORI_I_TAU10KM.LBL',
             'UVIS_HSP_2017_228_BETORI_I'),
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
            ('previews/COVIMS_0xxx', 'IMAGEDIR'),
            ('previews/COVIMS_0xxx/COVIMS_0001', 'IMAGEDIR'),
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
            ('volumes/EBROCC_xxxx/EBROCC_0001/DATA/ESO1M/ES1_EPD.TAB',
             'ES1_EPD.LBL'),
            ('volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31.dat',
             'HDAC1999_007_16_31.LBL'),
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
             PDS_DATA_DIR + '/volumes/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R.LBL'),
            ('volumes/GO_0xxx/GO_0017/J0/OPNAV', ''),
            ('metadata/GO_0xxx/GO_0017/GO_0017_index.tab',
             PDS_DATA_DIR + '/metadata/GO_0xxx/GO_0017/GO_0017_index.lbl'),
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
                None
             ]),
            ('previews/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R_med.jpg',
             [
                'Galileo Jupiter preview image 1996-06-03 to 1996-12-14 (SC clock 03464059-03740374)',
                None
             ]),
            ('metadata/COVIMS_0xxx/COVIMS_0001',
             [
                'Cassini VIMS metadata 1999-01-10 to 2000-09-18 (SC clock 1294638283-1347975444)',
                None
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
            ('volumes/HSTNx_xxxx/HSTN0_7176/DATA/VISIT_01/N4BI01L4Q.LBL',
             'hst-07176-nicmos-n4bi01l4q'),
            ('volumes/HSTJx_xxxx/HSTJ0_9296/DATA/VISIT_B1/J8M3B1021.lbl',
             'hst-09296-acs-j8m3b1021'),
            ('volumes/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R.LBL',
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
            ('volumes/HSTOx_xxxx/HSTO0_7308/DATA/VISIT_05/O43B05C1Q.LBL',
             'O43B05C1Q.LBL')
        ]
    )
    def test_alt(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.alt == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('previews/HSTOx_xxxx/HSTO0_7308/DATA/VISIT_05/O43B05C1Q_small.jpg',
             [
                 '/holdings/previews/HSTOx_xxxx/HSTO0_7308/DATA/VISIT_05/O43B05C1Q_small.jpg',
                 '/holdings/previews/HSTOx_xxxx/HSTO0_7308/DATA/VISIT_05/O43B05C1Q_thumb.jpg',
                 '/holdings/previews/HSTOx_xxxx/HSTO0_7308/DATA/VISIT_05/O43B05C1Q_full.jpg',
                 '/holdings/previews/HSTOx_xxxx/HSTO0_7308/DATA/VISIT_05/O43B05C1Q_med.jpg',
             ]
            ),
            ('volumes/HSTOx_xxxx/HSTO0_7308/DATA/VISIT_05/O43B05C1Q.LBL',
             [
                '/holdings/previews/HSTOx_xxxx/HSTO0_7308/DATA/VISIT_05/O43B05C1Q_small.jpg',
                '/holdings/previews/HSTOx_xxxx/HSTO0_7308/DATA/VISIT_05/O43B05C1Q_thumb.jpg',
                '/holdings/previews/HSTOx_xxxx/HSTO0_7308/DATA/VISIT_05/O43B05C1Q_full.jpg',
                '/holdings/previews/HSTOx_xxxx/HSTO0_7308/DATA/VISIT_05/O43B05C1Q_med.jpg',
             ]
            ),
        ]
    )
    def test_viewset(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.viewset
        assert isinstance(res, pdsviewable.PdsViewSet)
        viewables = res.to_dict()['viewables']
        for viewable in viewables:
            assert viewable['url'] in expected

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
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab',
             PDS_PDSDATA_PATH + 'shelves/index/metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.pickle')
        ]
    )
    def test_indexshelf_abspath(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.indexshelf_abspath == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab',
             True)
        ]
    )
    def test_is_index(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.is_index == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab',
             'HSTU0_5167_label.txt')
        ]
    )
    def test_index_pdslabel(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.index_pdslabel
        assert res != None
        assert res != 'failed'

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
            ('volumes/COCIRS_6xxx/COCIRS_6004/DATA/GEODATA/GEO1004021018_699.LBL',
             [
                PDS_DATA_DIR + '/volumes/COCIRS_6xxx/COCIRS_6004/DATA/GEODATA/GEO1004021018_699.TAB'
             ])
        ]
    )
    def test_data_abspaths(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.data_abspaths

        for path in res:
            assert path in expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            # Need to revisit and find a proper case for this one
            ('archives-volumes/COCIRS_0xxx/COCIRS_0010.tar.gz',
             '')
        ]
    )
    def test_exact_archive_url(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.exact_archive_url
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.DAT', ''),
            ('volumes/COCIRS_0xxx/COCIRS_0012/CALIB', ''),
            ('volumes/COCIRS_0xxx/COCIRS_0012',
             '/holdings/checksums-volumes/COCIRS_0xxx/COCIRS_0012_md5.txt')
        ]
    )
    def test_exact_checksum_url(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.exact_checksum_url
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('diagrams/COCIRS_5xxx/COCIRS_5401/BROWSE/TARGETS/IMG0401130240_FP1_thumb.jpg',
             False),
            ('diagrams/COCIRS_5xxx/COCIRS_5401/BROWSE/TARGETS/',
             True),
        ]
    )
    def test_grid_view_allowed(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.grid_view_allowed
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('diagrams/COCIRS_5xxx/COCIRS_5401/BROWSE/TARGETS/IMG0401130240_FP1_thumb.jpg',
             False),
            ('diagrams/COCIRS_5xxx/COCIRS_5401/BROWSE/TARGETS/',
             True),
        ]
    )
    def test_multipage_view_allowed(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.multipage_view_allowed
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('diagrams/COCIRS_5xxx/COCIRS_5401/BROWSE/TARGETS/IMG0401130240_FP1_thumb.jpg',
             False),
            ('diagrams/COCIRS_5xxx/COCIRS_5401/BROWSE/TARGETS/',
             True),
        ]
    )
    def test_continuous_view_allowed(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.continuous_view_allowed
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('diagrams/COCIRS_5xxx/COCIRS_5401/BROWSE/TARGETS/IMG0401130240_FP1_thumb.jpg',
             False),
            ('diagrams/COCIRS_5xxx/COCIRS_5401/BROWSE/TARGETS/',
             True),
        ]
    )
    def test_continuous_view_allowed(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.continuous_view_allowed
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COUVIS_0xxx/COUVIS_0001/DATA/', True),
            ('volumes/COUVIS_0xxx', False)
        ]
    )
    def test_has_neighbor_rule(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.has_neighbor_rule
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('previews/COUVIS_0xxx/COUVIS_0009/DATA/D2004_274/EUV2004_274_01_39_thumb.png',
             'f43e6fe3d9eb02ed72e0aba47be443f2')
        ]
    )
    def test_checksum(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.checksum
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31.LBL',
             (PDS_PDSDATA_PATH + 'shelves/info/volumes/COUVIS_0xxx/COUVIS_0001_info.pickle',
              'DATA/D1999_007/HDAC1999_007_16_31.LBL'))
        ]
    )
    def test_infoshelf_path_and_key(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.infoshelf_path_and_key
        assert res == expected

    ############################################################################
    # Test for functions
    ############################################################################
    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('previews/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_small.jpg',
             [
                'holdings/previews/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_small.jpg',
                'holdings/previews/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_med.jpg',
                'holdings/previews/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_full.jpg',
                'holdings/previews/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_thumb.jpg',
             ]
            ),
            ('previews/VGISS_5xxx/VGISS_5101/DATA/C13854XX',
             [
                'holdings/previews/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_small.jpg',
                'holdings/previews/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_med.jpg',
                'holdings/previews/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_full.jpg',
                'holdings/previews/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_thumb.jpg',
             ]
            ),
            ('volumes/VGISS_5xxx/VGISS_5101/DATA/C13854XX',
             [
                'holdings/previews/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_small.jpg',
                'holdings/previews/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_med.jpg',
                'holdings/previews/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_full.jpg',
                'holdings/previews/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_thumb.jpg',
             ]
            ),
        ]
    )
    def test_viewset_lookup(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.viewset_lookup()
        assert isinstance(res, pdsviewable.PdsViewSet)
        viewables = res.to_dict()['viewables']
        for viewable in viewables:
            assert viewable['url'] in expected

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
            ('previews/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_small.jpg',
             'PdsFile.VGISS_xxxx("' + PDS_DATA_DIR + '/previews/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_small.jpg")'),
        ]
    )
    def test___repr__1(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.__repr__()
        assert res == expected

    def test___repr__2(self):
        target_pdsfile = pdsfile.PdsFile()
        res = target_pdsfile.__repr__()
        assert res == 'PdsFile("")'

    ############################################################################
    # Test for alternative constructors
    ############################################################################
    @pytest.mark.parametrize(
        'input_path,basename,expected',
        [
            ('volumes/COCIRS_6xxx/COCIRS_6004/DATA/GEODATA/',
             'GEO1004021018_699.LBL',
             PDS_DATA_DIR + '/volumes/COCIRS_6xxx/COCIRS_6004/DATA/GEODATA/GEO1004021018_699.LBL'),
            ('metadata/COISS_1xxx/COISS_1001',
             'COISS_1001_inventory.tab',
             PDS_DATA_DIR + '/metadata/COISS_1xxx/COISS_1001/COISS_1001_inventory.tab'),
        ]
    )
    def test_child(self, input_path, basename, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        print(target_pdsfile.category_)
        res = target_pdsfile.child(basename=basename)
        assert isinstance(res, pdsfile.PdsFile)
        assert res.abspath == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COCIRS_0xxx_v3/COCIRS_0401/DATA/TSDR/NAV_DATA/TAR04012400.LBL',
             PDS_DATA_DIR + '/volumes/COCIRS_0xxx_v3/COCIRS_0401/DATA/TSDR/NAV_DATA'),
            ('volumes/COCIRS_1xxx/COCIRS_1001/DATA/TSDR/NAV_DATA/TAR10013100.DAT',
             PDS_DATA_DIR + '/volumes/COCIRS_1xxx/COCIRS_1001/DATA/TSDR/NAV_DATA'),
        ]
    )
    def test_parent(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.parent()
        assert isinstance(res, pdsfile.PdsFile)
        assert res.abspath == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COISS_0xxx/COISS_0001/data/wacfm/bit_wght/13302/133020.lbl',
             'volumes/COISS_0xxx/COISS_0001/data/wacfm/bit_wght/13302/133020.lbl')
        ]
    )
    def test_from_logical_path(self, input_path, expected):
        res = pdsfile.PdsFile.from_logical_path(path=input_path)
        assert isinstance(res, pdsfile.PdsFile)
        assert res.logical_path == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COISS_0xxx/COISS_0001/data/wacfm/bit_wght/13302/133020.lbl',
             True),
            (PDS_DATA_DIR + '/volumes/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1.LBL',
             PDS_DATA_DIR + '/volumes/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1.LBL'),
        ]
    )
    def test_from_abspath(self, input_path, expected):
        try:
            res = pdsfile.PdsFile.from_abspath(abspath=input_path)
            assert isinstance(res, pdsfile.PdsFile)
            assert res.abspath == expected
        except ValueError as e:
            assert True # input path is not an absolute path

    @pytest.mark.parametrize(
        'input_lid,expected',
        [
            ('CO-S-ISSNA/ISSWA-2-EDR-V1.0:COISS_2002:data/1460960653_1461048959:N1460960868_1.IMG',
             ['CO-S-ISSNA/ISSWA-2-EDR-V1.0', 'N1460960868_1.IMG']),
            ('CO-E/V/J-ISSNA/ISSWA-2-EDR-V1.0:COISS_1001:data/1294561143_1295221348:W1294561202_1.LBL',
             ['CO-E/V/J-ISSNA/ISSWA-2-EDR-V1.0', 'W1294561202_1.LBL']),
            ('CO-E/V/J/S-VIMS-2-QUBE-V1.0:COVIMS_0001:data/1999010T054026_1999010T060958:v1294638283_1.qub',
             ['CO-E/V/J/S-VIMS-2-QUBE-V1.0', 'v1294638283_1.qub']),
            ('ESO1M-SR-APPH-4-OCC-V1.0:EBROCC_0001:DATA/ESO1M:ES1_EPD.LBL',
             ['ESO1M-SR-APPH-4-OCC-V1.0', 'ES1_EPD.LBL']),
            ('ESO22M-SR-APPH-4-OCC-V1.0:EBROCC_0001:CATALOG:ESO22M_DATASET.CAT',
             ['ESO22M-SR-APPH-4-OCC-V1.0', 'ESO22M_DATASET.CAT']),
            ('IRTF-SR-URAC-4-OCC-V1.0:EBROCC_0001:GEOMETRY/IRTF:IRT_IGD.TAB',
             ['IRTF-SR-URAC-4-OCC-V1.0', 'IRT_IGD.TAB']),
            ('LICK1M-SR-CCDC-4-OCC-V1.0:EBROCC_0001:INDEX:LIC_INDEX.LBL',
             ['LICK1M-SR-CCDC-4-OCC-V1.0', 'LIC_INDEX.LBL']),
            ('MCD27M-SR-IIRAR-4-OCC-V1.0:EBROCC_0001:DATA/MCD27M:MCD_IPD.TAB',
             ['MCD27M-SR-IIRAR-4-OCC-V1.0', 'MCD_IPD.TAB']),
            ('PAL200-SR-CIRC-4-OCC-V1.0:EBROCC_0001:DATA/PAL200:PAL_EPD.LBL',
             ['PAL200-SR-CIRC-4-OCC-V1.0', 'PAL_EPD.LBL']),

        ]
    )
    def test_from_lid_valid_lid(self, input_lid, expected):
        res = pdsfile.PdsFile.from_lid(input_lid)
        assert isinstance(res, pdsfile.PdsFile)
        assert res.data_set_id == expected[0]
        assert res.basename == expected[1]

    @pytest.mark.parametrize(
        'input_lid,expected',
        [
            ('CO-E/V/J/S-VIMS-2-QUBE-V2.0:COVIMS_0001:data/1999010T054026_1999010T060958:v1294638283_1.qub',
             'CO-E/V/J/S-VIMS-2-QUBE-V1.0'),
        ]
    )
    def test_from_lid_mismatched_lid(self, input_lid, expected):
        try:
            res = pdsfile.PdsFile.from_lid(input_lid)
            # Must raise an exception
            assert False
        except ValueError as e:
            # input LID data set id doesn't match the one from res
            assert 'does not match the one from pdsfile:' in str(e)

    @pytest.mark.parametrize(
        'input_lid,expected',
        [
            ('CO-E/V/J/S-VIMS-2-QUBE-V2.0:data/1999010T054026_1999010T060958:v1294638283_1.qub',
             'CO-E/V/J/S-VIMS-2-QUBE-V1.0'),
        ]
    )
    def test_from_lid_invalid_lid(self, input_lid, expected):
        try:
            res = pdsfile.PdsFile.from_lid(input_lid)
            # Must raise an exception
            assert False
        except ValueError as e:
            # input LID is not a valid LID
            assert 'is not a valid LID' in str(e)

    @pytest.mark.parametrize(
        'input_path,relative_path,expected',
        [
            ('previews/COUVIS_0xxx_v1/COUVIS_0009/DATA',
             '/D2004_274/EUV2004_274_01_39_thumb.png',
             'previews/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274/EUV2004_274_01_39_thumb.png'),
            ('volumes/COUVIS_0xxx/COUVIS_0001',
             '/DATA/D1999_007/FUV1999_007_16_57.LBL',
             'volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/FUV1999_007_16_57.LBL'),
            ('volumes/COUVIS_0xxx/COUVIS_0001',
             '/DATAx/D1999_007/FUV1999_007_16_57.LBL',
             'volumes/COUVIS_0xxx/COUVIS_0001/DATAx/D1999_007/FUV1999_007_16_57.LBL'),
        ]
    )
    def test_from_relative_path(self, input_path, relative_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.from_relative_path(path=relative_path)
        assert isinstance(res, pdsfile.PdsFile)
        assert res.logical_path == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_CAL.LBL',
             PDS_DATA_DIR + '/volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_CAL.LBL'),
            (PDS_DATA_DIR + '/volumes/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1.LBL',
             PDS_DATA_DIR + '/volumes/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1.LBL'),
        ]
    )
    def test__from_absolute_or_logical_path(self, input_path, expected):
        res = pdsfile.PdsFile._from_absolute_or_logical_path(path=input_path)
        assert isinstance(res, pdsfile.PdsFile)
        assert res.abspath == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('holdings/volumes/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274/EUV2004_274_01_39.DAT',
             PDS_DATA_DIR + '/volumes/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274/EUV2004_274_01_39.DAT'),
            ('volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.DAT',
             PDS_DATA_DIR + '/volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.DAT'),
            ('COVIMS_0xxx/COVIMS_0001/data/1999010T054026_1999010T060958',
             PDS_DATA_DIR + '/volumes/COVIMS_0xxx/COVIMS_0001/data/1999010T054026_1999010T060958'),
            ('metadata/HSTOx_xxxx/HSTO0_7308',
             PDS_DATA_DIR + '/metadata/HSTOx_xxxx/HSTO0_7308'),
            ('HSTOx_xxxx', PDS_DATA_DIR + '/volumes/HSTOx_xxxx'),
            ('volumes/VGIRIS_xxxx_peer_review/VGIRIS_0001/DATA/JUPITER_VG1/C1547XXX.LBL',
             PDS_DATA_DIR + '/volumes/VGIRIS_xxxx_peer_review/VGIRIS_0001/DATA/JUPITER_VG1/C1547XXX.LBL'),
            ('COCIRS_1001/DATA/CUBE/EQUIRECTANGULAR/123RI_EQLBS002_____CI____699_F1_039E.tar.gz',
             PDS_DATA_DIR + '/volumes/COCIRS_1xxx/COCIRS_1001/DATA/CUBE/EQUIRECTANGULAR/123RI_EQLBS002_____CI____699_F1_039E.tar.gz'),
        ]
    )
    def test_from_path(self, input_path, expected):
        res = pdsfile.PdsFile.from_path(path=input_path)
        assert isinstance(res, pdsfile.PdsFile)
        assert res.abspath == expected

    ############################################################################
    # Test for OPUS support methods
    ############################################################################
    # from_filespec will only work with files under /volumes
    @pytest.mark.parametrize(
        'filespec,expected',
        [
            ('COISS_0001', PDS_DATA_DIR + '/volumes/COISS_0xxx/COISS_0001'),
            ('COISS_1001/data/1294561143_1295221348/W1294561202_1.IMG',
             PDS_DATA_DIR + '/volumes/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1.IMG'),
        ]
    )
    def test_from_filespec(self, filespec, expected):
        res = pdsfile.PdsFile.from_filespec(filespec=filespec)
        assert isinstance(res, pdsfile.PdsFile)
        assert res.abspath == expected

    @pytest.mark.parametrize(
        'input_id,expected',
        [
            ('co-cirs-0408010000-fp1',
             'volumes/COCIRS_5xxx/COCIRS_5408/DATA/APODSPEC/SPEC0408010000_FP1.DAT'),
            ('co-iss-w1294561143',
             'volumes/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561143_1.IMG'),
            ('co-uvis-hdac1999_007_16_33',
             'volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33.DAT'),
            ('co-vims-v1490784910_001',
             'volumes/COVIMS_0xxx/COVIMS_0006/data/2005088T102825_2005089T113931/v1490784910_3_001.qub'),
            ('go-ssi-c0346405900',
             'volumes/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R.IMG'),
            ('vg-iss-1-j-c1385455',
             'volumes/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_RAW.IMG'),
            ('hst-09296-acs-j8m3b1021',
             'volumes/HSTJx_xxxx/HSTJ0_9296/DATA/VISIT_B1/J8M3B1021.LBL'),
            ('hst-11559-wfc3-ib4v11mnq',
             'volumes/HSTIx_xxxx/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ.LBL'),
            ('hst-07176-nicmos-n4bi01l4q',
             'volumes/HSTNx_xxxx/HSTN0_7176/DATA/VISIT_01/N4BI01L4Q.LBL'),
            ('hst-07308-stis-o43b05c1q',
             'volumes/HSTOx_xxxx/HSTO0_7308/DATA/VISIT_05/O43B05C1Q.LBL'),
            ('hst-05167-wfpc2-u2no0404t',
             'volumes/HSTUx_xxxx/HSTU0_5167/DATA/VISIT_04/U2NO0404T.LBL'),
            ('nh-lorri-lor_0003103486',
             'volumes/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng.fit'),
            ('eso1m-apph-occ-1989-184-28sgr-e',
             'volumes/EBROCC_xxxx/EBROCC_0001/DATA/ESO1M/ES1_EPD.TAB'),
            ('eso22m-apph-occ-1989-184-28sgr-i',
             'volumes/EBROCC_xxxx/EBROCC_0001/DATA/ESO22M/ES2_IPD.TAB'),
            ('lick1m-ccdc-occ-1989-184-28sgr-e',
             'volumes/EBROCC_xxxx/EBROCC_0001/DATA/LICK1M/LIC_EPD.TAB'),
            ('irtf-urac-occ-1989-184-28sgr-i',
             'volumes/EBROCC_xxxx/EBROCC_0001/DATA/IRTF/IRT_IPD.TAB'),
            ('pal200-circ-occ-1989-184-28sgr-i',
             'volumes/EBROCC_xxxx/EBROCC_0001/DATA/PAL200/PAL_IPD.TAB'),
            ('mcd27m-iirar-occ-1989-184-28sgr-i',
             'volumes/EBROCC_xxxx/EBROCC_0001/DATA/MCD27M/MCD_IPD.TAB'),
            ('co-rss-occ-2005-159-rev009-k55-e',
             'volumes/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009E/Rev009E_RSS_2005_159_K55_E/RSS_2005_159_K55_E_TAU_01KM.TAB'),

            # ('nh-mvic-mc0_0032528036',
            # 'volumes/NHxxMV_xxxx/NHJUMV_1001/data/20070131_003252/mc0_0032528036_0x536_eng_1.fit'),
            # ('nh-mvic-mc0_0005261846',
            # 'volumes/NHxxMV_xxxx/NHLAMV_1001/data/20060321_000526/mc0_0005261846_0x536_eng_1.fit'),

        ]
    )
    def test_from_opus_id1(self, input_id, expected):
        target_pdsfile1 = pdsfile.PdsFile.from_opus_id(input_id)
        logical_path1 = target_pdsfile1.logical_path
        target_pdsfile2 = instantiate_target_pdsfile(
            logical_path1, is_abspath=False)
        assert logical_path1 == expected
        assert target_pdsfile1.opus_id == input_id
        assert target_pdsfile2.opus_id == input_id

    @pytest.mark.parametrize(
        'opus_id,expected',
        [
            ('hst-07176-nicmos-n4bi01l4q',
             PDS_DATA_DIR + '/volumes/HSTNx_xxxx/HSTN0_7176/DATA/VISIT_01/N4BI01L4Q.LBL')
        ]
    )
    def test_from_opus_id2(self, opus_id, expected):
        res = pdsfile.PdsFile.from_opus_id(opus_id=opus_id)
        assert isinstance(res, pdsfile.PdsFile)
        assert res.abspath == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1.IMG',
             {('Cassini ISS',
               0,
               'coiss_raw',
               'Raw Image',
               True): [PDS_DATA_DIR + '/volumes/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1.IMG',
                       PDS_DATA_DIR + '/volumes/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1.LBL',
                       PDS_DATA_DIR + '/volumes/COISS_1xxx/COISS_1001/label/prefix.fmt',
                       PDS_DATA_DIR + '/volumes/COISS_1xxx/COISS_1001/label/tlmtab.fmt'],
              ('Cassini ISS',
               110,
               'coiss_thumb',
               'Extra Preview (thumbnail)',
               False): [PDS_DATA_DIR + '/volumes/COISS_1xxx/COISS_1001/extras/thumbnail/1294561143_1295221348/W1294561202_1.IMG.jpeg_small'],
              ('Cassini ISS',
               120,
               'coiss_medium',
               'Extra Preview (medium)',
               False): [PDS_DATA_DIR + '/volumes/COISS_1xxx/COISS_1001/extras/browse/1294561143_1295221348/W1294561202_1.IMG.jpeg'],
              ('Cassini ISS',
               10,
               'coiss_calib',
               'Calibrated Image',
               True): [PDS_DATA_DIR + '/calibrated/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1_CALIB.IMG',
                       PDS_DATA_DIR + '/calibrated/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1_CALIB.LBL',
                       PDS_DATA_DIR + '/calibrated/COISS_1xxx_v1/COISS_1001/data/1294561143_1295221348/W1294561202_1_CALIB.IMG',
                       PDS_DATA_DIR + '/calibrated/COISS_1xxx_v1/COISS_1001/data/1294561143_1295221348/W1294561202_1_CALIB.LBL',
                       PDS_DATA_DIR + '/calibrated/COISS_1xxx_v2/COISS_1001/data/1294561143_1295221348/W1294561202_1_CALIB.IMG',
                       PDS_DATA_DIR + '/calibrated/COISS_1xxx_v2/COISS_1001/data/1294561143_1295221348/W1294561202_1_CALIB.LBL'],
              ('browse',
               10,
               'browse_thumb',
               'Browse Image (thumbnail)',
               False): [PDS_DATA_DIR + '/previews/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1_thumb.jpg'],
              ('browse',
               20,
               'browse_small',
               'Browse Image (small)',
               False): [PDS_DATA_DIR + '/previews/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1_small.jpg'],
              ('browse',
               30,
               'browse_medium',
               'Browse Image (medium)',
               False): [PDS_DATA_DIR + '/previews/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1_med.jpg'],
              ('browse',
               40,
               'browse_full',
               'Browse Image (full)',
               True): [PDS_DATA_DIR + '/previews/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1_full.png'],
              ('metadata',
               20,
               'planet_geometry',
               'Planet Geometry Index',
               False): [PDS_DATA_DIR + '/metadata/COISS_1xxx/COISS_1001/COISS_1001_jupiter_summary.tab',
                        PDS_DATA_DIR + '/metadata/COISS_1xxx/COISS_1001/COISS_1001_jupiter_summary.lbl'],
              ('metadata',
               30,
               'moon_geometry',
               'Moon Geometry Index',
               False): [PDS_DATA_DIR + '/metadata/COISS_1xxx/COISS_1001/COISS_1001_moon_summary.tab',
                        PDS_DATA_DIR + '/metadata/COISS_1xxx/COISS_1001/COISS_1001_moon_summary.lbl'],
              ('metadata',
               40,
               'ring_geometry',
               'Ring Geometry Index',
               False): [PDS_DATA_DIR + '/metadata/COISS_1xxx/COISS_1001/COISS_1001_ring_summary.tab',
                        PDS_DATA_DIR + '/metadata/COISS_1xxx/COISS_1001/COISS_1001_ring_summary.lbl'],
              ('metadata',
               10,
               'inventory',
               'Target Body Inventory',
               False): [PDS_DATA_DIR + '/metadata/COISS_1xxx/COISS_1001/COISS_1001_inventory.csv',
                        PDS_DATA_DIR + '/metadata/COISS_1xxx/COISS_1001/COISS_1001_inventory.lbl'],
              ('metadata',
               5,
               'rms_index',
               'RMS Node Augmented Index',
               False): [PDS_DATA_DIR + '/metadata/COISS_1xxx/COISS_1001/COISS_1001_index.tab',
                        PDS_DATA_DIR + '/metadata/COISS_1xxx/COISS_1001/COISS_1001_index.lbl']}
            ),
        ]
    )
    def test_opus_products_coiss_1xxx(self, input_path, expected):
        opus_products_test(input_path, expected)

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460960868_1.LBL',
             {('Cassini ISS',
               0,
               'coiss_raw',
               'Raw Image',
               True): [PDS_DATA_DIR + '/volumes/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460960868_1.IMG',
                       PDS_DATA_DIR + '/volumes/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460960868_1.LBL',
                       PDS_DATA_DIR + '/volumes/COISS_2xxx/COISS_2002/label/prefix2.fmt',
                       PDS_DATA_DIR + '/volumes/COISS_2xxx/COISS_2002/label/tlmtab.fmt'],
              ('Cassini ISS',
               110,
               'coiss_thumb',
               'Extra Preview (thumbnail)',
               False): [PDS_DATA_DIR + '/volumes/COISS_2xxx/COISS_2002/extras/thumbnail/1460960653_1461048959/N1460960868_1.IMG.jpeg_small'],
              ('Cassini ISS',
               120,
               'coiss_medium',
               'Extra Preview (medium)',
               False): [PDS_DATA_DIR + '/volumes/COISS_2xxx/COISS_2002/extras/browse/1460960653_1461048959/N1460960868_1.IMG.jpeg'],
              ('Cassini ISS',
               130,
               'coiss_full',
               'Extra Preview (full)',
               False): [PDS_DATA_DIR + '/volumes/COISS_2xxx/COISS_2002/extras/full/1460960653_1461048959/N1460960868_1.IMG.png'],
              ('Cassini ISS',
               10,
               'coiss_calib',
               'Calibrated Image',
               True): [PDS_DATA_DIR + '/calibrated/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460960868_1_CALIB.IMG',
                       PDS_DATA_DIR + '/calibrated/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460960868_1_CALIB.LBL',
                       PDS_DATA_DIR + '/calibrated/COISS_2xxx_v1/COISS_2002/data/1460960653_1461048959/N1460960868_1_CALIB.IMG',
                       PDS_DATA_DIR + '/calibrated/COISS_2xxx_v1/COISS_2002/data/1460960653_1461048959/N1460960868_1_CALIB.LBL',
                       PDS_DATA_DIR + '/calibrated/COISS_2xxx_v2/COISS_2002/data/1460960653_1461048959/N1460960868_1_CALIB.IMG',
                       PDS_DATA_DIR + '/calibrated/COISS_2xxx_v2/COISS_2002/data/1460960653_1461048959/N1460960868_1_CALIB.LBL'],
              ('browse',
               10,
               'browse_thumb',
               'Browse Image (thumbnail)',
               False): [PDS_DATA_DIR + '/previews/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460960868_1_thumb.jpg'],
              ('browse',
               20,
               'browse_small',
               'Browse Image (small)',
               False): [PDS_DATA_DIR + '/previews/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460960868_1_small.jpg'],
              ('browse',
               30,
               'browse_medium',
               'Browse Image (medium)',
               False): [PDS_DATA_DIR + '/previews/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460960868_1_med.jpg'],
              ('browse',
               40,
               'browse_full',
               'Browse Image (full)',
               True): [PDS_DATA_DIR + '/previews/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460960868_1_full.png'],
              ('metadata',
               20,
               'planet_geometry',
               'Planet Geometry Index',
               False): [PDS_DATA_DIR + '/metadata/COISS_2xxx/COISS_2002/COISS_2002_saturn_summary.tab',
                        PDS_DATA_DIR + '/metadata/COISS_2xxx/COISS_2002/COISS_2002_saturn_summary.lbl'],
              ('metadata',
               30,
               'moon_geometry',
               'Moon Geometry Index',
               False): [PDS_DATA_DIR + '/metadata/COISS_2xxx/COISS_2002/COISS_2002_moon_summary.tab',
                        PDS_DATA_DIR + '/metadata/COISS_2xxx/COISS_2002/COISS_2002_moon_summary.lbl'],
              ('metadata',
               40,
               'ring_geometry',
               'Ring Geometry Index',
               False): [PDS_DATA_DIR + '/metadata/COISS_2xxx/COISS_2002/COISS_2002_ring_summary.tab',
                        PDS_DATA_DIR + '/metadata/COISS_2xxx/COISS_2002/COISS_2002_ring_summary.lbl'],
              ('metadata',
               10,
               'inventory',
               'Target Body Inventory',
               False): [PDS_DATA_DIR + '/metadata/COISS_2xxx/COISS_2002/COISS_2002_inventory.csv',
                        PDS_DATA_DIR + '/metadata/COISS_2xxx/COISS_2002/COISS_2002_inventory.lbl'],
              ('metadata',
               5,
               'rms_index',
               'RMS Node Augmented Index',
               False): [PDS_DATA_DIR + '/metadata/COISS_2xxx/COISS_2002/COISS_2002_index.tab',
                        PDS_DATA_DIR + '/metadata/COISS_2xxx/COISS_2002/COISS_2002_index.lbl']}
            ),
        ]
    )
    def test_opus_products_coiss_2xxx(self, input_path, expected):
        opus_products_test(input_path, expected)


    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/HSTIx_xxxx/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ.ASC',
             {('HST',
               20,
               'hst_tiff',
               'Raw Data Preview (lossless)',
               True): [PDS_DATA_DIR + '/volumes/HSTIx_xxxx/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ_RAW.TIF',
                       PDS_DATA_DIR + '/volumes/HSTIx_xxxx/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ.LBL',
                       PDS_DATA_DIR + '/volumes/HSTIx_xxxx_v1.1/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ_RAW.TIF',
                       PDS_DATA_DIR + '/volumes/HSTIx_xxxx_v1.1/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ.LBL',
                       PDS_DATA_DIR + '/volumes/HSTIx_xxxx_v1.0/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ_RAW.TIF',
                       PDS_DATA_DIR + '/volumes/HSTIx_xxxx_v1.0/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ.LBL'],
              ('HST',
               40,
               'hst_calib',
               'Calibrated Data Preview',
               True): [PDS_DATA_DIR + '/volumes/HSTIx_xxxx/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ_FLT.JPG',
                       PDS_DATA_DIR + '/volumes/HSTIx_xxxx/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ.LBL',
                       PDS_DATA_DIR + '/volumes/HSTIx_xxxx_v1.1/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ_FLT.JPG',
                       PDS_DATA_DIR + '/volumes/HSTIx_xxxx_v1.1/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ.LBL',
                       PDS_DATA_DIR + '/volumes/HSTIx_xxxx_v1.0/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ_FLT.JPG',
                       PDS_DATA_DIR + '/volumes/HSTIx_xxxx_v1.0/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ.LBL'],
              ('HST',
               30,
               'hst_raw',
               'Raw Data Preview',
               True): [PDS_DATA_DIR + '/volumes/HSTIx_xxxx/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ_RAW.JPG',
                       PDS_DATA_DIR + '/volumes/HSTIx_xxxx/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ.LBL',
                       PDS_DATA_DIR + '/volumes/HSTIx_xxxx_v1.1/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ_RAW.JPG',
                       PDS_DATA_DIR + '/volumes/HSTIx_xxxx_v1.1/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ.LBL',
                       PDS_DATA_DIR + '/volumes/HSTIx_xxxx_v1.0/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ_RAW.JPG',
                       PDS_DATA_DIR + '/volumes/HSTIx_xxxx_v1.0/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ.LBL'],
              ('HST',
               70,
               'hst_drizzled',
               'Calibrated Geometrically Corrected Preview',
               True): [PDS_DATA_DIR + '/volumes/HSTIx_xxxx/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ_DRZ.JPG',
                       PDS_DATA_DIR + '/volumes/HSTIx_xxxx/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ.LBL',
                       PDS_DATA_DIR + '/volumes/HSTIx_xxxx_v1.1/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ_DRZ.JPG',
                       PDS_DATA_DIR + '/volumes/HSTIx_xxxx_v1.1/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ.LBL',
                       PDS_DATA_DIR + '/volumes/HSTIx_xxxx_v1.0/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ_DRZ.JPG',
                       PDS_DATA_DIR + '/volumes/HSTIx_xxxx_v1.0/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ.LBL'],
              ('HST',
               10,
               'hst_text',
               'FITS Header Text',
               True): [PDS_DATA_DIR + '/volumes/HSTIx_xxxx/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ.ASC',
                       PDS_DATA_DIR + '/volumes/HSTIx_xxxx/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ.LBL',
                       PDS_DATA_DIR + '/volumes/HSTIx_xxxx_v1.1/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ.ASC',
                       PDS_DATA_DIR + '/volumes/HSTIx_xxxx_v1.1/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ.LBL',
                       PDS_DATA_DIR + '/volumes/HSTIx_xxxx_v1.0/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ.ASC',
                       PDS_DATA_DIR + '/volumes/HSTIx_xxxx_v1.0/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ.LBL'],
              ('browse',
               10,
               'browse_thumb',
               'Browse Image (thumbnail)',
               False): [PDS_DATA_DIR + '/previews/HSTIx_xxxx/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ_thumb.jpg'],
              ('browse',
               20,
               'browse_small',
               'Browse Image (small)',
               False): [PDS_DATA_DIR + '/previews/HSTIx_xxxx/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ_small.jpg'],
              ('browse',
               30,
               'browse_medium',
               'Browse Image (medium)',
               False): [PDS_DATA_DIR + '/previews/HSTIx_xxxx/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ_med.jpg'],
              ('browse',
               40,
               'browse_full',
               'Browse Image (full)',
               True): [PDS_DATA_DIR + '/previews/HSTIx_xxxx/HSTI1_1559/DATA/VISIT_11/IB4V11MNQ_full.jpg'],
              ('metadata',
               5,
               'rms_index',
               'RMS Node Augmented Index',
               False): [PDS_DATA_DIR + '/metadata/HSTIx_xxxx/HSTI1_1559/HSTI1_1559_index.tab',
                        PDS_DATA_DIR + '/metadata/HSTIx_xxxx/HSTI1_1559/HSTI1_1559_index.lbl'],
              ('metadata',
               6,
               'hstfiles_index',
               'HST Files Associations Index',
               False): [PDS_DATA_DIR + '/metadata/HSTIx_xxxx/HSTI1_1559/HSTI1_1559_hstfiles.tab',
                        PDS_DATA_DIR + '/metadata/HSTIx_xxxx/HSTI1_1559/HSTI1_1559_hstfiles.lbl']}
            ),
        ]
    )
    def test_opus_products_hstix_xxxx(self, input_path, expected):
        opus_products_test(input_path, expected)

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COVIMS_0xxx/COVIMS_0006/data/2005088T102825_2005089T113931/v1490784910_3_001.qub',
            {('Cassini VIMS',
              0,
              'covims_raw',
              'Raw Cube',
              True): [PDS_DATA_DIR + '/volumes/COVIMS_0xxx/COVIMS_0006/data/2005088T102825_2005089T113931/v1490784910_3_001.qub',
                      PDS_DATA_DIR + '/volumes/COVIMS_0xxx/COVIMS_0006/data/2005088T102825_2005089T113931/v1490784910_3_001.lbl',
                      PDS_DATA_DIR + '/volumes/COVIMS_0xxx/COVIMS_0006/label/band_bin_center.fmt',
                      PDS_DATA_DIR + '/volumes/COVIMS_0xxx/COVIMS_0006/label/core_description.fmt',
                      PDS_DATA_DIR + '/volumes/COVIMS_0xxx/COVIMS_0006/label/suffix_description.fmt'],
             ('Cassini VIMS',
              110,
              'covims_thumb',
              'Extra Preview (thumbnail)',
              False): [PDS_DATA_DIR + '/volumes/COVIMS_0xxx/COVIMS_0006/extras/thumbnail/2005088T102825_2005089T113931/v1490784910_3_001.qub.jpeg_small'],
             ('Cassini VIMS',
              120,
              'covims_medium',
              'Extra Preview (medium)',
              False): [PDS_DATA_DIR + '/volumes/COVIMS_0xxx/COVIMS_0006/extras/browse/2005088T102825_2005089T113931/v1490784910_3_001.qub.jpeg'],
             ('Cassini VIMS',
              130,
              'covims_full',
              'Extra Preview (full)',
              False): [PDS_DATA_DIR + '/volumes/COVIMS_0xxx/COVIMS_0006/extras/tiff/2005088T102825_2005089T113931/v1490784910_3_001.qub.tiff'],
             ('browse',
              40,
              'browse_full',
              'Browse Image (full)',
              True): [PDS_DATA_DIR + '/previews/COVIMS_0xxx/COVIMS_0006/data/2005088T102825_2005089T113931/v1490784910_3_001_full.png'],
             ('browse',
              30,
              'browse_medium',
              'Browse Image (medium)',
              False): [PDS_DATA_DIR + '/previews/COVIMS_0xxx/COVIMS_0006/data/2005088T102825_2005089T113931/v1490784910_3_001_med.png'],
             ('browse',
              20,
              'browse_small',
              'Browse Image (small)',
              False): [PDS_DATA_DIR + '/previews/COVIMS_0xxx/COVIMS_0006/data/2005088T102825_2005089T113931/v1490784910_3_001_small.png'],
             ('browse',
              10,
              'browse_thumb',
              'Browse Image (thumbnail)',
              False): [PDS_DATA_DIR + '/previews/COVIMS_0xxx/COVIMS_0006/data/2005088T102825_2005089T113931/v1490784910_3_001_thumb.png'],
             ('metadata',
              30,
              'moon_geometry',
              'Moon Geometry Index',
              False): [PDS_DATA_DIR + '/metadata/COVIMS_0xxx/COVIMS_0006/COVIMS_0006_moon_summary.tab',
               PDS_DATA_DIR + '/metadata/COVIMS_0xxx/COVIMS_0006/COVIMS_0006_moon_summary.lbl'],
             ('metadata',
              40,
              'ring_geometry',
              'Ring Geometry Index',
              False): [PDS_DATA_DIR + '/metadata/COVIMS_0xxx/COVIMS_0006/COVIMS_0006_ring_summary.tab',
               PDS_DATA_DIR + '/metadata/COVIMS_0xxx/COVIMS_0006/COVIMS_0006_ring_summary.lbl'],
             ('metadata',
              20,
              'planet_geometry',
              'Planet Geometry Index',
              False): [PDS_DATA_DIR + '/metadata/COVIMS_0xxx/COVIMS_0006/COVIMS_0006_saturn_summary.tab',
               PDS_DATA_DIR + '/metadata/COVIMS_0xxx/COVIMS_0006/COVIMS_0006_saturn_summary.lbl'],
             ('metadata',
              10,
              'inventory',
              'Target Body Inventory',
              False): [PDS_DATA_DIR + '/metadata/COVIMS_0xxx/COVIMS_0006/COVIMS_0006_inventory.csv',
               PDS_DATA_DIR + '/metadata/COVIMS_0xxx/COVIMS_0006/COVIMS_0006_inventory.lbl'],
             ('metadata',
              5,
              'rms_index',
              'RMS Node Augmented Index',
              False): [PDS_DATA_DIR + '/metadata/COVIMS_0xxx/COVIMS_0006/COVIMS_0006_index.tab',
               PDS_DATA_DIR + '/metadata/COVIMS_0xxx/COVIMS_0006/COVIMS_0006_index.lbl'],
             ('metadata',
              9,
              'supplemental_index',
              'Supplemental Index',
              False): [PDS_DATA_DIR + '/metadata/COVIMS_0xxx/COVIMS_0006/COVIMS_0006_supplemental_index.tab',
               PDS_DATA_DIR + '/metadata/COVIMS_0xxx/COVIMS_0006/COVIMS_0006_supplemental_index.lbl']}
            ),
        ]
    )
    def test_opus_products_covims_0xxx(self, input_path, expected):
        opus_products_test(input_path, expected)

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COVIMS_8xxx/COVIMS_8001/data/VIMS_2005_144_OMICET_E_TAU_01KM.TAB',
            {('Cassini VIMS',
              10,
              'covims_occ_01',
              'Occultation Profile (1 km)',
              True): [PDS_DATA_DIR + '/volumes/COVIMS_8xxx/COVIMS_8001/data/VIMS_2005_144_OMICET_E_TAU_01KM.TAB',
                      PDS_DATA_DIR + '/volumes/COVIMS_8xxx/COVIMS_8001/data/VIMS_2005_144_OMICET_E_TAU_01KM.LBL',
                      PDS_DATA_DIR + '/volumes/COVIMS_8xxx_v2.0/COVIMS_8001/data/VIMS_2005_144_OMICET_E_TAU_01KM.TAB',
                      PDS_DATA_DIR + '/volumes/COVIMS_8xxx_v2.0/COVIMS_8001/data/VIMS_2005_144_OMICET_E_TAU_01KM.LBL',
                      PDS_DATA_DIR + '/volumes/COVIMS_8xxx_v1/COVIMS_8001/EASYDATA/VIMS_2005_144_OMICET_E_TAU_01KM.TAB',
                      PDS_DATA_DIR + '/volumes/COVIMS_8xxx_v1/COVIMS_8001/EASYDATA/VIMS_2005_144_OMICET_E_TAU_01KM.LBL'],
             ('Cassini VIMS',
              20,
              'covims_occ_10',
              'Occultation Profile (10 km)',
              True): [PDS_DATA_DIR + '/volumes/COVIMS_8xxx/COVIMS_8001/data/VIMS_2005_144_OMICET_E_TAU_10KM.TAB',
                      PDS_DATA_DIR + '/volumes/COVIMS_8xxx/COVIMS_8001/data/VIMS_2005_144_OMICET_E_TAU_10KM.LBL',
                      PDS_DATA_DIR + '/volumes/COVIMS_8xxx_v2.0/COVIMS_8001/data/VIMS_2005_144_OMICET_E_TAU_10KM.TAB',
                      PDS_DATA_DIR + '/volumes/COVIMS_8xxx_v2.0/COVIMS_8001/data/VIMS_2005_144_OMICET_E_TAU_10KM.LBL',
                      PDS_DATA_DIR + '/volumes/COVIMS_8xxx_v1/COVIMS_8001/EASYDATA/VIMS_2005_144_OMICET_E_TAU_10KM.TAB',
                      PDS_DATA_DIR + '/volumes/COVIMS_8xxx_v1/COVIMS_8001/EASYDATA/VIMS_2005_144_OMICET_E_TAU_10KM.LBL'],
             ('browse',
              40,
              'browse_full',
              'Browse Image (full)',
              True): [PDS_DATA_DIR + '/previews/COVIMS_8xxx/COVIMS_8001/data/VIMS_2005_144_OMICET_E_TAU_full.jpg',
                      PDS_DATA_DIR + '/previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_STAR_full.jpg',
                      PDS_DATA_DIR + '/previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_NPOLE_full.jpg',
                      PDS_DATA_DIR + '/previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_LIGHTCURVE_full.jpg',
                      PDS_DATA_DIR + '/previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_GEOMETRY_full.jpg'],
             ('browse',
              30,
              'browse_medium',
              'Browse Image (medium)',
              False): [PDS_DATA_DIR + '/previews/COVIMS_8xxx/COVIMS_8001/data/VIMS_2005_144_OMICET_E_TAU_med.jpg',
                       PDS_DATA_DIR + '/previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_STAR_med.jpg',
                       PDS_DATA_DIR + '/previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_NPOLE_med.jpg',
                       PDS_DATA_DIR + '/previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_LIGHTCURVE_med.jpg', PDS_DATA_DIR + '/previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_GEOMETRY_med.jpg'],
             ('browse',
              20,
              'browse_small',
              'Browse Image (small)',
              False): [PDS_DATA_DIR + '/previews/COVIMS_8xxx/COVIMS_8001/data/VIMS_2005_144_OMICET_E_TAU_small.jpg',
                       PDS_DATA_DIR + '/previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_STAR_small.jpg',
                       PDS_DATA_DIR + '/previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_NPOLE_small.jpg',
                       PDS_DATA_DIR + '/previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_LIGHTCURVE_small.jpg', PDS_DATA_DIR + '/previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_GEOMETRY_small.jpg'],
             ('browse',
              10,
              'browse_thumb',
              'Browse Image (thumbnail)',
              False): [PDS_DATA_DIR + '/previews/COVIMS_8xxx/COVIMS_8001/data/VIMS_2005_144_OMICET_E_TAU_thumb.jpg',
                       PDS_DATA_DIR + '/previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_STAR_thumb.jpg',
                       PDS_DATA_DIR + '/previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_NPOLE_thumb.jpg',
                       PDS_DATA_DIR + '/previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_LIGHTCURVE_thumb.jpg', PDS_DATA_DIR + '/previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_GEOMETRY_thumb.jpg'],
             ('diagram',
              40,
              'diagram_full',
              'Browse Diagram (full)',
              True): [PDS_DATA_DIR + '/diagrams/COVIMS_8xxx/COVIMS_8001/data/VIMS_2005_144_OMICET_E_full.jpg'],
             ('diagram',
              30,
              'diagram_medium',
              'Browse Diagram (medium)',
              False): [PDS_DATA_DIR + '/diagrams/COVIMS_8xxx/COVIMS_8001/data/VIMS_2005_144_OMICET_E_med.jpg'],
             ('diagram',
              20,
              'diagram_small',
              'Browse Diagram (small)',
              False): [PDS_DATA_DIR + '/diagrams/COVIMS_8xxx/COVIMS_8001/data/VIMS_2005_144_OMICET_E_small.jpg'],
             ('diagram',
              10,
              'diagram_thumb',
              'Browse Diagram (thumbnail)',
              False): [PDS_DATA_DIR + '/diagrams/COVIMS_8xxx/COVIMS_8001/data/VIMS_2005_144_OMICET_E_thumb.jpg'],
             ('metadata',
              5,
              'rms_index',
              'RMS Node Augmented Index',
              False): [PDS_DATA_DIR + '/metadata/COVIMS_8xxx/COVIMS_8001/COVIMS_8001_index.tab',
                       PDS_DATA_DIR + '/metadata/COVIMS_8xxx/COVIMS_8001/COVIMS_8001_index.lbl'],
             ('metadata',
              8,
              'profile_index',
              'Profile Index',
              False): [PDS_DATA_DIR + '/metadata/COVIMS_8xxx/COVIMS_8001/COVIMS_8001_profile_index.tab',
                       PDS_DATA_DIR + '/metadata/COVIMS_8xxx/COVIMS_8001/COVIMS_8001_profile_index.lbl'],
             ('metadata',
              9,
              'supplemental_index',
              'Supplemental Index',
              False): [PDS_DATA_DIR + '/metadata/COVIMS_8xxx/COVIMS_8001/COVIMS_8001_supplemental_index.tab',
                       PDS_DATA_DIR + '/metadata/COVIMS_8xxx/COVIMS_8001/COVIMS_8001_supplemental_index.lbl']}
            ),
        ]
    )
    def test_opus_products_covims_8xxx(self, input_path, expected):
        opus_products_test(input_path, expected)

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COCIRS_5xxx/COCIRS_5408/DATA/POIDATA/POI0408010000_FP1.LBL',
             {('Cassini CIRS',
               0,
               'cocirs_spec',
               'Calibrated Interferograms',
               True): [PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/DATA/APODSPEC/SPEC0408010000_FP1.DAT',
                       PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/DATA/APODSPEC/SPEC0408010000_FP1.LBL'],
              ('Cassini CIRS',
               110,
               'cocirs_geo',
               'System Geometry',
               True): [PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/DATA/GEODATA/GEO0408010000_699.TAB',
                       PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/DATA/GEODATA/GEO0408010000_699.LBL',
                       PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/DATA/GEODATA/GEODATA.FMT',
                       PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/DATA/GEODATA/GEO0408010000_617.TAB',
                       PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/DATA/GEODATA/GEO0408010000_617.LBL',
                       PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/DATA/GEODATA/GEODATA.FMT',
                       PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/DATA/GEODATA/GEO0408010000_611.TAB',
                       PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/DATA/GEODATA/GEO0408010000_611.LBL',
                       PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/DATA/GEODATA/GEODATA.FMT'],
              ('Cassini CIRS',
               120,
               'cocirs_ispm',
               'Observation Metadata',
               True): [PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/DATA/ISPMDATA/ISPM0408010000_FP1.TAB',
                       PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/DATA/ISPMDATA/ISPM0408010000_FP1.LBL',
                       PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/DATA/ISPMDATA/ISPMDATA.FMT'],
              ('Cassini CIRS',
               130,
               'cocirs_poi',
               'Footprint Geometry on Bodies',
               True): [PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/DATA/POIDATA/POI0408010000_FP1.TAB',
                       PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/DATA/POIDATA/POI0408010000_FP1.LBL',
                       PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/DATA/POIDATA/POIDATA.FMT'],
              ('Cassini CIRS',
               140,
               'cocirs_rin',
               'Footprint Geometry on Rings',
               True): [PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/DATA/RINDATA/RIN0408010000_FP1.TAB',
                       PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/DATA/RINDATA/RIN0408010000_FP1.LBL',
                       PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/DATA/RINDATA/RINDATA.FMT'],
              ('Cassini CIRS',
               150,
               'cocirs_tar',
               'Target Body Identifications',
               True): [PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/DATA/TARDATA/TAR0408010000_FP1.TAB',
                       PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/DATA/TARDATA/TAR0408010000_FP1.LBL',
                       PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/DATA/TARDATA/TARDATA.FMT'],
              ('Cassini CIRS',
               510,
               'cocirs_browse_target',
               'Extra Browse Diagram (Default)',
               True): [PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/BROWSE/TARGETS/IMG0408010000_FP1.PNG',
                       PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/BROWSE/TARGETS/IMG0408010000_FP1.LBL'],
              ('Cassini CIRS',
               520,
               'cocirs_browse_saturn',
               'Extra Browse Diagram (Saturn)',
               True): [PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/BROWSE/SATURN/POI0408010000_FP1.PNG',
                       PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/BROWSE/SATURN/POI0408010000_FP1.LBL'],
              ('Cassini CIRS',
               530,
               'cocirs_browse_rings',
               'Extra Browse Diagram (Rings)',
               True): [PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/BROWSE/S_RINGS/RIN0408010000_FP1.PNG',
                       PDS_DATA_DIR + '/volumes/COCIRS_5xxx/COCIRS_5408/BROWSE/S_RINGS/RIN0408010000_FP1.LBL'],
              ('diagram',
               40,
               'diagram_full',
               'Browse Diagram (full)',
               True): [PDS_DATA_DIR + '/diagrams/COCIRS_5xxx/COCIRS_5408/BROWSE/S_RINGS/RIN0408010000_FP1_full.jpg',
                       PDS_DATA_DIR + '/diagrams/COCIRS_5xxx/COCIRS_5408/BROWSE/SATURN/POI0408010000_FP1_full.jpg'],
              ('diagram',
               30,
               'diagram_medium',
               'Browse Diagram (medium)',
               False): [PDS_DATA_DIR + '/diagrams/COCIRS_5xxx/COCIRS_5408/BROWSE/S_RINGS/RIN0408010000_FP1_med.jpg',
                        PDS_DATA_DIR + '/diagrams/COCIRS_5xxx/COCIRS_5408/BROWSE/SATURN/POI0408010000_FP1_med.jpg'],
              ('diagram',
               20,
               'diagram_small',
               'Browse Diagram (small)',
               False): [PDS_DATA_DIR + '/diagrams/COCIRS_5xxx/COCIRS_5408/BROWSE/S_RINGS/RIN0408010000_FP1_small.jpg',
                        PDS_DATA_DIR + '/diagrams/COCIRS_5xxx/COCIRS_5408/BROWSE/SATURN/POI0408010000_FP1_small.jpg'],
              ('diagram',
               10,
               'diagram_thumb',
               'Browse Diagram (thumbnail)',
               False): [PDS_DATA_DIR + '/diagrams/COCIRS_5xxx/COCIRS_5408/BROWSE/S_RINGS/RIN0408010000_FP1_thumb.jpg',
                        PDS_DATA_DIR + '/diagrams/COCIRS_5xxx/COCIRS_5408/BROWSE/SATURN/POI0408010000_FP1_thumb.jpg'],
              ('browse',
               30,
               'browse_medium',
               'Browse Image (medium)',
               False): [PDS_DATA_DIR + '/diagrams/COCIRS_5xxx/COCIRS_5408/BROWSE/TARGETS/IMG0408010000_FP1_med.jpg'],
              ('browse',
               10,
               'browse_thumb',
               'Browse Image (thumbnail)',
               False): [PDS_DATA_DIR + '/diagrams/COCIRS_5xxx/COCIRS_5408/BROWSE/TARGETS/IMG0408010000_FP1_thumb.jpg'],
              ('browse',
               20,
               'browse_small',
               'Browse Image (small)',
               False): [PDS_DATA_DIR + '/diagrams/COCIRS_5xxx/COCIRS_5408/BROWSE/TARGETS/IMG0408010000_FP1_small.jpg'],
              ('browse',
               40,
               'browse_full',
               'Browse Image (full)',
               True): [PDS_DATA_DIR + '/diagrams/COCIRS_5xxx/COCIRS_5408/BROWSE/TARGETS/IMG0408010000_FP1_full.jpg']}
            )
        ]
    )
    def test_opus_products_cocir_0xxx(self, input_path, expected):
        opus_products_test(input_path, expected)

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/FUV1999_007_16_57.DAT',
             {('Cassini UVIS',
               10,
               'couvis_raw',
               'Raw Data',
               True): [PDS_DATA_DIR + '/volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/FUV1999_007_16_57.DAT',
                       PDS_DATA_DIR + '/volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/FUV1999_007_16_57.LBL'],
              ('Cassini UVIS',
               20,
               'couvis_calib_corr',
               'Calibration Data',
               True): [PDS_DATA_DIR + '/volumes/COUVIS_0xxx/COUVIS_0001/CALIB/VERSION_3/D1999_007/FUV1999_007_16_57_CAL_3.DAT',
                       PDS_DATA_DIR + '/volumes/COUVIS_0xxx/COUVIS_0001/CALIB/VERSION_3/D1999_007/FUV1999_007_16_57_CAL_3.LBL'],
              ('browse',
               10,
               'browse_thumb',
               'Browse Image (thumbnail)',
               False): [PDS_DATA_DIR + '/previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/FUV1999_007_16_57_thumb.png'],
              ('browse',
               20,
               'browse_small',
               'Browse Image (small)',
               False): [PDS_DATA_DIR + '/previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/FUV1999_007_16_57_small.png'],
              ('browse',
               30,
               'browse_medium',
               'Browse Image (medium)',
               False): [PDS_DATA_DIR + '/previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/FUV1999_007_16_57_med.png'],
              ('browse',
               40,
               'browse_full',
               'Browse Image (full)',
               True): [PDS_DATA_DIR + '/previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/FUV1999_007_16_57_full.png'],
              ('metadata',
               5,
               'rms_index',
               'RMS Node Augmented Index',
               False): [PDS_DATA_DIR + '/metadata/COUVIS_0xxx/COUVIS_0001/COUVIS_0001_index.tab',
                        PDS_DATA_DIR + '/metadata/COUVIS_0xxx/COUVIS_0001/COUVIS_0001_index.lbl'],
              ('metadata',
               9,
               'supplemental_index',
               'Supplemental Index',
               False): [PDS_DATA_DIR + '/metadata/COUVIS_0xxx/COUVIS_0001/COUVIS_0001_supplemental_index.tab',
                        PDS_DATA_DIR + '/metadata/COUVIS_0xxx/COUVIS_0001/COUVIS_0001_supplemental_index.lbl']}
            )
        ]
    )
    def test_opus_products_couvis_0xxx(self, input_path, expected):
        opus_products_test(input_path, expected)

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_TAU01KM.TAB',
            {('Cassini UVIS',
              10,
              'couvis_occ_01',
              'Occultation Profile (1 km)',
              True): [PDS_DATA_DIR + '/volumes/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_TAU01KM.TAB',
                      PDS_DATA_DIR + '/volumes/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_TAU01KM.LBL',
                      PDS_DATA_DIR + '/volumes/COUVIS_8xxx_v2.1/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_TAU01KM.TAB',
                      PDS_DATA_DIR + '/volumes/COUVIS_8xxx_v2.1/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_TAU01KM.LBL',
                      PDS_DATA_DIR + '/volumes/COUVIS_8xxx_v2.0/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_TAU01KM.TAB',
                      PDS_DATA_DIR + '/volumes/COUVIS_8xxx_v2.0/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_TAU01KM.LBL',
                      PDS_DATA_DIR + '/volumes/COUVIS_8xxx_v1/COUVIS_8001/DATA/EASYDATA/UVIS_HSP_2005_139_126TAU_E_TAU_01KM.TAB',
                      PDS_DATA_DIR + '/volumes/COUVIS_8xxx_v1/COUVIS_8001/DATA/EASYDATA/UVIS_HSP_2005_139_126TAU_E_TAU_01KM.LBL'],
             ('Cassini UVIS',
              20,
              'couvis_occ_10',
              'Occultation Profile (10 km)',
              True): [PDS_DATA_DIR + '/volumes/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_TAU10KM.TAB',
                      PDS_DATA_DIR + '/volumes/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_TAU10KM.LBL',
                      PDS_DATA_DIR + '/volumes/COUVIS_8xxx_v2.1/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_TAU10KM.TAB',
                      PDS_DATA_DIR + '/volumes/COUVIS_8xxx_v2.1/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_TAU10KM.LBL',
                      PDS_DATA_DIR + '/volumes/COUVIS_8xxx_v2.0/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_TAU10KM.TAB',
                      PDS_DATA_DIR + '/volumes/COUVIS_8xxx_v2.0/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_TAU10KM.LBL',
                      PDS_DATA_DIR + '/volumes/COUVIS_8xxx_v1/COUVIS_8001/DATA/EASYDATA/UVIS_HSP_2005_139_126TAU_E_TAU_10KM.TAB',
                      PDS_DATA_DIR + '/volumes/COUVIS_8xxx_v1/COUVIS_8001/DATA/EASYDATA/UVIS_HSP_2005_139_126TAU_E_TAU_10KM.LBL'],
             ('browse',
              40,
              'browse_full',
              'Browse Image (full)',
              True): [PDS_DATA_DIR + '/previews/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_full.jpg'],
             ('browse',
              30,
              'browse_medium',
              'Browse Image (medium)',
              False): [PDS_DATA_DIR + '/previews/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_med.jpg'],
             ('browse',
              20,
              'browse_small',
              'Browse Image (small)',
              False): [PDS_DATA_DIR + '/previews/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_small.jpg'],
             ('browse',
              10,
              'browse_thumb',
              'Browse Image (thumbnail)',
              False): [PDS_DATA_DIR + '/previews/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_thumb.jpg'],
             ('diagram',
              40,
              'diagram_full',
              'Browse Diagram (full)',
              True): [PDS_DATA_DIR + '/diagrams/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_full.jpg'],
             ('diagram',
              30,
              'diagram_medium',
              'Browse Diagram (medium)',
              False): [PDS_DATA_DIR + '/diagrams/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_med.jpg'],
             ('diagram',
              20,
              'diagram_small',
              'Browse Diagram (small)',
              False): [PDS_DATA_DIR + '/diagrams/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_small.jpg'],
             ('diagram',
              10,
              'diagram_thumb',
              'Browse Diagram (thumbnail)',
              False): [PDS_DATA_DIR + '/diagrams/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_thumb.jpg'],
             ('metadata',
              5,
              'rms_index',
              'RMS Node Augmented Index',
              False): [PDS_DATA_DIR + '/metadata/COUVIS_8xxx/COUVIS_8001/COUVIS_8001_index.tab',
                       PDS_DATA_DIR + '/metadata/COUVIS_8xxx/COUVIS_8001/COUVIS_8001_index.lbl'],
             ('metadata',
              8,
              'profile_index',
              'Profile Index',
              False): [PDS_DATA_DIR + '/metadata/COUVIS_8xxx/COUVIS_8001/COUVIS_8001_profile_index.tab',
                       PDS_DATA_DIR + '/metadata/COUVIS_8xxx/COUVIS_8001/COUVIS_8001_profile_index.lbl'],
             ('metadata',
              9,
              'supplemental_index',
              'Supplemental Index',
              False): [PDS_DATA_DIR + '/metadata/COUVIS_8xxx/COUVIS_8001/COUVIS_8001_supplemental_index.tab',
                       PDS_DATA_DIR + '/metadata/COUVIS_8xxx/COUVIS_8001/COUVIS_8001_supplemental_index.lbl']}
            )
        ]
    )
    def test_opus_products_couvis_8xxx(self, input_path, expected):
        opus_products_test(input_path, expected)

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009E/Rev009E_RSS_2005_159_K55_E/RSS_2005_159_K55_E_TAU_01KM.TAB',
             {('Cassini RSS',
               40,
               'corss_occ_cal',
               'Occultation Calibration Parameters',
               True): [PDS_DATA_DIR + '/volumes/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009E/Rev009E_RSS_2005_159_K55_E/RSS_2005_159_K55_E_CAL.TAB',
                       PDS_DATA_DIR + '/volumes/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009E/Rev009E_RSS_2005_159_K55_E/RSS_2005_159_K55_E_CAL.LBL'],
              ('Cassini RSS',
               30,
               'corss_occ_dlp',
               'Diffraction-Ltd Occultation Profile',
               True): [PDS_DATA_DIR + '/volumes/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009E/Rev009E_RSS_2005_159_K55_E/RSS_2005_159_K55_E_DLP_500M.TAB',
                       PDS_DATA_DIR + '/volumes/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009E/Rev009E_RSS_2005_159_K55_E/RSS_2005_159_K55_E_DLP_500M.LBL'],
              ('Cassini RSS',
               50,
               'corss_occ_geo',
               'Occultation Geometry Parameters',
               True): [PDS_DATA_DIR + '/volumes/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009E/Rev009E_RSS_2005_159_K55_E/RSS_2005_159_K55_E_GEO.TAB',
                       PDS_DATA_DIR + '/volumes/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009E/Rev009E_RSS_2005_159_K55_E/RSS_2005_159_K55_E_GEO.LBL'],
              ('Cassini RSS',
               10,
               'corss_occ_best_res',
               'Occultation Profile (~1 km res)',
               True): [PDS_DATA_DIR + '/volumes/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009E/Rev009E_RSS_2005_159_K55_E/RSS_2005_159_K55_E_TAU_01KM.TAB',
                       PDS_DATA_DIR + '/volumes/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009E/Rev009E_RSS_2005_159_K55_E/RSS_2005_159_K55_E_TAU_01KM.LBL'],
              ('Cassini RSS',
               20,
               'corss_occ_10km_res',
               'Occultation Profile (10 km res)',
               True): [PDS_DATA_DIR + '/volumes/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009E/Rev009E_RSS_2005_159_K55_E/RSS_2005_159_K55_E_TAU_10KM.TAB',
                       PDS_DATA_DIR + '/volumes/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009E/Rev009E_RSS_2005_159_K55_E/RSS_2005_159_K55_E_TAU_10KM.LBL'],
              ('Cassini RSS',
               60,
               'corss_occ_doc',
               'Occultation Documentation',
               True): [PDS_DATA_DIR + '/volumes/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009_TimeLine_Table.pdf',
                       PDS_DATA_DIR + '/volumes/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009_TimeLine_Table.LBL',
                       PDS_DATA_DIR + '/volumes/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009_TimeLine_Figure.pdf',
                       PDS_DATA_DIR + '/volumes/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009_TimeLine_Figure.LBL',
                       PDS_DATA_DIR + '/volumes/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009_DSN_Elevation.pdf',
                       PDS_DATA_DIR + '/volumes/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009_DSN_Elevation.LBL',
                       PDS_DATA_DIR + '/volumes/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009E/Rev009E_RSS_2005_159_K55_E/Rev009E_RSS_2005_159_K55_E_Summary.pdf',
                       PDS_DATA_DIR + '/volumes/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009E/Rev009E_RSS_2005_159_K55_E/Rev009E_RSS_2005_159_K55_E_Summary.LBL',
                       PDS_DATA_DIR + '/volumes/CORSS_8xxx/CORSS_8001/browse/Rev009_OccTrack_Geometry.pdf',
                       PDS_DATA_DIR + '/volumes/CORSS_8xxx/CORSS_8001/browse/Rev009_OccTrack_Geometry.LBL'],
              ('browse',
               40,
               'browse_full',
               'Browse Image (full)',
               True): [PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009_TimeLine_Table_full.jpg',
                       PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009_TimeLine_Figure_full.jpg',
                       PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009_DSN_Elevation_full.jpg',
                       PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009E/Rev009E_RSS_2005_159_K55_E/Rev009E_RSS_2005_159_K55_E_Summary_full.jpg',
                       PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009E/Rev009E_RSS_2005_159_K55_E/RSS_2005_159_K55_E_TAU_full.jpg',
                       PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009E/Rev009E_RSS_2005_159_K55_E/RSS_2005_159_K55_E_GEO_full.jpg',
                       PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/browse/Rev009_OccTrack_Geometry_full.jpg'],
              ('browse',
               30,
               'browse_medium',
               'Browse Image (medium)',
               False): [PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009_TimeLine_Table_med.jpg',
                        PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009_TimeLine_Figure_med.jpg',
                        PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009_DSN_Elevation_med.jpg',
                        PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009E/Rev009E_RSS_2005_159_K55_E/Rev009E_RSS_2005_159_K55_E_Summary_med.jpg',
                        PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009E/Rev009E_RSS_2005_159_K55_E/RSS_2005_159_K55_E_TAU_med.jpg',
                        PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009E/Rev009E_RSS_2005_159_K55_E/RSS_2005_159_K55_E_GEO_med.jpg',
                        PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/browse/Rev009_OccTrack_Geometry_med.jpg'],
              ('browse',
               20,
               'browse_small',
               'Browse Image (small)',
               False): [PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009_TimeLine_Table_small.jpg',
                        PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009_TimeLine_Figure_small.jpg',
                        PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009_DSN_Elevation_small.jpg',
                        PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009E/Rev009E_RSS_2005_159_K55_E/Rev009E_RSS_2005_159_K55_E_Summary_small.jpg',
                        PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009E/Rev009E_RSS_2005_159_K55_E/RSS_2005_159_K55_E_TAU_small.jpg',
                        PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009E/Rev009E_RSS_2005_159_K55_E/RSS_2005_159_K55_E_GEO_small.jpg',
                        PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/browse/Rev009_OccTrack_Geometry_small.jpg'],
              ('browse',
               10,
               'browse_thumb',
               'Browse Image (thumbnail)',
               False): [PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009_TimeLine_Table_thumb.jpg',
                        PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009_TimeLine_Figure_thumb.jpg',
                        PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009_DSN_Elevation_thumb.jpg',
                        PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009E/Rev009E_RSS_2005_159_K55_E/Rev009E_RSS_2005_159_K55_E_Summary_thumb.jpg',
                        PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009E/Rev009E_RSS_2005_159_K55_E/RSS_2005_159_K55_E_TAU_thumb.jpg',
                        PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/data/Rev009/Rev009E/Rev009E_RSS_2005_159_K55_E/RSS_2005_159_K55_E_GEO_thumb.jpg',
                        PDS_DATA_DIR + '/previews/CORSS_8xxx/CORSS_8001/browse/Rev009_OccTrack_Geometry_thumb.jpg'],
              ('metadata',
               5,
               'rms_index',
               'RMS Node Augmented Index',
               False): [PDS_DATA_DIR + '/metadata/CORSS_8xxx/CORSS_8001/CORSS_8001_index.tab',
                        PDS_DATA_DIR + '/metadata/CORSS_8xxx/CORSS_8001/CORSS_8001_index.lbl'],
              ('metadata',
               8,
               'profile_index',
               'Profile Index',
               False): [PDS_DATA_DIR + '/metadata/CORSS_8xxx/CORSS_8001/CORSS_8001_profile_index.tab',
                        PDS_DATA_DIR + '/metadata/CORSS_8xxx/CORSS_8001/CORSS_8001_profile_index.lbl'],
              ('metadata',
               9,
               'supplemental_index',
               'Supplemental Index',
               False): [PDS_DATA_DIR + '/metadata/CORSS_8xxx/CORSS_8001/CORSS_8001_supplemental_index.tab',
                        PDS_DATA_DIR + '/metadata/CORSS_8xxx/CORSS_8001/CORSS_8001_supplemental_index.lbl']}
            )
        ]
    )
    def test_opus_products_corss_8xxx(self, input_path, expected):
        opus_products_test(input_path, expected)

    @pytest.mark.parametrize(
    # Allow duplicated '/volumes/EBROCC_xxxx/EBROCC_0001/BROWSE/ESO1M/ES1_EGB.LBL'
    # and '/volumes/EBROCC_xxxx/EBROCC_0001/BROWSE/ESO1M/ES1_EPB.LBL' here. OPUS
    # will ignore the duplicated items
        'input_path,expected',
        [
            ('volumes/EBROCC_xxxx/EBROCC_0001/DATA/ESO1M/ES1_EPD.TAB',
            {('Earth-based Occultations',
              0,
              'ebro_profile',
              'Occultation Profile',
              True): [PDS_DATA_DIR + '/volumes/EBROCC_xxxx/EBROCC_0001/DATA/ESO1M/ES1_EPD.TAB',
                      PDS_DATA_DIR + '/volumes/EBROCC_xxxx/EBROCC_0001/DATA/ESO1M/ES1_EPD.LBL'],
             ('Earth-based Occultations',
              30,
              'ebro_diagram',
              'Geometry Diagram',
              False): [PDS_DATA_DIR + '/volumes/EBROCC_xxxx/EBROCC_0001/BROWSE/ESO1M/ES1_EGB.PS',
                       PDS_DATA_DIR + '/volumes/EBROCC_xxxx/EBROCC_0001/BROWSE/ESO1M/ES1_EGB.PDF',
                       PDS_DATA_DIR + '/volumes/EBROCC_xxxx/EBROCC_0001/BROWSE/ESO1M/ES1_EGB.LBL',
                       PDS_DATA_DIR + '/volumes/EBROCC_xxxx/EBROCC_0001/BROWSE/ESO1M/ES1_EGB.LBL'],
             ('Earth-based Occultations',
              20,
              'ebro_preview',
              'Preview Plot',
              True): [PDS_DATA_DIR + '/volumes/EBROCC_xxxx/EBROCC_0001/BROWSE/ESO1M/ES1_EPB.PS',
                      PDS_DATA_DIR + '/volumes/EBROCC_xxxx/EBROCC_0001/BROWSE/ESO1M/ES1_EPB.PDF',
                      PDS_DATA_DIR + '/volumes/EBROCC_xxxx/EBROCC_0001/BROWSE/ESO1M/ES1_EPB.LBL',
                      PDS_DATA_DIR + '/volumes/EBROCC_xxxx/EBROCC_0001/BROWSE/ESO1M/ES1_EPB.LBL'],
             ('Earth-based Occultations',
              10,
              'ebro_geom',
              'Geometry Table',
              True): [PDS_DATA_DIR + '/volumes/EBROCC_xxxx/EBROCC_0001/GEOMETRY/ESO1M/ES1_EGD.TAB',
                      PDS_DATA_DIR + '/volumes/EBROCC_xxxx/EBROCC_0001/GEOMETRY/ESO1M/ES1_EGD.LBL'],
             ('Earth-based Occultations',
              40,
              'ebro_source',
              'Source Data',
              False): [PDS_DATA_DIR + '/volumes/EBROCC_xxxx/EBROCC_0001/SORCDATA/ESO1M/ES1_EGRESS_GEOMETRY.DAT',
                       PDS_DATA_DIR + '/volumes/EBROCC_xxxx/EBROCC_0001/SORCDATA/ESO1M/ES1_EGRESS_GEOMETRY.LBL',
                       PDS_DATA_DIR + '/volumes/EBROCC_xxxx/EBROCC_0001/SORCDATA/ESO1M/ES1_EGRESS.OUT',
                       PDS_DATA_DIR + '/volumes/EBROCC_xxxx/EBROCC_0001/SORCDATA/ESO1M/ES1_EGRESS.LBL'],
             ('browse',
              40,
              'browse_full',
              'Browse Image (full)',
              True): [PDS_DATA_DIR + '/previews/EBROCC_xxxx/EBROCC_0001/DATA/ESO1M/ES1_EPD_full.jpg',
                      PDS_DATA_DIR + '/previews/EBROCC_xxxx/EBROCC_0001/BROWSE/ESO1M/ES1_EPB_full.jpg',
                      PDS_DATA_DIR + '/previews/EBROCC_xxxx/EBROCC_0001/BROWSE/ESO1M/ES1_EGB_full.jpg'],
             ('browse',
              30,
              'browse_medium',
              'Browse Image (medium)',
              False): [PDS_DATA_DIR + '/previews/EBROCC_xxxx/EBROCC_0001/DATA/ESO1M/ES1_EPD_med.jpg',
                       PDS_DATA_DIR + '/previews/EBROCC_xxxx/EBROCC_0001/BROWSE/ESO1M/ES1_EPB_med.jpg',
                       PDS_DATA_DIR + '/previews/EBROCC_xxxx/EBROCC_0001/BROWSE/ESO1M/ES1_EGB_med.jpg'],
             ('browse',
              20,
              'browse_small',
              'Browse Image (small)',
              False): [PDS_DATA_DIR + '/previews/EBROCC_xxxx/EBROCC_0001/DATA/ESO1M/ES1_EPD_small.jpg',
                       PDS_DATA_DIR + '/previews/EBROCC_xxxx/EBROCC_0001/BROWSE/ESO1M/ES1_EPB_small.jpg',
                       PDS_DATA_DIR + '/previews/EBROCC_xxxx/EBROCC_0001/BROWSE/ESO1M/ES1_EGB_small.jpg'],
             ('browse',
              10,
              'browse_thumb',
              'Browse Image (thumbnail)',
              False): [PDS_DATA_DIR + '/previews/EBROCC_xxxx/EBROCC_0001/DATA/ESO1M/ES1_EPD_thumb.jpg',
                       PDS_DATA_DIR + '/previews/EBROCC_xxxx/EBROCC_0001/BROWSE/ESO1M/ES1_EPB_thumb.jpg',
                       PDS_DATA_DIR + '/previews/EBROCC_xxxx/EBROCC_0001/BROWSE/ESO1M/ES1_EGB_thumb.jpg'],
             ('metadata',
              5,
              'rms_index',
              'RMS Node Augmented Index',
              False): [PDS_DATA_DIR + '/metadata/EBROCC_xxxx/EBROCC_0001/EBROCC_0001_index.tab',
                       PDS_DATA_DIR + '/metadata/EBROCC_xxxx/EBROCC_0001/EBROCC_0001_index.lbl'],
             ('metadata',
              8,
              'profile_index',
              'Profile Index',
              False): [PDS_DATA_DIR + '/metadata/EBROCC_xxxx/EBROCC_0001/EBROCC_0001_profile_index.tab',
                       PDS_DATA_DIR + '/metadata/EBROCC_xxxx/EBROCC_0001/EBROCC_0001_profile_index.lbl'],
             ('metadata',
              9,
              'supplemental_index',
              'Supplemental Index',
              False): [PDS_DATA_DIR + '/metadata/EBROCC_xxxx/EBROCC_0001/EBROCC_0001_supplemental_index.tab',
                       PDS_DATA_DIR + '/metadata/EBROCC_xxxx/EBROCC_0001/EBROCC_0001_supplemental_index.lbl']}
            )
        ]
    )
    def test_opus_products_ebrocc_xxxx(self, input_path, expected):
        opus_products_test(input_path, expected)

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R.IMG',
            {('Galileo SSI',
              10,
              'gossi_raw',
              'Raw Image',
              True): [PDS_DATA_DIR + '/volumes/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R.IMG',
                      PDS_DATA_DIR + '/volumes/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R.LBL',
                      PDS_DATA_DIR + '/volumes/GO_0xxx/GO_0017/LABEL/RLINEPRX.FMT',
                      PDS_DATA_DIR + '/volumes/GO_0xxx/GO_0017/LABEL/RTLMTAB.FMT'],
             ('browse',
              40,
              'browse_full',
              'Browse Image (full)',
              True): [PDS_DATA_DIR + '/previews/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R_full.jpg'],
             ('browse',
              30,
              'browse_medium',
              'Browse Image (medium)',
              False): [PDS_DATA_DIR + '/previews/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R_med.jpg'],
             ('browse',
              20,
              'browse_small',
              'Browse Image (small)',
              False): [PDS_DATA_DIR + '/previews/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R_small.jpg'],
             ('browse',
              10,
              'browse_thumb',
              'Browse Image (thumbnail)',
              False): [PDS_DATA_DIR + '/previews/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R_thumb.jpg'],
             ('metadata',
              5,
              'rms_index',
              'RMS Node Augmented Index',
              False): [PDS_DATA_DIR + '/metadata/GO_0xxx/GO_0017/GO_0017_index.tab',
                       PDS_DATA_DIR + '/metadata/GO_0xxx/GO_0017/GO_0017_index.lbl']}
            )
        ]
    )
    def test_opus_products_go_0xxx(self, input_path, expected):
        opus_products_test(input_path, expected)

    @pytest.mark.parametrize(
    # 1001 is the raw volume and 2001 is the calibrated volume.
        'input_path,expected',
        [
            ('volumes/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng.fit',
             {('New Horizons LORRI',
               0,
               'nh_lorri_raw',
               'Raw Image',
               True): [PDS_DATA_DIR + '/volumes/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng.fit',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng.lbl',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx_v3/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng_1.fit',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx_v3/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng_1.lbl',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx_v2/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng_1.fit',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx_v2/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng_1.lbl',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx_v1/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng_1.fit',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx_v1/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng_1.lbl'],
              ('New Horizons LORRI',
               100,
               'nh_lorri_calib',
               'Calibrated Image',
               True): [PDS_DATA_DIR + '/volumes/NHxxLO_xxxx/NHLALO_2001/data/20060224_000310/lor_0003103486_0x630_sci.fit',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx/NHLALO_2001/data/20060224_000310/lor_0003103486_0x630_sci.lbl',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx_v3/NHLALO_2001/data/20060224_000310/lor_0003103486_0x630_sci_1.fit',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx_v3/NHLALO_2001/data/20060224_000310/lor_0003103486_0x630_sci_1.lbl',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx_v2/NHLALO_2001/data/20060224_000310/lor_0003103486_0x630_sci_1.fit',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx_v2/NHLALO_2001/data/20060224_000310/lor_0003103486_0x630_sci_1.lbl',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx_v1/NHLALO_2001/data/20060224_000310/lor_0003103486_0x630_sci_1.fit',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx_v1/NHLALO_2001/data/20060224_000310/lor_0003103486_0x630_sci_1.lbl'],
              ('browse',
               10,
               'browse_thumb',
               'Browse Image (thumbnail)',
               False): [PDS_DATA_DIR + '/previews/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x631_eng_thumb.jpg',
                        PDS_DATA_DIR + '/previews/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng_thumb.jpg'],
              ('browse',
               20,
               'browse_small',
               'Browse Image (small)',
               False): [PDS_DATA_DIR + '/previews/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x631_eng_small.jpg',
                        PDS_DATA_DIR + '/previews/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng_small.jpg'],
              ('browse',
               30,
               'browse_medium',
               'Browse Image (medium)',
               False): [PDS_DATA_DIR + '/previews/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x631_eng_med.jpg',
                        PDS_DATA_DIR + '/previews/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng_med.jpg'],
              ('browse',
               40,
               'browse_full',
               'Browse Image (full)',
               True): [PDS_DATA_DIR + '/previews/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x631_eng_full.jpg',
                       PDS_DATA_DIR + '/previews/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng_full.jpg'],
               ('New Horizons LORRI',
                200,
                'nh_lorri_calib_browse',
                'Extra Preview (calibrated)',
                False): [PDS_DATA_DIR + '/previews/NHxxLO_xxxx/NHLALO_2001/data/20060224_000310/lor_0003103486_0x631_sci_thumb.jpg',
                         PDS_DATA_DIR + '/previews/NHxxLO_xxxx/NHLALO_2001/data/20060224_000310/lor_0003103486_0x631_sci_small.jpg',
                         PDS_DATA_DIR + '/previews/NHxxLO_xxxx/NHLALO_2001/data/20060224_000310/lor_0003103486_0x631_sci_med.jpg',
                         PDS_DATA_DIR + '/previews/NHxxLO_xxxx/NHLALO_2001/data/20060224_000310/lor_0003103486_0x631_sci_full.jpg',
                         PDS_DATA_DIR + '/previews/NHxxLO_xxxx/NHLALO_2001/data/20060224_000310/lor_0003103486_0x630_sci_thumb.jpg',
                         PDS_DATA_DIR + '/previews/NHxxLO_xxxx/NHLALO_2001/data/20060224_000310/lor_0003103486_0x630_sci_small.jpg',
                         PDS_DATA_DIR + '/previews/NHxxLO_xxxx/NHLALO_2001/data/20060224_000310/lor_0003103486_0x630_sci_med.jpg',
                         PDS_DATA_DIR + '/previews/NHxxLO_xxxx/NHLALO_2001/data/20060224_000310/lor_0003103486_0x630_sci_full.jpg'],
              ('metadata',
               20,
               'planet_geometry',
               'Planet Geometry Index',
               False): [PDS_DATA_DIR + '/metadata/NHxxLO_xxxx/NHLALO_1001/NHLALO_1001_jupiter_summary.tab',
                        PDS_DATA_DIR + '/metadata/NHxxLO_xxxx/NHLALO_1001/NHLALO_1001_jupiter_summary.lbl'],
              ('metadata',
               30,
               'moon_geometry',
               'Moon Geometry Index',
               False): [PDS_DATA_DIR + '/metadata/NHxxLO_xxxx/NHLALO_1001/NHLALO_1001_moon_summary.tab',
                        PDS_DATA_DIR + '/metadata/NHxxLO_xxxx/NHLALO_1001/NHLALO_1001_moon_summary.lbl'],
              ('metadata',
               40,
               'ring_geometry',
               'Ring Geometry Index',
               False): [PDS_DATA_DIR + '/metadata/NHxxLO_xxxx/NHLALO_1001/NHLALO_1001_ring_summary.tab',
                        PDS_DATA_DIR + '/metadata/NHxxLO_xxxx/NHLALO_1001/NHLALO_1001_ring_summary.lbl'],
              ('metadata',
               10,
               'inventory',
               'Target Body Inventory',
               False): [PDS_DATA_DIR + '/metadata/NHxxLO_xxxx/NHLALO_1001/NHLALO_1001_inventory.csv',
                        PDS_DATA_DIR + '/metadata/NHxxLO_xxxx/NHLALO_1001/NHLALO_1001_inventory.lbl'],
              ('metadata',
               5,
               'rms_index',
               'RMS Node Augmented Index',
               False): [PDS_DATA_DIR + '/metadata/NHxxLO_xxxx/NHLALO_1001/NHLALO_1001_index.tab',
                        PDS_DATA_DIR + '/metadata/NHxxLO_xxxx/NHLALO_1001/NHLALO_1001_index.lbl'],
              ('metadata',
               9,
               'supplemental_index',
               'Supplemental Index',
               False): [PDS_DATA_DIR + '/metadata/NHxxLO_xxxx/NHLALO_1001/NHLALO_1001_supplemental_index.tab',
                        PDS_DATA_DIR + '/metadata/NHxxLO_xxxx/NHLALO_1001/NHLALO_1001_supplemental_index.lbl'],
              ('New Horizons LORRI',
               50,
               'nh_lorri_raw_alternate',
               'Raw Image Alternate Downlink',
               True): [PDS_DATA_DIR + '/volumes/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x631_eng.fit',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x631_eng.lbl',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx_v3/NHLALO_1001/data/20060224_000310/lor_0003103486_0x631_eng_1.fit',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx_v3/NHLALO_1001/data/20060224_000310/lor_0003103486_0x631_eng_1.lbl',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx_v2/NHLALO_1001/data/20060224_000310/lor_0003103486_0x631_eng_1.fit',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx_v2/NHLALO_1001/data/20060224_000310/lor_0003103486_0x631_eng_1.lbl',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx_v1/NHLALO_1001/data/20060224_000310/lor_0003103486_0x631_eng_1.fit',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx_v1/NHLALO_1001/data/20060224_000310/lor_0003103486_0x631_eng_1.lbl'],
              ('New Horizons LORRI',
               150,
               'nh_lorri_calib_alternate',
               'Calibrated Image Alternate Downlink',
               True): [PDS_DATA_DIR + '/volumes/NHxxLO_xxxx/NHLALO_2001/data/20060224_000310/lor_0003103486_0x631_sci.fit',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx/NHLALO_2001/data/20060224_000310/lor_0003103486_0x631_sci.lbl',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx_v3/NHLALO_2001/data/20060224_000310/lor_0003103486_0x631_sci_1.fit',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx_v3/NHLALO_2001/data/20060224_000310/lor_0003103486_0x631_sci_1.lbl',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx_v2/NHLALO_2001/data/20060224_000310/lor_0003103486_0x631_sci_1.fit',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx_v2/NHLALO_2001/data/20060224_000310/lor_0003103486_0x631_sci_1.lbl',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx_v1/NHLALO_2001/data/20060224_000310/lor_0003103486_0x631_sci_1.fit',
                       PDS_DATA_DIR + '/volumes/NHxxLO_xxxx_v1/NHLALO_2001/data/20060224_000310/lor_0003103486_0x631_sci_1.lbl']}
            )
        ]
    )
    def test_opus_products_NHxxxx_xxxx(self, input_path, expected):
        opus_products_test(input_path, expected)

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_RAW.IMG',
            {('Voyager ISS',
              20,
              'vgiss_calib',
              'Calibrated Image',
              True): [PDS_DATA_DIR + '/volumes/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_CALIB.IMG',
                      PDS_DATA_DIR + '/volumes/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_CALIB.LBL'],
             ('Voyager ISS',
              10,
              'vgiss_cleaned',
              'Cleaned Image',
              True): [PDS_DATA_DIR + '/volumes/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_CLEANED.IMG',
                      PDS_DATA_DIR + '/volumes/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_CLEANED.LBL'],
             ('Voyager ISS',
              30,
              'vgiss_geomed',
              'Geometrically Corrected Image',
              True): [PDS_DATA_DIR + '/volumes/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_GEOMED.IMG',
                      PDS_DATA_DIR + '/volumes/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_GEOMED.LBL'],
             ('Voyager ISS',
              0,
              'vgiss_raw',
              'Raw Image',
              True): [PDS_DATA_DIR + '/volumes/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_RAW.IMG',
                      PDS_DATA_DIR + '/volumes/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_RAW.LBL'],
             ('Voyager ISS',
              50,
              'vgiss_geoma',
              'Geometric Tiepoint Table',
              True): [PDS_DATA_DIR + '/volumes/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_GEOMA.TAB',
                      PDS_DATA_DIR + '/volumes/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_GEOMA.LBL',
                      PDS_DATA_DIR + '/volumes/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_GEOMA.DAT',
                      PDS_DATA_DIR + '/volumes/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_GEOMA.LBL'],
             ('Voyager ISS',
              40,
              'vgiss_resloc',
              'Reseau Table',
              True): [PDS_DATA_DIR + '/volumes/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_RESLOC.TAB',
                      PDS_DATA_DIR + '/volumes/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_RESLOC.LBL',
                      PDS_DATA_DIR + '/volumes/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_RESLOC.DAT',
                      PDS_DATA_DIR + '/volumes/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_RESLBOC.LBL'],
             ('Voyager ISS',
              80,
              'vgiss_calib_browse',
              'Extra Preview (calibrated)',
              False): [PDS_DATA_DIR + '/volumes/VGISS_5xxx/VGISS_5101/BROWSE/C13854XX/C1385455_CALIB.JPG',
                       PDS_DATA_DIR + '/volumes/VGISS_5xxx/VGISS_5101/BROWSE/C13854XX/C1385455_CALIB.LBL'],
             ('Voyager ISS',
              70,
              'vgiss_cleaned_browse',
              'Extra Preview (cleaned)',
              False): [PDS_DATA_DIR + '/volumes/VGISS_5xxx/VGISS_5101/BROWSE/C13854XX/C1385455_CLEANED.JPG',
                       PDS_DATA_DIR + '/volumes/VGISS_5xxx/VGISS_5101/BROWSE/C13854XX/C1385455_CLEANED.LBL'],
             ('Voyager ISS',
              90,
              'vgiss_geomed_browse',
              'Extra Preview (geometrically corrected)',
              False): [PDS_DATA_DIR + '/volumes/VGISS_5xxx/VGISS_5101/BROWSE/C13854XX/C1385455_GEOMED.JPG',
                       PDS_DATA_DIR + '/volumes/VGISS_5xxx/VGISS_5101/BROWSE/C13854XX/C1385455_GEOMED.LBL'],
             ('Voyager ISS',
              60,
              'vgiss_raw_browse',
              'Extra Preview (raw)',
              False): [PDS_DATA_DIR + '/volumes/VGISS_5xxx/VGISS_5101/BROWSE/C13854XX/C1385455_RAW.JPG',
                       PDS_DATA_DIR + '/volumes/VGISS_5xxx/VGISS_5101/BROWSE/C13854XX/C1385455_RAW.LBL'],
             ('browse',
              40,
              'browse_full',
              'Browse Image (full)',
              True): [PDS_DATA_DIR + '/previews/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_full.jpg'],
             ('browse',
              30,
              'browse_medium',
              'Browse Image (medium)',
              False): [PDS_DATA_DIR + '/previews/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_med.jpg'],
             ('browse',
              20,
              'browse_small',
              'Browse Image (small)',
              False): [PDS_DATA_DIR + '/previews/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_small.jpg'],
             ('browse',
              10,
              'browse_thumb',
              'Browse Image (thumbnail)',
              False): [PDS_DATA_DIR + '/previews/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_thumb.jpg'],
             ('metadata',
              5,
              'rms_index',
              'RMS Node Augmented Index',
              False): [PDS_DATA_DIR + '/metadata/VGISS_5xxx/VGISS_5101/VGISS_5101_index.tab',
                       PDS_DATA_DIR + '/metadata/VGISS_5xxx/VGISS_5101/VGISS_5101_index.lbl'],
             ('metadata',
              7,
              'raw_image_index',
              'Raw Image Index',
              False): [PDS_DATA_DIR + '/metadata/VGISS_5xxx/VGISS_5101/VGISS_5101_raw_image_index.tab',
                       PDS_DATA_DIR + '/metadata/VGISS_5xxx/VGISS_5101/VGISS_5101_raw_image_index.lbl'],
             ('metadata',
              9,
              'supplemental_index',
              'Supplemental Index',
              False): [PDS_DATA_DIR + '/metadata/VGISS_5xxx/VGISS_5101/VGISS_5101_supplemental_index.tab',
                       PDS_DATA_DIR + '/metadata/VGISS_5xxx/VGISS_5101/VGISS_5101_supplemental_index.lbl']}
            )
        ]
    )
    def test_opus_products_vgiss_5xxx(self, input_path, expected):
        opus_products_test(input_path, expected)


    ############################################################################
    # Test for associated volumes and volsets
    ############################################################################
    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COVIMS_0xxx/COVIMS_0001/data/1999010T054026_1999010T060958/v1294638283_1.lbl',
             'volumes/COVIMS_0xxx/COVIMS_0001'),
        ]
    )
    def test_volume_pdsfile(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.volume_pdsfile()
        assert isinstance(res, pdsfile.PdsFile)
        assert res.logical_path == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/HSTNx_xxxx/HSTN0_7176/DATA/VISIT_01/N4BI01L4Q.lbl',
             'volumes/HSTNx_xxxx/HSTN0_7176'),
            ('volumes/HSTNx_xxxx/HSTN0_7176', 'volumes/HSTNx_xxxx/HSTN0_7176')
        ]
    )
    def test_volume_pdsdir(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.volume_pdsdir()
        assert isinstance(res, pdsfile.PdsFile)
        assert res.logical_path == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/NHSP_xxxx/NHSP_1000/DATA/CK/MERGED_NHPC_2006_V011.LBL',
             'volumes/NHSP_xxxx'),
        ]
    )
    def test_volset_pdsfile(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.volset_pdsfile()
        assert isinstance(res, pdsfile.PdsFile)
        assert res.logical_path == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/NHSP_xxxx/NHSP_1000/DATA/CK/MERGED_NHPC_2006_V011.LBL',
             False),
            ('volumes', True)
        ]
    )
    def test_is_category_dir(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.is_category_dir()
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('metadata/VGISS_8xxx/VGISS_8201/VGISS_8201_inventory.tab',
             PDS_DATA_DIR + '/metadata/VGISS_8xxx/VGISS_8201'),
            ('metadata/VGISS_6xxx/VGISS_6101',
             PDS_DATA_DIR + '/metadata/VGISS_6xxx/VGISS_6101'),
            ('volumes/VGISS_7xxx/VGISS_7201/DATA/C24476XX/C2447654_RAW.lbl',
             PDS_DATA_DIR + '/volumes/VGISS_7xxx/VGISS_7201')
        ]
    )
    def test_volume_abspath(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.volume_abspath() == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/HSTOx_xxxx/HSTO0_7308/DATA/VISIT_05/O43B05C1Q.ASC',
             PDS_DATA_DIR + '/volumes/HSTOx_xxxx'),
            ('previews/HSTNx_xxxx/HSTN0_7176/DATA/VISIT_01/N4BI01L4Q_thumb.jpg',
             PDS_DATA_DIR + '/previews/HSTNx_xxxx')
        ]
    )
    def test_volset_abspath(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.volset_abspath() == expected

    ############################################################################
    # Test for support for PdsFile objects representing index rows
    ############################################################################
    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab',
             {'U2NO0401T': [0], 'U2NO0402T': [1], 'U2NO0403T': [2], 'U2NO0404T': [3]}),
        ]
    )
    def test_get_indexshelf(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.get_indexshelf()
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,selection,flag,expected',
        [
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab',
             'U2NO0403T', '', 'U2NO0403T'),
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab',
             'U2NO0404Tx', '<', 'U2NO0404T'),
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab',
             'U2NO0404T', '<', 'U2NO0404T'),
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab',
             'U2NO0402Tx', '>', 'U2NO0402T'),
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab',
             'U2NO0402T', '>', 'U2NO0402T'),
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab',
             'U2NO0401T', '=', 'U2NO0401T'),
            ('metadata/HSTOx_xxxx/HSTO0_7308/HSTO0_7308x_index.tab',
             'O43B06BTQ', '', 'O43B06BTQ'),
        ]
    )
    def test_find_selected_row_key(self, input_path, selection, flag, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        print(target_pdsfile.childnames)
        res = target_pdsfile.find_selected_row_key(selection, flag)
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,selection,flag,expected',
        [
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab',
             'U2NO0404T', '=',
             'metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab/U2NO0404T'),
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab',
             'U2NO0403Tx', '>',
             'metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab/U2NO0403T'),
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab',
             'U2NO0403T', '>',
             'metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab/U2NO0403T'),
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab',
             'U2NO0401Tx', '<',
             'metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab/U2NO0401T'),
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab',
             'U2NO0401T', '<',
             'metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab/U2NO0401T'),
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab',
             'U2NO0402T', '',
             'metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab/U2NO0402T'),
        ]
    )
    def test_child_of_index(self, input_path, selection, flag, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.child_of_index(selection, flag)
        assert isinstance(res, pdsfile.PdsFile)
        # The path doesn't point to an actual file.
        assert res.logical_path == expected

    @pytest.mark.parametrize(
        'input_path,selection,flag,expected',
        [
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab',
             'U2NO0404T', '',
             PDS_DATA_DIR + '/volumes/HSTUx_xxxx/HSTU0_5167/DATA/VISIT_04/U2NO0404T.LBL'),
        ]
    )
    def test_data_abspath_associated_with_index_row(self, input_path,
                                                    selection, flag,
                                                    expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        index_row = target_pdsfile.child_of_index(selection, flag)
        res = index_row.data_abspath_associated_with_index_row()
        if pdsfile.SHELVES_ONLY:
            assert res == ''
        else:
            assert res == expected

    ############################################################################
    # Test for checksum path associations
    ############################################################################
    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274/EUV2004_274_01_39.lbl',
             PDS_DATA_DIR + '/checksums-volumes/COUVIS_0xxx_v1/COUVIS_0009_md5.txt'),
            ('metadata/VGISS_5xxx/VGISS_5101/VGISS_5101_supplemental_index.tab',
             PDS_DATA_DIR + '/checksums-metadata/VGISS_5xxx/VGISS_5101_metadata_md5.txt')
        ]
    )
    def test_checksum_path_and_lskip(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        if target_pdsfile.archives_:
            lskip = (len(target_pdsfile.root_) + len('checksums_')
                     + len(target_pdsfile.category_))
        else:
            lskip = (len(target_pdsfile.root_) + len('checksums_')
                     + len(target_pdsfile.category_)
                     + len(target_pdsfile.volset_))
        expected = (expected, lskip)
        assert target_pdsfile.checksum_path_and_lskip() == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('archives-volumes/COCIRS_0xxx/COCIRS_0010.tar.gz',
             PDS_DATA_DIR + '/checksums-archives-volumes/COCIRS_0xxx_md5.txt'),
            ('volumes/COCIRS_0xxx/COCIRS_0010',
             PDS_DATA_DIR + '/checksums-volumes/COCIRS_0xxx/COCIRS_0010_md5.txt'),
            ('checksums-volumes/COCIRS_0xxx/COCIRS_0010_md5.txt', '')
        ]
    )
    def test_checksum_path_if_exact(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.checksum_path_if_exact()
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            # ('archives-volumes/COCIRS_0xxx/COCIRS_0010.tar.gz',
            #  (
            #     PDS_DATA_DIR + '/archives-volumes/COCIRS_0xxx',
            #     PDS_DATA_DIR + '/archives-volumes/COCIRS_0xxx/')),
            ('checksums-volumes/COCIRS_0xxx/COCIRS_0010_md5.txt',
             (
                PDS_DATA_DIR + '/volumes/COCIRS_0xxx/COCIRS_0010',
                PDS_DATA_DIR + '/volumes/COCIRS_0xxx/')),
        ]
    )
    def test_dirpath_and_prefix_for_checksum(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.dirpath_and_prefix_for_checksum()
        assert res == expected

    ############################################################################
    # Test for archive path associations
    ############################################################################
    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab',
             PDS_DATA_DIR + '/archives-metadata/HSTUx_xxxx/HSTU0_5167_metadata.tar.gz'),
            ('volumes/EBROCC_xxxx/EBROCC_0001/DATA/ESO1M/ES1_EPD.LBL',
             PDS_DATA_DIR + '/archives-volumes/EBROCC_xxxx/EBROCC_0001.tar.gz')
        ]
    )
    def test_archive_path_and_lskip(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        lskip = (len(target_pdsfile.root_) + len(target_pdsfile.category_)
                 + len(target_pdsfile.volset_))
        expected = (expected, lskip)
        assert target_pdsfile.archive_path_and_lskip() == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('archives-volumes/COCIRS_0xxx/COCIRS_0010.tar.gz', ''),
            ('volumes/COCIRS_0xxx/COCIRS_0010',
             PDS_DATA_DIR + '/archives-volumes/COCIRS_0xxx/COCIRS_0010.tar.gz'),
        ]
    )
    def test_archive_path_if_exact(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.archive_path_if_exact()
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('archives-volumes/COCIRS_0xxx/COCIRS_0010.tar.gz',
             (PDS_DATA_DIR + '/volumes/COCIRS_0xxx/COCIRS_0010',
              PDS_DATA_DIR + '/volumes/COCIRS_0xxx/')),
        ]
    )
    def test_dirpath_and_prefix_for_archive(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.dirpath_and_prefix_for_archive()
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,task,expected',
        [
            ('archives-volumes/COCIRS_0xxx/COCIRS_0012.tar.gz', '',
             PDS_PDSDATA_PATH + 'logs/archives/volumes/COCIRS_0xxx/COCIRS_0012_targz_.*.log')
        ]
    )
    def test_archive_logpath(self, input_path, task, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.archive_logpath(task=task)
        # escape possible "(" & ")" if that exists in PDS_PDSDATA_PATH
        expected = expected.replace('(', '\\(')
        expected = expected.replace(')', '\\)')
        assert re.match(expected, res)

    ############################################################################
    # Test for shelf support
    ############################################################################
    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_RAW.lbl',
             PDS_PDSDATA_PATH + 'shelves/info/volumes/VGISS_5xxx/VGISS_5101_info.pickle'),
            ('metadata/NHxxLO_xxxx/NHLALO_1001/NHLALO_1001_inventory.tab',
             PDS_PDSDATA_PATH + 'shelves/info/metadata/NHxxLO_xxxx/NHLALO_1001_info.pickle'),
            ('archives-volumes/EBROCC_xxxx/EBROCC_0001.tar.gz',
             PDS_PDSDATA_PATH + 'shelves/info/archives-volumes/EBROCC_xxxx_info.pickle')
        ]
    )
    def test_shelf_path_and_lskip(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        if target_pdsfile.archives_:
            lskip = (len(target_pdsfile.root_) + len(target_pdsfile.category_)
                     + len(target_pdsfile.volset_))
        else:
            lskip = (len(target_pdsfile.root_) + len(target_pdsfile.category_)
                     + len(target_pdsfile.volset_) + len(target_pdsfile.volname)
                     + 1)
        expected = (expected, lskip)
        assert target_pdsfile.shelf_path_and_lskip() == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            (PDS_PDSDATA_PATH + 'shelves/info/volumes/VGISS_5xxx/VGISS_5101_info.pickle',
             None),
        ]
    )
    def test__get_shelf(self, input_path, expected):
        assert pdsfile.PdsFile._get_shelf(input_path) != expected

    ############################################################################
    # Test for log path associations
    ############################################################################
    @pytest.mark.parametrize(
        'root,expected',
        [
            (None, None),
            (PDS_PDSDATA_PATH + 'logs/', PDS_PDSDATA_PATH + 'logs/')
        ]
    )
    def test_set_log_root(self, root, expected):
        pdsfile.PdsFile.set_log_root(root=root)
        assert pdsfile.PdsFile.LOG_ROOT_ == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/HSTIx_xxxx/HSTI1_1556',
             PDS_PDSDATA_PATH + 'logs/volumes/HSTIx_xxxx/HSTI1_1556_.*.log'),
        ]
    )
    def test_log_path_for_volume(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.log_path_for_volume(id='', task='', dir='')
        # escape possible "(" & ")" if that exists in PDS_PDSDATA_PATH
        expected = expected.replace('(', '\\(')
        expected = expected.replace(')', '\\)')
        assert re.match(expected, res)

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/HSTIx_xxxx/HSTI1_1556',
             PDS_PDSDATA_PATH + 'logs/volumes/HSTIx_xxxx_.*.log'),
        ]
    )
    def test_log_path_for_volset(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.log_path_for_volset()
        # escape possible "(" & ")" if that exists in PDS_PDSDATA_PATH
        expected = expected.replace('(', '\\(')
        expected = expected.replace(')', '\\)')
        assert re.match(expected, res)

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/HSTIx_xxxx/HSTI1_1556',
             PDS_PDSDATA_PATH + 'logs/volumes/HSTIx_xxxx_.*.log'),
        ]
    )
    def test_log_path_for_volset2(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.log_path_for_volset(place='parallel')
        # escape possible "(" & ")" if that exists in PDS_PDSDATA_PATH
        expected = expected.replace('(', '\\(')
        expected = expected.replace(')', '\\)')
        assert re.match(expected, res)

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/HSTIx_xxxx/HSTI1_1556',
             PDS_PDSDATA_PATH + 'logs/index/_.*.log'),
        ]
    )
    def test_log_path_for_index(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.log_path_for_index()
        # escape possible "(" & ")" if that exists in PDS_PDSDATA_PATH
        expected = expected.replace('(', '\\(')
        expected = expected.replace(')', '\\)')
        assert re.match(expected, res)

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/HSTIx_xxxx/HSTI1_1556',
             PDS_PDSDATA_PATH + 'logs/index/_.*.log'),
        ]
    )
    def test_log_path_for_index2(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.log_path_for_index(place='parallel')
        # escape possible "(" & ")" if that exists in PDS_PDSDATA_PATH
        expected = expected.replace('(', '\\(')
        expected = expected.replace(')', '\\)')
        assert re.match(expected, res)

    ############################################################################
    # Test for split and sort filenames
    ############################################################################
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
            ('previews/COUVIS_0xxx/COUVIS_0009/DATA/D2004_274',
             [
                # Sorted order
                'EUV2004_274_01_39_thumb.png',
                'EUV2004_274_02_25_med.png',
                'EUV2004_274_07_10_full.png',
                'EUV2004_274_09_50_small.png',
             ]),
        ]
    )
    def test_sort_childnames(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.sort_childnames()
        li = []
        for child in res:
            if child in expected:
                li.append(child)
        assert li == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('previews/COUVIS_0xxx/COUVIS_0009/DATA/D2004_274',
             [
                # Sorted order
                'EUV2004_274_01_39_thumb.png',
                'EUV2004_274_02_25_med.png',
                'EUV2004_274_07_10_full.png',
                'EUV2004_274_09_50_small.png',
             ]),
        ]
    )
    def test_viewable_childnames(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.viewable_childnames()
        li = []
        for child in res:
            if child in expected:
                li.append(child)
        assert li == expected

    ############################################################################
    # Test for transformations
    ############################################################################
    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ([
                'volumes/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1.LBL',
                'volumes/HSTNx_xxxx/HSTN0_7176/DATA/VISIT_01/N4BI01L4Q.LBL'
             ],
             [
                 PDS_DATA_DIR + '/volumes/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1.LBL',
                 PDS_DATA_DIR + '/volumes/HSTNx_xxxx/HSTN0_7176/DATA/VISIT_01/N4BI01L4Q.LBL'
             ])
        ]
    )
    def test_abspaths_for_pdsfiles(self, input_path, expected):
        pdsfiles = []
        for path in input_path:
            pdsfiles.append(instantiate_target_pdsfile(path))

        res = pdsfile.PdsFile.abspaths_for_pdsfiles(
            pdsfiles=pdsfiles, must_exist=True)

        for path in res:
            assert path in expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ([
                'volumes/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1.LBL',
                'volumes/HSTNx_xxxx/HSTN0_7176/DATA/VISIT_01/N4BI01L4Q.LBL'
             ],
             [
                'volumes/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1.LBL',
                'volumes/HSTNx_xxxx/HSTN0_7176/DATA/VISIT_01/N4BI01L4Q.LBL'
             ])
        ]
    )
    def test_logicals_for_pdsfiles(self, input_path, expected):
        pdsfiles = []
        for path in input_path:
            pdsfiles.append(instantiate_target_pdsfile(path, is_abspath=False))

        res = pdsfile.PdsFile.logicals_for_pdsfiles(pdsfiles=pdsfiles)

        for path in res:
            assert path in expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ([
                'volumes/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1.LBL',
                'volumes/HSTNx_xxxx/HSTN0_7176/DATA/VISIT_01/N4BI01L4Q.LBL'
             ],
             ['W1294561202_1.LBL', 'N4BI01L4Q.LBL'])
        ]
    )
    def test_basenames_for_pdsfiles(self, input_path, expected):
        pdsfiles = []
        for path in input_path:
            pdsfiles.append(instantiate_target_pdsfile(path, is_abspath=False))

        res = pdsfile.PdsFile.basenames_for_pdsfiles(pdsfiles=pdsfiles)

        for basename in res:
            assert basename in expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ([
                PDS_DATA_DIR + '/volumes/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1.LBL',
                PDS_DATA_DIR + '/volumes/HSTNx_xxxx/HSTN0_7176/DATA/VISIT_01/N4BI01L4Q.LBL'
             ],
             [
                'volumes/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1.LBL',
                'volumes/HSTNx_xxxx/HSTN0_7176/DATA/VISIT_01/N4BI01L4Q.LBL',
             ])
        ]
    )
    def test_logicals_for_abspaths(self, input_path, expected):
        res = pdsfile.PdsFile.logicals_for_abspaths(abspaths=input_path,
                                                    must_exist=True)

        for path in res:
            assert path in expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ([
                PDS_DATA_DIR + '/volumes/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1.LBL',
                PDS_DATA_DIR + '/volumes/HSTNx_xxxx/HSTN0_7176/DATA/VISIT_01/N4BI01L4Q.LBL'
             ],
             ['W1294561202_1.LBL', 'N4BI01L4Q.LBL'])
        ]
    )
    def test_basenames_for_abspaths(self, input_path, expected):
        res = pdsfile.PdsFile.basenames_for_abspaths(abspaths=input_path)

        for basename in res:
            assert basename in expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ([
                'volumes/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1.LBL',
                'volumes/HSTNx_xxxx/HSTN0_7176/DATA/VISIT_01/N4BI01L4Q.LBL'
             ],
             [
                'volumes/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1.LBL',
                'volumes/HSTNx_xxxx/HSTN0_7176/DATA/VISIT_01/N4BI01L4Q.LBL'
             ])
        ]
    )
    def test_pdsfiles_for_logicals(self, input_path, expected):
        res = pdsfile.PdsFile.pdsfiles_for_logicals(logical_paths=input_path)

        for pdsf in res:
            assert isinstance(pdsf, pdsfile.PdsFile)
            assert pdsf.logical_path in expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ([
                'volumes/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1.LBL',
                'volumes/HSTNx_xxxx/HSTN0_7176/DATA/VISIT_01/N4BI01L4Q.LBL'
             ],
             [
                PDS_DATA_DIR + '/volumes/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1.LBL',
                PDS_DATA_DIR + '/volumes/HSTNx_xxxx/HSTN0_7176/DATA/VISIT_01/N4BI01L4Q.LBL',
             ])
        ]
    )
    def test_abspaths_for_logicals(self, input_path, expected):
        res = pdsfile.PdsFile.abspaths_for_logicals(logical_paths=input_path,
                                                    must_exist=True)

        for path in res:
            assert path in expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ([
                'volumes/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1.LBL',
                'volumes/HSTNx_xxxx/HSTN0_7176/DATA/VISIT_01/N4BI01L4Q.LBL'
             ],
             ['W1294561202_1.LBL', 'N4BI01L4Q.LBL'])
        ]
    )
    def test_basenames_for_logicals(self, input_path, expected):
        res = pdsfile.PdsFile.basenames_for_logicals(logical_paths=input_path)

        for basename in res:
            assert basename in expected

    @pytest.mark.parametrize(
        'input_path,basenames,expected',
        [
            ('volumes/COISS_0xxx/COISS_0001/data/wacfm/bit_wght/13302',
             ['133020.lbl'],
             [PDS_DATA_DIR + '/volumes/COISS_0xxx/COISS_0001/data/wacfm/bit_wght/13302/133020.lbl'])
        ]
    )
    def test_abspaths_for_basenames(self, input_path, basenames, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.abspaths_for_basenames(basenames=basenames)

        for path in res:
            assert path in expected

    @pytest.mark.parametrize(
        'input_path,basenames,expected',
        [
            ('volumes/COCIRS_6xxx/COCIRS_6004/DATA/GEODATA/',
             ['GEO1004021018_699.LBL'],
             ['volumes/COCIRS_6xxx/COCIRS_6004/DATA/GEODATA/GEO1004021018_699.LBL'])
        ]
    )
    def test_logicals_for_basenames(self, input_path, basenames, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path, is_abspath=False)
        res = target_pdsfile.logicals_for_basenames(basenames=basenames)

        for path in res:
            assert path in expected

    ############################################################################
    # Test for associations
    ############################################################################
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
            ('volumes/COUVIS_0xxx/COUVIS_0058/DATA/D2017_001/EUV2017_001_03_49.LBL',
             [
                PDS_DATA_DIR + '/volumes/COUVIS_0xxx/COUVIS_0058/CALIB/VERSION_5/D2017_001/EUV2017_001_03_49_CAL_5.DAT',
                PDS_DATA_DIR + '/volumes/COUVIS_0xxx/COUVIS_0058/DATA/D2017_001/EUV2017_001_03_49.LBL',
                PDS_DATA_DIR + '/volumes/COUVIS_0xxx/COUVIS_0058/DATA/D2017_001/EUV2017_001_03_49.DAT',
                PDS_DATA_DIR + '/volumes/COUVIS_0xxx/COUVIS_0058/CALIB/VERSION_5/D2017_001/EUV2017_001_03_49_CAL_5.LBL',
                PDS_DATA_DIR + '/volumes/COUVIS_0xxx/COUVIS_0058/CALIB/VERSION_4/D2017_001/EUV2017_001_03_49_CAL_4.LBL',
                PDS_DATA_DIR + '/volumes/COUVIS_0xxx/COUVIS_0058/CALIB/VERSION_4/D2017_001/EUV2017_001_03_49_CAL_4.DAT'
             ]),
            ('volumes/COUVIS_0xxx/COUVIS_0058/DATA',
             [
                PDS_DATA_DIR + '/volumes/COUVIS_0xxx/COUVIS_0058/DATA',
                PDS_DATA_DIR + '/volumes/COUVIS_0xxx/COUVIS_0058/CALIB/VERSION_5',
                PDS_DATA_DIR + '/volumes/COUVIS_0xxx/COUVIS_0058/CALIB/VERSION_4',
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
             'volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/FUV1999_007_16_57.DAT'),
            ('volumes', 'volumes')
        ]
    )
    def test_associated_parallel(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        print(target_pdsfile.category_.rstrip('/'))
        print(target_pdsfile.volset)
        target_associated_parallel = target_pdsfile.associated_parallel()
        print(target_associated_parallel.logical_path)
        assert target_associated_parallel.logical_path == expected

    @pytest.mark.parametrize(
        'input_path,category,expected',
        [
            ('volumes/HSTUx_xxxx/HSTU0_5167/DATA/VISIT_04/U2NO0404T.LBL',
             'metadata',
             # should we have the "/" at the end?
             [PDS_DATA_DIR + '/metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab/U2NO0404T',
              PDS_DATA_DIR + '/metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_hstfiles.tab/U2NO0404T',
              PDS_DATA_DIR + '/metadata/HSTUx_xxxx/HSTU0_5167/',
              PDS_DATA_DIR + '/metadata/HSTUx_xxxx/HSTU0_5167',
             ]),
            ('volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/FUV1999_007_16_57.DAT',
             'archives-volumes',
             [PDS_DATA_DIR + '/archives-volumes/COUVIS_0xxx/COUVIS_0001.tar.gz']),
            ('volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/FUV1999_007_16_57.DAT',
             'checksums-volumes',
             [PDS_DATA_DIR + '/checksums-volumes/COUVIS_0xxx/COUVIS_0001_md5.txt']),
        ]
    )
    def test__associated_paths(self, input_path, category, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile._associated_paths(
            category=category)
        print(res)
        for path in res:
            assert path in expected

    @pytest.mark.parametrize(
        'input_path,expected_path',
        [
            ('volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.DAT',
             [PDS_DATA_DIR + '/volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.DAT']),

        ]
    )
    def test_copy(self, input_path, expected_path):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        pdsf_copy = target_pdsfile.copy()
        assert pdsf_copy.abspath in expected_path

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
             'previews-COUVIS_0xxx-COUVIS_0001-DATA-D1999_007-HDAC1999_007_16_31'),
            ('previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/',
             'previews-COUVIS_0xxx-COUVIS_0001-DATA-D1999_007')
        ]
    )
    def test_global_anchor(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.global_anchor
        assert res == expected


################################################################################
# Blackbox test for functions & properties in PdsGroup class
################################################################################
class TestPdsGroupBlackBox:
    @pytest.mark.parametrize(
        'input_paths,expected_achor,expected_path',
        [
            ([
                'volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.DAT',
                'volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.LBL'
             ],
             'GEO00120100',
             [
                 'volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.DAT',
                 'volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.LBL'
             ],
            ),

        ]
    )
    def test_copy(self, input_paths, expected_achor, expected_path):
        pdsfiles = get_pdsfiles(input_paths)
        res = pdsgroup.PdsGroup(pdsfiles=pdsfiles)
        res_copy = res.copy()
        assert isinstance(res_copy, pdsgroup.PdsGroup)
        assert res.anchor == expected_achor
        assert res.anchor == res_copy.anchor
        for pdsf in res.iterator_for_all():
            assert pdsf.logical_path in expected_path

    @pytest.mark.parametrize(
        'input_paths,expected',
        [
            ([
                'volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.DAT',
                'volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.LBL'
             ],
             'volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA'),

        ]
    )
    def test_parent_logical_path(self, input_paths, expected):
        pdsfiles = get_pdsfiles(input_paths)
        target_pdsgroup = pdsgroup.PdsGroup(pdsfiles=pdsfiles)
        res = target_pdsgroup.parent_logical_path
        assert res == expected

    @pytest.mark.parametrize(
        'input_paths,expected',
        [
            ([
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
             ],
             False),
            (['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/'], True)
        ]
    )
    def test_isdir(self, input_paths, expected):
        pdsfiles = get_pdsfiles(input_paths)
        target_pdsgroup = pdsgroup.PdsGroup(pdsfiles=pdsfiles)
        res = target_pdsgroup.isdir
        assert res == expected

    @pytest.mark.parametrize(
        'input_paths,expected',
        [
            ([
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
             ],
             [
                'holdings/previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'holdings/previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'holdings/previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                'holdings/previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
             ]
            ),
            (['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/'],
             [
                'holdings/previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'holdings/previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'holdings/previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                'holdings/previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
             ]
            )
        ]
    )
    def test_viewset(self, input_paths, expected):
        pdsfiles = get_pdsfiles(input_paths)
        target_pdsgroup = pdsgroup.PdsGroup(pdsfiles=pdsfiles)
        res = target_pdsgroup.viewset
        assert isinstance(res, pdsviewable.PdsViewSet)
        viewables = res.to_dict()['viewables']
        for viewable in viewables:
            assert viewable['url'] in expected

    @pytest.mark.parametrize(
        'input_paths,expected',
        [
            ([
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
             ],
             'previews-COUVIS_0xxx-COUVIS_0001-DATA-D1999_007-HDAC1999_007_16_31'),
            (['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/'],
             'previews-COUVIS_0xxx-COUVIS_0001-DATA-D1999_007')
        ]
    )
    def test_global_anchor(self, input_paths, expected):
        pdsfiles = get_pdsfiles(input_paths)
        target_pdsgroup = pdsgroup.PdsGroup(pdsfiles=pdsfiles)
        res = target_pdsgroup.global_anchor
        assert res == expected

    @pytest.mark.parametrize(
        'input_paths,expected',
        [
            ([
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
             ],
             [
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
             ])
        ]
    )
    def test_sort(self, input_paths, expected):
        pdsfiles = get_pdsfiles(input_paths)
        target_pdsgroup = pdsgroup.PdsGroup(pdsfiles=pdsfiles)
        target_pdsgroup.sort()
        for idx in range(len(target_pdsgroup.rows)):
            assert target_pdsgroup.rows[idx].logical_path == expected[idx]

    @pytest.mark.parametrize(
        'input_paths,remove_path,expected',
        [
            ([
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
             ],
             'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
             True),
            ([
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
             ],
             'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumbx.png',
             False),
        ]
    )
    def test_remove(self, input_paths, remove_path, expected):
        pdsfiles = get_pdsfiles(input_paths)
        target_pdsgroup = pdsgroup.PdsGroup(pdsfiles=pdsfiles)
        pdsf = instantiate_target_pdsfile(remove_path)
        res = target_pdsgroup.remove(pdsf=pdsf)
        assert res == expected
        if res:
            for file in target_pdsgroup.rows:
                assert file.logical_path != remove_path

    @pytest.mark.parametrize(
        'input_paths,hide_path,expected',
        [
            ([
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
             ],
             'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
             True),
            ([
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
             ],
             'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumbx.png',
             False),
        ]
    )
    def test_hide(self, input_paths, hide_path, expected):
        pdsfiles = get_pdsfiles(input_paths)
        target_pdsgroup = pdsgroup.PdsGroup(pdsfiles=pdsfiles)
        pdsf = instantiate_target_pdsfile(hide_path)
        res = target_pdsgroup.hide(pdsf=pdsf)
        assert res == expected
        if res:
            assert pdsf.logical_path in target_pdsgroup.hidden

    @pytest.mark.parametrize(
        'input_paths,expected',
        [
            ([
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
             ],
             [
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
             ]),
        ]
    )
    def test_hide_all(self, input_paths, expected):
        pdsfiles = get_pdsfiles(input_paths)
        target_pdsgroup = pdsgroup.PdsGroup(pdsfiles=pdsfiles)
        target_pdsgroup.hide_all()
        for path in expected:
            assert path in target_pdsgroup.hidden

    @pytest.mark.parametrize(
        'input_paths,unhide_path,expected',
        [
            ([
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
             ],
             'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
             True),
            ([
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
             ],
             'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumbx.png',
             False),
        ]
    )
    def test_unhide(self, input_paths, unhide_path, expected):
        pdsfiles = get_pdsfiles(input_paths)
        target_pdsgroup = pdsgroup.PdsGroup(pdsfiles=pdsfiles)
        target_pdsgroup.hide_all()
        pdsf = instantiate_target_pdsfile(unhide_path)
        res = target_pdsgroup.unhide(pdsf=pdsf)
        assert res == expected
        if res:
            assert pdsf.logical_path not in target_pdsgroup.hidden

    @pytest.mark.parametrize(
        'input_paths,expected',
        [
            ([
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
             ],
             0),
        ]
    )
    def test_unhide_all(self, input_paths, expected):
        pdsfiles = get_pdsfiles(input_paths)
        target_pdsgroup = pdsgroup.PdsGroup(pdsfiles=pdsfiles)
        target_pdsgroup.hide_all()
        target_pdsgroup.unhide_all()
        assert len(target_pdsgroup.hidden) == expected

    @pytest.mark.parametrize(
        'input_paths,hide_path,expected',
        [
            ([
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
             ],
             'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
             [
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
             ]),
        ]
    )
    def test_iterator(self, input_paths, hide_path, expected):
        pdsfiles = get_pdsfiles(input_paths)
        target_pdsgroup = pdsgroup.PdsGroup(pdsfiles=pdsfiles)
        pdsf = instantiate_target_pdsfile(hide_path)
        target_pdsgroup.hide(pdsf=pdsf)
        for pdsf in target_pdsgroup.iterator():
            assert pdsf.logical_path != hide_path
            assert pdsf.logical_path in expected

    @pytest.mark.parametrize(
        'input_paths,expected',
        [
            ([
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
             ],
             [
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
             ]),
        ]
    )
    def test_iterator_for_all(self, input_paths, expected):
        pdsfiles = get_pdsfiles(input_paths)
        target_pdsgroup = pdsgroup.PdsGroup(pdsfiles=pdsfiles)
        for pdsf in target_pdsgroup.iterator_for_all():
            assert pdsf.logical_path in expected

    @pytest.mark.parametrize(
        'input_paths,hide_path,expected',
        [
            ([
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
             ],
             'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
             [
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png'
             ]),
        ]
    )
    def test_iterator_for_hidden(self, input_paths, hide_path, expected):
        pdsfiles = get_pdsfiles(input_paths)
        target_pdsgroup = pdsgroup.PdsGroup(pdsfiles=pdsfiles)
        pdsf = instantiate_target_pdsfile(hide_path)
        target_pdsgroup.hide(pdsf=pdsf)
        for pdsf in target_pdsgroup.iterator_for_hidden():
            assert pdsf.logical_path in expected

################################################################################
# Blackbox test for functions & properties in PdsGroupTable class
################################################################################
class TestPdsGroupTableBlackBox:
    #  PdsGroup parent does not match PdsGroupTable parent
    @pytest.mark.parametrize(
        'input_groups,expected',
        [
            ([
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007'],
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010']
             ],
             'previews/COUVIS_0xxx/COUVIS_0001/DATA'),
            ([
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                ],
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
                ]
             ],
             'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007'),
        ]
    )
    def test_copy(self, input_groups, expected):
        pdsgroups = get_pdsgroups(input_groups)
        res = pdsgrouptable.PdsGroupTable(pdsgroups=pdsgroups)
        res_copy = res.copy()
        assert isinstance(res_copy, pdsgrouptable.PdsGroupTable)
        assert res.parent_logical_path == expected
        assert res.parent_logical_path == res_copy.parent_logical_path

    @pytest.mark.parametrize(
        'input_groups,expected',
        [
            ([
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007'],
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010']
             ],
             'previews/COUVIS_0xxx/COUVIS_0001/DATA'),
            ([
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                ],
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
                ]
             ],
             'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007'),
        ]
    )
    def test_parent_logical_path(self, input_groups, expected):
        pdsgroups = get_pdsgroups(input_groups)
        res = pdsgrouptable.PdsGroupTable(pdsgroups=pdsgroups)
        assert isinstance(res, pdsgrouptable.PdsGroupTable)
        assert res.parent_logical_path == expected

    @pytest.mark.parametrize(
        'input_groups,expected',
        [
            ([
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007'],
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010']
             ],
             [
                'previews/COUVIS_0xxx/COUVIS_0001/DATA',
                'previews/COUVIS_0xxx/COUVIS_0001',
                'previews/COUVIS_0xxx',
                'previews',
             ]),
            ([
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                ],
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
                ]
             ],
             [
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA',
                'previews/COUVIS_0xxx/COUVIS_0001',
                'previews/COUVIS_0xxx',
                'previews',
             ]),
        ]
    )
    def test_levels(self, input_groups, expected):
        pdsgroups = get_pdsgroups(input_groups)
        target_pdsgrouptable = pdsgrouptable.PdsGroupTable(pdsgroups=pdsgroups)
        res = target_pdsgrouptable.levels
        for idx in range(len(res)):
            assert res[idx].logical_path == expected[idx]

    @pytest.mark.parametrize(
        'input_groups,expected',
        [
            ([
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007'],
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010']
             ],
             [
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA',
                'previews/COUVIS_0xxx/COUVIS_0001',
                'previews/COUVIS_0xxx',
                'previews',
             ]),
            ([
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                ],
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
                ]
             ],
             [
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA',
                'previews/COUVIS_0xxx/COUVIS_0001',
                'previews/COUVIS_0xxx',
                'previews',
             ]),
        ]
    )
    def test_levels_plus_one(self, input_groups, expected):
        pdsgroups = get_pdsgroups(input_groups)
        target_pdsgrouptable = pdsgrouptable.PdsGroupTable(pdsgroups=pdsgroups)
        #  first element at the first row of first group + self.levels
        res = target_pdsgrouptable.levels_plus_one
        for idx in range(len(res)):
            assert res[idx].logical_path == expected[idx]

    @pytest.mark.parametrize(
        'input_groups,expected',
        [
            ([
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007'],
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010']
             ],
             [
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010']
             ]),
            ([
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                ],
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
                ]
             ],
             [
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
                ]
             ]),
        ]
    )
    def test_iterator(self, input_groups, expected):
        pdsgroups = get_pdsgroups(input_groups)
        pdsgroups[0].hide_all()
        target_pdsgrouptable = pdsgrouptable.PdsGroupTable(pdsgroups=pdsgroups)
        res = target_pdsgrouptable.iterator()
        for table_idx in range(len(res)):
            group = res[table_idx]
            assert isinstance(group, pdsgroup.PdsGroup)
            group_list = group.iterator()
            for idx in range(len(group_list)):
                assert group_list[idx].logical_path == expected[table_idx][idx]

    @pytest.mark.parametrize(
        'input_groups,expected',
        [
            ([
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007'],
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010']
             ],
             [
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007'],
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010']
             ]),
            ([
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                ],
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
                ]
             ],
             [
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                ],
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
                ]
             ]),
        ]
    )
    def test_iterator_for_all(self, input_groups, expected):
        pdsgroups = get_pdsgroups(input_groups)
        pdsgroups[0].hide_all()
        target_pdsgrouptable = pdsgrouptable.PdsGroupTable(pdsgroups=pdsgroups)
        res = target_pdsgrouptable.iterator_for_all()
        for table_idx in range(len(res)):
            group = res[table_idx]
            assert isinstance(group, pdsgroup.PdsGroup)
            group_list = group.iterator_for_all()
            for idx in range(len(group_list)):
                print(group_list[idx].logical_path, idx)
                assert group_list[idx].logical_path == expected[table_idx][idx]

    @pytest.mark.parametrize(
        'input_groups,expected',
        [
            ([
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007'],
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010']
             ],
             [
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007']
             ]),
            ([
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                ],
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
                ]
             ],
             [
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                ]
             ]),
        ]
    )
    def test_iterator_for_hidden(self, input_groups, expected):
        pdsgroups = get_pdsgroups(input_groups)
        pdsgroups[0].hide_all()
        target_pdsgrouptable = pdsgrouptable.PdsGroupTable(pdsgroups=pdsgroups)
        res = target_pdsgrouptable.iterator_for_hidden()
        for table_idx in range(len(res)):
            group = res[table_idx]
            assert isinstance(group, pdsgroup.PdsGroup)
            group_list = group.iterator_for_hidden()
            for idx in range(len(group_list)):
                assert group_list[idx].logical_path == expected[table_idx][idx]

    @pytest.mark.parametrize(
        'input_groups,expected',
        [
            ([
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007'],
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010']
             ],
             ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010']),
            ([
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                ],
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
                ]
             ],
             [
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
             ]),
        ]
    )
    def test_pdsfile_iterator(self, input_groups, expected):
        pdsgroups = get_pdsgroups(input_groups)
        pdsgroups[0].hide_all()
        target_pdsgrouptable = pdsgrouptable.PdsGroupTable(pdsgroups=pdsgroups)
        res = target_pdsgrouptable.pdsfile_iterator()
        for idx in range(len(res)):
            pdsf = res[idx]
            assert isinstance(pdsf, pdsfile.PdsFile)
            assert pdsf.logical_path == expected[idx]

    @pytest.mark.parametrize(
        'input_groups,expected',
        [
            ([
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007'],
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010']
             ],
             [
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010'
             ]),
            ([
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                ],
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
                ]
             ],
             [
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
             ]),
        ]
    )
    def test_pdsfile_iterator_for_all(self, input_groups, expected):
        pdsgroups = get_pdsgroups(input_groups)
        pdsgroups[0].hide_all()
        target_pdsgrouptable = pdsgrouptable.PdsGroupTable(pdsgroups=pdsgroups)
        res = target_pdsgrouptable.pdsfile_iterator_for_all()
        for idx in range(len(res)):
            pdsf = res[idx]
            assert isinstance(pdsf, pdsfile.PdsFile)
            assert pdsf.logical_path == expected[idx]

    @pytest.mark.parametrize(
        'input_groups,expected',
        [
            ([
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007'],
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010']
             ],
             [
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007'
             ]),
            ([
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                ],
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
                ]
             ],
             [
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
             ]),
        ]
    )
    def test_pdsfile_iterator_for_hidden(self, input_groups, expected):
        pdsgroups = get_pdsgroups(input_groups)
        pdsgroups[0].hide_all()
        target_pdsgrouptable = pdsgrouptable.PdsGroupTable(pdsgroups=pdsgroups)
        res = target_pdsgrouptable.pdsfile_iterator_for_hidden()
        for idx in range(len(res)):
            pdsf = res[idx]
            assert isinstance(pdsf, pdsfile.PdsFile)
            assert pdsf.logical_path == expected[idx]

    @pytest.mark.parametrize(
        'input_groups,expected',
        [
            ([
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007'],
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010']
             ],
             2)
        ]
    )
    def test___len__(self, input_groups, expected):
        pdsgroups = get_pdsgroups(input_groups)
        target_pdsgrouptable = pdsgrouptable.PdsGroupTable(pdsgroups=pdsgroups)
        res = target_pdsgrouptable.__len__()
        assert res == expected

    @pytest.mark.parametrize(
        'input_groups,new_paths,expected',
        [
            ([
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007']
             ],
             ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010'],
             [
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010'
             ]),
            ([
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                ]
             ],
             [
                 'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                 'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                 'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                 'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
             ],
             [
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
             ]),
        ]
    )
    def test_insert_group(self, input_groups, new_paths, expected):
        pdsgroups = get_pdsgroups(input_groups)
        target_pdsgrouptable = pdsgrouptable.PdsGroupTable(pdsgroups=pdsgroups)
        pdsfiles = get_pdsfiles(new_paths)
        group = pdsgroup.PdsGroup(pdsfiles=pdsfiles)
        target_pdsgrouptable.insert_group(group=group)
        res = target_pdsgrouptable.pdsfile_iterator_for_all()
        for idx in range(len(res)):
            pdsf = res[idx]
            assert pdsf.logical_path == expected[idx]

    @pytest.mark.parametrize(
        'input_groups,new_paths,expected',
        [
            ([
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007']
             ],
             ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010'],
             [
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010'
             ]),
            ([
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                ]
             ],
             [
                 'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                 'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                 'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                 'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
             ],
             [
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
             ]),
        ]
    )
    def test_insert_file(self, input_groups, new_paths, expected):
        pdsgroups = get_pdsgroups(input_groups)
        target_pdsgrouptable = pdsgrouptable.PdsGroupTable(pdsgroups=pdsgroups)

        for path in new_paths:
            pdsf = instantiate_target_pdsfile(path)
            target_pdsgrouptable.insert_file(pdsf=pdsf)

        res = target_pdsgrouptable.pdsfile_iterator_for_all()
        for idx in range(len(res)):
            pdsf = res[idx]
            assert pdsf.logical_path == expected[idx]

    @pytest.mark.parametrize(
        'input_groups,things,expected',
        [
            ([
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007']
             ],
             [instantiate_target_pdsfile('previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010')],
             [
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010'
             ]),
            ([
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                ]
             ],
             [
                 'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                 'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                 'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                 'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
             ],
             [
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
             ]),
        ]
    )
    def test_insert(self, input_groups, things, expected):
        pdsgroups = get_pdsgroups(input_groups)
        target_pdsgrouptable = pdsgrouptable.PdsGroupTable(pdsgroups=pdsgroups)

        for path in things:
            target_pdsgrouptable.insert(things=things)

        res = target_pdsgrouptable.pdsfile_iterator_for_all()
        for idx in range(len(res)):
            pdsf = res[idx]
            assert pdsf.logical_path == expected[idx]

    @pytest.mark.parametrize(
        'input_groups,expected',
        [
            ([
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007'],
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010']
             ],
             [
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010'
             ]),
            ([
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                ],
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
                ]
             ],
             [
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
             ]),
        ]
    )
    def test_sort_in_groups(self, input_groups, expected):
        pdsgroups = get_pdsgroups(input_groups)
        target_pdsgrouptable = pdsgrouptable.PdsGroupTable(pdsgroups=pdsgroups)
        # sort within each group
        target_pdsgrouptable.sort_in_groups()
        res = target_pdsgrouptable.pdsfile_iterator_for_all()
        for idx in range(len(res)):
            pdsf = res[idx]
            assert isinstance(pdsf, pdsfile.PdsFile)
            assert pdsf.logical_path == expected[idx]

    @pytest.mark.parametrize(
        'input_groups,expected',
        [
            ([
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010'],
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007']
             ],
             [
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010'
             ]),
            ([
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
                ],
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                ]
             ],
             [
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
             ]),
        ]
    )
    def test_sort_groups(self, input_groups, expected):
        pdsgroups = get_pdsgroups(input_groups)
        target_pdsgrouptable = pdsgrouptable.PdsGroupTable(pdsgroups=pdsgroups)
        # sort between different groups
        target_pdsgrouptable.sort_groups()
        res = target_pdsgrouptable.pdsfile_iterator_for_all()
        for idx in range(len(res)):
            pdsf = res[idx]
            assert isinstance(pdsf, pdsfile.PdsFile)
            assert pdsf.logical_path == expected[idx]

    @pytest.mark.parametrize(
        'input_groups,hide_path,expected',
        [
            ([
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010'],
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007']
             ],
             'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010',
             True),
            ([
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010'],
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007']
             ],
             'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_011',
             False),
            ([
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
                ],
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                ]
             ],
             'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
             True),
        ]
    )
    def test_hide_pdsfile(self, input_groups, hide_path, expected):
        pdsgroups = get_pdsgroups(input_groups)
        target_pdsgrouptable = pdsgrouptable.PdsGroupTable(pdsgroups=pdsgroups)
        pdsf = instantiate_target_pdsfile(hide_path)
        res = target_pdsgrouptable.hide_pdsfile(pdsf=pdsf)
        hidden_pdsf = target_pdsgrouptable.pdsfile_iterator_for_hidden()
        for pdsf in hidden_pdsf:
            assert pdsf.logical_path == hide_path
        assert res == expected

    @pytest.mark.parametrize(
        'input_groups,remove_path,expected',
        [
            ([
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010'],
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007']
             ],
             'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010',
             True),
            ([
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010'],
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007']
             ],
             'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_011',
             False),
            ([
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
                ],
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                ]
             ],
             'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
             True),
        ]
    )
    def test_remove_pdsfile(self, input_groups, remove_path, expected):
        pdsgroups = get_pdsgroups(input_groups)
        target_pdsgrouptable = pdsgrouptable.PdsGroupTable(pdsgroups=pdsgroups)
        pdsf = instantiate_target_pdsfile(remove_path)
        res = target_pdsgrouptable.remove_pdsfile(pdsf=pdsf)
        pdsfiles = target_pdsgrouptable.pdsfile_iterator_for_all()
        for pdsf in pdsfiles:
            assert pdsf.logical_path != remove_path
        assert res == expected

    @pytest.mark.parametrize(
        'input_groups,regex,expected',
        [
            ([
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010'],
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007']
             ],
             re.compile(r'\_010'),
             ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010']),
            ([
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
                ],
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                ]
             ],
             re.compile(r'16\_31\_thumb.*'),
             ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png']),
        ]
    )
    def test_filter(self, input_groups, regex, expected):
        pdsgroups = get_pdsgroups(input_groups)
        target_pdsgrouptable = pdsgrouptable.PdsGroupTable(pdsgroups=pdsgroups)
        target_pdsgrouptable.filter(regex=regex)
        pdsfiles = target_pdsgrouptable.pdsfile_iterator()
        for pdsf in pdsfiles:
            assert pdsf.logical_path in expected

    @pytest.mark.parametrize(
        'input_paths,expected',
        [
            ([
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007'
             ],
             [
                 'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010',
                 'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007'
             ]),
            ([
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
             ],
             [
                 'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                 'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                 'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                 'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
                 'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                 'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                 'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                 'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
              ]
             ),
        ]
    )
    def test_tables_from_pdsfiles(self, input_paths, expected):
        pdsfiles = get_pdsfiles(input_paths)
        tables = pdsgrouptable.PdsGroupTable.tables_from_pdsfiles(pdsfiles=pdsfiles)
        for table in tables:
            assert isinstance(table, pdsgrouptable.PdsGroupTable)
            for group in table.iterator_for_all():
                for pdsf in group.iterator_for_all():
                    assert pdsf.logical_path in expected

    @pytest.mark.parametrize(
        'input_groups,hide_path,expected',
        [
            ([
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010'],
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007']
             ],
             'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010',
             0),
            ([
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_010'],
                ['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007']
             ],
             'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_011',
             0),
            ([
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_med.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_33_full.png',
                ],
                [
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                    'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                ]
             ],
             'previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
             0),
        ]
    )
    def test_remove_hidden(self, input_groups, hide_path, expected):
        pdsgroups = get_pdsgroups(input_groups)
        target_pdsgrouptable = pdsgrouptable.PdsGroupTable(pdsgroups=pdsgroups)
        pdsf = instantiate_target_pdsfile(hide_path)
        target_pdsgrouptable.hide_pdsfile(pdsf=pdsf)
        new_table = target_pdsgrouptable.remove_hidden()
        hidden_pdsf = new_table.pdsfile_iterator_for_hidden()
        assert len(hidden_pdsf) == expected

    @pytest.mark.parametrize(
        'input_groups1,input_groups2,expected',
        [
            ([
                [
                    'metadata/NHxxMV_xxxx/NHLAMV_1001/NHLAMV_1001_index.tab',
                    'metadata/NHxxMV_xxxx/NHLAMV_1001/NHLAMV_1001_index.lbl',
                ]
             ],
             [
                 [
                    'metadata/NHxxMV_xxxx/NHLAMV_1001/NHLAMV_1001_supplemental_index.lbl',
                    'metadata/NHxxMV_xxxx/NHLAMV_1001/NHLAMV_1001_supplemental_index.tab',
                 ]
              ],
             [
                'metadata/NHxxMV_xxxx/NHLAMV_1001/NHLAMV_1001_index.tab',
                'metadata/NHxxMV_xxxx/NHLAMV_1001/NHLAMV_1001_index.lbl',
                'metadata/NHxxMV_xxxx/NHLAMV_1001/NHLAMV_1001_supplemental_index.lbl',
                'metadata/NHxxMV_xxxx/NHLAMV_1001/NHLAMV_1001_supplemental_index.tab',
             ]),
        ]
    )
    def test_merge_index_row_tables(self, input_groups1, input_groups2, expected):
        pdsgroups1 = get_pdsgroups(input_groups1)
        pdsgrouptable1 = pdsgrouptable.PdsGroupTable(pdsgroups=pdsgroups1)
        pdsgroups2 = get_pdsgroups(input_groups2)
        pdsgrouptable2 = pdsgrouptable.PdsGroupTable(pdsgroups=pdsgroups2)
        tables = [pdsgrouptable1, pdsgrouptable2]

        new_tables = pdsgrouptable.PdsGroupTable.merge_index_row_tables(tables=tables)
        for table in tables:
            assert isinstance(table, pdsgrouptable.PdsGroupTable)
            for pdsf in table.pdsfile_iterator():
                assert pdsf.logical_path in expected


################################################################################
# Blackbox test for heler functions in pdsfile.py
################################################################################
class TestPdsFileHelperBlackBox:
    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COVIMS_8xxx/COVIMS_8001/data/VIMS_2017_251_GAMCRU_I_TAU_10KM.tab',
             True),
            (PDS_DATA_DIR + '/metadata/COVIMS_0xxx/COVIMS_0001',
             False),
        ]
    )
    def test_is_logical_path(self, input_path, expected):
        res = pdsfile.is_logical_path(path=input_path)
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            (PDS_DATA_DIR + '/volumes/COUVIS_0xxx/COUVIS_0058/DATA/D2017_001/EUV2017_001_03_49.dat',
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
            (PDS_DATA_DIR + '/volumes/COUVIS_0xxx/COUVIS_0058/DATA/D2017_001/EUV2017_001_03_49.DAT',
             PDS_DATA_DIR + '/volumes/COUVIS_0xxx/COUVIS_0058/DATA/D2017_001/EUV2017_001_03_49.DAT')
        ]
    )
    def test_repair_case(self, input_path, expected):
        res = pdsfile.repair_case(abspath=input_path)
        assert res.lower() == expected.lower()

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            (PDS_DATA_DIR + '/volumes/COUVIS_0xxx/COUVIS_0058/DATA/D2017_001/EUV2017_001_03_49.dat',
             PDS_DATA_DIR + '/volumes/COUVIS_0xxx/COUVIS_0058/DATA/D2017_001/EUV2017_001_03_49.dat'),
            ('volumes/COISS_0xxx/COISS_0001/data/wacfm/bit_wght/13302/133020.lbl',
             PDS_DATA_DIR + '/volumes/COISS_0xxx/COISS_0001/data/wacfm/bit_wght/13302/133020.lbl'),
        ]
    )
    def test_selected_path_from_path(self, input_path, expected):
        res = pdsfile.selected_path_from_path(path=input_path)
        assert res == expected
