### Possible issues:
* anchor:
    * Test case: volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_CAL.tab
    * Expected result: RSS_2005_123_K34_E_CAL
    * Actual result: RSS_2005
    * Should the anchor be RSS_2005_123_K34_E_CAL? Because if anchor is RSS_2005, then RSS_2005_123_K34_E_CAL.TAB and RSS_2005_123_K34_E_DLP_500M.TAB will be in the same row in viewmaster. The issue is caused by the regex pattern VOLNAME_PLUS_REGEX

* Note:
    * is_index:
        * definition is changed, this is determined by whether an index shelf file exists under /shelves/index or not.
