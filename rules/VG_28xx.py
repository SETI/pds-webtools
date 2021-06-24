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
# VIEWABLES
####################################################################################################################################
# TODO: NEED to add VIEWABLES later when they are available
default_viewables = translator.TranslatorByRegex([])
diagrams_viewables = translator.TranslatorByRegex([])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    # VG_2801/2802
    (r'.*/VG_28xx/(VG_28..)/EASYDATA/(?:FILTER.*|KM0.*)/(.*)\..*', 0,
            [r'volumes/VG_28xx/\1/EASYDATA/FILTER01/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER01/\2.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER02/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER02/\2.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER03/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER03/\2.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER04/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER04/\2.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER05/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER05/\2.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_1/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_1/\2.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_2/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_2/\2.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_5/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_5/\2.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM001/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM001/\2.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM002/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM002/\2.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM005/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM005/\2.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM010/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM010/\2.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM020/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM020/\2.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM050/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM050/\2.TAB',
            ]),
    # VG_2803
    (r'.*/VG_28xx/(VG_28..)/(S|U)_RINGS/EASYDATA/KM0.*/(.*)\..*', 0,
            [r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM000_2/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM000_2/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM000_5/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM000_5/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM001/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM001/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM002/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM002/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM002_5/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM002_5/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM005/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM005/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM010/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM010/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM020/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM020/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM050/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM050/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM00_025/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM00_025/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM00_05/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM00_05/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM00_1/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM00_1/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM00_2/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM00_2/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM00_5/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM00_5/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM00_25/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM00_25/\3.TAB',
            ]),
    # VG_2810
    (r'.*/VG_28xx/(VG_28..)/DATA/(IS\d_P...._...)_KM0.*\..*', 0,
            [r'volumes/VG_28xx/\1/DATA/\2_KM002.LBL',
             r'volumes/VG_28xx/\1/DATA/\2_KM002.TAB',
             r'volumes/VG_28xx/\1/DATA/\2_KM004.LBL',
             r'volumes/VG_28xx/\1/DATA/\2_KM004.TAB',
             r'volumes/VG_28xx/\1/DATA/\2_KM010.LBL',
             r'volumes/VG_28xx/\1/DATA/\2_KM010.TAB',
             r'volumes/VG_28xx/\1/DATA/\2_KM020.LBL',
             r'volumes/VG_28xx/\1/DATA/\2_KM020.TAB',
            ]),
])

# TODO: Add images later when they are available.
associations_to_previews = translator.TranslatorByRegex([])
associations_to_diagrams = translator.TranslatorByRegex([])

# TODO: Need to check the .*.tab/basename URL, currently the URL won't work in viewmaster.
associations_to_metadata = translator.TranslatorByRegex([
    (r'volumes/VG_28xx/(VG_28..)/EASYDATA/(?:FILTER.*|KM0.*)/(.*)\..*', 0,
            [r'metadata/VG_28xx/\1/\1_index.tab/\2',
             r'metadata/VG_28xx/\1/\1_profile_index.tab/\2',
             r'metadata/VG_28xx/\1/\1_supplemental_index.tab/\2',
            ]),
    (r'volumes/VG_28xx/(VG_28..)/(?:S|U)_RINGS/EASYDATA/KM0.*/(.*)\..*', 0,
            [r'metadata/VG_28xx/\1/\1_index.tab/\2',
             r'metadata/VG_28xx/\1/\1_profile_index.tab/\2',
             r'metadata/VG_28xx/\1/\1_supplemental_index.tab/\2',
            ]),
    (r'volumes/VG_28xx/(VG_28..)/DATA/(IS\d_P...._..._KM0.*)\..*', 0,
            [r'metadata/VG_28xx/\1/\1_index.tab/\2',
             r'metadata/VG_28xx/\1/\1_profile_index.tab/\2',
             r'metadata/VG_28xx/\1/\1_supplemental_index.tab/\2',
            ]),
])


####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'volumes/VG_28xx(|/\w+)/VG_28../IMAGES', 0, (True, False, False)),
])


####################################################################################################################################
# FILESPEC_TO_VOLSET
####################################################################################################################################

filespec_to_volset = translator.TranslatorByRegex([
    (r'VG_28\d{2}.*', 0, r'VG_28xx'),
])


####################################################################################################################################
# SPLIT_RULES
####################################################################################################################################

split_rules = translator.TranslatorByRegex([
    # VG_2810
    (r'(IS[12]_....._...)_(\w+)\.(.*)$', 0, (r'\1', r'_\2', r'.\3')),
])


