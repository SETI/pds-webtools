import pdsfile
import settings

PDS_DATA_DIR = settings.PDS_DATA_DIR
TESTFILE_PATH = settings.TESTFILE_PATH

def instantiate_target_pdsfile(path, is_abspath=True):
    if is_abspath:
        TESTFILE_PATH = PDS_DATA_DIR + path
        target_pdsfile = pdsfile.PdsFile.from_abspath(TESTFILE_PATH)
    else:
        TESTFILE_PATH = path
        target_pdsfile = pdsfile.PdsFile.from_logical_path(TESTFILE_PATH)
    return target_pdsfile
