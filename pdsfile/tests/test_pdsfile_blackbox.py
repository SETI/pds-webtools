import pdsfile
from pdsfile.general_helper import PDS_HOLDINGS_DIR

import pytest

##########################################################################################
# Blackbox test for functions & properties in PdsFile class
##########################################################################################
class TestPdsFileBlackBox:
    ############################################################################
    # Local implementations of basic filesystem operations
    ############################################################################
    @pytest.mark.parametrize(
        'input_path,expected',
        [
            (PDS_HOLDINGS_DIR + '/volumes/COISS_2xxx',
             [
                'COISS_2090', 'COISS_2025', 'COISS_2055', 'COISS_2058',
                'COISS_2086', 'COISS_2105', 'COISS_2067', 'COISS_2017',
                'COISS_2049', 'COISS_2011', 'COISS_2026', 'COISS_2039',
                'COISS_2073', 'COISS_2044', 'COISS_2062', 'COISS_2037',
                'COISS_2114', 'COISS_2110', 'COISS_2072', 'COISS_2002',
                'COISS_2108', 'COISS_2093', 'COISS_2030', 'COISS_2081',
                'COISS_2040', 'COISS_2007', 'COISS_2098', 'COISS_2077',
                'COISS_2115', 'COISS_2029', 'COISS_2050', 'COISS_2111',
                'COISS_2059', 'COISS_2005', 'COISS_2032', 'COISS_2045',
                'COISS_2035', 'COISS_2084', 'COISS_2109', 'COISS_2096',
                'COISS_2019', 'COISS_2083', 'COISS_2008', 'COISS_2095',
                'COISS_2020', 'COISS_2023', 'COISS_2014', 'COISS_2100',
                'COISS_2041', 'COISS_2076', 'COISS_2012', 'COISS_2089',
                'COISS_2103', 'COISS_2061', 'COISS_2107', 'COISS_2024',
                'COISS_2013', 'COISS_2046', 'COISS_2071', 'COISS_2053',
                'COISS_2092', 'COISS_2038', 'COISS_2080', 'COISS_2068',
                'COISS_2018', 'COISS_2036', 'COISS_2060', 'COISS_2057',
                'COISS_2116', 'COISS_2004', 'COISS_2074', 'COISS_2033',
                'COISS_2043', 'COISS_2079', 'COISS_2113', 'COISS_2001',
                'COISS_2052', 'COISS_2065', 'COISS_2016', 'COISS_2021',
                'COISS_2102', 'COISS_2064', 'COISS_2099', 'COISS_2106',
                'COISS_2085', 'COISS_2078', 'COISS_2097', 'COISS_2056',
                'COISS_2066', 'COISS_2051', 'COISS_2101', 'COISS_2063',
                'COISS_2082', 'COISS_2094', 'COISS_2034', 'COISS_2009',
                'COISS_2088', 'COISS_2006', 'COISS_2022', 'COISS_2015',
                'COISS_2028', 'COISS_2091', 'COISS_2031', 'COISS_2104',
                'COISS_2010', 'COISS_2027', 'COISS_2003', 'COISS_2054',
                'COISS_2048', 'COISS_2087', 'COISS_2112', 'COISS_2070',
                'COISS_2075', 'COISS_2042', 'COISS_2069', 'COISS_2047'
            ]
           ),
        ]
    )
    def test_os_listdir(self, input_path, expected):
        res = pdsfile.PdsFile.os_listdir(abspath=input_path)
        assert len(res) == len(expected)
        assert res.sort() == expected.sort()
