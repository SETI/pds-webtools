import os
import pdsfile
import pytest
################################################################################
# Setup before pytest
################################################################################
try:        # PDS_DATA_DIR overrides the default holdings directory location
    pdsfile.LOCAL_HOLDINGS_DIRS = [os.environ['PDS_DATA_DIR']]
except KeyError:
    pass

def pytest_addoption(parser):
    parser.addoption("--mode", action="store")

@pytest.fixture(scope='session', autouse=True)
def setup(request):
    mode = request.config.option.mode
    if mode == '1':
        pdsfile.use_shelves_only(True)
    elif mode == '2':
        pdsfile.use_shelves_only(False)
    else: # default
        pdsfile.use_shelves_only(True)
