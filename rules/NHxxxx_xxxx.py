####################################################################################################################################
# rules/NHxxxx_xxxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# Special procedure to define and prioritize OPUS_TYPES
####################################################################################################################################

# Define the priority among file types
FILE_CODE_PRIORITY = {

    # LORRI codes
    '630': 0,  #- LORRI High-res Lossless (CDH 1)/LOR
    '631': 2,  #- LORRI High-res Packetized (CDH 1)/LOR
    '632': 4,  #- LORRI High-res Lossy (CDH 1)/LOR
    '633': 6,  #- LORRI 4x4 Binned Lossless (CDH 1)/LOR
    '634': 8,  #- LORRI 4x4 Binned Packetized (CDH 1)/LOR
    '635': 10, #- LORRI 4x4 Binned Lossy (CDH 1)/LOR
    '636': 1,  #- LORRI High-res Lossless (CDH 2)/LOR
    '637': 3,  #- LORRI High-res Packetized (CDH 2)/LOR
    '638': 5,  #- LORRI High-res Lossy (CDH 2)/LOR
    '639': 7,  #- LORRI 4x4 Binned Lossless (CDH 2)/LOR
    '63A': 9,  #- LORRI 4x4 Binned Packetized (CDH 2)/LOR
    '63B': 11, #- LORRI 4x4 Binned Lossy (CDH 2)/LOR

    # MVIC codes
    '530': 12, #- MVIC Panchromatic TDI Lossless (CDH 1)/MP1,MP2
    '531': 18, #- MVIC Panchromatic TDI Packetized (CDH 1)/MP1,MP2
    '532': 24, #- MVIC Panchromatic TDI Lossy (CDH 1)/MP1,MP2

    '533': 30, #- MVIC Panchromatic TDI 3x3 Binned Lossless (CDH 1)/MP1,MP2
    '534': 32, #- MVIC Panchromatic TDI 3x3 Binned Packetized (CDH 1)/MP1,MP2
    '535': 34, #- MVIC Panchromatic TDI 3x3 Binned Lossy (CDH 1)/MP1,MP2

    '536': 13, #- MVIC Color TDI Lossless (CDH 1)/MC0,MC1,MC2,MC3
    '537': 19, #- MVIC Color TDI Packetized (CDH 1)/MC0,MC1,MC2,MC3
    '538': 25, #- MVIC Color TDI Lossy (CDH 1)/MC0,MC1,MC2,MC3

    '539': 14, #- MVIC Panchromatic Frame Transfer Lossless (CDH 1)/MPF
    '53A': 20, #- MVIC Panchromatic Frame Transfer Packetized (CDH 1)/MPF
    '53B': 26, #- MVIC Panchromatic Frame Transfer Lossy (CDH 1)/MPF

    '53F': 15, #- MVIC Panchromatic TDI Lossless (CDH 2)/MP1,MP2
    '540': 21, #- MVIC Panchromatic TDI Packetized (CDH 2)/MP1,MP2
    '541': 27, #- MVIC Panchromatic TDI Lossy (CDH 2)/MP1,MP2

    '542': 31, #- MVIC Panchromatic TDI 3x3 Binned Lossless (CDH 2)/MP1,MP2
    '543': 33, #- MVIC Panchromatic TDI 3x3 Binned Packetized (CDH 2)/MP1,MP2
    '544': 35, #- MVIC Panchromatic TDI 3x3 Binned Lossy (CDH 2)/MP1,MP2

    '545': 16, #- MVIC Color TDI Lossless (CDH 2)/MC0,MC1,MC2,MC3
    '546': 22, #- MVIC Color TDI Packetized (CDH 2)/MC0,MC1,MC2,MC3
    '547': 28, #- MVIC Color TDI Lossy (CDH 2)/MC0,MC1,MC2,MC3

    '548': 17, #- MVIC Panchromatic Frame Transfer Lossless (CDH 2)/MPF
    '549': 23, #- MVIC Panchromatic Frame Transfer Packetized (CDH 2)/MPF
    '54A': 29, #- MVIC Panchromatic Frame Transfer Lossy (CDH 2)/MPF
}

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/NH.*/NH...._1.../data(|/[0-9_]+)', re.I, ('Raw images grouped by date',        'IMAGEDIR')),
    (r'volumes/NH.*/NH...._2.../data(|/[0-9_]+)', re.I, ('Calibrated images grouped by date', 'IMAGEDIR')),

    (r'volumes/NH.*0x(533|534|535|542|543|544)_eng(|_\d+)\.fit'        , re.I, ('Raw image (3x3 binned), FITS'       , 'IMAGE')),
    (r'volumes/NH.*0x(533|534|535|542|543|544)_sci(|_\d+)\.fit'        , re.I, ('Calibrated image (3x3 binned), FITS', 'IMAGE')),
    (r'volumes/NH.*0x(633|634|635|639|63A|63B)_eng(|_\d+)\.fit'        , re.I, ('Raw image (4x4 binned), FITS'       , 'IMAGE')),
    (r'volumes/NH.*0x(633|634|635|639|63A|63B)_sci(|_\d+)\.fit'        , re.I, ('Calibrated image (4x4 binned), FITS', 'IMAGE')),
    (r'volumes/NH.*0x(530|536|539|53F|545|548|630|636)_eng(|_\d+)\.fit', re.I, ('Raw image (lossless), FITS'         , 'IMAGE')),
    (r'volumes/NH.*0x(530|536|539|53F|545|548|630|636)_sci(|_\d+)\.fit', re.I, ('Calibrated image (lossless), FITS'  , 'IMAGE')),
    (r'volumes/NH.*0x(532|538|53B|541|547|54A|632|638)_eng(|_\d+)\.fit', re.I, ('Raw image (lossy), FITS'            , 'IMAGE')),
    (r'volumes/NH.*0x(532|538|53B|541|547|54A|632|638)_sci(|_\d+)\.fit', re.I, ('Calibrated image (lossy), FITS'     , 'IMAGE')),
    (r'volumes/NH.*0x(531|537|53A|540|546|549|631|637)_eng(|_\d+)\.fit', re.I, ('Raw imag, FITS'                     , 'IMAGE')),
    (r'volumes/NH.*0x(531|537|53A|540|546|549|631|637)_sci(|_\d+)\.fit', re.I, ('Calibrated imag, FITS'              , 'IMAGE')),

    (r'.*/catalog/NH.CAT'           , re.I, ('Mission description',                     'INFO'    )),
    (r'.*/catalog/NHSC.CAT'         , re.I, ('Spacecraft description',                  'INFO'    )),
    (r'.*/catalog/(LORRI|MVIC)\.CAT', re.I, ('Instrument description',                  'INFO'    )),
    (r'.*/catalog/.*RELEASE\.CAT'   , re.I, ('Release information',                     'INFO'    )),
    (r'.*/catalog/132524_apl\.cat'  , re.I, ('Target information',                      'INFO'    )),
    (r'volumes/.*/data(|\w+)'       , re.I, ('Data files organized by date',            'IMAGEDIR')),
    (r'.*/NH...._1...\.tar\.gz'     , 0,    ('Downloadable archive of raw data',        'TARBALL' )),
    (r'.*/NH...._2...\.tar\.gz'     , 0,    ('Downloadable archive of calibrated data', 'TARBALL' )),

    (r'.*/calib/sap.*\.fit'         , re.I, ('Debias image',                            'IMAGE'   )),
    (r'.*/calib/c?flat.*\.fit'      , re.I, ('Flat field image',                        'IMAGE'   )),
    (r'.*/calib/dead.*\.fit'        , re.I, ('Dead pixel image',                        'IMAGE'   )),
    (r'.*/calib/hot.*\.fit'         , re.I, ('Hot pixel image',                         'IMAGE'   )),

    (r'volumes/.*/document/lorri_ssr\.pdf', 0, ('&#11013; <b>LORRI Description (Space Science Reviews)</b>',
                                                                                        'INFO')),
    (r'volumes/.*/document/ralph_ssr\.pdf', 0, ('&#11013; <b>Ralph Description (Space Science Reviews)</b>',
                                                                                        'INFO')),
    (r'volumes/.*/document/payload_ssr\.pdf', 0, ('&#11013; <b>Payload Description (Space Science Reviews)</b>',
                                                                                        'INFO')),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'.*\.lbl',  re.I, ''),
    (r'volumes/(NHxx.._xxxx)(|_[0-9]\.]+)/(NH...._....)/data/(\w+/\w{3}_[0-9]{10}_0x...)_(eng|sci).*', 0,
            [r'previews/\1/\3/data/#LOWER#\4_\5_full.jpg',
             r'previews/\1/\3/data/#LOWER#\4_\5_med.jpg',
             r'previews/\1/\3/data/#LOWER#\4_\5_small.jpg',
             r'previews/\1/\3/data/#LOWER#\4_\5_thumb.jpg',
            ]),
])

