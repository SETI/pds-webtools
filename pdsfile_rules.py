####################################################################################################################################
# rules/__init__.py
#
# Definitions of Translator objects used by the PdsFile class.
####################################################################################################################################
# DESCRIPTION_AND_ICON
#
# Translates an absolute file path within any directory tree to a brief description of the file and an associated icon type.
####################################################################################################################################

import re
import translator

GENERIC_VOLUME_DESC = 'Data volume'
GENERIC_VOLSET_DESC = 'Volume collection'

DESCRIPTION_AND_ICON = translator.TranslatorByRegex([

    # PDS3 labels
    (r'.*\.lbl', re.I, ('PDS3 label', 'LABEL')),

    # Checksums
    (r'checksums-archives-\w+', 0, ('<em>Checksums</em> of downloadable archives', 'CHECKDIR')),
    (r'checksums-calibrated',   0, ('<em>Checksums</em> of calibrated products',   'CHECKDIR')),
    (r'checksums-diagrams',     0, ('<em>Checksums</em> of observation diagrams',  'CHECKDIR')),
    (r'checksums-metadata',     0, ('<em>Checksums</em> of indices and metadata',  'CHECKDIR')),
    (r'checksums-previews',     0, ('<em>Checksums</em> of preview images',        'CHECKDIR')),
    (r'checksums-volumes',      0, ('<em>Checksums</em> of PDS volumes',           'CHECKDIR')),

    (r'checksums-archives-\w+/.*_md5\.txt', 0, ('Checksum index of downloadable archives', 'CHECKSUM')),
    (r'checksums-calibrated/.*_md5\.txt',   0, ('Checksum index of calibrated products',   'CHECKSUM')),
    (r'checksums-diagrams/.*_md5\.txt',     0, ('Checksum index of observation diagrams',  'CHECKSUM')),
    (r'checksums-metadata/.*_md5\.txt',     0, ('Checksum index of indices and metadatas', 'CHECKSUM')),
    (r'checksums-previews/.*_md5\.txt',     0, ('Checksum index of preview images',        'CHECKSUM')),
    (r'checksums-volumes/.*_md5\.txt',      0, ('Checksum index of entire volume',         'CHECKSUM')),

    # Archives
    (r'archives-calibrated', 0, ('<em>Downloadable archives</em> of calibrated products',  'TOPFILE')),
    (r'archives-diagrams',   0, ('<em>Downloadable archives</em> of observation diagrams', 'TOPFILE')),
    (r'archives-metadata',   0, ('<em>Downloadable archives</em> of indices and metadata', 'TOPFILE')),
    (r'archives-previews',   0, ('<em>Downloadable archives</em> of preview images',       'TOPFILE')),
    (r'archives-volumes',    0, ('<em>Downloadable archives</em> of PDS volumes',          'TOPFILE')),

    (r'archives-calibrated/[^/]+', 0, ('Downloadable archives of calibrated products',  'TARDIR')),
    (r'archives-diagrams/[^/]+',   0, ('Downloadable archives of observation diagrams', 'TARDIR')),
    (r'archives-metadata/[^/]+',   0, ('Downloadable archives of indices and metadata', 'TARDIR')),
    (r'archives-previews/[^/]+',   0, ('Downloadable archives of preview images',       'TARDIR')),
    (r'archives-volumes/[^/]+',    0, ('Downloadable archives of PDS volumes',          'TARDIR')),

    (r'archives-calibrated/[^/]+/.*\.tar\.gz', 0, ('Downloadable archive of calibrated products',  'TARBALL')),
    (r'archives-diagrams/[^/]+/.*\.tar\.gz',   0, ('Downloadable archive of observation diagrams', 'TARBALL')),
    (r'archives-metadata/[^/]+/.*\.tar\.gz',   0, ('Downloadable archive of indices and metadata', 'TARBALL')),
    (r'archives-previews/[^/]+/.*\.tar\.gz',   0, ('Downloadable archive of preview images',       'TARBALL')),
    (r'archives-volumes/[^/]+/.*\.tar\.gz',    0, ('Downloadable archive of entire PDS volume',    'TARBALL')),

    # Volume types
    (r'volumes',                0, ('<em>PDS volumes</em> in Viewmaster', 'TOPFILE')),
    (r'volumes/[^/]+$',         0, (GENERIC_VOLSET_DESC, 'VOLDIR')),
    (r'volumes/[^/]+$',         0, (GENERIC_VOLSET_DESC, 'VOLDIR')),
    (r'volumes/[^/]+/[^/]+$',   0, (GENERIC_VOLUME_DESC, 'VOLUME')),

    (r'calibrated',       0, ('<em>Calibrated products</em> created by Node',     'TOPFILE')),
    (r'diagrams',         0, ('<em>Observation diagrams</em> created by Node',    'TOPFILE')),
    (r'metadata',         0, ('<em>Supplemental metadata</em> generated by Node', 'TOPFILE')),
    (r'previews',         0, ('<em>Preview images</em> created by Node',          'TOPFILE')),

    (r'calibrated/[^/]+', 0, ('Calibrated products created by Node',     'DATADIR' )),
    (r'diagrams/[^/]+',   0, ('Observation diagrams created by Node',    'GEOMDIR' )),
    (r'metadata/[^/]+',   0, ('Supplemental metadata generated by Node', 'INDEXDIR')),
    (r'previews/[^/]+',   0, ('Preview images created by Node',          'IMAGEDIR')),

    (r'calibrated/[^/]+/[^/]+',    0, ('Calibrated products for volume',               'DATADIR' )),
    (r'diagrams/[^/]+/[^/]+',      0, ('Observation diagrams for volume',              'GEOMDIR' )),
    (r'metadata/[^/]+/[^/]+999',   0, ('Cumulative supplemental metadata for volumes', 'INDEXDIR')),
    (r'metadata/[^/]+/[^/]+',      0, ('Supplemental metadata for volume',             'INDEXDIR')),
    (r'previews/[^/]+/[^/]+',      0, ('Preview images for volume',                    'IMAGEDIR')),

    # Metadata directory file names
    (r'metadata/.*999.*_index\.tab',           0, ('Cumulative product index of volume series',       'INDEX')),
    (r'metadata/.*999.*_inventory\.tab',       0, ('Cumulative list of observed bodies by product',   'INDEX')),
    (r'metadata/.*999.*_moon_summary\.tab',    0, ('Cumulative list of observed geometry on moons',   'INDEX')),
    (r'metadata/.*999.*_ring_summary\.tab',    0, ('Cumulative list of observed geometry on rings',   'INDEX')),
    (r'metadata/.*999.*_saturn_summary\.tab',  0, ('Cumulative list of observed geometry on Saturn',  'INDEX')),
    (r'metadata/.*999.*_jupiter_summary\.tab', 0, ('Cumulative list of observed geometry on Jupiter', 'INDEX')),
    (r'metadata/.*999.*_uranus_summary\.tab',  0, ('Cumulative list of observed geometry on Uranus',  'INDEX')),
    (r'metadata/.*999.*_neptune_summary\.tab', 0, ('Cumulative list of observed geometry on Neptune', 'INDEX')),
    (r'metadata/.*999.*_pluto_summary\.tab',   0, ('Cumulative list of observed geometry on Pluto',   'INDEX')),
    (r'metadata/.*999.*_charon_summary\.tab',  0, ('Cumulative list of observed geometry on Charon',  'INDEX')),

    (r'metadata/.*_index\.tab',           0, ('Product index generated by data provider', 'INDEX')),
    (r'metadata/.*_inventory\.tab',       0, ('List of observed bodies by product',      'INDEX')),
    (r'metadata/.*_moon_summary\.tab',    0, ('Index of observed geometry on moons',     'INDEX')),
    (r'metadata/.*_ring_summary\.tab',    0, ('Index of observed geometry on rings',     'INDEX')),
    (r'metadata/.*_saturn_summary\.tab',  0, ('Index of observed geometry on Saturn',    'INDEX')),
    (r'metadata/.*_jupiter_summary\.tab', 0, ('Index of observed geometry on Jupiter',   'INDEX')),
    (r'metadata/.*_uranus_summary\.tab',  0, ('Index of observed geometry on Uranus',    'INDEX')),
    (r'metadata/.*_neptune_summary\.tab', 0, ('Index of observed geometry on Neptune',   'INDEX')),
    (r'metadata/.*_pluto_summary\.tab',   0, ('Index of observed geometry on Pluto',     'INDEX')),
    (r'metadata/.*_charon_summary\.tab',  0, ('Index of observed geometry on Charon',    'INDEX')),

    # Previews and diagrams
    (r'(previews|diagrams)/.*_thumb\.(jpg|png)', 0, ('Thumbnail preview image',       'BROWSE')),
    (r'(previews|diagrams)/.*_small\.(jpg|png)', 0, ('Small preview image',           'BROWSE')),
    (r'(previews|diagrams)/.*_med\.(jpg|png)',   0, ('Medium preview image',          'BROWSE')),
    (r'(previews|diagrams)/.*_full\.(jpg|png)',  0, ('Full-resolution preview image', 'BROWSE')),
    (r'previews/.*',                             0, ('Preview images',                'BROWDIR')),
    (r'diagrams/.*',                             0, ('Observation diagrams',          'BROWDIR')),

    # Standard information files
    (r'.*/aareadme\.(txt|vms)',         re.I, ('Read Me First!',                'INFO'    )),
    (r'.*/voldesc\.(cat|sfd)',          re.I, ('Volume description',            'INFO'    )),
    (r'.*/errata\.txt',                 re.I, ('Errata file',                   'INFO'    )),
    (r'.*info\.txt',                    re.I, ('Info about this directory',     'INFO'    )),
    (r'.*/vicar2.txt',                  re.I, ('VICAR documentation',           'INFO'    )),
    (r'.*/fitsinfo\..*',                re.I, ('FITS documentation',            'INFO'    )),

    # Data file types, misc.
    (r'.*/easydata(/\w+)*',             re.I, ('Easy-to-use data',              'DATADIR' )),
    (r'.*/sorcdata(/\w+)*',             re.I, ('Original source data',          'DATADIR' )),
    (r'.*/spice(/\w+)*',                re.I, ('SPICE kernels',                 'GEOMDIR' )),

    # Browse directories
    (r'.*/browse(/\w+)*',               re.I, ('Browse image collection',       'BROWDIR' )),
    (r'.*/browse/.*\.(gif|jpg|jpeg|jpeg_small|tif|tiff|png)', 
                                        re.I, ('Browse image',                  'BROWSE'  )),

    # Extras directories
    (r'.*/extras(/\w+)*',               re.I, ('Supplemental files',            'EXTRADIR')),

    # Document directories
    (r'.*/document/.*\.(txt|asc)',      re.I, ('Text document',                 'INFO'    )),
    (r'.*/document(/\w+)*(|/)',         re.I, ('Documentation',                 'INFODIR' )),
    (r'.*/document/.*\.(gif|jpg|jpeg|tif|tiff|png)', 
                                        re.I, ('Documentation figure',          'BROWSE'  )),
    (r'.*\.asc',                        re.I, ('ASCII document',                'INFO'    )),
    (r'.*\.pdf',                        re.I, ('PDF document',                  'INFO'    )),
    (r'.*\.(eps|ps)',                   re.I, ('Postscript document',           'INFO'    )),
    (r'.*\.(htm|html)',                 re.I, ('HTML document',                 'INFO'    )),
    (r'.*\.doc',                        re.I, ('Word document',                 'INFO'    )),

    # Software directories
    (r'.*/software(.*)/bin/\w+',        re.I, ('Program binary',                'CODE'    )),
    (r'.*/software(.*)README',          re.I, ('Software documentation',        'INFO'    )),
    (r'.*/software(.*)CHANGES',         re.I, ('Software documentation',        'INFO'    )),
    (r'.*/software(.*)Makefile.*',      re.I, ('Source code',                   'CODE'    )),
    (r'.*/software(/\w+)*',             re.I, ('Software directory',            'CODEDIR' )),
    (r'.*/software/.*\.(TXT|PDF|PS|EPS|ASC|HTM|HTML|DOC)', 
                                        re.I, ('Software documentation',        'INFO'    )),

    # Catalog file names gleaned from the archives
    (r'.*/catalog(|/)',                 re.I, ('PDS3 Catalog files',            'INFODIR' )),
    (r'.*/catalog/DATASET\.CAT',        re.I, ('Data set description',          'INFO'    )),
    (r'.*/catalog/.*DS\.CAT',           re.I, ('Data set description',          'INFO'    )),
    (r'.*/catalog/.*DSCOLL\.CAT',       re.I, ('Collection description',        'INFO'    )),
    (r'.*/catalog/.*(HOST|SC)\.CAT',    re.I, ('Instrument host description',   'INFO'    )),
    (r'.*/catalog/PERS\w*\.CAT',        re.I, ('Personnel summary',             'INFO'    )),
    (r'.*/catalog/MISSION\.CAT',        re.I, ('Mission description',           'INFO'    )),
    (r'.*/catalog/.*REF\.CAT',          re.I, ('Reference list',                'INFO'    )),
    (r'.*/catalog/.*INST\.CAT',         re.I, ('Instrument description',        'INFO'    )),
    (r'.*/catalog/.*RELEASE\.CAT',      re.I, ('Release information',           'INFO'    )),
    (r'.*/catalog/CALIBRATION\.CAT',    re.I, ('Calibration information',       'INFO'    )),
    (r'.*/catalog/.*TARGET\.CAT',       re.I, ('Target information',            'INFO'    )),
    (r'.*/catalog/SOFTWARE\.CAT',       re.I, ('Software information',          'INFO'    )),

    # Index files
    ('.*/index/cum.*\.tab',             re.I, ('Cumulative index',              'INDEX'   )),
    ('.*/index/.*\.tab',                re.I, ('Index table',                   'INDEX'   )),

    # SPICE kernels
    (r'.*\.(bsp|spk)',                  re.I, ('SPICE trajectory kernel',       'GEOM'    )),
    (r'.*\.(ck|bc)',                    re.I, ('SPICE pointing kernel',         'GEOM'    )),
    (r'.*\.(pck|tpc)',                  re.I, ('SPICE constants kernel',        'GEOM'    )),
    (r'.*\.tf',                         re.I, ('SPICE frames kernel',           'GEOM'    )),
    (r'.*\.ti',                         re.I, ('SPICE instrument kernel',       'GEOM'    )),
    (r'.*\.(lsk|tls)',                  re.I, ('SPICE leapseconds kernel',      'GEOM'    )),
    (r'.*\.tsc',                        re.I, ('SPICE spacecraft clock kernel', 'GEOM'    )),

    (r'.*/ck',                          re.I, ('SPICE pointing kernels',        'GEOMDIR' )),
    (r'.*/ek',                          re.I, ('SPICE events kernels',          'GEOMDIR' )),
    (r'.*/fk',                          re.I, ('SPICE frames kernels',          'GEOMDIR' )),
    (r'.*/ik',                          re.I, ('SPICE instrument kernels',      'GEOMDIR' )),
    (r'.*/lsk',                         re.I, ('SPICE leap seconds kernels',    'GEOMDIR' )),
    (r'.*/pck',                         re.I, ('SPICE constants kernels',       'GEOMDIR' )),
    (r'.*/sclk',                        re.I, ('SPICE SC clock kernels',        'GEOMDIR' )),
    (r'.*/spk',                         re.I, ('SPICE trajectory kernels',      'GEOMDIR' )),

    # Other standard directories
    (r'.*/calib(/\w+)*',                re.I, ('Calibration files',             'DATADIR' )),
    (r'.*/geometry(/\w+)*',             re.I, ('Geometry files',                'GEOMDIR' )),
    (r'.*/index',                       re.I, ('Index files',                   'INDEXDIR')),
    (r'.*/label',                       re.I, ('PDS3 label include files',      'LABELDIR')),
    (r'.*/data(/\w+)*',                 re.I, ('Data files',                    'DATADIR' )),

    # Standard file extensions, if nothing else worked
    (r'.*\.img',                        re.I, ('Binary image file',             'IMAGE'   )),
    (r'.*\.(tab|csv)',                  re.I, ('ASCII table',                   'TABLE'   )),
    (r'.*\.dat',                        re.I, ('Binary data file',              'DATA'    )),
    (r'.*\.fits{0,1}',                  re.I, ('FITS data file',                'DATA'    )),
    (r'.*\.(c|q)ub',                    re.I, ('Spectral image cube',           'CUBE'    )),
    (r'.*\.fmt',                        re.I, ('PDS3 label include file',       'LABEL'   )),
    (r'.*\.txt',                        re.I, ('Text file',                     'INFO'    )),
    (r'.*\.tar.gz',                     re.I, ('Compressed tar archive',        'TARBALL' )),
    (r'.*\.tar',                        re.I, ('Tar archive',                   'TARBALL' )),
    (r'.*\.zip',                        re.I, ('Zip archive',                   'TARBALL' )),
    (r'.*\.(jpg|jpeg|jpeg_small)',      re.I, ('JPEG viewable image',           'BROWSE'  )),
    (r'.*\.gif',                        re.I, ('GIF vewable image',             'BROWSE'  )),
    (r'.*\.(tif|tiff)',                 re.I, ('TIFF viewable image',           'BROWSE'  )),
    (r'.*\.png',                        re.I, ('PNG viewable image',            'BROWSE'  )),
    (r'.*\.sav',                        re.I, ('IDL save file',                 'DATA'    )),

    (r'.*\.(f|for|f77|inc)',            re.I, ('FORTRAN source code',           'CODE'    )),
    (r'.*\.(c|h)',                      re.I, ('C source code',                 'CODE'    )),
    (r'.*\.cpp',                        re.I, ('C++ source code',               'CODE'    )),
    (r'.*\.py',                         re.I, ('Python source code',            'CODE'    )),
    (r'.*\.(sh|com|csh)',               re.I, ('Shell script',                  'CODE'    )),
    (r'.*\.(pro|idl)',                  re.I, ('IDL source code',               'CODE'    )),
    (r'.*\.(jar|java)',                 re.I, ('Java source code',              'CODE'    )),
    (r'.*\.(pl|pm)',                    re.I, ('Perl source code',              'CODE'    )),
    (r'.*\.a',                          re.I, ('Unix object library',           'CODE'    )),
    (r'.*\.o',                          re.I, ('Unix object file',              'CODE'    )),

    (r'',                               0,    ('Root directory',                'FOLDER'  )),
    (r'.*/[^\.]+',                      0,    ('Directory',                     'FOLDER'  )),
    (r'.*\..*',                         0,    ('Document',                      'UNKNOWN' )),
])

