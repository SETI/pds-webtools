import os
import pdsfile
import pdsviewable
import pytest
import re

from tests.helper import *

PDS_DATA_DIR = os.environ['PDS_DATA_DIR']
PDS_PDSDATA_PATH = PDS_DATA_DIR[:PDS_DATA_DIR.index('holdings')]
################################################################################
# Whitebox test for functions & properties in PdsFile class
################################################################################
class TestPdsFileWhiteBox:
    ############################################################################
    # Test for properties
    ############################################################################
    def test_exists_1(self):
        # Note: line 1015, the path will never be hit.
        target_pdsfile = pdsfile.PdsFile.new_virtual('volumes')
        assert target_pdsfile.exists == True

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes', False),
        ]
    )
    def test_exists_2(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(
            input_path, is_abspath=False)
        # Something doesn't exist
        child = target_pdsfile.child(basename='ASTROM_xxxx')
        assert child.is_virtual == False
        assert child.abspath == None
        assert child.exists == expected

    def test_isdir_1(self):
        # Note: similar to test_exists_1
        target_pdsfile = pdsfile.PdsFile.new_virtual('volumes')
        expected = 'volumes'
        assert target_pdsfile.isdir == True

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/ASTROM_xxxx/ASTROM_0001', False),
        ]
    )
    def test_isdir_2(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(
            input_path, is_abspath=False)
        # Something doesn't exist
        child = target_pdsfile.child(basename='VOLDESC.CAT')
        assert child.is_virtual == False
        assert child.abspath == None
        assert child.isdir == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            # virtual directory
            ('volumes', 'holdings/volumes'),
        ]
    )
    def test_html_path(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(
            input_path, is_abspath=False)
        assert target_pdsfile.abspath == None
        assert target_pdsfile.html_path == expected

    @pytest.mark.parametrize(
        'input_path,selection,expected',
        [
            ('metadata/HSTOx_xxxx/HSTO0_7308/HSTO0_7308_index.tab',
             'O43BA4DUQ', 'HSTO0_7308_index-O43BA4DUQ'),
        ]
    )
    def test_anchor(self, input_path, selection, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.row_pdsfile(selection=selection)
        assert res.anchor == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes', ''),
        ]
    )
    def test_parent_logical_path(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(
            input_path, is_abspath=False)
        assert target_pdsfile.parent_logical_path == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('', ['', 'UNKNOWN']),
        ]
    )
    def test__volume_info(self, input_path, expected):
        # Same as pdsfile.PdsFile()
        target_pdsfile = instantiate_target_pdsfile(input_path)
        print(target_pdsfile._volume_info)
        assert target_pdsfile._volume_info[0] == expected[0]
        assert target_pdsfile._volume_info[1] == expected[1]

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('diagrams/COCIRS_6xxx/COCIRS_6004',
             'Diagrams for Cassini CIRS data, reformatted, 2010-04-01 to 2010-04-30 (SC clock 1648773882-1651332653)'),
            ('calibrated/COISS_1xxx/COISS_1001',
             'Calibrated Cassini ISS Jupiter images 1999-01-09 to 2000-10-31 (SC clock 1294562621-1351672562)')
        ]
    )
    def test_description1(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.description == expected

    @pytest.mark.parametrize(
        'input_path,selection,expected',
        [
            ('metadata/HSTOx_xxxx/HSTO0_7308/HSTO0_7308_index.tab',
             'O43BA4DUQ', 'Selected row of index'),
        ]
    )
    def test_description2(self, input_path, selection, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.row_pdsfile(selection=selection)
        print(res.row_dicts)
        assert res.description == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('previews/HSTUx_xxxx/HSTU0_5167/DATA/VISIT_04', ''),
            ('volumes/RPX_xxxx/RPX_0001/CALIB/F130LP.tabx', '')
        ]
    )
    def test_mime_type(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.mime_type == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COCIRS_6xxx/COCIRS_6004/DATA/GEODATA/GEO1004021018_699.TAB',
            'GEO1004021018_699.LBL'),
            ('volumes/COCIRS_6xxx/COCIRS_6004/DATA/GEODATA/', '')
        ]
    )
    def test_info_basename(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.info_basename == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            # Something that don't exist
            ('volumes/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274/EUV2004_274_01_39x.lbl',
            ''),
            ('volumes/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274/EUV2004_274_01_39x',
            '.LBL'),
            ('volumes/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274/EUV2004_274_01_39x.cat',
            ''),
        ]
    )
    def test_label_basename(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.label_basename == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            # Something that doesn't exist
            ('previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_fullx.png',
            False),
        ]
    )
    def test_viewset(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.viewset == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('', ''),
        ]
    )
    def test_volume_publication_date(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.volume_publication_date == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            # The 1st case should return [], instead of None
            ('volumes/VGISS_8xxx/VGISS_8201/DATA/C08966XX/C0896631xx_RAW.lbl',
             []),
            ('volumes/VGISS_8xxx', [999999]),
            ('volumes', []),
            ('', []),
        ]
    )
    def test_version_ranks(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.version_ranks == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            # nonexistent pdsfile path
            ('archives-volumes/COCIRS_xxxx/COCIRS_0010.tar.gz',''),
        ]
    )
    def test_exact_archive_url(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.exact_archive_url
        res2 = target_pdsfile.exact_archive_url
        assert res1 == expected
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            # nonexistent pdsfile path
            ('archives-volumes/COCIRS_xxxx/COCIRS_0012.tar.gz',
             ''),
        ]
    )
    def test_exact_checksum_url(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.exact_checksum_url
        res2 = target_pdsfile.exact_checksum_url
        assert res1 == expected
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('diagrams/COCIRS_5xxx/COCIRS_5401/BROWSE/TARGETS/IMG0401130240_FP1_x.jpg',
             False),
        ]
    )
    def test_grid_view_allowed(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.grid_view_allowed
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COVIMS_0xxx', 11),
        ]
    )
    def test_filename_keylen(self, input_path, expected):
        """filename_keylen: return self._filename_keylen_filled"""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.filename_keylen == expected

    ############################################################################
    # Test for class functions
    ############################################################################
    @pytest.mark.parametrize(
        'input_suffix,expected',
        [
            ('_in_prep', (990100, 'In preparation', '')),
            ('_lien_resolution', (990400, 'In lien resolution', '')),
        ]
    )
    def test_version_info(self, input_suffix, expected):
        res = pdsfile.PdsFile.version_info(suffix=input_suffix)
        assert res == expected

    ############################################################################
    # Test for functions
    ############################################################################
    @pytest.mark.parametrize(
        'input_path,expected',
        [
            # ('previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007',
            #  pdsviewable.PdsViewSet),
            # ('archives-volumes/COCIRS_0xxx/', None),
            # ('volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31.lbl',
            #  None),
            # ('metadata/COUVIS_0xxx/COUVIS_0001/COUVIS_0001_index.tab',
            #  pdsviewable.PdsViewable),
            ('volumes/COCIRS_6xxx/COCIRS_6002/DATA/RINDATA/RIN1002071502_FP3.LBL',
             pdsviewable.PdsViewable),
        ]
    )
    def test_viewset_lookup(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        print(pdsfile._isstr(target_pdsfile.VIEWABLES['default'].first(target_pdsfile.logical_path)))
        print(target_pdsfile.VIEWABLES['default'].first(target_pdsfile.logical_path))
        print(target_pdsfile.VIEWABLES['default'].all(target_pdsfile.logical_path))
        print(target_pdsfile.is_viewable)
        print(target_pdsfile.isdir)
        if expected is not None:
            assert isinstance(target_pdsfile.viewset_lookup(), expected)
        else:
            assert target_pdsfile.viewset_lookup() == expected

    ############################################################################
    # Test for associated volumes and volsets
    ############################################################################
    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('', 'No associated volume'),
        ]
    )
    def test_volume_pdsdir(self, input_path, expected):
        with pytest.raises(ValueError) as excinfo:
            target_pdsfile = instantiate_target_pdsfile(input_path)
            target_pdsfile.volume_pdsdir()
        assert expected in str(excinfo.value)
        # target_pdsfile = instantiate_target_pdsfile(input_path)
        # assert target_pdsfile.volume_pdsdir() == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/HSTNx_xxxx/HSTN0_7176', 'volumes/HSTNx_xxxx')
        ]
    )
    def test_volset_pdsdir(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        assert target_pdsfile.volset_pdsdir().logical_path == expected

    ############################################################################
    # Test for support for PdsFile objects representing index rows
    ############################################################################
    @pytest.mark.parametrize(
        'input_path,selection,expected',
        [
            # ['O43B05C1Q', 'O43B05C3Q', 'O43B06BTQ', 'O43B06BVQ', 'O43B09B3Q', 'O43B09B5Q', 'O43B11D7Q', 'O43B11D8Q', 'O43B12XAQ', 'O43B13S4Q', 'O43B13S6Q', 'O43B13S8Q', 'O43B13SAQ', 'O43B14SFQ', 'O43B14SIQ', 'O43B15XEQ', 'O43B20010', 'O43B20X9Q', 'O43B21010', 'O43B21020', 'O43B22010', 'O43B22LXQ', 'O43B22MBQ', 'O43B2AXBQ', 'O43B2AXCQ', 'O43B2QXCQ', 'O43B2RXEQ', 'O43B2SXGQ', 'O43B2SXIQ', 'O43B2TXKQ', 'O43B2TXMQ', 'O43B2XCLQ', 'O43B2XCMQ', 'O43B4ASKQ', 'O43B5HXGQ', 'O43B5HXIQ', 'O43BA1BNQ', 'O43BA1BPQ', 'O43BA2H4Q', 'O43BA2H6Q', 'O43BA3M4Q', 'O43BA3M6Q', 'O43BA4DUQ', 'O43BA4DWQ', 'O43BA5C5Q', 'O43BA5C7Q', 'O43BA6BXQ', 'O43BA6BZQ', 'O43BA9B7Q', 'O43BA9B9Q', 'O43BB9BBQ', 'O43BC9BDQ', 'O43BD9BFQ', 'O43BD9BHQ', 'O43BE9BJQ']
            ('metadata/HSTOx_xxxx/HSTO0_7308/HSTO0_7308x_index.tab',
             'O43B06BTQ', 2),
            ('volumes/HSTOx_xxxx/HSTO0_7308/DATA/VISIT_05/O43B05C1Q.lbl',
             'O43BB9BBQ', 50),
        ]
    )
    def test_find_selected_row_number(self, input_path, selection, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        try:
            res = target_pdsfile.find_selected_row_number(selection=selection)
            assert res == expected
        except IOError as e:
            assert 'Row selections' in e # Index row is not found
            # assert e == True # Index row is not found

    def test_absolute_or_logical_path(self):
        """absolute_or_logical_path: get logical path."""
        target_pdsfile = pdsfile.PdsFile.new_virtual('volumes')
        expected = 'volumes'
        assert target_pdsfile.absolute_or_logical_path == expected
