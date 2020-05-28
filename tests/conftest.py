import os
import pdsfile
import pytest

PDS_DATA_DIR = os.environ['PDS_DATA_DIR']
################################################################################
# Setup before all tests
################################################################################
@pytest.fixture(scope='session', autouse=True)
def setup():
    # pdsfile.use_pickles()
    pdsfile.use_shelves_only()
    pdsfile.preload(PDS_DATA_DIR)