####################################################################################################################################
# ASSOCIATIONS
#
# Used for defining the default places of directories associated with a particular directory elsewhere in the tree, as part of
# another version or category of file.
####################################################################################################################################

ASSOCIATIONS_TO_VOLUMES = translator.TranslatorByRegex([
    (r'metadata/(\w+)/.*999.*', 0, r'volumes/\1'),
    (r'[a-z]+/(.*)', 0, r'volumes/\1')
])

VOLUMES_TO_CALIBRATED = translator.TranslatorByRegex([
    (r'volumes/(.*)', 0, r'calibrated/\1')
])

VOLUMES_TO_DIAGRAMS = translator.TranslatorByRegex([
    (r'volumes/(.*)\.(\w+)', 0, [r'diagrams/\1_thumb.*',
                                 r'diagrams/\1_small.*',
                                 r'diagrams/\1_med.*',
                                 r'diagrams/\1_full.*']),
    (r'volumes/(.*)', 0, r'diagrams/\1')
])

VOLUMES_TO_METADATA = translator.TranslatorByRegex([
    (r'volumes/(\w+)/(\w+)(|/index)', re.I, [r'metadata/\1/\2',
                                             r'metadata/\1/*999*']),
    (r'volumes/(.*)', 0, r'metadata/\1')
])

