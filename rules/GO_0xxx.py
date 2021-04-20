####################################################################################################################################
# rules/GO_0xxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/\w+/\w+(|/REDO)/[CEGIJ][0-9]{1,2}',               re.I, ('Images grouped by orbit',        'IMAGEDIR')),
    (r'volumes/\w+/\w+(|/REDO)/[CEGIJ][0-9]{1,2}/\w+',           re.I, ('Images grouped by target',       'IMAGEDIR')),
    (r'volumes/\w+/\w+(|/REDO)/[CEGIJ][0-9]{1,2}/\w+/C[0-9]{6}', re.I, ('Images grouped by SC clock',     'IMAGEDIR')),
    (r'volumes/\w+/\w+/REDO',                                    re.I, ('Redone images grouped by orbit', 'IMAGEDIR')),
    (r'volumes/.*\.IMG',                                         re.I, ('Raw image, VICAR',               'IMAGE'   )),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'.*\.lbl',  re.I, ''),
    (r'volumes/(.*/C[0-9]{10}[A-Z])\.(IMG|LBL)', 0,
            [r'previews/\1_full.jpg',
             r'previews/\1_med.jpg',
             r'previews/\1_small.jpg',
             r'previews/\1_thumb.jpg',
            ]),
    (r'volumes/(GO_0xxx_v1/.*/C[0-9]{6}/.*)\.(IMG|LBL)', 0,
            [r'previews/\1_full.jpg',
             r'previews/\1_med.jpg',
             r'previews/\1_small.jpg',
             r'previews/\1_thumb.jpg',
            ]),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    (r'.*/(GO_0xxx/GO_..../.*/C[0-9]{10}[A-Z]).*', 0,
            [r'volumes/\1.IMG',
             r'volumes/\1.LBL',
            ]),
    (r'.*/GO_0xxx_v1/(GO_..../.*/C[0-9]{6})/([0-9]{4}[A-Z]).*', 0,
            [r'volumes/GO_0xxx_v1/\1/\2.IMG',
             r'volumes/GO_0xxx_v1/\1/\2.LBL',
             r'volumes/GO_0xxx/\1\2.IMG',
             r'volumes/GO_0xxx/\1\2.LBL'
            ]),
    (r'.*/previews/(GO_0..._v1/.*)_[a-z]+\.jpg', 0,
            [r'volumes/\1.IMG',
             r'volumes/\1.LBL',
            ]),
    (r'.*/metadata/GO_0xxx/GO_0999.*', 0,
            r'volumes/GO_0xxx'),
    (r'.*/metadata/GO_0xxx_v1/GO_0999.*', 0,
            r'volumes/GO_0xxx_v1'),
])

associations_to_previews = translator.TranslatorByRegex([
    (r'.*/(GO_0xxx/GO_..../.*/C[0-9]{10}[A-Z]).*', 0,
            [r'previews/\1_full.jpg',
             r'previews/\1_med.jpg',
             r'previews/\1_small.jpg',
             r'previews/\1_thumb.jpg',
            ]),
    (r'.*/GO_0xxx_v1/(GO_..../.*/C[0-9]{6})/([0-9]{4}[A-Z]).*', 0,
            [r'previews/GO_0xxx_v1/\1/\2_full.jpg',
             r'previews/GO_0xxx_v1/\1/\2_med.jpg',
             r'previews/GO_0xxx_v1/\1/\2_small.jpg',
             r'previews/GO_0xxx_v1/\1/\2_thumb.jpg',
             r'previews/GO_0xxx/\1\2_full.jpg',
             r'previews/GO_0xxx/\1\2_med.jpg',
             r'previews/GO_0xxx/\1\2_small.jpg',
             r'previews/GO_0xxx/\1\2_thumb.jpg',
            ]),
    (r'.*/metadata/GO_0xxx/GO_0999.*', 0,
            r'previews/GO_0xxx'),
    (r'.*/metadata/GO_0xxx_v1/GO_0999.*', 0,
            r'previews/GO_0xxx_v1'),
])

associations_to_metadata = translator.TranslatorByRegex([
    (r'volumes/(GO_0xxx)/(GO_....)/.*/(C[0-9]{10})[A-Z].*', 0,
            r'metadata/\1/\2/\2_index.tab/\3'),
    (r'volumes/(GO_0xxx_v1)/(GO_....).*', 0,
            r'metadata/\1/\2'),
    (r'metadata/GO_0xxx(|_v[\d\.]+)/GO_00..', 0,
            r'metadata/GO_0xxx/GO_0999'),
    (r'metadata/GO_0xxx(|_v[\d\.]+)/GO_00../GO_00.._(.*)\..*', 0,
            [r'metadata/GO_0xxx/GO_0999/GO_0999_\2.tab',
             r'metadata/GO_0xxx/GO_0999/GO_0999_\2.lbl',
            ]),
])

####################################################################################################################################
# VERSIONS
####################################################################################################################################

