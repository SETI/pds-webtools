##########################################################################################
# pds3file/tests/conftest.py
#
# Configuration & setup before running tests on pds3file
##########################################################################################

import os
import pdsfile.pds3file as pds3file
from pdsfile.general_helper import (PDS_HOLDINGS_DIR,
                                    set_logger)
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
    set_logger(pds3file.Pds3File, LOGGER)

# We only use use_pickles and use_shelves_only
@pytest.fixture(scope='session', autouse=True)
def setup(request):
    mode = request.config.option.mode
    if mode == 's':
        use_shelves_only(pds3file.Pds3File, True)
    elif mode == 'ns':
        use_shelves_only(pds3file.Pds3File, False)
    else: # pragma: no cover
        use_shelves_only(pds3file.Pds3File, True)

    # turn_on_logger("test_log.txt")
    pds3file.Pds3File.preload(PDS_HOLDINGS_DIR)