VOLUMES_TO_PREVIEWS = translator.TranslatorByRegex([
    (r'volumes/(.*)\.(\w+)', 0,  [r'previews/\1_thumb.*',
                                  r'previews/\1_small.*',
                                  r'previews/\1_med.*',
                                  r'previews/\1_full.*']),
    (r'volumes/(.*)', 0, r'previews/\1')
])

VOLUMES_TO_VOLUMES = translator.SelfTranslator()

# Group translators into dictionaries
VOLUMES_TO_ASSOCIATIONS = {
    'calibrated': VOLUMES_TO_CALIBRATED,
    'diagrams':   VOLUMES_TO_DIAGRAMS,
    'metadata':   VOLUMES_TO_METADATA,
    'previews':   VOLUMES_TO_PREVIEWS,
    'volumes':    VOLUMES_TO_VOLUMES,
}

####################################################################################################################################
# VIEWABLES
#
# A dictionary of translators, each of which translates a file path to a set of viewables. The key 'default' defines the viewable
# used by default.
####################################################################################################################################

VIEWABLES = {'default': translator.NullTranslator()}

####################################################################################################################################
# VIEW_OPTIONS
#
# Given a file path, returns (grid_flag, multipage_flag, continuous_flag). Each flag indicates True if that particular options is
# allowed for this directory.
####################################################################################################################################