raw_viewables = translator.TranslatorByRegex([
    (r'.*\.lbl',  re.I, ''),
    (r'volumes/(NHxx.._xxxx)(|_[0-9]\.]+)/(NH....)_1(...)/data/(\w+/\w{3}_[0-9]{10}_0x...)_eng.*', 0,
           [r'previews/\1/\3_1\4/data/#LOWER#\5_eng_full.jpg',
            r'previews/\1/\3_1\4/data/#LOWER#\5_eng_med.jpg',
            r'previews/\1/\3_1\4/data/#LOWER#\5_eng_small.jpg',
            r'previews/\1/\3_1\4/data/#LOWER#\5_eng_thumb.jpg',
           ]),
])

calibrated_viewables = translator.TranslatorByRegex([
    (r'.*\.lbl',  re.I, ''),
    (r'volumes/(NHxx.._xxxx)(|_[0-9]\.]+)/(NH....)_1(...)/data/(\w+/\w{3}_[0-9]{10}_0x...)_sci.*', 0,
           [r'previews/\1/\3_2\4/data/#LOWER#\5_sci_full.jpg',
            r'previews/\1/\3_2\4/data/#LOWER#\5_sci_med.jpg',
            r'previews/\1/\3_2\4/data/#LOWER#\5_sci_small.jpg',
            r'previews/\1/\3_2\4/data/#LOWER#\5_sci_thumb.jpg',
           ]),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    (r'.*/(NHxx.._xxxx)(|_v[0-9\.]+)/(NH....)_[12](...)/data/(\w+/[a-z0-9]{3}_[0-9]{10})_0x.*', re.I,
            [r'volumes/\1\2/\3_1\4/data/#LOWER#\5*',
             r'volumes/\1\2/\3_1\4/DATA/#UPPER#\5*',    # NHxxMV_xxxx_v1/NHJUMV_1001 is upper case
             r'volumes/\1\2/\3_2\4/data/#LOWER#\5*',
            ]),
    (r'.*/(NHxx.._xxxx)(|_v[0-9\.]+)/(NH....)_[12](...)/data(|/\w+)', re.I,
            [r'volumes/\1\2/\3_1\4/data\5',
             r'volumes/\1\2/\3_1\4/DATA\5',
             r'volumes/\1\2/\3_2\4/data\5',
            ]),
    (r'documents/NHxxxx_xxxx.*', 0,
            [r'volumes/NHxxLO_xxxx',
             r'volumes/NHxxMV_xxxx'
            ]),
])

