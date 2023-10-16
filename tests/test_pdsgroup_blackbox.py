import pdsfile.pds3file as pds3file
import pdsgroup
import pdsgrouptable
import pdsviewable

import pytest
import re

from pdsfile.pds3file.tests.helper import (get_pdsfiles,
                                           get_pdsgroups,
                                           instantiate_target_pdsfile)

##########################################################################################
# Blackbox test for functions & properties in PdsGroup class
##########################################################################################
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
                '/holdings/previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                '/holdings/previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                '/holdings/previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                '/holdings/previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
             ]
            ),
            (['previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/'],
             [
                '/holdings/previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png',
                '/holdings/previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_med.png',
                '/holdings/previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_small.png',
                '/holdings/previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_full.png',
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

##########################################################################################
# Blackbox test for functions & properties in PdsGroupTable class
##########################################################################################
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
            assert isinstance(pdsf, pds3file.Pds3File)
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
            assert isinstance(pdsf, pds3file.Pds3File)
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
            assert isinstance(pdsf, pds3file.Pds3File)
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
            assert isinstance(pdsf, pds3file.Pds3File)
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
            assert isinstance(pdsf, pds3file.Pds3File)
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
