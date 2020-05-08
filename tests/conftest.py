import pdsfile
import pytest
import settings

PDS_DATA_DIR = settings.PDS_DATA_DIR
TESTFILE_PATH = settings.TESTFILE_PATH
################################################################################
# Setup before all tests
################################################################################
@pytest.fixture(scope='session', autouse=True)
def setup():
    # pdsfile_data_path = os.path.abspath(PDS_DATA_DIR)
    pdsfile.preload(PDS_DATA_DIR)
    pdsfile.use_pickles()