associations_to_previews = translator.TranslatorByRegex([
    (r'.*/(NHxx.._xxxx)(|_v[0-9\.]+)/(NH....)_[12](...)/data/(\w+/[a-z0-9]{3}_[0-9]{10}_0x...)_(eng|sci).*', re.I,
            [r'previews/\1/\3_1\4/data/#LOWER#\4_\5_eng_full.jpg',
             r'previews/\1/\3_1\4/data/#LOWER#\4_\5_eng_med.jpg',
             r'previews/\1/\3_1\4/data/#LOWER#\4_\5_eng_small.jpg',
             r'previews/\1/\3_1\4/data/#LOWER#\4_\5_eng_thumb.jpg',
             r'previews/\1/\3_2\4/data/#LOWER#\4_\5_sci_full.jpg',
             r'previews/\1/\3_2\4/data/#LOWER#\4_\5_sci_med.jpg',
             r'previews/\1/\3_2\4/data/#LOWER#\4_\5_sci_small.jpg',
             r'previews/\1/\3_2\4/data/#LOWER#\4_\5_sci_thumb.jpg',
            ]),
    (r'.*/(NHxx.._xxxx)(|_v[0-9\.]+)/(NH....)_[12](...)/data(|/\w+)', re.I,
            r'previews/\1/\3_1\4/data\5'),
])

associations_to_metadata = translator.TranslatorByRegex([
    (r'volumes/(NHxx.._xxxx)(|_v[0-9\.]+)/(NH...._[12]...)/data/\w+/([a-z0-9]{3}_[0-9]{10}_0x...)_(eng|sci).*', re.I,
            [r'metadata/\1/\3/\3_index.tab/#LOWER#\4_\5',
             r'metadata/\1/\3/\3_supplemental_index.tab/#LOWER#\4_\5',
             r'metadata/\1/\3/\3_moon_summary.tab/#LOWER#\4_\5',
             r'metadata/\1/\3/\3_ring_summary.tab/#LOWER#\4_\5',
             r'metadata/\1/\3/\3_charon_summary.tab/#LOWER#\4_\5',
             r'metadata/\1/\3/\3_pluto_summary.tab/#LOWER#\4_\5',
             r'metadata/\1/\3/\3_jupiter_summary.tab/#LOWER#\4_\5',
            ]),
])

associations_to_documents = translator.TranslatorByRegex([
    (r'(volumes/.*/NH...._.001).*', 0,
            [r'\1/document/lorri_ssr.pdf',
             r'\1/document/ralph_ssr.pdf',
             r'\1/document/payload_ssr.pdf',
            ]),
    (r'volumes/NH...._xxxx.*', 0,
            r'documents/NHxxxx_xxxx/*'),
])

####################################################################################################################################
# VERSIONS
####################################################################################################################################

# Sometimes NH .fits files have a numeric suffix, other times not
# Also, volume NHJUMV_1001 is in upper case
versions = translator.TranslatorByRegex([
    (r'volumes/(NHxx.._xxxx)(|_v[0-9\.]+)/(NH...._....)/(data/\w+/\w+0x\d\d\d_[a-z]{3}).*\.(.*)', re.I,
            [r'volumes/\1*/\3/#LOWER#\4*.\5',
             r'volumes/\1_v1/\3/#UPPER#\4*.\5',
            ]),
    (r'volumes/(NHxx.._xxxx)(|_v[0-9\.]+)/(NH...._....)/(.*)', re.I,
            [r'volumes/\1*/\3/#LOWER#\4',
             r'volumes/\1_v1/\3/#UPPER#\4',
            ]),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|previews)/NHxx(LO|MV)_....(|_v[\.0-9]+)/NH...._..../data(|/\w+)', re.I, (True, True, True)),
])

####################################################################################################################################
# NEIGHBORS
####################################################################################################################################

neighbors = translator.TranslatorByRegex([
    (r'(volumes|previews)/(NHxx.._xxxx.*/NH)..(.._[12])...',             0,  r'\1/\2??\3*'),
    (r'(volumes|previews)/(NHxx.._xxxx.*/NH)..(.._[12]).../data',     re.I, (r'\1/\2??\3*/data',   r'\1/\2??\3*/DATA'  )),
    (r'(volumes|previews)/(NHxx.._xxxx.*/NH)..(.._[12]).../data/\w+', re.I, (r'\1/\2??\3*/data/*', r'\1/\2??\3*/DATA/*')),
])

####################################################################################################################################
# SORT_KEY
####################################################################################################################################

sort_key = translator.TranslatorByRegex([

    # Order volumes by LA, JU, PC, PE
    (r'NHLA(.._[0-9]{4}.*)', 0, r'NH1LA\1'),
    (r'NHJU(.._[0-9]{4}.*)', 0, r'NH2JU\1'),
    (r'NHPC(.._[0-9]{4}.*)', 0, r'NH3PC\1'),
    (r'NHPE(.._[0-9]{4}.*)', 0, r'NH4PE\1'),
    (r'(\w{3})_([0-9]{10})(.*)', re.I, r'\2\1\3'),
])