VIEW_OPTIONS = translator.TranslatorByRegex([
    (r'.*', 0, (False, True, False)),       # default is for discontinuous multipage viewing
])

####################################################################################################################################
# NEIGHBORS
#
# Given a directory path, return the file fnmatch pattern to indicate other directories to be treated as adjacent.
####################################################################################################################################

NEIGHBORS = translator.TranslatorByRegex([
    (r'(\w+/\w+/)\w+',                   0, r'\1*'),
    (r'(\w+/\w+/)\w+(/\w+)',             0, r'\1*\2'),
    (r'(\w+/\w+/)\w+(/\w+/w+)',          0, r'\1*\2'),
    (r'(\w+/\w+/)\w+(/\w+/\w+/\w+)',     0, r'\1*\2'),
    (r'(\w+/\w+/)\w+(/\w+/\w+/\w+/\w+)', 0, r'\1*\2'),
])

####################################################################################################################################
# INFO_FILE_BASENAMES
#
# Translates a file basename it itself if it is a suitable information file about the directory in which it is found.
####################################################################################################################################

INFO_FILE_BASENAMES = translator.TranslatorByRegex([
    (r'(voldesc\.(?:cat|sfd))', re.I, r'\1'),
    (r'(\w+INFO\.txt)',         re.I, r'\1'),
    (r'(\w+INF\.txt)',          re.I, r'\1'),
])

