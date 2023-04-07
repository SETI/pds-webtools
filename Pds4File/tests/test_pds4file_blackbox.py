import os
import pytest

from tests.helper import instantiate_target_pdsfile

# Check environment variables or else look in the default places
try:
    PDS4_HOLDINGS_DIR = os.environ['PDS4_HOLDINGS_DIR']
except KeyError: # pragma: no cover
    # TODO: update this when we know the actual path of pds4 holdings on the webserver
    PDS4_HOLDINGS_DIR = os.path.realpath('/Library/WebServer/Documents/holdings')

################################################################################
# Blackbox tests for pds4file.py
################################################################################
class TestPds4FileBlackBox:
    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/data/atmosphere/u0_kao_91cm_734nm_counts-v-time_atmos_ingress.xml',
             'uranus_occ_u0_kao_91cm'),
            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/data/global/u0_kao_91cm_734nm_counts-v-time_occult.xml',
             'uranus_occ_u0_kao_91cm'),
            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/data/rings/u0_kao_91cm_734nm_radius_alpha_egress_1000m.tab',
             'uranus_occ_u0_kao_91cm'),
        ]
    )
    def test_opus_id(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.opus_id
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm',
             f'{PDS4_HOLDINGS_DIR}/uranus_occs_earthbased/uranus_occ_u0_kao_91cm'),
        ]
    )
    def test_abspath(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.abspath
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/data/rings/u0_kao_91cm_734nm_radius_alpha_egress_1000m.xml',
             'bundles/uranus_occs_earthbased/uranus_occ_u0_kao_91cm/data/rings/u0_kao_91cm_734nm_radius_alpha_egress_1000m.xml'),
        ]
    )
    def test_logical_path(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.logical_path
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/data/rings/u0_kao_91cm_734nm_radius_alpha_egress_1000m.xml',
             True),
            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/data/rings/non-existent-filename.txt',
             False),
        ]
    )
    def test_exists(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.exists
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('uranus_occs_earthbased/',
             ''), # bundlesets currently have empty string instead of False
            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm',
             True),
            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/bundle.xml',
             False),
            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/data/atmosphere/u0_kao_91cm_734nm_counts-v-time_atmos_egress.xml',
             False),
        ]
    )
    def test_is_bundle(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.is_bundle
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm',
             True), # This test fails with `ValueError: Illegal bundle set directory "": bundles`, because of match failure with BUNDLE_SET_PLUS_REGEX_I on line 3254 of pds4file.py
            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/browse',
             False),
            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/xml_schema/collection_xml_schema.csv',
             False),
            ('uranus_occs_earthbased',
             ''), # Bundlesets return empty string, rather than False at the moment
            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/bundle.xml',
             False),
            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/data/atmosphere/u0_kao_91cm_734nm_counts-v-time_atmos_egress.xml',
             False),
            ('uranus_occs_earthbased/',
             ''), # bundlesets currently have empty string instead of False
        ]
    )
    def test_is_bundle_dir(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.is_bundle_dir
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/data/rings/u0_kao_91cm_734nm_radius_alpha_egress_1000m.xml',
             False),
             ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/bundle.xml',
             False),
        ]
    )
    def test_is_bundle_file(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.is_bundle_file
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('uranus_occs_earthbased',
             True),
            ('uranus_occs_earthbased/',
             True),
             ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/bundle.xml',
             False),
        ]
    )
    def test_is_bundleset(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.is_bundleset
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('uranus_occs_earthbased',
             True),
            ('uranus_occs_earthbased/',
             True),
            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/bundle.xml',
             False),
        ]
    )
    def test_is_bundleset_dir(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.is_bundleset_dir
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('uranus_occs_earthbased/',
             'uranus_occs_earthbased'),
            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm',
             'uranus_occs_earthbased'),
            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/bundle.xml',
             'uranus_occs_earthbased'),
            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/data/atmosphere/u0_kao_91cm_734nm_counts-v-time_atmos_ingress.tab',
             'uranus_occs_earthbased'),
        ]
    )
    def test_bundleset(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.bundleset
        assert res == expected


    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('uranus_occs_earthbased/',
             ['uranus_occ_u0_kao_91cm']),
            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm',
             ['browse', 'bundle.xml', 'bundle_member_index.csv', 'bundle_member_index230313.csv', 'context', 'data', 'document', 'readme.txt', 'xml_schema']),
            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/bundle.xml',
             []),
            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/data/atmosphere/u0_kao_91cm_734nm_counts-v-time_atmos_egress.xml',
             []),
        ]
    )
    def test_childnames(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.childnames
        assert res == expected