####################################################################################################################################
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
    (r'volumes/.*/NH..LO_1.../data/.*\.(fit|lbl)', re.I, ('New Horizons LORRI',   0, 'nh_lorri_raw',          'Raw Image',        True)),
    (r'volumes/.*/NH..LO_2.../data/.*\.(fit|lbl)', re.I, ('New Horizons LORRI', 100, 'nh_lorri_calib',        'Calibrated Image', True)),
    (r'previews/.*/NH..LO_2.../data/.*\.jpg',      0,    ('New Horizons LORRI', 200, 'nh_lorri_calib_browse', 'Extra Preview (calibrated)', False)),

    (r'volumes/.*/NH..MV_1.../data/.*\.(fit|lbl)', re.I, ('New Horizons MVIC',   0, 'nh_mvic_raw',            'Raw Image',        True)),
    (r'volumes/.*/NH..MV_2.../data/.*\.(fit|lbl)', re.I, ('New Horizons MVIC', 100, 'nh_mvic_calib',          'Calibrated Image', True)),
    (r'previews/.*/NH..MV_2.../data/.*\.jpg',      0,    ('New Horizons MVIC', 200, 'nh_mvic_calib_browse',   'Extra Preview (calibrated)', False)),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

opus_products = translator.TranslatorByRegex([
    (r'.*/(NHxx.._xxxx)(|_v[0-9\.]+)/(NH....)_([12])(...)/data/(\w+/[a-z0-9]{3}_\d{10})_.*', re.I,
            [r'volumes/\1*/\3_1\5/data/#LOWER#\6_*',
             r'volumes/\1*/\3_2\5/data/#LOWER#\6_*',
             r'volumes/\1_v1/\3_1\5/DATA/#UPPER#\6_*',
             r'previews/\1/\3_1\5/data/#LOWER#\6_*',
             r'previews/\1/\3_2\5/data/#LOWER#\6_*',
             r'metadata/\1/\3_1\5/\3_1\5_index.tab',
             r'metadata/\1/\3_1\5/\3_1\5_index.lbl',
             r'metadata/\1/\3_1\5/\3_1\5_supplemental_index.tab',
             r'metadata/\1/\3_1\5/\3_1\5_supplemental_index.lbl',
             r'metadata/\1/\3_1\5/\3_1\5_inventory.csv',
             r'metadata/\1/\3_1\5/\3_1\5_inventory.lbl',
             r'metadata/\1/\3_1\5/\3_1\5_jupiter_summary.tab',
             r'metadata/\1/\3_1\5/\3_1\5_jupiter_summary.lbl',
             r'metadata/\1/\3_1\5/\3_1\5_moon_summary.tab',
             r'metadata/\1/\3_1\5/\3_1\5_moon_summary.lbl',
             r'metadata/\1/\3_1\5/\3_1\5_ring_summary.tab',
             r'metadata/\1/\3_1\5/\3_1\5_ring_summary.lbl',
             r'metadata/\1/\3_1\5/\3_1\5_pluto_summary.tab',
             r'metadata/\1/\3_1\5/\3_1\5_pluto_summary.lbl',
             r'metadata/\1/\3_1\5/\3_1\5_charon_summary.tab',
             r'metadata/\1/\3_1\5/\3_1\5_charon_summary.lbl',
            ]),
])

####################################################################################################################################
# OPUS_ID
####################################################################################################################################

opus_id = translator.TranslatorByRegex([
    (r'.*/NH..LO_.xxx.*/data/\w+/(lor_\d{10})_.*', re.I, r'nh-lorri-\1'),
    (r'.*/NH..MV_.xxx.*/data/\w+/(m.._\d{10})_.*', re.I, r'nh-mvic-#LOWER#\1'),
])

####################################################################################################################################
# OPUS_ID_TO_PRIMARY_LOGICAL_PATH
####################################################################################################################################