####################################################################################################################################
# SORT_KEY
#
# Translates a file basename into a key used for sorting. For example, this is used to force COISS data files to sort
# chronologically, by ignoring the leading "N" or "W".
####################################################################################################################################

SORT_KEY = translator.TranslatorByRegex([

    # Previews sort into increasing size
    (r'(.*)_thumb\.(jpg|png)', 0, r'\1_1thumb.\2'),
    (r'(.*)_small\.(jpg|png)', 0, r'\1_2small.\2'),
    (r'(.*)_med\.(jpg|png)',   0, r'\1_3med.\2'  ),
    (r'(.*)_full\.(jpg|png)',  0, r'\1_9full.\2' ),

    # If all else fails, sort alphabetically
    (r'(.*)', 0, r'\1'),
])

####################################################################################################################################
# SPLIT_RULES
#
# Used for defining how to group files by separating a leading anchor, which is possibly shared among multiple files, with an
# optional middle part and an extension.
#
# These translations take a file basename and return a tuple of three strings that concatenate to the original basename.
#
# Note that they must also work for the sort keys of basenames.
####################################################################################################################################

SPLIT_RULES = translator.TranslatorByRegex([

    # Preview files (before and after SORT_RULES were applied)
    (r'(.*)_(thumb|small|med|full)\.(jpg|png)$',     0, (r'\1', r'_\2', r'.\3')),
    (r'(.*)_(1thumb|2small|3med|9full)\.(jpg|png)$', 0, (r'\1', r'_\2', r'.\3')),

    # Calibrated images
    (r'(.*)(_CALIB)\.(IMG|LBL)$', re.I, (r'\1', r'\2', r'.\3')),

    # If all else fails, split at last period
    (r'(.*)(\..*)', 0, (r'\1', '', r'\2')),
    (r'(.*)',       0, (r'\1', '', '')),
])

