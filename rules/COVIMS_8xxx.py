####################################################################################################################################
# rules/COVIMS_8xxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/.*_TAU_01KM\.TAB', 0, ('Occultation Profile (1 km)',  'SERIES')),
    (r'volumes/.*_TAU_10KM\.TAB', 0, ('Occultation Profile (10 km)', 'SERIES')),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'volumes/COVIMS_8xxx(|_v[0-9\.]+)/(COVIMS_8...)/(data|EASYDATA)/(\w+)_TAU_\d+KM\.(TAB|LBL)', 0,
            [r'previews/COVIMS_8xxx/\2/data/\4_TAU_full.jpg',
             r'previews/COVIMS_8xxx/\2/data/\4_TAU_med.jpg',
             r'previews/COVIMS_8xxx/\2/data/\4_TAU_small.jpg',
             r'previews/COVIMS_8xxx/\2/data/\4_TAU_thumb.jpg',
            ]),
    (r'volumes/COVIMS_8xxx(|_v[0-9\.]+)/(COVIMS_8.../browse/.\w_+)\.(PDF|LBL)', 0,
            [r'previews/COVIMS_8xxx/\2_full.jpg',
             r'previews/COVIMS_8xxx/\2_med.jpg',
             r'previews/COVIMS_8xxx/\2_small.jpg',
             r'previews/COVIMS_8xxx/\2_thumb.jpg',
            ]),
])

diagrams_viewables = translator.TranslatorByRegex([
    (r'volumes/COVIMS_8xxx(|_v[0-9\.]+)/(COVIMS_8...)/(data|EASYDATA)/(\w+)_TAU_\d+KM\.(TAB|LBL)', 0,
            [r'diagrams/COVIMS_8xxx/\2/data/\4_full.jpg',
             r'diagrams/COVIMS_8xxx/\2/data/\4_med.jpg',
             r'diagrams/COVIMS_8xxx/\2/data/\4_small.jpg',
             r'previews/COVIMS_8xxx/\2/data/\4_thumb.jpg',
            ]),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    (r'.*/COVIMS_8xxx(|_v[0-9\.]+)/(COVIMS_8...)/(data|browse)', 0,
            [r'volumes/COVIMS_8xxx\1/\2/data',
             r'volumes/COVIMS_8xxx\1/\2/browse',
            ]),
    (r'.*/COVIMS_8xxx(|_v[0-9\.]+)/(COVIMS_8...)/(data|browse|EASYDATA)/(VIMS_.*)_(TAU.*|[a-z]\.jpg)', 0,
            [r'volumes/COVIMS_8xxx\1/\2/data/\4_TAU_01KM.LBL',
             r'volumes/COVIMS_8xxx\1/\2/data/\4_TAU_01KM.TAB',
             r'volumes/COVIMS_8xxx\1/\2/data/\4_TAU_10KM.LBL',
             r'volumes/COVIMS_8xxx\1/\2/data/\4_TAU_10KM.TAB',
             r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_GEOMETRY_full.jpg',
             r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_GEOMETRY_med.jpg',
             r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_GEOMETRY_small.jpg',
             r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_GEOMETRY_thumb.jpg',
             r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_LIGHTCURVE_full.jpg',
             r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_LIGHTCURVE_med.jpg',
             r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_LIGHTCURVE_small.jpg',
             r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_LIGHTCURVE_thumb.jpg',
             r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_NPOLE_full.jpg',
             r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_NPOLE_med.jpg',
             r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_NPOLE_small.jpg',
             r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_NPOLE_thumb.jpg',
             r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_STAR_full.jpg',
             r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_STAR_med.jpg',
             r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_STAR_small.jpg',
             r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_STAR_thumb.jpg',
            ]),
    (r'volumes/COVIMS_8xxx_v1/COVIMS_8001/EASYDATA', 0,
            [r'volumes/COVIMS_8xxx/COVIMS_8001/data',
             r'volumes/COVIMS_8xxx/COVIMS_8001/browse',
            ]),
    (r'documents/COVIMS_8xxx.*', 0,
            r'volumes/COVIMS_8xxx'),
])