# Organized giving priority to lossless, full-resolution
opus_id_to_primary_logical_path = translator.TranslatorByRegex([
    (r'nh-lorri-lor_(00[0-2].*)', 0,
            [r'volumes/NHxxLO_xxxx/NHLALO_1001/data/*/lor_\1_0x63[06]_eng*.fit',        # High-res lossless
             r'volumes/NHxxLO_xxxx/NHLALO_1001/data/*/lor_\1_0x63[17]_eng*.fit',        # High-res packetized
             r'volumes/NHxxLO_xxxx/NHLALO_1001/data/*/lor_\1_0x63[28]_eng*.fit',        # High-res lossy
             r'volumes/NHxxLO_xxxx/NHLALO_1001/data/*/lor_\1_0x63[39]_eng*.fit',        # 4x4 lossless
             r'volumes/NHxxLO_xxxx/NHLALO_1001/data/*/lor_\1_0x63[4aA]_eng*.fit',       # 4x4 packetized
             r'volumes/NHxxLO_xxxx/NHLALO_1001/data/*/lor_\1_0x63[5bB]_eng*.fit']),     # 4x4 lossy

    (r'nh-lor_(00[3-4].*)', 0,
            [r'volumes/NHxxLO_xxxx/NHJULO_1001/data/*/lor_\1_0x63[06]_eng*.fit',        # High-res lossless
             r'volumes/NHxxLO_xxxx/NHJULO_1001/data/*/lor_\1_0x63[17]_eng*.fit',        # High-res packetized
             r'volumes/NHxxLO_xxxx/NHJULO_1001/data/*/lor_\1_0x63[28]_eng*.fit',        # High-res lossy
             r'volumes/NHxxLO_xxxx/NHJULO_1001/data/*/lor_\1_0x63[39]_eng*.fit',        # 4x4 lossless
             r'volumes/NHxxLO_xxxx/NHJULO_1001/data/*/lor_\1_0x63[4aA]_eng*.fit',       # 4x4 packetized
             r'volumes/NHxxLO_xxxx/NHJULO_1001/data/*/lor_\1_0x63[5bB]_eng*.fit']),     # 4x4 lossy

    (r'nh-lorri-lor_(00[5-9]|01|02[0-6])(.*)', 0,
            [r'volumes/NHxxLO_xxxx/NHPCLO_1001/data/*/lor_\1\2_0x63[06]_eng*.fit',      # High-res lossless
             r'volumes/NHxxLO_xxxx/NHPCLO_1001/data/*/lor_\1\2_0x63[17]_eng*.fit',      # High-res packetized
             r'volumes/NHxxLO_xxxx/NHPCLO_1001/data/*/lor_\1\2_0x63[28]_eng*.fit',      # High-res lossy
             r'volumes/NHxxLO_xxxx/NHPCLO_1001/data/*/lor_\1\2_0x63[39]_eng*.fit',      # 4x4 lossless
             r'volumes/NHxxLO_xxxx/NHPCLO_1001/data/*/lor_\1\2_0x63[4aA]_eng*.fit',     # 4x4 packetized
             r'volumes/NHxxLO_xxxx/NHPCLO_1001/data/*/lor_\1\2_0x63[5bB]_eng*.fit']),   # 4x4 lossy

    (r'nh-lorri-lor_(02[89]|03[0-3])(.*)', 0,
            [r'volumes/NHxxLO_xxxx/NHPELO_1001/data/*/lor_\1\2_0x63[06]_eng*.fit',      # High-res lossless
             r'volumes/NHxxLO_xxxx/NHPELO_1001/data/*/lor_\1\2_0x63[17]_eng*.fit',      # High-res packetized
             r'volumes/NHxxLO_xxxx/NHPELO_1001/data/*/lor_\1\2_0x63[28]_eng*.fit',      # High-res lossy
             r'volumes/NHxxLO_xxxx/NHPELO_1001/data/*/lor_\1\2_0x63[39]_eng*.fit',      # 4x4 lossless
             r'volumes/NHxxLO_xxxx/NHPELO_1001/data/*/lor_\1\2_0x63[4aA]_eng*.fit',     # 4x4 packetized
             r'volumes/NHxxLO_xxxx/NHPELO_1001/data/*/lor_\1\2_0x63[5bB]_eng*.fit']),   # 4x4 lossy

    (r'nh-mvic-(m..)_(00[0-2].*)', 0,
            [r'volumes/NHxxMV_xxxx/NHLAMV_1001/data/*/\1_\2_0x53[069fF]_eng.fit',       # High-res lossless
             r'volumes/NHxxMV_xxxx/NHLAMV_1001/data/*/\1_\2_0x54[58]_eng.fit',          # High-res lossless
             r'volumes/NHxxMV_xxxx/NHLAMV_1001/data/*/\1_\2_0x53[17aA]_eng.fit',        # High-res packetized
             r'volumes/NHxxMV_xxxx/NHLAMV_1001/data/*/\1_\2_0x54[069]_eng.fit',         # High-res packetized
             r'volumes/NHxxMV_xxxx/NHLAMV_1001/data/*/\1_\2_0x53[28]_eng.fit',          # High-res lossy
             r'volumes/NHxxMV_xxxx/NHLAMV_1001/data/*/\1_\2_0x54[17aA]_eng.fit',        # High-res lossy
             r'volumes/NHxxMV_xxxx/NHLAMV_1001/data/*/\1_\2_0x533_eng.fit',             # 3x3 lossless
             r'volumes/NHxxMV_xxxx/NHLAMV_1001/data/*/\1_\2_0x542_eng.fit',             # 3x3 lossless
             r'volumes/NHxxMV_xxxx/NHLAMV_1001/data/*/\1_\2_0x534_eng.fit',             # 3x3 packetized
             r'volumes/NHxxMV_xxxx/NHLAMV_1001/data/*/\1_\2_0x543_eng.fit',             # 3x3 packetized
             r'volumes/NHxxMV_xxxx/NHLAMV_1001/data/*/\1_\2_0x535_eng.fit',             # 3x3 lossy
             r'volumes/NHxxMV_xxxx/NHLAMV_1001/data/*/\1_\2_0x544_eng.fit']),           # 3x3 lossy

    (r'nh-mvic-(m..)_(00[3-4]|01|02[0-6])(.*)', 0,
            [r'volumes/NHxxMV_xxxx/NHJUMV_1001/data/*/\1_\2_0x53[069fF]_eng.fit',       # High-res lossless
             r'volumes/NHxxMV_xxxx/NHJUMV_1001/data/*/\1_\2_0x54[58]_eng.fit',          # High-res lossless
             r'volumes/NHxxMV_xxxx/NHJUMV_1001/data/*/\1_\2_0x53[17aA]_eng.fit',        # High-res packetized
             r'volumes/NHxxMV_xxxx/NHJUMV_1001/data/*/\1_\2_0x54[069]_eng.fit',         # High-res packetized
             r'volumes/NHxxMV_xxxx/NHJUMV_1001/data/*/\1_\2_0x53[28]_eng.fit',          # High-res lossy
             r'volumes/NHxxMV_xxxx/NHJUMV_1001/data/*/\1_\2_0x54[17aA]_eng.fit',        # High-res lossy
             r'volumes/NHxxMV_xxxx/NHJUMV_1001/data/*/\1_\2_0x533_eng.fit',             # 3x3 lossless
             r'volumes/NHxxMV_xxxx/NHJUMV_1001/data/*/\1_\2_0x542_eng.fit',             # 3x3 lossless
             r'volumes/NHxxMV_xxxx/NHJUMV_1001/data/*/\1_\2_0x534_eng.fit',             # 3x3 packetized
             r'volumes/NHxxMV_xxxx/NHJUMV_1001/data/*/\1_\2_0x543_eng.fit',             # 3x3 packetized
             r'volumes/NHxxMV_xxxx/NHJUMV_1001/data/*/\1_\2_0x535_eng.fit',             # 3x3 lossy
             r'volumes/NHxxMV_xxxx/NHJUMV_1001/data/*/\1_\2_0x544_eng.fit']),           # 3x3 lossy

    (r'nh-mvic-(m..)_(00[5-9]|01|02[0-6])(.*)', 0,
            [r'volumes/NHxxMV_xxxx/NHPCMV_1001/data/*/\1_\2_0x53[069fF]_eng.fit',       # High-res lossless
             r'volumes/NHxxMV_xxxx/NHPCMV_1001/data/*/\1_\2_0x54[58]_eng.fit',          # High-res lossless
             r'volumes/NHxxMV_xxxx/NHPCMV_1001/data/*/\1_\2_0x53[17aA]_eng.fit',        # High-res packetized
             r'volumes/NHxxMV_xxxx/NHPCMV_1001/data/*/\1_\2_0x54[069]_eng.fit',         # High-res packetized
             r'volumes/NHxxMV_xxxx/NHPCMV_1001/data/*/\1_\2_0x53[28]_eng.fit',          # High-res lossy
             r'volumes/NHxxMV_xxxx/NHPCMV_1001/data/*/\1_\2_0x54[17aA]_eng.fit',        # High-res lossy
             r'volumes/NHxxMV_xxxx/NHPCMV_1001/data/*/\1_\2_0x533_eng.fit',             # 3x3 lossless
             r'volumes/NHxxMV_xxxx/NHPCMV_1001/data/*/\1_\2_0x542_eng.fit',             # 3x3 lossless
             r'volumes/NHxxMV_xxxx/NHPCMV_1001/data/*/\1_\2_0x534_eng.fit',             # 3x3 packetized
             r'volumes/NHxxMV_xxxx/NHPCMV_1001/data/*/\1_\2_0x543_eng.fit',             # 3x3 packetized
             r'volumes/NHxxMV_xxxx/NHPCMV_1001/data/*/\1_\2_0x535_eng.fit',             # 3x3 lossy
             r'volumes/NHxxMV_xxxx/NHPCMV_1001/data/*/\1_\2_0x544_eng.fit']),           # 3x3 lossy

    (r'nh-mvic-(m..)_(02[89]|03[0-3])(.*)', 0,
            [r'volumes/NHxxMV_xxxx/NHPEMV_1001/data/*/\1_\2_0x53[069fF]_eng.fit',       # High-res lossless
             r'volumes/NHxxMV_xxxx/NHPEMV_1001/data/*/\1_\2_0x54[58]_eng.fit',          # High-res lossless
             r'volumes/NHxxMV_xxxx/NHPEMV_1001/data/*/\1_\2_0x53[17aA]_eng.fit',        # High-res packetized
             r'volumes/NHxxMV_xxxx/NHPEMV_1001/data/*/\1_\2_0x54[069]_eng.fit',         # High-res packetized
             r'volumes/NHxxMV_xxxx/NHPEMV_1001/data/*/\1_\2_0x53[28]_eng.fit',          # High-res lossy
             r'volumes/NHxxMV_xxxx/NHPEMV_1001/data/*/\1_\2_0x54[17aA]_eng.fit',        # High-res lossy
             r'volumes/NHxxMV_xxxx/NHPEMV_1001/data/*/\1_\2_0x533_eng.fit',             # 3x3 lossless
             r'volumes/NHxxMV_xxxx/NHPEMV_1001/data/*/\1_\2_0x542_eng.fit',             # 3x3 lossless
             r'volumes/NHxxMV_xxxx/NHPEMV_1001/data/*/\1_\2_0x534_eng.fit',             # 3x3 packetized
             r'volumes/NHxxMV_xxxx/NHPEMV_1001/data/*/\1_\2_0x543_eng.fit',             # 3x3 packetized
             r'volumes/NHxxMV_xxxx/NHPEMV_1001/data/*/\1_\2_0x535_eng.fit',             # 3x3 lossy
             r'volumes/NHxxMV_xxxx/NHPEMV_1001/data/*/\1_\2_0x544_eng.fit']),           # 3x3 lossy
])