####################################################################################################################################
# OPUS_TYPE
#
# Used for indicating the type of a data file as it will appear in OPUS, e.g., "Raw Data", "Calibrated Data", etc.
#
# These translations take a file's logical path and return a string indicating the file's OPUS_TYPE.
####################################################################################################################################

OPUS_TYPE = translator.TranslatorByRegex([

    # Default for a volumes directory is raw data with an indication that calibrated products are unavailable
    (r'volumes/[^/]+/[^/]+/data/.*\..*', re.I, 'Raw Data (calibrated unavailable)'),

    # Previews
    (r'previews/.*\_thumb\..*$', 0, 'Browse Image (thumbnail)'),
    (r'previews/.*\_small\..*$', 0, 'Browse Image (small)'),
    (r'previews/.*\_med\..*$',   0, 'Browse Image (medium)'),
    (r'previews/.*\_full\..*$',  0, 'Browse Image (full-size)'),

    # Diagrams
    (r'diagrams/.*\_thumb\..*$', 0, 'Browse Diagram (thumbnail)'),
    (r'diagrams/.*\_small\..*$', 0, 'Browse Diagram (small)'),
    (r'diagrams/.*\_med\..*$',   0, 'Browse Diagram (medium)'),
    (r'diagrams/.*\_full\..*$',  0, 'Browse Diagram (full-size)'),

    # Metadata
    (r'metadata/.*_inventory\..*', 0, 'Target Body Inventory'),
    (r'metadata/.*_ring_summary\..*', 0, 'Ring Geometry Index'),
    (r'metadata/.*_(moon|charon)_summary\..*', 0, 'Satellite Geometry Index'),
    (r'metadata/.*_(jupiter|saturn|uranus|neptune|pluto)_summary\..*', 0, 'Planet Geometry Index'),
])