associations_to_previews = translator.TranslatorByRegex([
    (r'.*/COVIMS_8xxx(|_v[0-9\.]+)/(COVIMS_8...)/(data|browse|EASYDATA)', 0,
            [r'previews/COVIMS_8xxx/\2/data',
             r'previews/COVIMS_8xxx/\2/browse',
            ]),
    (r'.*/COVIMS_8xxx(|_v[0-9\.]+)/(COVIMS_8...)/(data|browse|EASYDATA)/(VIMS_.*)_(TAU.*|[a-z]\.jpg)', 0,
            [r'previews/COVIMS_8xxx/\2/data/\4_TAU_full.jpg',
             r'previews/COVIMS_8xxx/\2/data/\4_TAU_med.jpg',
             r'previews/COVIMS_8xxx/\2/data/\4_TAU_small.jpg',
             r'previews/COVIMS_8xxx/\2/data/\4_TAU_thumb.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_GEOMETRY_full.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_GEOMETRY_med.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_GEOMETRY_small.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_GEOMETRY_thumb.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_LIGHTCURVE_full.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_LIGHTCURVE_med.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_LIGHTCURVE_small.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_LIGHTCURVE_thumb.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_NPOLE_full.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_NPOLE_med.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_NPOLE_small.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_NPOLE_thumb.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_STAR_full.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_STAR_med.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_STAR_small.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_STAR_thumb.jpg',
           ]),
])

associations_to_diagrams = translator.TranslatorByRegex([
    (r'.*/COVIMS_8xxx(|_v[0-9\.]+)/(COVIMS_8...)/(data|browse|EASYDATA)', 0,
            r'diagrams/COVIMS_8xxx/\2/data'),
    (r'.*/COVIMS_8xxx(|_v[0-9\.]+)/(COVIMS_8...)/(data|EASYDATA)/(VIMS_.*)_(TAU.*|[a-z]\.jpg)', 0,
            [r'diagrams/COVIMS_8xxx/\2/data/\3_full.jpg',
             r'diagrams/COVIMS_8xxx/\2/data/\3_med.jpg',
             r'diagrams/COVIMS_8xxx/\2/data/\3_small.jpg',
             r'diagrams/COVIMS_8xxx/\2/data/\3_thumb.jpg',
            ]),
])

associations_to_metadata = translator.TranslatorByRegex([
    (r'volumes/COVIMS_8xxx(|_v[0-9\.]+)/(COVIMS_8...)/data/(VIMS_.*)_(TAU_\d+KM)\..*', 0,
            [r'metadata/COVIMS_8xxx/\2/\2_index.tab/\3_\4',
             r'metadata/COVIMS_8xxx/\2/\2_profile_index.tab/\3_TAU01',
             r'metadata/COVIMS_8xxx/\2/\2_supplemental_index.tab/\3_TAU01',
            ]),
])

associations_to_documents = translator.TranslatorByRegex([
        (r'volumes/COVIMS_8xxx.*', 0,
                r'documents/COVIMS_8xxx/*'),
])

####################################################################################################################################
# VERSIONS
####################################################################################################################################

# _v1 had upper case file names and used "EASYDATA" in place of "data"
# Case conversions are inconsistent, sometimes mixed case file names are unchanged
versions = translator.TranslatorByRegex([
    (r'volumes/COVIMS_8xxx(|_v[0-9\.]+)/(COVIMS_8...)/(data|EASYDATA)(|/.*)', 0,
            [r'volumes/COVIMS_8xxx*/\2/data\4',
             r'volumes/COVIMS_8xxx_v1/\2/EASYDATA\4',
            ]),
    (r'volumes/COVIMS_8xxx(|_v[0-9\.]+)/(COVIMS_8...)/(\w+)(|/.*)', 0,
            [r'volumes/COVIMS_8xxx*/\2/#LOWER#\3\4',
             r'volumes/COVIMS_8xxx*/\2/#LOWER#\3#MIXED#\4',
             r'volumes/COVIMS_8xxx_v1/\2/#UPPER#\3\4',
             r'volumes/COVIMS_8xxx_v1/\2/#UPPER#\3#MIXED#\4',
            ]),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|previews|diagrams)/COVIMS_8xxx.*/COVIMS_8.../(data|browse|EASYDATA)', 0, (True, False, False)),
])

####################################################################################################################################
# SPLIT_RULES
####################################################################################################################################

split_rules = translator.TranslatorByRegex([
    (r'(VIMS_...._..._\w+_[IE])_(TAU_\d\w+)\.(.*)', 0, (r'\1', r'_\2', r'.\3')),
])

####################################################################################################################################
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
    (r'volumes/.*_TAU_01KM\.(TAB|LBL)', 0, ('Cassini VIMS', 10, 'covims_occ_01', 'Occultation Profile (1 km)',  True)),
    (r'volumes/.*_TAU_10KM\.(TAB|LBL)', 0, ('Cassini VIMS', 20, 'covims_occ_10', 'Occultation Profile (10 km)', True)),
    # Documentation
    (r'documents/COVIMS_8xxx/.*',       0, ('Cassini VIMS', 30, 'covims_occ_documentation', 'Documentation', False)),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

