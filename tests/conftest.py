import os
import pdsfile
import pytest

PDS_DATA_DIR = os.environ['PDS_DATA_DIR']
################################################################################
# Setup before all tests
################################################################################
def pytest_addoption(parser):
    parser.addoption("--mode", action="store")

@pytest.fixture(scope='session', autouse=True)
def setup(request):
    mode = request.config.option.mode
    # print(f'Current mode: {mode}')
    # print(f'Current mode: {isinstance(mode, str)}')
    # print(f'Current mode: {mode == "1"}')
    # pdsfile.use_pickles()
    # pdsfile.use_shelves_only()
    if mode == '1':
        pdsfile.use_pickles(True)
        pdsfile.use_shelves_only(True)
    elif mode == '2':
        pdsfile.use_pickles(True)
        pdsfile.use_shelves_only(False)
    elif mode == '3':
        pdsfile.use_pickles(False)
        pdsfile.use_shelves_only(True)
    elif mode == '4':
        pdsfile.use_pickles(False)
        pdsfile.use_shelves_only(False)
    pdsfile.preload(PDS_DATA_DIR)
