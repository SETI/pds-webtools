import pdsgroup
import pdsviewable

import pytest

from pdsfile.pds3file.tests.helper import get_pdsfiles

##########################################################################################
# Blackbox test for internal cached in PdsGroup class
##########################################################################################
class TestPdsGroupBlackBox:
    @pytest.mark.parametrize(
        'input_paths,expected',
        [
            ([
                'volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.DAT',
                'volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.LBL'
             ],
             [
                '/holdings/_icons/blue/png-100/document_geometry.png',
                '/holdings/_icons/blue/png-500/document_geometry.png',
                '/holdings/_icons/blue/png-30/document_geometry.png',
                '/holdings/_icons/blue/png-200/document_geometry.png',
                '/holdings/_icons/blue/png-50/document_geometry.png',
             ]
            ),
            (['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007'],
             [
                '/holdings/_icons/blue/png-500/folder_previews.png',
                '/holdings/_icons/blue/png-200/folder_previews.png',
                '/holdings/_icons/blue/png-30/folder_previews.png',
                '/holdings/_icons/blue/png-100/folder_previews.png',
                '/holdings/_icons/blue/png-50/folder_previews.png',
             ]
            )
        ]
    )
    def test__iconset(self, input_paths, expected):
        """filename_keylen: return self._iconset_filled[0]"""
        target_pdsfile = get_pdsfiles(input_paths)
        target_pdsgroup = pdsgroup.PdsGroup(pdsfiles=target_pdsfile)
        res1 = target_pdsgroup._iconset
        res2 = target_pdsgroup._iconset
        assert isinstance(res1, pdsviewable.PdsViewSet)
        assert res1 == res2
        viewables = res1.to_dict()['viewables']
        for viewable in viewables:
            assert viewable['url'] in expected

    @pytest.mark.parametrize(
        'input_paths,expected',
        [
            ([
                'volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.DAT',
                'volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.LBL'
             ],
             [
                '/holdings/_icons/blue/png-100/document_geometry.png',
                '/holdings/_icons/blue/png-500/document_geometry.png',
                '/holdings/_icons/blue/png-30/document_geometry.png',
                '/holdings/_icons/blue/png-200/document_geometry.png',
                '/holdings/_icons/blue/png-50/document_geometry.png',
             ]
            ),
            (['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007'],
             [
                '/holdings/_icons/blue/png-200/folder_previews_open.png',
                '/holdings/_icons/blue/png-500/folder_previews_open.png',
                '/holdings/_icons/blue/png-30/folder_previews_open.png',
                '/holdings/_icons/blue/png-100/folder_previews_open.png',
                '/holdings/_icons/blue/png-50/folder_previews_open.png',
             ]
            )
        ]
    )
    def test_iconset_open(self, input_paths, expected):
        """filename_keylen: return self._iconset_filled[0]"""
        target_pdsfile = get_pdsfiles(input_paths)
        target_pdsgroup = pdsgroup.PdsGroup(pdsfiles=target_pdsfile)
        res1 = target_pdsgroup.iconset_open
        res2 = target_pdsgroup.iconset_open
        assert isinstance(res1, pdsviewable.PdsViewSet)
        assert res1 == res2
        viewables = res1.to_dict()['viewables']
        for viewable in viewables:
            assert viewable['url'] in expected

    @pytest.mark.parametrize(
        'input_paths,expected',
        [
            ([
                'volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.DAT',
                'volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.LBL'
             ],
             [
                '/holdings/_icons/blue/png-100/document_geometry.png',
                '/holdings/_icons/blue/png-500/document_geometry.png',
                '/holdings/_icons/blue/png-30/document_geometry.png',
                '/holdings/_icons/blue/png-200/document_geometry.png',
                '/holdings/_icons/blue/png-50/document_geometry.png',
             ]
            ),
            (['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007'],
             [
                '/holdings/_icons/blue/png-200/folder_previews.png',
                '/holdings/_icons/blue/png-500/folder_previews.png',
                '/holdings/_icons/blue/png-30/folder_previews.png',
                '/holdings/_icons/blue/png-100/folder_previews.png',
                '/holdings/_icons/blue/png-50/folder_previews.png',
             ]
            )
        ]
    )
    def test_iconset_closed(self, input_paths, expected):
        """filename_keylen: return self._iconset_filled[0]"""
        target_pdsfile = get_pdsfiles(input_paths)
        target_pdsgroup = pdsgroup.PdsGroup(pdsfiles=target_pdsfile)
        res1 = target_pdsgroup.iconset_closed
        res2 = target_pdsgroup.iconset_closed
        assert isinstance(res1, pdsviewable.PdsViewSet)
        assert res1 == res2
        viewables = res1.to_dict()['viewables']
        for viewable in viewables:
            assert viewable['url'] in expected