# Use of explicit file names means we don't need to invoke glob.glob(); this goes much faster
opus_products = translator.TranslatorByRegex([
    (r'.*/COVIMS_8xxx(|_v[0-9\.]+)/(COVIMS_....)/(data|EASYDATA)/(VIMS_.*)_(TAU.*|[a-z]+)\..*', 0,
            [r'volumes/COVIMS_8xxx*/\2/data/\4_TAU_01KM.LBL',
             r'volumes/COVIMS_8xxx*/\2/data/\4_TAU_01KM.TAB',
             r'volumes/COVIMS_8xxx*/\2/data/\4_TAU_10KM.LBL',
             r'volumes/COVIMS_8xxx*/\2/data/\4_TAU_10KM.TAB',
             r'volumes/COVIMS_8xxx_v1/\2/EASYDATA/\4_TAU_01KM.LBL',
             r'volumes/COVIMS_8xxx_v1/\2/EASYDATA/\4_TAU_01KM.TAB',
             r'volumes/COVIMS_8xxx_v1/\2/EASYDATA/\4_TAU_10KM.LBL',
             r'volumes/COVIMS_8xxx_v1/\2/EASYDATA/\4_TAU_10KM.TAB',
             r'previews/COVIMS_8xxx/\2/data/\4_TAU_full.jpg',
             r'previews/COVIMS_8xxx/\2/data/\4_TAU_med.jpg',
             r'previews/COVIMS_8xxx/\2/data/\4_TAU_small.jpg',
             r'previews/COVIMS_8xxx/\2/data/\4_TAU_thumb.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_GEOMETRY_full.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_GEOMETRY_med.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_GEOMETRY_small.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_GEOMETRY_thumb.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_LIGHTCURVE_full.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_LIGHTCURVE_med.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_LIGHTCURVE_small.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_LIGHTCURVE_thumb.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_NPOLE_full.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_NPOLE_med.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_NPOLE_small.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_NPOLE_thumb.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_STAR_full.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_STAR_med.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_STAR_small.jpg',
             r'previews/COVIMS_8xxx/\2/browse/\4_TAU_STAR_thumb.jpg',
             r'diagrams/COVIMS_8xxx/\2/data/\4_full.jpg',
             r'diagrams/COVIMS_8xxx/\2/data/\4_med.jpg',
             r'diagrams/COVIMS_8xxx/\2/data/\4_small.jpg',
             r'diagrams/COVIMS_8xxx/\2/data/\4_thumb.jpg',
             r'metadata/COVIMS_8xxx/\2/\2_index.lbl',
             r'metadata/COVIMS_8xxx/\2/\2_index.tab',
             r'metadata/COVIMS_8xxx/\2/\2_profile_index.lbl',
             r'metadata/COVIMS_8xxx/\2/\2_profile_index.tab',
             r'metadata/COVIMS_8xxx/\2/\2_supplemental_index.lbl',
             r'metadata/COVIMS_8xxx/\2/\2_supplemental_index.tab',
            ]),
])

####################################################################################################################################
# OPUS_ID
####################################################################################################################################

opus_id = translator.TranslatorByRegex([
    (r'.*/COVIMS_8xxx.*/(data|EASYDATA)/VIMS_(\d{4})_(\d{3})_(\w+)_([IE]).*', 0, r'co-vims-occ-#LOWER#\2-\3-\4-\5'),
])

####################################################################################################################################
# OPUS_ID_TO_PRIMARY_LOGICAL_PATH
####################################################################################################################################