####################################################################################################################################
# OPUS_FORMAT
#
# Returns a tuple (interchange format, file format) where the first is 'Binary', 'ASCII' or 'UTF-8' and the latter is the format
# of the file, e.g., 'Vicar', 'FITS', 'Table', 'PDS3 Label', etc.
####################################################################################################################################

OPUS_FORMAT = translator.TranslatorByRegex([
    (r'.*\.LBL$',     0, ('ASCII',  'PDS3 Label')),
    (r'.*\.TAB$',     0, ('ASCII',  'Table')),
    (r'.*\.FMT$',     0, ('ASCII',  'PDS3 Format File')),
    (r'.*\.CSV$',     0, ('ASCII',  'Comma-Separated Values')),
    (r'.*\.TXT$',     0, ('ASCII',  'Text')),
    (r'.*\.ASC$',     0, ('ASCII',  'Text')),
    (r'.*\.FIT(|S)$', 0, ('Binary', 'FITS')),
    (r'.*\.TIF(|F)$', 0, ('Binary', 'TIFF')),
    (r'.*\.JPG$',     0, ('Binary', 'JPEG')),
    (r'.*\.GIF$',     0, ('Binary', 'GIF')),
    (r'.*\.PNG$',     0, ('Binary', 'PNG')),
    (r'.*\.PDF$',     0, ('Binary', 'PDF')),
    (r'.*\.BSP$',     0, ('Binary', 'SPICE SPK')),
    (r'.*\.BC$',      0, ('Binary', 'SPICE CK')),
    (r'.*\.TPC$',     0, ('ASCII',  'SPICE PCK')),
    (r'.*\.TLS$',     0, ('ASCII',  'SPICE LSK')),
    (r'.*\.TI$',      0, ('ASCII',  'SPICE IK')),
])

####################################################################################################################################
# OPUS_PRODUCTS
#
# Returns a list of glob.glob() patterns that match the absolute paths to the all associated files for an OPUS
# query, given the logical path to the primary data file or its label.
####################################################################################################################################

# Default is to return an empty list
OPUS_PRODUCTS = translator.TranslatorByRegex([
    (r'.*', 0, []),
])

####################################################################################################################################
# OPUS_ID_TO_FILESPEC
#
# Translates an OPUS ID to the volume ID + file specification path of the primary data product.
# Note: This is a class attribute, not an object attribute. It is shared by all subclasses.
####################################################################################################################################

OPUS_ID_TO_FILESPEC = translator.TranslatorByRegex([])

####################################################################################################################################
# FILESPEC_TO_OPUS_ID
#
# Translates a volume ID + file specification path to an OPUS ID.
####################################################################################################################################

FILESPEC_TO_OPUS_ID = translator.TranslatorByRegex([])

####################################################################################################################################
# FILESPEC_TO_LOGICAL_PATH
#
# Translates a volume ID + file specification path to a logical path.
# Note: This is a class attribute, not an object attribute. It is shared by all subclasses.
####################################################################################################################################

# Default rules assume that the volset is the volume ID with the last three digits replaced by "xxx"
FILESPEC_TO_LOGICAL_PATH = translator.TranslatorByRegex([
    (r'([A-Z0-9]{2,6}_[0-9])([0-9]{3}.*_(thumb|small|med|full)\.(jpg|png|pdf))', 0,    r'previews/\1xxx/\1\2'),
    (r'([A-Z0-9]{2,6}_[0-9])([0-9]{3}.*_CALIB\.(IMG|LBL))',                      re.I, r'calibrated/\1xxx/\1\2'),
    (r'([A-Z0-9]{2,6}_[0-9])([0-9]{3}.*)',                                       0,    r'volumes/\1xxx/\1\2'),
])

####################################################################################################################################
