### Possible issues:
* Blackbox:
    * Still looking:
        * version_ranks:
            * When with pdsfile.use_shelves_only(True), it will always return None.
        * \_associated_paths
            * row_pdsfile:
                * This is removed, line 4570 in pdsfile.py will cause AttributeError, not sure what's the proper replacement function for row_pdsfile.
    * Fix added:
        * CACHE:
            * '$RANKS-' & '$VOLS-' didn't get updated in preload.
                * In \_update_ranks_and_vols (during preload), LOCAL_PRELOADED flag is not updated so the function will always return without updating the CACHE (line 2618-2619).
        * unhide:
            * line 4972, NameError: name 'pdf' is not defined, should be 'pdsf'
        * unhide_all:
            * line 4978, need to removed unused argument 'pdsf'
        * remove_pdsfile:
            * line 5188, need to add pdsf to the function argument so that it can be passed to remove function at line 5190.
* Blackbox cached:
    * version_ranks:
        * return None.
* Whitebox:
    * version_ranks:
        * KeyError for ranks from CACHE

* Note:
    * The following functions are removed:
        * find_selected_row_number
        * find_row_number_at_or_below
        * test_cache_child_row_pdsfiles
        * row_pdsfile
            * line 4570 in pdsfile.py will cause AttributeError
        * nearest_row_pdsfile
        * data_pdsfile_for_index_and_selection
    * exists/isdir:
        * Some path can only be test with pdsfile.use_shelves_only(False), because if shelves info are loaded, those files will have abspath and be treated as existing files.
    * is_index:
        * definition is changed, this is determined by whether an index shelf file exists under /shelves/index or not.
    * anchor: (ignore this case for now, it's not used in OPUS)
        * Note: the following test case is not used in OPUS
        * Test case: volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_CAL.tab
        * Expected result: RSS_2005_123_K34_E_CAL
        * Actual result: RSS_2005
        * Should the anchor be RSS_2005_123_K34_E_CAL? Because if anchor is RSS_2005, then RSS_2005_123_K34_E_CAL.TAB and RSS_2005_123_K34_E_DLP_500M.TAB will be in the same row in viewmaster. The issue is caused by the regex pattern VOLNAME_PLUS_REGEX