####################################################################################################################################
# FILESPEC_TO_VOLSET
####################################################################################################################################

filespec_to_volset = translator.TranslatorByRegex([
    (r'NH..(MV|LO)_\d{4}.*', 0, r'NHxx\1_xxxx'),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class NHxxxx_xxxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('NHxx.._xxxx', re.I, 'NHxxxx_xxxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors + pdsfile.PdsFile.NEIGHBORS
    SORT_KEY = sort_key + pdsfile.PdsFile.SORT_KEY

    OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    OPUS_PRODUCTS = opus_products
    OPUS_ID = opus_id
    OPUS_ID_TO_PRIMARY_LOGICAL_PATH = opus_id_to_primary_logical_path

    VIEWABLES = {
        'default'   : default_viewables,
        'raw'       : raw_viewables,
        'calibrated': calibrated_viewables,
    }

    VIEWABLE_TOOLTIPS = {
        'default'   : 'Default browse product for this file',
        'raw'       : 'Preview of the raw image',
        'calibrated': 'Preview of the calibrated image',
    }

    ASSOCIATIONS = pdsfile.PdsFile.ASSOCIATIONS.copy()
    ASSOCIATIONS['volumes']   += associations_to_volumes
    ASSOCIATIONS['previews']  += associations_to_previews
    ASSOCIATIONS['metadata']  += associations_to_metadata
    ASSOCIATIONS['documents'] += associations_to_documents

    VERSIONS = versions + pdsfile.PdsFile.VERSIONS

    FILENAME_KEYLEN = 14    # trim off suffixes

    def opus_prioritizer(self, pdsfiles):
        """Prioritizes items that have been downlinked in multiple ways."""

        for header in list(pdsfiles.keys()): # We change pdsfiles in the loop!
            sublists = pdsfiles[header]
            if len(sublists) == 1: continue
            if header == '' or not header[0].startswith('New Horizons'):
                continue
            if 'browse' in header[2]:
                continue

            priority = []
            for sublist in sublists:
                code = (sublist[0].basename.replace('X','x')
                        .partition('_0x')[2][:3]).upper()
                rank = sublist[0].version_rank
                priority.append((FILE_CODE_PRIORITY[code],
                                code, -rank, sublist))

            priority.sort()
            code0 = priority[0][1]
            list0 = [priority[0][3]]

            for (prio, code, _, sublist) in priority[1:]:
                if code == code0:
                    list0.append(sublist)
                    continue

                new_header = (header[0],
                              header[1]+50,
                              header[2]+'_alternate',
                              header[3]+' Alternate Downlink',
                              True)
                if new_header not in pdsfiles:
                    pdsfiles[new_header] = []
                pdsfiles[new_header].append(sublist)
            pdsfiles[header] = list0

        return pdsfiles

# Global attribute shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS = translator.TranslatorByRegex([(r'nh-.*', 0, NHxxxx_xxxx)]) + \
                                      pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS

pdsfile.PdsFile.FILESPEC_TO_VOLSET = filespec_to_volset + pdsfile.PdsFile.FILESPEC_TO_VOLSET

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['NHxxxx_xxxx'] = NHxxxx_xxxx

####################################################################################################################################

import pytest
from .pytest_support import *

def test_opus_products_count():

    TESTS = [
        (4, 'volumes/NHxx.._xxxx/.*/data/.*'),
        (4, 'volumes/NHxx.._xxxx_v1/.*/data/.*'),
        (8, 'previews/NHxx.._xxxx/.*/data/.*'),
        (4, 'metadata/.*index.*'),
        (8, 'metadata/.*summary.*'),
        (2, 'metadata/.*supplemental.*'),
        (2, 'metadata/.*inventory.*'),
    ]

    PATH = 'volumes/NHxxLO_xxxx/NHPELO_2001/data/20150125_028445/lor_0284457178_0x630_sci.lbl'
    abspaths = translate_all(opus_products, PATH)
    trimmed = [p.rpartition('holdings/')[-1] for p in abspaths]
    for (count, pattern) in TESTS:
        subset = [p for p in trimmed if re.fullmatch(pattern, p)]
        assert len(subset) == count, f'Miscount: {pattern} {len(subset)} {trimmed}'

@pytest.mark.parametrize(
# 1001 is the raw volume and 2001 is the calibrated volume.
    'input_path,expected',
    [
        ('volumes/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng.fit',
         {('New Horizons LORRI',
           0,
           'nh_lorri_raw',
           'Raw Image',
           True): ['volumes/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng.fit',
                   'volumes/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng.lbl',
                   'volumes/NHxxLO_xxxx_v3/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng_1.fit',
                   'volumes/NHxxLO_xxxx_v3/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng_1.lbl',
                   'volumes/NHxxLO_xxxx_v2/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng_1.fit',
                   'volumes/NHxxLO_xxxx_v2/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng_1.lbl',
                   'volumes/NHxxLO_xxxx_v1/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng_1.fit',
                   'volumes/NHxxLO_xxxx_v1/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng_1.lbl'],
          ('New Horizons LORRI',
           100,
           'nh_lorri_calib',
           'Calibrated Image',
           True): ['volumes/NHxxLO_xxxx/NHLALO_2001/data/20060224_000310/lor_0003103486_0x630_sci.fit',
                   'volumes/NHxxLO_xxxx/NHLALO_2001/data/20060224_000310/lor_0003103486_0x630_sci.lbl',
                   'volumes/NHxxLO_xxxx_v3/NHLALO_2001/data/20060224_000310/lor_0003103486_0x630_sci_1.fit',
                   'volumes/NHxxLO_xxxx_v3/NHLALO_2001/data/20060224_000310/lor_0003103486_0x630_sci_1.lbl',
                   'volumes/NHxxLO_xxxx_v2/NHLALO_2001/data/20060224_000310/lor_0003103486_0x630_sci_1.fit',
                   'volumes/NHxxLO_xxxx_v2/NHLALO_2001/data/20060224_000310/lor_0003103486_0x630_sci_1.lbl',
                   'volumes/NHxxLO_xxxx_v1/NHLALO_2001/data/20060224_000310/lor_0003103486_0x630_sci_1.fit',
                   'volumes/NHxxLO_xxxx_v1/NHLALO_2001/data/20060224_000310/lor_0003103486_0x630_sci_1.lbl'],
          ('browse',
           10,
           'browse_thumb',
           'Browse Image (thumbnail)',
           False): ['previews/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x631_eng_thumb.jpg',
                    'previews/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng_thumb.jpg'],
          ('browse',
           20,
           'browse_small',
           'Browse Image (small)',
           False): ['previews/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x631_eng_small.jpg',
                    'previews/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng_small.jpg'],
          ('browse',
           30,
           'browse_medium',
           'Browse Image (medium)',
           False): ['previews/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x631_eng_med.jpg',
                    'previews/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng_med.jpg'],
          ('browse',
           40,
           'browse_full',
           'Browse Image (full)',
           True): ['previews/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x631_eng_full.jpg',
                   'previews/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng_full.jpg'],
           ('New Horizons LORRI',
            200,
            'nh_lorri_calib_browse',
            'Extra Preview (calibrated)',
            False): ['previews/NHxxLO_xxxx/NHLALO_2001/data/20060224_000310/lor_0003103486_0x631_sci_thumb.jpg',
                     'previews/NHxxLO_xxxx/NHLALO_2001/data/20060224_000310/lor_0003103486_0x631_sci_small.jpg',
                     'previews/NHxxLO_xxxx/NHLALO_2001/data/20060224_000310/lor_0003103486_0x631_sci_med.jpg',
                     'previews/NHxxLO_xxxx/NHLALO_2001/data/20060224_000310/lor_0003103486_0x631_sci_full.jpg',
                     'previews/NHxxLO_xxxx/NHLALO_2001/data/20060224_000310/lor_0003103486_0x630_sci_thumb.jpg',
                     'previews/NHxxLO_xxxx/NHLALO_2001/data/20060224_000310/lor_0003103486_0x630_sci_small.jpg',
                     'previews/NHxxLO_xxxx/NHLALO_2001/data/20060224_000310/lor_0003103486_0x630_sci_med.jpg',
                     'previews/NHxxLO_xxxx/NHLALO_2001/data/20060224_000310/lor_0003103486_0x630_sci_full.jpg'],
          ('metadata',
           20,
           'planet_geometry',
           'Planet Geometry Index',
           False): ['metadata/NHxxLO_xxxx/NHLALO_1001/NHLALO_1001_jupiter_summary.tab',
                    'metadata/NHxxLO_xxxx/NHLALO_1001/NHLALO_1001_jupiter_summary.lbl'],
          ('metadata',
           30,
           'moon_geometry',
           'Moon Geometry Index',
           False): ['metadata/NHxxLO_xxxx/NHLALO_1001/NHLALO_1001_moon_summary.tab',
                    'metadata/NHxxLO_xxxx/NHLALO_1001/NHLALO_1001_moon_summary.lbl'],
          ('metadata',
           40,
           'ring_geometry',
           'Ring Geometry Index',
           False): ['metadata/NHxxLO_xxxx/NHLALO_1001/NHLALO_1001_ring_summary.tab',
                    'metadata/NHxxLO_xxxx/NHLALO_1001/NHLALO_1001_ring_summary.lbl'],
          ('metadata',
           10,
           'inventory',
           'Target Body Inventory',
           False): ['metadata/NHxxLO_xxxx/NHLALO_1001/NHLALO_1001_inventory.csv',
                    'metadata/NHxxLO_xxxx/NHLALO_1001/NHLALO_1001_inventory.lbl'],
          ('metadata',
           5,
           'rms_index',
           'RMS Node Augmented Index',
           False): ['metadata/NHxxLO_xxxx/NHLALO_1001/NHLALO_1001_index.tab',
                    'metadata/NHxxLO_xxxx/NHLALO_1001/NHLALO_1001_index.lbl'],
          ('metadata',
           9,
           'supplemental_index',
           'Supplemental Index',
           False): ['metadata/NHxxLO_xxxx/NHLALO_1001/NHLALO_1001_supplemental_index.tab',
                    'metadata/NHxxLO_xxxx/NHLALO_1001/NHLALO_1001_supplemental_index.lbl'],
          ('New Horizons LORRI',
           50,
           'nh_lorri_raw_alternate',
           'Raw Image Alternate Downlink',
           True): ['volumes/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x631_eng.fit',
                   'volumes/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x631_eng.lbl',
                   'volumes/NHxxLO_xxxx_v3/NHLALO_1001/data/20060224_000310/lor_0003103486_0x631_eng_1.fit',
                   'volumes/NHxxLO_xxxx_v3/NHLALO_1001/data/20060224_000310/lor_0003103486_0x631_eng_1.lbl',
                   'volumes/NHxxLO_xxxx_v2/NHLALO_1001/data/20060224_000310/lor_0003103486_0x631_eng_1.fit',
                   'volumes/NHxxLO_xxxx_v2/NHLALO_1001/data/20060224_000310/lor_0003103486_0x631_eng_1.lbl',
                   'volumes/NHxxLO_xxxx_v1/NHLALO_1001/data/20060224_000310/lor_0003103486_0x631_eng_1.fit',
                   'volumes/NHxxLO_xxxx_v1/NHLALO_1001/data/20060224_000310/lor_0003103486_0x631_eng_1.lbl'],
          ('New Horizons LORRI',
           150,
           'nh_lorri_calib_alternate',
           'Calibrated Image Alternate Downlink',
           True): ['volumes/NHxxLO_xxxx/NHLALO_2001/data/20060224_000310/lor_0003103486_0x631_sci.fit',
                   'volumes/NHxxLO_xxxx/NHLALO_2001/data/20060224_000310/lor_0003103486_0x631_sci.lbl',
                   'volumes/NHxxLO_xxxx_v3/NHLALO_2001/data/20060224_000310/lor_0003103486_0x631_sci_1.fit',
                   'volumes/NHxxLO_xxxx_v3/NHLALO_2001/data/20060224_000310/lor_0003103486_0x631_sci_1.lbl',
                   'volumes/NHxxLO_xxxx_v2/NHLALO_2001/data/20060224_000310/lor_0003103486_0x631_sci_1.fit',
                   'volumes/NHxxLO_xxxx_v2/NHLALO_2001/data/20060224_000310/lor_0003103486_0x631_sci_1.lbl',
                   'volumes/NHxxLO_xxxx_v1/NHLALO_2001/data/20060224_000310/lor_0003103486_0x631_sci_1.fit',
                   'volumes/NHxxLO_xxxx_v1/NHLALO_2001/data/20060224_000310/lor_0003103486_0x631_sci_1.lbl']}
        )
    ]
)
def test_opus_products(input_path, expected):
    opus_products_test(input_path, expected)
    
####################################################################################################################################
