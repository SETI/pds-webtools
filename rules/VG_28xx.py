####################################################################################################################################
# rules/VG_28xx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'.*/EDITDATA', re.I, ('Edited data',                   'DATADIR')),
    (r'.*/FOVMAPS',  re.I, ('Field-of-view maps',            'IMAGEDIR')),
    (r'.*/IMAGES',   re.I, ('Star reference image files',    'IMAGEDIR')),
    (r'.*/JITTER',   re.I, ('Pointing data',                 'GEOMDIR')),
    (r'.*/NOISDATA', re.I, ('Noise data',                    'DATADIR')),
    (r'.*/RAWDATA',  re.I, ('Raw data',                      'DATADIR')),
    (r'.*/TRAJECT',  re.I, ('Trajectory data',               'GEOMDIR')),
    (r'.*/VECTORS',  re.I, ('Pointing data',                 'GEOMDIR')),
    (r'.*/S_RINGS',  re.I, ('Saturn ring occultation data',  'DATADIR')),
    (r'.*/U_RINGS',  re.I, ('Uranian ring occultation data', 'DATADIR')),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

# view_options = translator.TranslatorByRegex([
#     (r'volumes/VG_28xx(|/\w+)/VG_28../IMAGES', 0, (True, False, False)),
# ])

####################################################################################################################################
# FILESPEC_TO_VOLSET
####################################################################################################################################

filespec_to_volset = translator.TranslatorByRegex([
    # (r'VG_2803.*',    0, r'VG_28xx_peer_review'),
    (r'VG_28\d{2}.*', 0, r'VG_28xx'),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class VG_28xx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('VG_28xxx', re.I, 'VG_28xx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
#     VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS

pdsfile.PdsFile.FILESPEC_TO_VOLSET = filespec_to_volset + pdsfile.PdsFile.FILESPEC_TO_VOLSET

####################################################################################################################################
# OPUS_ID
####################################################################################################################################

opus_id = translator.TranslatorByRegex([
    # (r'.*/VG_28xx/VG_28(\d{2})/EASYDATA/KM0(.*)/(.*{5})(\w{2})\..*', 0, r'vg-pps-occ'),
    (r'.*/VG_28xx/VG_28(\d{2})/EASYDATA/KM0(.*)/(.*)\..*', 0, r'vg-pps-occ-\1-\3'),
    (r'.*/VG_28xx/VG_28(\d{2})/EASYDATA/(FILTER.*|KM0.*)/(.*)\..*', 0, r'vg-uvs-occ-\1-\3'),
    (r'.*/VG_28xx/VG_28(\d{2})/(S|U)_RINGS/EASYDATA/KM0.*/(.*)\..*', 0, r'vg-rss-occ-\1-\2-\3'),
    (r'.*/VG_28xx/VG_28(\d{2})/DATA/(IS\d_P....).*\..*', 0, r'vg-iss-occ-\1-\2'),
])


####################################################################################################################################
# Subclass definition
####################################################################################################################################

class VG_28xx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('VG_28xx', re.I, 'VG_28xx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    # DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    # VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    # SPLIT_RULES = split_rules + pdsfile.PdsFile.SPLIT_RULES
    #
    # OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    # OPUS_PRODUCTS = opus_products
    OPUS_ID = opus_id
    # OPUS_ID_TO_PRIMARY_LOGICAL_PATH = opus_id_to_primary_logical_path
    #
    # VIEWABLES = {
    #     'default': default_viewables,
    #     'diagram': diagrams_viewables,
    # }
    #
    # ASSOCIATIONS = pdsfile.PdsFile.ASSOCIATIONS.copy()
    # ASSOCIATIONS['volumes']  += associations_to_volumes
    # ASSOCIATIONS['previews'] += associations_to_previews
    # ASSOCIATIONS['diagrams'] += associations_to_diagrams
    # ASSOCIATIONS['metadata'] += associations_to_metadata
    #
    # VERSIONS = versions + pdsfile.PdsFile.VERSIONS

# Global attribute shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS = translator.TranslatorByRegex([(r'vg-pps-occ.*', 0, VG_28xx)]) + \
                                      translator.TranslatorByRegex([(r'vg-uvs-occ.*', 0, VG_28xx)]) + \
                                      translator.TranslatorByRegex([(r'vg-rss-occ.*', 0, VG_28xx)]) + \
                                      pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS


####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['VG_28xx'] = VG_28xx

####################################################################################################################################
