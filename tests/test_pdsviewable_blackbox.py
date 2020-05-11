import pdsfile
import pdsviewable
import pytest
import settings

from tests.helper import instantiate_target_pdsfile

PDS_DATA_DIR = settings.PDS_DATA_DIR
TESTFILE_PATH = settings.TESTFILE_PATH

################################################################################
# PdsViewSet Blackbox test
################################################################################
class TestPdsViewSetBlackBox:
    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('previews/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274/' \
            'EUV2004_274_01_39_thumb.png', ''),

        ]
    )
    def test_thumbnail(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        pdsviewset = pdsviewable.PdsViewSet.from_pdsfiles(target_pdsfile)
        pds_viewable = pdsviewable.PdsViewable.from_pdsfile(target_pdsfile)
        print(isinstance(target_pdsfile, pdsfile.PdsFile))
        print(pds_viewable)
        assert pdsviewset.thumbnail.abspath == expected