# File names are split in _v1, merged afterward
versions = translator.TranslatorByRegex([
    (r'volumes/GO_0xxx.*/(GO_0.../.*/C\d{6})/?(\d{4}[A-Z]\..*)', 0,
            [r'volumes/GO_0xxx/\1\2',
             r'volumes/GO_0xxx_v1/\1/\2',
            ]),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|previews)/GO_0xxx/GO_....(|/BROWSE)/([CEGIJ][0-9]{1,2}|REDO)/.*',               0, (True, True, True)),

    (r'(volumes|previews)/GO_0xxx_v1/GO_....(|/BROWSE)/([CEGIJ][0-9]{1,2}|REDO)/.*/C[0-9]{6}',  0, (True, True, False)),
    (r'(volumes|previews)/GO_0xxx_v1/GO_....(|/BROWSE)/([CEGIJ][0-9]{1,2}|REDO)/.*',            0, (True, True, True)),
])

####################################################################################################################################
# NEIGHBORS
####################################################################################################################################

neighbors = translator.TranslatorByRegex([
    (r'(volumes|previews)/GO_0xxx(|_v[1-9])/\w+(|/REDO)/([CEGIJ][0-9]{1,2})', 0,
            [r'\1/GO_0xxx\2/*/\4',
             r'\1/GO_0xxx\2/*/REDO/\4'
            ]),
    (r'(volumes|previews)/GO_0xxx(|_v[1-9])/\w+(|/REDO)/[CEGIJ][0-9]{1,2}/(\w+)', 0,
            [r'\1/GO_0xxx\2/*/*/\4',
             r'\1/GO_0xxx\2/*/REDO/*/\4',
            ]),
    (r'(volumes|previews)/GO_0xxx(|_v[1-9])/\w+(|/REDO)/[CEGIJ][0-9]{1,2}/(\w+)/C\d{6}', 0, 
            [r'\1/GO_0xxx\2/*/*/\4/*',
             r'\1/GO_0xxx\2/*/REDO/*/\4/*',
            ]),
])

####################################################################################################################################
# SORT_KEY
####################################################################################################################################

sort_key = translator.TranslatorByRegex([

    # Puts encounters in chronological order, after AAREADME, in root directory
    (r'([CEGIJ])([0-9])',      0, r'AAZ0\2\1'),
    (r'([CEGIJ])([0-9][0-9])', 0, r'AAZ\2\1'),
    (r'(AAREADME.TXT)',        0, r'\1'),
    (r'(CATALOG)',             0, r'\1'),
    (r'(DOCUMENT)',            0, r'\1'),
    (r'(ERRATA.TXT)',          0, r'\1'),
    (r'(INDEX)',               0, r'\1'),
    (r'(LABEL)',               0, r'\1'),
    (r'(REDO)',                0, r'\1'),
    (r'(VOLDESC.CAT)',         0, r'\1'),
])

####################################################################################################################################
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
    (r'volumes/GO_0xxx(|_v[1-9])/GO_0.../(?!CATALOG|DOCUMENT|INDEX|LABEL).*\.(IMG|LBL)', 0, ('Galileo SSI', 10, 'gossi_raw', 'Raw Image', True)),
])

####################################################################################################################################
# OPUS_FORMAT
####################################################################################################################################

