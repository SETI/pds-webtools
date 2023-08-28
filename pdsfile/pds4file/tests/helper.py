import os
import pdsfile.pds4file as pds4file

from pdsfile.cfg import PDS4_BUNDLES_DIR
from pdsfile.general_helper import instantiate_target_pdsfile_for_class

def instantiate_target_pdsfile(path, is_abspath=True):
    return instantiate_target_pdsfile_for_class(path, pds4file.Pds4File,
                                                PDS4_BUNDLES_DIR, is_abspath)