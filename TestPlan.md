## Test plan for PdsFile
Date: 05/05/20<br />
Author: Dave Chang
### Objective:
* Check pdsfile classes to identify properties and functions that need to have either black box or white box testing.
* We will mainly focus on unit testing for now.
* Will use code coverage (https://coverage.readthedocs.io/en/coverage-5.1/) to find the miss tests.

### Black box test:
* Test for external properties/functions that do not cached:
    * Test method:
        1. Manually come up with the expected results and store them first.
        2. Call the target property/function and check if the result is as expected (from step 1).
    * Files needed: one viewable file, one .lbl/.dat file per volume (can have multiple different files from different instruments), and one index file. For testing translator functions, we need one file from each instrument with customized rules.
    * Lists of targeted external properties:
        * **PdsFile:**
            * The following can be tested using .lbl/.dat file, ex: 'pdsdata/holdings/volumes/COUVIS_0xxx/COUVIS_0002/DATA/D2001_090/HDAC2001_090_23_55.DAT'
                * exists
                * filespec (volname)
                * islabel
                * absolute_or_logical_path
                * html_path (or url)
                * extension
                * parent_logical_path
                * anchor
                * description
                * icon_type
                * label_basename (info_basename (check if corresponding .LBL exists))
                * label_abspath
                * \_volume_info
                * opus_id
            * The following require a viewable file for testing (jpegs, tiffs, pngs), ex: 'pdsdata/holdings/previews/COUVIS_0xxx/COUVIS_0002/DATA/D2001_090/HDAC2001_090_23_55_thumb.png'
                * is_viewable
                * alt
                * viewset (need to check viewset_lookup('default'))
            * The following require a directory for testing, ex: 'pdsdata/holdings/volumes/COUVIS_0xxx/COUVIS_0002'
                * isdir
                * childnames (need to use a directory, parent directory of .DAT file can be used)
            * The following require a index file under /metadata, ex: 'pdsdata/holdings/metadata/COUVIS_0xxx/COUVIS_0002/COUVIS_0002_index.tab'
                * is_index
        * **PdsViewSet**
            * thumbnail
            * small
            * medium
            * full_size
    * Lists of targeted functions:
        * **PdsFile:**
            * Associations:
                * \_associated_paths
                * associated_logical_paths
                * associated_abspaths
                * associated_parallel
        * **TranslatorByRegex:**
            * all
            * first

* Test for CACHE:
    * Test method: call the target property twice and check if both results match, and also check if the result is the correct value.
    * Files needed: one viewable file and one .lbl/.dat file per volume (can have multiple different files from different instruments).
    * Lists of external properties that return self.\_*\_filled:
        * **PdsFile:**
            * isdir (return self.\_isdir_filled)
            * islabel (return self.\_islabel_filled)
            * is_viewable (return self.\_is_viewable_filled)
            * split (self.\_split_filled)
            * global_anchor (return self.\_global_anchor_filled)
            * childnames (return self.\_childnames_filled)
            * \_info (return self.\_info_filled)
            * date (return self.\_date_filled)
            * formatted_size (return self.\_formatted_size_filled)
            * \_volume_info (return self.\_volume_info_filled)
            * description (return  part of self.\_description_and_icon_filled)
            * icon_type (return  part of self.\_description_and_icon_filled)
            * mime_type (return self.\_mime_type_filled)
            * opus_id (return self.\_opus_id_filled)
            * opus_format (return self.\_opus_format_filled)
            * opus_type (return self.\_opus_type_filled)
            * info_basename (return self.\_info_basename_filled)
            * internal_link_info (return self.\_internal_links_filled)
            * label_basename (return self.\_label_basename_filled)
            * viewset (return self.\_viewset_filled)
            * local_viewset (return self.\_local_viewset_filled)
            * \_iconset (return part of self.\_iconset_filled)
            * volume_publication_date (return self.\_volume_publication_date_filled)
            * volume_version_id (return self.\_volume_version_id_filled)
            * volume_data_set_ids (return self.\_volume_data_set_ids_filled)
            * version_ranks (return self.\_version_ranks_filled)
            * exact_archive_url (return self.\_exact_archive_url_filled)
            * exact_checksum_url (return self.\_exact_checksum_url_filled)
            * filename_keylen (return self.\_filename_keylen_filled)


### White box test:
* Test for external properties/functions:
    * Test method:  
        * Path testing:
            * In each function, make sure each return path has been tested.
        * Condition testing:
            * In each function, make sure both conditions of every if statement has been tested.
        * Loop testing:
            * In each function, if there is a loop, make sure each break & continue condition is tested.
    * Files needed: one viewable file, one .lbl/.dat file per volume, and one index file. For testing associations & translator functions, we need one file from each instrument with customized rules.
    * Lists of targeted functions:
        * **PdsFile:**
            * viewset_lookup
            * volume_abspath
            * volset_abspath
            * checksum_path_and_lskip
            * archive_path_and_lskip
            * shelf_path_and_lskip
            * split_basename
            * sort_basenames
            * sort_logical_paths
            * is_logical_path
            * logical_path_from_abspath
            * from_logical_path
            * from_abspath
            * from_relative_path
            * from_path
            * opus_products
            * These need to be tested with a index file:
                * find_selected_row_number
                * find_row_number_at_or_below
                * cache_child_row_pdsfiles
                * row_pdsfile
                * nearest_row_pdsfile
                * data_pdsfile_for_index_and_selection
            * This needs to be tested with a directory:
                * group_children
            * Constructors:
                * parent
                * child
                * \_complete
                * \_recache
            * Shelf cache:
                * \_get_shelf
                * \_close_shelf
            * Associations:
                * \_associated_paths
                * associated_logical_paths
                * associated_abspaths
                * associated_parallel
        * **TranslatorByRegex:**
            * all
            * first

### Regression test:
* Test for external properties/functions:
    * Test target & files needed: same as ones from black box test.
    * Test method:
        1. For the very first time, call the target property/function and store the results as the golden copy.
        2. In the future, call the target property/function and compare the results with the golden copy. Check to see if the results change over time.

### List of files for testing: (continuously updating the list)
* COCIRS_0xxx:
    * holdings/volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.DAT
    * holdings/volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.lbl
* COCIRS_1xxx:
    * holdings/volumes/COCIRS_1xxx/COCIRS_1001/DATA/TSDR/NAV_DATA/TAR10013100.DAT
    * holdings/volumes/COCIRS_1xxx/COCIRS_1001/DATA/TSDR/NAV_DATA/TAR10013100.lbl
    * holdings/previews/COCIRS_1xxx/COCIRS_1001/DATA/CUBE/EQUIRECTANGULAR/123RI_EQLBS002_____CI____699_F1_039E_thumb.jpg
* COCIRS_5xxx:
    * holdings/volumes/COCIRS_5xxx/COCIRS_5401/DATA/GEODATA/GEO0401130240_699.TAB
    * holdings/volumes/COCIRS_5xxx/COCIRS_5401/DATA/GEODATA/GEO0401130240_699.lbl
    * holdings/diagrams/COCIRS_5xxx/COCIRS_5401/BROWSE/TARGETS/IMG0401130240_FP1_thumb.jpg
* COCIRS_6xxx:
    * holdings/volumes/COCIRS_6xxx/COCIRS_6004/DATA/GEODATA/GEO1004021018_699.TAB
    * holdings/volumes/COCIRS_6xxx/COCIRS_6004/DATA/GEODATA/GEO1004021018_699.lbl
    * holdings/diagrams/COCIRS_6xxx/COCIRS_6004/BROWSE/SATURN/POI1004010000_FP1_small.jpg
* COISS_0xxx:
    * holdings/volumes/COISS_0xxx/COISS_0001/data/wacfm/bit_wght/13302/133020.img
    * holdings/volumes/COISS_0xxx/COISS_0001/data/wacfm/bit_wght/13302/133020.lbl
* COISS_1xxx:
    * holdings/volumes/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1.lbl
    * holdings/volumes/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561202_1.IMG
    * holdings/previews/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561261_1_thumb.jpg
    * holdings/metadata/COISS_1xxx/COISS_1001/COISS_1001_inventory.tab
* COISS_2xxx:
    * holdings/volumes/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460960868_1.IMG
    * holdings/volumes/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460960868_1.lbl
    * holdings/previews/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460960908_1_thumb.jpg
    * holdings/metadata/COISS_2xxx/COISS_2002_inventory.tab
* COISS_3xxx:
    * holdings/volumes/COISS_3xxx/COISS_3002/data/maps/SE_400K_90S_0_SMN.lbl
    * holdings/previews/COISS_3xxx/COISS_3002/data/maps/SE_400K_0_108_SMN_thumb.png
* CORSS_8xxx:
    * holdings/volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_CAL.lbl
    * holdings/volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_CAL.tab
* COUVIS_0xxx:
    * holdings/volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31.dat
    * holdings/volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31.lbl
    * holdings/previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31_thumb.png
    * holdings/metadata/COUVIS_0xxx/COUVIS_0001/COUVIS_0001_index.tab
    * holdings/volumes/COUVIS_0xxx/COUVIS_0058/DATA/DATA/D2017_001/EUV2017_001_03_49.LBL
    * holdings/volumes/COUVIS_0xxx/COUVIS_0058/DATA/DATA/D2017_001/EUV2017_001_03_49.DAT
    * holdings/volumes/COUVIS_0xxx/COUVIS_0058/CALIB/VERSION_4/D2017_001/EUV2017_001_03_49_CAL_4.LBL
    * holdings/volumes/COUVIS_0xxx/COUVIS_0058/CALIB/VERSION_4/D2017_001/EUV2017_001_03_49_CAL_4.DAT
    * holdings/volumes/COUVIS_0xxx/COUVIS_0058/CALIB/VERSION_5/D2017_001/EUV2017_001_03_49_CAL_5.LBL
    * holdings/volumes/COUVIS_0xxx/COUVIS_0058/CALIB/VERSION_5/D2017_001/EUV2017_001_03_49_CAL_5.DAT
    * holdings/volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/FUV1999_007_16_57.DAT
    * holdings/volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/FUV1999_007_16_57.LBL
    * holdings/volumes/COUVIS_0xxx/COUVIS_0001/CALIB/VERSION_3/D1999_007/FUV1999_007_16_57_CAL_3.DAT
    * holdings/volumes/COUVIS_0xxx/COUVIS_0001/CALIB/VERSION_3/D1999_007/FUV1999_007_16_57_CAL_3.LBL
* COUVIS_0xxx_v1:
    * holdings/volumes/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274/EUV2004_274_01_39.lbl
    * holdings/volumes/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274/EUV2004_274_01_39.dat
    * holdings/previews/COUVIS_0xxx_v1/COUVIS_0009/DATA/EUV2004_274_01_39_thumb.png
    * holdings/previews/COUVIS_0xxx_v1/COUVIS_0009/DATA/EUV2004_274_02_25_med.png
    * holdings/previews/COUVIS_0xxx_v1/COUVIS_0009/DATA/EUV2004_274_07_10_full.png
    * holdings/previews/COUVIS_0xxx_v1/COUVIS_0009/DATA/EUV2004_274_09_50_small.png
* COUVIS_8xxx:
    * holdings/volumes/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2017_228_BETORI_I_TAU10KM.lbl
    * holdings/volumes/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2017_228_BETORI_I_TAU10KM.tab
* COVIMS_0xxx
    * holdings/volumes/COVIMS_0xxx/COVIMS_0001/data/1999010T054026_1999010T060958/v1294638283_1.lbl
    * holdings/volumes/COVIMS_0xxx/COVIMS_0001/data/1999010T054026_1999010T060958/v1294638283_1.qub
    * holdings/previews/COVIMS_0xxx/COVIMS_0001/data/1999010T054026_1999010T060958/v1294638283_1_thumb.png
    * holdings/metadata/COVIMS_0xxx/COVIMS_0001/COVIMS_0001_index.tab
* COVIMS_8xxx
    * holdings/volumes/COVIMS_8xxx/COVIMS_8001/data/VIMS_2017_251_GAMCRU_I_TAU_10KM.lbl
    * holdings/volumes/COVIMS_8xxx/COVIMS_8001/data/VIMS_2017_251_GAMCRU_I_TAU_10KM.tab
* EBROCC_xxxx:
    * holdings/volumes/EBROCC_xxxx/EBROCC_0001/DATA/ESO1M/ES1_EPD.lbl
    * holdings/volumes/EBROCC_xxxx/EBROCC_0001/DATA/ESO1M/ES1_EPD.tab
* GO_0xxx:
    * holdings/volumes/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R.IMG
    * holdings/volumes/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R.lbl
    * holdings/previews/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R_med.jpg
    * holdings/metadata/GO_0xxx/GO_0017/GO_0017_index.tab
* HSTIx_xxxx:
    * holdings/volumes/HSTIx_xxxx/HSTI1_1556/DATA/VISIT_01/IB4W01I5Q.lbl
    * holdings/volumes/HSTIx_xxxx/HSTI1_1556/DATA/VISIT_01/IB4W01I5Q.asc
    * holdings/previews/HSTIx_xxxx/HSTI1_1556/DATA/VISIT_01/IB4W01I5Q_thumb.jpg
    * holdings/metadata/HSTIx_xxxx/HSTI1_1556/HSTI1_1556_index.tab
* HSTJx_xxxx:
    * holdings/volumes/HSTJx_xxxx/HSTJ0_9296/DATA/VISIT_B1/J8M3B1021.asc
    * holdings/volumes/HSTJx_xxxx/HSTJ0_9296/DATA/VISIT_B1/J8M3B1021.lbl
    * holdings/previews/HSTJx_xxxx/HSTJ0_9296/DATA/VISIT_B1/J8M3B1021_thumb.jpg
    * holdings/metadata/HSTJx_xxxx/HSTJ0_9296/HSTJ0_9296_index.tab
* HSTNx_xxxx:
    * holdings/volumes/HSTNx_xxxx/HSTN0_7176/DATA/VISIT_01/N4BI01L4Q.asc
    * holdings/volumes/HSTNx_xxxx/HSTN0_7176/DATA/VISIT_01/N4BI01L4Q.lbl
    * holdings/previews/HSTNx_xxxx/HSTN0_7176/DATA/VISIT_01/N4BI01L4Q_thumb.jpg
    * holdings/metadata/HSTNx_xxxx/HSTN0_7176/HSTN0_7176_index.tab
* HSTOx_xxxx:
    * holdings/volumes/HSTOx_xxxx/HSTO0_7308/DATA/VISIT_05/O43B05C1Q.asc
    * holdings/volumes/HSTOx_xxxx/HSTO0_7308/DATA/VISIT_05/O43B05C1Q.lbl
    * holdings/previews/HSTOx_xxxx/HSTO0_7308/DATA/VISIT_05/O43B05C1Q_small.jpg
    * holdings/metadata/HSTOx_xxxx/HSTO0_7308/HSTO0_7308_index.tab
* HSTUx_xxxx:
    * holdings/volumes/HSTUx_xxxx/HSTU0_5167/DATA/VISIT_04/U2NO0404T.asc
    * holdings/volumes/HSTUx_xxxx/HSTU0_5167/DATA/VISIT_04/U2NO0404T.lbl
    * holdings/previews/HSTUx_xxxx/HSTU0_5167/DATA/VISIT_04/U2NO0401T_thumb.jpg
    * holdings/metadata/HSTUx_xxxx/HSTU0_5167/HSTU0_5167_index.tab
* NHSP_xxxx:
    * holdings/volumes/NHSP_xxxx/NHSP_1000/DATA/CK/MERGED_NHPC_2006_V011.LBL
* NHxxLO_xxxx:
    * holdings/volumes/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng.fit
    * holdings/volumes/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng.lbl
    * holdings/previews/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/lor_0003103486_0x630_eng_thumb.jpg
    * holdings/metadata/NHxxLO_xxxx/NHLALO_1001/NHLALO_1001_inventory.tab
* NHxxMV_xxxx:
    * holdings/volumes/NHxxMV_xxxx/NHLAMV_1001/data/20060321_000526/mc0_0005261846_0x536_eng_1.fit
    * holdings/volumes/NHxxMV_xxxx/NHLAMV_1001/data/20060321_000526/mc0_0005261846_0x536_eng_1.lbl
    * holdings/previews/NHxxMV_xxxx/NHLAMV_1001/data/20060321_000526/mc1_0005261846_0x536_eng_1_thumb.jpg
    * holdings/metadata/NHxxMV_xxxx/NHLAMV_1001/NHLAMV_1001_index.tab
* RES_xxxx_prelim:
    * holdings/volumes/RES_xxxx_prelim/RES_0001/data/601_cas.lbl
    * holdings/volumes/RES_xxxx_prelim/RES_0001/data/601_cas.tab
* RPX_xxxx:
    * holdings/volumes/RPX_xxxx/RPX_0001/CALIB/F130LP.lbl
    * holdings/volumes/RPX_xxxx/RPX_0001/CALIB/F130LP.tab
* VGIRIS_xxxx_peer_review
    * holdings/volumes/VGIRIS_xxxx_peer_review/VGIRIS_0001/DATA/JUPITER_VG1/C1547XXX.lbl
    * holdings/volumes/VGIRIS_xxxx_peer_review/VGIRIS_0001/DATA/JUPITER_VG1/C1547XXX.tab
* VGISS_5xxx:
    * holdings/volumes/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_RAW.IMG
    * holdings/volumes/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_RAW.lbl
    * holdings/previews/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_small.jpg
    * holdings/previews/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_full.jpg
    * holdings/previews/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_med.jpg
    * holdings/previews/VGISS_5xxx/VGISS_5101/DATA/C13854XX/C1385455_thumb.jpg
    * holdings/metadata/VGISS_5xxx/VGISS_5101/VGISS_5101_supplemental_index.tab
* VGISS_6xxx:
    * holdings/volumes/VGISS_6xxx/VGISS_6101/DATA/C27830XX/C2783018_RAW.IMG
    * holdings/volumes/VGISS_6xxx/VGISS_6101/DATA/C27830XX/C2783018_RAW.lbl
    * holdings/previews/VGISS_6xxx/VGISS_6101/DATA/C27830XX/C2783018_med.jpg
    * holdings/metadata/VGISS_6xxx/VGISS_6101/VGISS_6101_inventory.tab
* VGISS_7xxx:
    * holdings/volumes/VGISS_7xxx/VGISS_7201/DATA/C24476XX/C2447654_RAW.IMG
    * holdings/volumes/VGISS_7xxx/VGISS_7201/DATA/C24476XX/C2447654_RAW.lbl
    * holdings/previews/VGISS_7xxx/VGISS_7201/DATA/C24476XX/C2447654_small.jpg
    * holdings/metadata/VGISS_7xxx/VGISS_7201/VGISS_7201_inventory.tab
* VGISS_8xxx
    * holdings/volumes/VGISS_8xxx/VGISS_8201/DATA/C08966XX/C0896631_RAW.IMG
    * holdings/volumes/VGISS_8xxx/VGISS_8201/DATA/C08966XX/C0896631_RAW.lbl
    * holdings/previews/VGISS_8xxx/VGISS_8201/DATA/C08966XX/C0896631_thumb.jpg
    * holdings/metadata/VGISS_8xxx/VGISS_8201/VGISS_8201_inventory.tab
* VG_20xx:
    * holdings/volumes/VG_20xx/VG_2001/JUPITER/CALIB/VG1PREJT.DAT
    * holdings/volumes/VG_20xx/VG_2001/JUPITER/CALIB/VG1PREJT.lbl
* VG_28xx:
    * holdings/volumes/VG_28xx/VG_2801/EDITDATA/PN1D01.dat
    * holdings/volumes/VG_28xx/VG_2801/EDITDATA/PN1D01.lbl

* Note:
    * these volumes don't have any preview images (no preview folder) or .\*\_index.tab files (no metadata folder):
        * COISS_0xxx
        * CORSS_8xxx
        * COUVIS_8xxx
        * COVIMS_8xxx
        * EBROCC_xxxx
        * NHSP_xxxx
        * RES_xxxx_prelim
        * RPX_xxxx
        * VGIRIS_xxxx_peer_review
        * VG_20xx
        * VG_28xx
    * Didn't pick any file from ASTROM_xxxx and VG_0xxx.

### Possible issues:
* PdsFile.exists:
    * This paths won't be hit: when is_virtual is set to True, self.\_exists_filled is also True, and the function will return at the beginning of the function.
    ```
    if self.is_virtual:
        self._exists_filled = True
    ```
    * Can't find a proper test case where self.abspath is None & self.virtual is True.
* PdsFile.isdir:
    * This paths won't be hit: when is_virtual is set to True, self.\_isdir_filled  is also True, and the function will return at the beginning of the function.
    ```
    if self.is_virtual:
        self._isdir_filled = True
    ```
    * Can't find a proper test case where self.abspath is None & self.virtual is True.
* PdsFile.alt:
    * None viewable object will also return basename as alt, not sure if this is expected behavior.
* PdsFile.is_index:
    * Only return true for index table file under metadata directory. If it's under
    volume directory, it will return false

* Note: these are not used at all in pds-webtools, might be used at other places:
    * PdsFile.filespec
    * PdsFile.absolute_or_logical_path
    * PdsFile.opus_id
    * PdsFile.associated_logical_paths
    * PdsViewSet.thumbnail
    * PdsViewSet.small
    * PdsViewSet.medium
    * PdsViewSet.full_size