opus_id_to_primary_logical_path = translator.TranslatorByRegex([
    (r'co-vims-occ-(....)-(...)-(.*)-([ie])', 0,  r'volumes/COVIMS_8xxx/COVIMS_8001/data/#UPPER#VIMS_\1_\2_\3_\4_TAU_01KM.TAB'),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class COVIMS_8xxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('COVIMS_8xxx', re.I, 'COVIMS_8xxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    SPLIT_RULES = split_rules + pdsfile.PdsFile.SPLIT_RULES

    OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    OPUS_PRODUCTS = opus_products + pdsfile.PdsFile.OPUS_PRODUCTS
    OPUS_ID = opus_id
    OPUS_ID_TO_PRIMARY_LOGICAL_PATH = opus_id_to_primary_logical_path

    VIEWABLES = {
        'default': default_viewables,
        'diagram': diagrams_viewables,
    }

    ASSOCIATIONS = pdsfile.PdsFile.ASSOCIATIONS.copy()
    ASSOCIATIONS['volumes']  += associations_to_volumes
    ASSOCIATIONS['previews'] += associations_to_previews
    ASSOCIATIONS['diagrams'] += associations_to_diagrams
    ASSOCIATIONS['metadata'] += associations_to_metadata
    ASSOCIATIONS['documents'] = associations_to_documents

    VERSIONS = versions + pdsfile.PdsFile.VERSIONS

# Global attribute shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS = translator.TranslatorByRegex([(r'co-vims-occ-.*', 0, COVIMS_8xxx)]) + \
                                      pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['COVIMS_8xxx'] = COVIMS_8xxx

####################################################################################################################################
# Unit tests
####################################################################################################################################

import pytest
from .pytest_support import *

@pytest.mark.parametrize(
    'input_path,expected',
    [
        ('volumes/COVIMS_8xxx/COVIMS_8001/data/VIMS_2005_144_OMICET_E_TAU_01KM.TAB',
        {('Cassini VIMS',
          10,
          'covims_occ_01',
          'Occultation Profile (1 km)',
          True): ['volumes/COVIMS_8xxx/COVIMS_8001/data/VIMS_2005_144_OMICET_E_TAU_01KM.TAB',
                  'volumes/COVIMS_8xxx/COVIMS_8001/data/VIMS_2005_144_OMICET_E_TAU_01KM.LBL',
                  'volumes/COVIMS_8xxx_v2.0/COVIMS_8001/data/VIMS_2005_144_OMICET_E_TAU_01KM.TAB',
                  'volumes/COVIMS_8xxx_v2.0/COVIMS_8001/data/VIMS_2005_144_OMICET_E_TAU_01KM.LBL',
                  'volumes/COVIMS_8xxx_v1/COVIMS_8001/EASYDATA/VIMS_2005_144_OMICET_E_TAU_01KM.TAB',
                  'volumes/COVIMS_8xxx_v1/COVIMS_8001/EASYDATA/VIMS_2005_144_OMICET_E_TAU_01KM.LBL'],
         ('Cassini VIMS',
          20,
          'covims_occ_10',
          'Occultation Profile (10 km)',
          True): ['volumes/COVIMS_8xxx/COVIMS_8001/data/VIMS_2005_144_OMICET_E_TAU_10KM.TAB',
                  'volumes/COVIMS_8xxx/COVIMS_8001/data/VIMS_2005_144_OMICET_E_TAU_10KM.LBL',
                  'volumes/COVIMS_8xxx_v2.0/COVIMS_8001/data/VIMS_2005_144_OMICET_E_TAU_10KM.TAB',
                  'volumes/COVIMS_8xxx_v2.0/COVIMS_8001/data/VIMS_2005_144_OMICET_E_TAU_10KM.LBL',
                  'volumes/COVIMS_8xxx_v1/COVIMS_8001/EASYDATA/VIMS_2005_144_OMICET_E_TAU_10KM.TAB',
                  'volumes/COVIMS_8xxx_v1/COVIMS_8001/EASYDATA/VIMS_2005_144_OMICET_E_TAU_10KM.LBL'],
         ('browse',
          40,
          'browse_full',
          'Browse Image (full)',
          True): ['previews/COVIMS_8xxx/COVIMS_8001/data/VIMS_2005_144_OMICET_E_TAU_full.jpg',
                  'previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_STAR_full.jpg',
                  'previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_NPOLE_full.jpg',
                  'previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_LIGHTCURVE_full.jpg',
                  'previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_GEOMETRY_full.jpg'],
         ('browse',
          30,
          'browse_medium',
          'Browse Image (medium)',
          False): ['previews/COVIMS_8xxx/COVIMS_8001/data/VIMS_2005_144_OMICET_E_TAU_med.jpg',
                   'previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_STAR_med.jpg',
                   'previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_NPOLE_med.jpg',
                   'previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_LIGHTCURVE_med.jpg', 'previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_GEOMETRY_med.jpg'],
         ('browse',
          20,
          'browse_small',
          'Browse Image (small)',
          False): ['previews/COVIMS_8xxx/COVIMS_8001/data/VIMS_2005_144_OMICET_E_TAU_small.jpg',
                   'previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_STAR_small.jpg',
                   'previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_NPOLE_small.jpg',
                   'previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_LIGHTCURVE_small.jpg', 'previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_GEOMETRY_small.jpg'],
         ('browse',
          10,
          'browse_thumb',
          'Browse Image (thumbnail)',
          False): ['previews/COVIMS_8xxx/COVIMS_8001/data/VIMS_2005_144_OMICET_E_TAU_thumb.jpg',
                   'previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_STAR_thumb.jpg',
                   'previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_NPOLE_thumb.jpg',
                   'previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_LIGHTCURVE_thumb.jpg', 'previews/COVIMS_8xxx/COVIMS_8001/browse/VIMS_2005_144_OMICET_E_TAU_GEOMETRY_thumb.jpg'],
         ('diagram',
          40,
          'diagram_full',
          'Browse Diagram (full)',
          True): ['diagrams/COVIMS_8xxx/COVIMS_8001/data/VIMS_2005_144_OMICET_E_full.jpg'],
         ('diagram',
          30,
          'diagram_medium',
          'Browse Diagram (medium)',
          False): ['diagrams/COVIMS_8xxx/COVIMS_8001/data/VIMS_2005_144_OMICET_E_med.jpg'],
         ('diagram',
          20,
          'diagram_small',
          'Browse Diagram (small)',
          False): ['diagrams/COVIMS_8xxx/COVIMS_8001/data/VIMS_2005_144_OMICET_E_small.jpg'],
         ('diagram',
          10,
          'diagram_thumb',
          'Browse Diagram (thumbnail)',
          False): ['diagrams/COVIMS_8xxx/COVIMS_8001/data/VIMS_2005_144_OMICET_E_thumb.jpg'],
         ('metadata',
          5,
          'rms_index',
          'RMS Node Augmented Index',
          False): ['metadata/COVIMS_8xxx/COVIMS_8001/COVIMS_8001_index.tab',
                   'metadata/COVIMS_8xxx/COVIMS_8001/COVIMS_8001_index.lbl'],
         ('metadata',
          8,
          'profile_index',
          'Profile Index',
          False): ['metadata/COVIMS_8xxx/COVIMS_8001/COVIMS_8001_profile_index.tab',
                   'metadata/COVIMS_8xxx/COVIMS_8001/COVIMS_8001_profile_index.lbl'],
         ('metadata',
          9,
          'supplemental_index',
          'Supplemental Index',
          False): ['metadata/COVIMS_8xxx/COVIMS_8001/COVIMS_8001_supplemental_index.tab',
                   'metadata/COVIMS_8xxx/COVIMS_8001/COVIMS_8001_supplemental_index.lbl'],
         ('Cassini VIMS',
          30,
          'covims_occ_documentation',
          'Documentation',
          False): ['documents/COVIMS_8xxx/VIMS-ring-occultations-summary.pdf',
                   'documents/COVIMS_8xxx/Cassini-VIMS-Final-Report.pdf']}
        ),
    ]
)
def test_opus_products(input_path, expected):
    opus_products_test(input_path, expected)

def test_opus_id_to_primary_logical_path():
    TESTS = [
        'volumes/COVIMS_8xxx/COVIMS_8001/data/VIMS_2005_144_OMICET_E_TAU_01KM.TAB',
    ]

    for logical_path in TESTS:
        test_pdsf = pdsfile.PdsFile.from_logical_path(logical_path)
        opus_id = test_pdsf.opus_id
        opus_id_pdsf = pdsfile.PdsFile.from_opus_id(opus_id)
        assert opus_id_pdsf.logical_path == logical_path

        # Gather all the associated OPUS products
        product_dict = test_pdsf.opus_products()
        product_pdsfiles = []
        for pdsf_lists in product_dict.values():
            for pdsf_list in pdsf_lists:
                product_pdsfiles += pdsf_list

        # Filter out the metadata/documents products and format files
        product_pdsfiles = [pdsf for pdsf in product_pdsfiles
                                 if pdsf.voltype_ != 'metadata/'
                                 and pdsf.voltype_ != 'documents/']
        product_pdsfiles = [pdsf for pdsf in product_pdsfiles
                                 if pdsf.extension.lower() != '.fmt']

        # Gather the set of absolute paths
        opus_id_abspaths = set()
        for pdsf in product_pdsfiles:
            opus_id_abspaths.add(pdsf.abspath)

        for pdsf in product_pdsfiles:
            # Every version is in the product set
            for version_pdsf in pdsf.all_versions().values():
                assert version_pdsf.abspath in opus_id_abspaths

            # Every viewset is in the product set
            for viewset in pdsf.all_viewsets.values():
                for viewable in viewset.viewables:
                    assert viewable.abspath in opus_id_abspaths

            # Every associated product is in the product set except metadata
            for category in ('volumes', 'previews', 'diagrams'):
                for abspath in pdsf.associated_abspaths(category):
                    if '.' not in os.path.basename(abspath): continue   # skip dirs
                    assert abspath in opus_id_abspaths

####################################################################################################################################
