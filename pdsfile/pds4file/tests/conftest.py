##########################################################################################
# pds4file/tests/conftest.py
#
# Configuration & setup before running tests on pds4file
##########################################################################################

import os
import pdsfile.pds4file as pds4file
from pdsfile.cfg import PDS4_HOLDINGS_DIR
from pdsfile.general_helper import set_logger
from pdsfile.preload_and_cache import (use_shelves_only)
import pdslogger
import pytest

##########################################################################################
# Setup before all tests
##########################################################################################
def pytest_addoption(parser):
    parser.addoption("--mode", action="store")

def turn_on_logger(filename):
    LOGGER = pdslogger.PdsLogger(filename)
    set_logger(pds4file.Pds4File, LOGGER)

@pytest.fixture(scope='session', autouse=True)
def setup(request):
    mode = request.config.option.mode
    if mode == 's':
        use_shelves_only(pds4file.Pds4File, True)
    elif mode == 'ns':
        use_shelves_only(pds4file.Pds4File, False)
    else: # pragma: no cover
        use_shelves_only(pds4file.Pds4File, True)

    # turn_on_logger("test_log.txt")
    pds4file.Pds4File.preload(PDS4_HOLDINGS_DIR)
