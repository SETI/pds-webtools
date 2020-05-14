import os
import pdsfile
import pytest

PDS_DATA_DIR = os.environ['PDS_DATA_DIR']
################################################################################
# Setup before all tests
################################################################################
@pytest.fixture(scope='session', autouse=True)
def setup():
    # pdsfile_data_path = os.path.abspath(PDS_DATA_DIR)
    pdsfile.preload(PDS_DATA_DIR)
    pdsfile.use_pickles()