####################################################################################################################################
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
    # VG_2801
    (r'volumes/.*/VG_2801/EASYDATA/KM000_1/(.*)\.(TAB|LBL)',  0, ('Voyager PPS', 10, 'vgpps_occ_0_1', 'Occultation Profile (0.1 km)',  True)),
    (r'volumes/.*/VG_2801/EASYDATA/KM000_2/(.*)\.(TAB|LBL)',  0, ('Voyager PPS', 20, 'vgpps_occ_0_2', 'Occultation Profile (0.2 km)',  True)),
    (r'volumes/.*/VG_2801/EASYDATA/KM000_5/(.*)\.(TAB|LBL)',  0, ('Voyager PPS', 30, 'vgpps_occ_0_5', 'Occultation Profile (0.5 km)',  True)),
    (r'volumes/.*/VG_2801/EASYDATA/KM001/(.*)\.(TAB|LBL)',    0, ('Voyager PPS', 40, 'vgpps_occ_01', 'Occultation Profile (1 km)',  True)),
    (r'volumes/.*/VG_2801/EASYDATA/KM002/(.*)\.(TAB|LBL)',    0, ('Voyager PPS', 50, 'vgpps_occ_02', 'Occultation Profile (2 km)',  True)),
    (r'volumes/.*/VG_2801/EASYDATA/KM005/(.*)\.(TAB|LBL)',    0, ('Voyager PPS', 60, 'vgpps_occ_05', 'Occultation Profile (5 km)',  True)),
    (r'volumes/.*/VG_2801/EASYDATA/KM010/(.*)\.(TAB|LBL)',    0, ('Voyager PPS', 70, 'vgpps_occ_10', 'Occultation Profile (10 km)',  True)),
    (r'volumes/.*/VG_2801/EASYDATA/KM020/(.*)\.(TAB|LBL)',    0, ('Voyager PPS', 80, 'vgpps_occ_20', 'Occultation Profile (20 km)',  True)),
    (r'volumes/.*/VG_2801/EASYDATA/KM050/(.*)\.(TAB|LBL)',    0, ('Voyager PPS', 90, 'vgpps_occ_50', 'Occultation Profile (50 km)',  True)),
    # VG_2802
    (r'volumes/.*/VG_2802/EASYDATA/FILTER01/(.*)\.(TAB|LBL)', 0, ('Voyager UVS', 10, 'vguvs_occ_full_res', 'Occultation Profile (full resolution)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/FILTER02/(.*)\.(TAB|LBL)', 0, ('Voyager UVS', 20, 'vguvs_occ_sampled_2', 'Occultation Profile (1/2 resolution)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/FILTER03/(.*)\.(TAB|LBL)', 0, ('Voyager UVS', 30, 'vguvs_occ_sampled_3', 'Occultation Profile (1/3 resolution)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/FILTER04/(.*)\.(TAB|LBL)', 0, ('Voyager UVS', 40, 'vguvs_occ_sampled_4', 'Occultation Profile (1/4 resolution)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/FILTER05/(.*)\.(TAB|LBL)', 0, ('Voyager UVS', 50, 'vguvs_occ_sampled_5', 'Occultation Profile (1/5 resolution)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/KM000_2/(.*)\.(TAB|LBL)',  0, ('Voyager UVS', 60, 'vguvs_occ_0_2', 'Occultation Profile (0.2 km)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/KM000_5/(.*)\.(TAB|LBL)',  0, ('Voyager UVS', 70, 'vguvs_occ_0_5', 'Occultation Profile (0.5 km)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/KM001/(.*)\.(TAB|LBL)',    0, ('Voyager UVS', 80, 'vguvs_occ_01', 'Occultation Profile (1 km)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/KM002/(.*)\.(TAB|LBL)',    0, ('Voyager UVS', 90, 'vguvs_occ_02', 'Occultation Profile (2 km)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/KM005/(.*)\.(TAB|LBL)',    0, ('Voyager UVS', 100, 'vguvs_occ_05', 'Occultation Profile (5 km)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/KM010/(.*)\.(TAB|LBL)',    0, ('Voyager UVS', 110, 'vguvs_occ_10', 'Occultation Profile (10 km)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/KM020/(.*)\.(TAB|LBL)',    0, ('Voyager UVS', 120, 'vguvs_occ_20', 'Occultation Profile (20 km)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/KM050/(.*)\.(TAB|LBL)',    0, ('Voyager UVS', 130, 'vguvs_occ_50', 'Occultation Profile (50 km)',  True)),
    # VG_2803
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM000_2/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 10, 'vgrss_occ_0_2', 'Occultation Profile (0.4 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM000_5/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 20, 'vgrss_occ_0_5', 'Occultation Profile (1 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM001/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 30, 'vgrss_occ_01', 'Occultation Profile (2 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM002/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 40, 'vgrss_occ_02', 'Occultation Profile (4 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM002_5/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 50, 'vgrss_occ_02_5', 'Occultation Profile (5 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM005/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 60, 'vgrss_occ_05', 'Occultation Profile (10 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM010/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 70, 'vgrss_occ_10', 'Occultation Profile (20 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM020/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 80, 'vgrss_occ_20', 'Occultation Profile (40 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM050/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 90, 'vgrss_occ_50', 'Occultation Profile (100 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM00_025/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 10, 'vgrss_occ_0_025', 'Occultation Profile (0.05 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM00_05/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 20, 'vgrss_occ_0_05', 'Occultation Profile (0.1 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM00_1/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 30, 'vgrss_occ_0_1', 'Occultation Profile (0.2 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM00_2/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 40, 'vgrss_occ_0_2', 'Occultation Profile (0.4 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM00_25/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 50, 'vgrss_occ_0_25', 'Occultation Profile (0.5 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM00_5/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 60, 'vgrss_occ_0_5', 'Occultation Profile (1 km)',  True)),
    # VG_2810
    (r'volumes/.*/VG_2810/DATA/.*KM002\.(TAB|LBL)',  0, ('Voyager ISS', 10, 'vgiss_prof_02', 'Intensity Profile (2 km)',  True)),
    (r'volumes/.*/VG_2810/DATA/.*KM004\.(TAB|LBL)',  0, ('Voyager ISS', 10, 'vgiss_prof_04', 'Intensity Profile (4 km)',  True)),
    (r'volumes/.*/VG_2810/DATA/.*KM010\.(TAB|LBL)',  0, ('Voyager ISS', 10, 'vgiss_prof_10', 'Intensity Profile (10 km)',  True)),
    (r'volumes/.*/VG_2810/DATA/.*KM020\.(TAB|LBL)',  0, ('Voyager ISS', 10, 'vgiss_prof_20', 'Intensity Profile (20 km)',  True)),
])


####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################
# Use of explicit file names means we don't need to invoke glob.glob(); this goes much faster
# TODO: Need to add images when they are available
opus_products = translator.TranslatorByRegex([
    # VG_2801/2802
    (r'.*/VG_28xx/(VG_28..)/EASYDATA/(?:FILTER.*|KM0.*)/(.*)\..*', 0,
            [r'volumes/VG_28xx/\1/EASYDATA/FILTER01/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER01/\2.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER02/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER02/\2.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER03/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER03/\2.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER04/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER04/\2.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER05/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER05/\2.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_1/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_1/\2.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_2/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_2/\2.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_5/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_5/\2.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM001/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM001/\2.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM002/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM002/\2.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM005/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM005/\2.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM010/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM010/\2.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM020/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM020/\2.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM050/\2.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM050/\2.TAB',
             r'metadata/VG_28xx/\1/\1_index.lbl',
             r'metadata/VG_28xx/\1/\1_index.tab',
             r'metadata/VG_28xx/\1/\1_profile_index.lbl',
             r'metadata/VG_28xx/\1/\1_profile_index.tab',
             r'metadata/VG_28xx/\1/\1_supplemental_index.lbl',
             r'metadata/VG_28xx/\1/\1_supplemental_index.tab',
            ]),
    # VG_2803
    (r'.*/VG_28xx/(VG_28..)/(S|U)_RINGS/EASYDATA/KM0.*/(.*)\..*', 0,
            [r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM000_2/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM000_2/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM000_5/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM000_5/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM001/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM001/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM002/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM002/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM002_5/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM002_5/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM005/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM005/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM010/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM010/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM020/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM020/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM050/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM050/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM00_025/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM00_025/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM00_05/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM00_05/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM00_1/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM00_1/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM00_2/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM00_2/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM00_5/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM00_5/\3.TAB',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM00_25/\3.LBL',
             r'volumes/VG_28xx/\1/\2_RINGS/EASYDATA/KM00_25/\3.TAB',
             r'metadata/VG_28xx/\1/\1_index.lbl',
             r'metadata/VG_28xx/\1/\1_index.tab',
             r'metadata/VG_28xx/\1/\1_profile_index.lbl',
             r'metadata/VG_28xx/\1/\1_profile_index.tab',
             r'metadata/VG_28xx/\1/\1_supplemental_index.lbl',
             r'metadata/VG_28xx/\1/\1_supplemental_index.tab',
            ]),
    # VG_2810
    (r'.*/VG_28xx/(VG_28..)/DATA/(IS\d_P...._...)_KM0.*\..*', 0,
            [r'volumes/VG_28xx/\1/DATA/\2_KM002.LBL',
             r'volumes/VG_28xx/\1/DATA/\2_KM002.TAB',
             r'volumes/VG_28xx/\1/DATA/\2_KM004.LBL',
             r'volumes/VG_28xx/\1/DATA/\2_KM004.TAB',
             r'volumes/VG_28xx/\1/DATA/\2_KM010.LBL',
             r'volumes/VG_28xx/\1/DATA/\2_KM010.TAB',
             r'volumes/VG_28xx/\1/DATA/\2_KM020.LBL',
             r'volumes/VG_28xx/\1/DATA/\2_KM020.TAB',
             r'metadata/VG_28xx/\1/\1_index.lbl',
             r'metadata/VG_28xx/\1/\1_index.tab',
             r'metadata/VG_28xx/\1/\1_profile_index.lbl',
             r'metadata/VG_28xx/\1/\1_profile_index.tab',
             r'metadata/VG_28xx/\1/\1_supplemental_index.lbl',
             r'metadata/VG_28xx/\1/\1_supplemental_index.tab',
            ]),
])


####################################################################################################################################
# OPUS_ID
####################################################################################################################################

opus_id = translator.TranslatorByRegex([
    (r'.*/VG_28xx/VG_28(\d{2})/EASYDATA/KM0(.*)/(.*)\..*', 0, r'vg-pps-occ-\1-\3'),
    (r'.*/VG_28xx/VG_28(\d{2})/EASYDATA/(FILTER.*|KM0.*)/(.*)\..*', 0, r'vg-uvs-occ-\1-\3'),
    (r'.*/VG_28xx/VG_28(\d{2})/(S|U)_RINGS/EASYDATA/KM0.*/(.*)\..*', 0, r'vg-rss-occ-\1-\2-\3'),
    (r'.*/VG_28xx/VG_28(\d{2})/DATA/(IS\d_P....).*\..*', 0, r'vg-iss-prof-\1-\2'),
])


####################################################################################################################################
# OPUS_ID_TO_PRIMARY_LOGICAL_PATH
####################################################################################################################################
#
# opus_id_to_primary_logical_path = translator.TranslatorByRegex([
#     (r'co-uvis-occ-(....)-(...)-(.*)-([ie])', 0,  r'volumes/COUVIS_8xxx/COUVIS_8001/data/#UPPER#UVIS_HSP_\1_\2_\3_\4_TAU01KM.TAB'),
# ])


####################################################################################################################################
# Subclass definition
####################################################################################################################################

class VG_28xx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('VG_28xx', re.I, 'VG_28xx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    SPLIT_RULES = split_rules + pdsfile.PdsFile.SPLIT_RULES
    #
    OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    OPUS_PRODUCTS = opus_products
    OPUS_ID = opus_id
    # OPUS_ID_TO_PRIMARY_LOGICAL_PATH = opus_id_to_primary_logical_path

    VIEWABLES = {
        'default': default_viewables,
        'diagram': diagrams_viewables,
    }

    ASSOCIATIONS = pdsfile.PdsFile.ASSOCIATIONS.copy()
    ASSOCIATIONS['volumes']  += associations_to_volumes
    ASSOCIATIONS['previews'] += associations_to_previews
    ASSOCIATIONS['diagrams'] += associations_to_diagrams
    ASSOCIATIONS['metadata'] += associations_to_metadata

pdsfile.PdsFile.FILESPEC_TO_VOLSET = filespec_to_volset + pdsfile.PdsFile.FILESPEC_TO_VOLSET

# Global attribute shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS = translator.TranslatorByRegex([(r'vg-pps-occ.*', 0, VG_28xx)]) + \
                                      translator.TranslatorByRegex([(r'vg-uvs-occ.*', 0, VG_28xx)]) + \
                                      translator.TranslatorByRegex([(r'vg-rss-occ.*', 0, VG_28xx)]) + \
                                      translator.TranslatorByRegex([(r'vg-iss-occ.*', 0, VG_28xx)]) + \
                                      pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS


####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['VG_28xx'] = VG_28xx

####################################################################################################################################