opus_format = translator.TranslatorByRegex([
    (r'.*\.IMG', 0, ('Binary', 'VICAR')),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

# NOTE: _v1 files have been intentionally removed
opus_products = translator.TranslatorByRegex([
    (r'.*volumes/(GO_0xxx)/(GO_0...)/(.*/C[0-9]{6})([0-9]{4}[A-Z])\.(IMG|LBL)', 0,
            [r'volumes/\1/\2/\3\4.IMG',
             r'volumes/\1/\2/\3\4.LBL',
             r'previews/\1/\2/\3\4_full.jpg',
             r'previews/\1/\2/\3\4_med.jpg',
             r'previews/\1/\2/\3\4_small.jpg',
             r'previews/\1/\2/\3\4_thumb.jpg',
             r'metadata/\1/\2/\2_index.lbl',
             r'metadata/\1/\2/\2_index.tab',
            ]),
])

####################################################################################################################################
# OPUS_ID
####################################################################################################################################

opus_id = translator.TranslatorByRegex([
    (r'.*/GO_0xxx/GO_00../.*/C([0-9]{10})[A-Z]\.(IMG|LBL)', 0, r'go-ssi-c\1'),
])

####################################################################################################################################
# OPUS_ID_TO_PRIMARY_LOGICAL_PATH
####################################################################################################################################

opus_id_to_primary_logical_path = translator.TranslatorByRegex([
    (r'go-ssi-c(03[4-5].*)', 0, [r'volumes/GO_0xxx/GO_0017/??/*/C\1R.IMG']),
    (r'go-ssi-c(036.*)'    , 0, [r'volumes/GO_0xxx/GO_0017/??/*/C\1R.IMG',
                                 r'volumes/GO_0xxx/GO_0018/??/*/C\1R.IMG',
                                 r'volumes/GO_0xxx/GO_0018/REDO/??/*/C\1R.IMG',
                                 r'volumes/GO_0xxx/GO_0019/REDO/??/*/C\1R.IMG']),
    (r'go-ssi-c(037.*)'    , 0, [r'volumes/GO_0xxx/GO_0018/??/*/C\1R.IMG',
                                 r'volumes/GO_0xxx/GO_0018/REDO/??/*/C\1R.IMG',
                                 r'volumes/GO_0xxx/GO_0019/REDO/??/*/C\1R.IMG']),
    (r'go-ssi-c(038.*)'    , 0, [r'volumes/GO_0xxx/GO_0018/??/*/C\1R.IMG',
                                 r'volumes/GO_0xxx/GO_0018/REDO/??/*/C\1R.IMG',
                                 r'volumes/GO_0xxx/GO_0019/REDO/??/*/C\1R.IMG']),
    (r'go-ssi-c(039.*)'    , 0, [r'volumes/GO_0xxx/GO_0019/??/*/C\1R.IMG']),
    (r'go-ssi-c(040.*)'    , 0, [r'volumes/GO_0xxx/GO_0019/??/*/C\1R.IMG',
                                 r'volumes/GO_0xxx/GO_0019/???/*/C\1R.IMG']),
    (r'go-ssi-c(041.*)'    , 0, [r'volumes/GO_0xxx/GO_0019/???/*/C\1R.IMG']),
    (r'go-ssi-c(04[2-6].*)', 0, [r'volumes/GO_0xxx/GO_0020/???/*/C\1R.IMG',
                                 r'volumes/GO_0xxx/GO_0023/REDO/E11/*/C\1R.IMG']),
    (r'go-ssi-c(04[7-9].*)', 0, [r'volumes/GO_0xxx/GO_0021/???/*/C\1R.IMG']),
    (r'go-ssi-c(05[0-1].*)', 0, [r'volumes/GO_0xxx/GO_0021/???/*/C\1R.IMG']),
    (r'go-ssi-c(052.*)'    , 0, [r'volumes/GO_0xxx/GO_0022/???/*/C\1R.IMG',
                                 r'volumes/GO_0xxx/GO_0022/???/*/*/C\1R.IMG']),
    (r'go-ssi-c(05[3-9].*)', 0, [r'volumes/GO_0xxx/GO_0023/???/*/C\1R.IMG',
                                 r'volumes/GO_0xxx/GO_0023/G28/REPAIRED/C\1S.IMG']),
    (r'go-ssi-c(06.*)'     , 0, [r'volumes/GO_0xxx/GO_0023/???/*/C\1R.IMG',
                                 r'volumes/GO_0xxx/GO_0023/G29/REPAIRED/C\1S.IMG']),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class GO_0xxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('GO_0xxx', re.I, 'GO_0xxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors + pdsfile.PdsFile.NEIGHBORS
    SORT_KEY = sort_key + pdsfile.PdsFile.SORT_KEY

    OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    OPUS_FORMAT = opus_format + pdsfile.PdsFile.OPUS_FORMAT
    OPUS_PRODUCTS = opus_products
    OPUS_ID = opus_id
    OPUS_ID_TO_PRIMARY_LOGICAL_PATH = opus_id_to_primary_logical_path

    VIEWABLES = {'default': default_viewables}

    ASSOCIATIONS = pdsfile.PdsFile.ASSOCIATIONS.copy()
    ASSOCIATIONS['volumes']  += associations_to_volumes
    ASSOCIATIONS['previews'] += associations_to_previews
    ASSOCIATIONS['metadata'] += associations_to_metadata

    VERSIONS = versions + pdsfile.PdsFile.VERSIONS

    FILENAME_KEYLEN = 11    # trim off suffixes

# Global attribute shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS = translator.TranslatorByRegex([(r'go-ssi-.*', 0, GO_0xxx)]) + \
                                      pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['GO_0xxx'] = GO_0xxx

####################################################################################################################################
# Unit tests
####################################################################################################################################

import pytest
from .pytest_support import *

@pytest.mark.parametrize(
    'input_path,expected',
    [
        ('volumes/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R.IMG',
         {('Galileo SSI',
           10,
           'gossi_raw',
           'Raw Image',
           True): ['volumes/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R.IMG',
                   'volumes/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R.LBL',
                   'volumes/GO_0xxx/GO_0017/LABEL/RLINEPRX.FMT',
                   'volumes/GO_0xxx/GO_0017/LABEL/RTLMTAB.FMT'],
          ('browse',
           10,
           'browse_thumb',
           'Browse Image (thumbnail)',
           False): ['previews/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R_thumb.jpg'],
          ('browse',
           20,
           'browse_small',
           'Browse Image (small)',
           False): ['previews/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R_small.jpg'],
          ('browse',
           30,
           'browse_medium',
           'Browse Image (medium)',
           False): ['previews/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R_med.jpg'],
          ('browse',
           40,
           'browse_full',
           'Browse Image (full)',
           True): ['previews/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R_full.jpg'],
          ('metadata',
           5,
           'rms_index',
           'RMS Node Augmented Index',
           False): ['metadata/GO_0xxx/GO_0017/GO_0017_index.tab',
                    'metadata/GO_0xxx/GO_0017/GO_0017_index.lbl']}
        )
    ]
)
def test_opus_products(input_path, expected):
    opus_products_test(input_path, expected)

####################################################################################################################################
