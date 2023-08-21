################################################################################
# pds4file/ruless/pytest_support.py
################################################################################

import pdsfile_reorg.pds4file as pds4file

def translate_first(trans, path):
    """Logical paths of "first" files found using given translator on path."""

    patterns = trans.first(path)
    if not patterns:
        return []

    if isinstance(patterns, str):
        patterns = [patterns]

    patterns = [p for p in patterns if p]       # skip empty translations
    patterns = pds4file.Pds4File.abspaths_for_logicals(patterns)

    abspaths = []
    for pattern in patterns:
        abspaths += pds4file.Pds4File.glob_glob(pattern)

    return abspaths

def translate_all(trans, path):
    """Logical paths of all files found using given translator on path."""

    patterns = trans.all(path)
    if not patterns:
        return []

    if isinstance(patterns, str):
        patterns = [patterns]

    patterns = [p for p in patterns if p]       # skip empty translations
    patterns = pds4file.Pds4File.abspaths_for_logicals(patterns)

    abspaths = []
    for pattern in patterns:
        abspaths += pds4file.Pds4File.glob_glob(pattern)

    return abspaths

def unmatched_patterns(trans, path):
    """List all translated patterns that did not find a matching path in the
    file system."""

    patterns = trans.all(path)
    patterns = [p for p in patterns if p]       # skip empty translations
    patterns = pds4file.Pds4File.abspaths_for_logicals(patterns)

    unmatched = []
    for pattern in patterns:
        abspaths = pds4file.Pds4File.glob_glob(pattern)
        if not abspaths:
            unmatched.append(pattern)

    return unmatched

################################################################################
# Dave's test suite helpers
################################################################################

def instantiate_target_pdsfile(path, is_abspath=True):
    if is_abspath:
        TESTFILE_PATH = pds4file.abspath_for_logical_path(path)
        target_pdsfile = pds4file.Pds4File.from_abspath(TESTFILE_PATH)
    else:
        TESTFILE_PATH = path
        target_pdsfile = pds4file.Pds4File.from_logical_path(TESTFILE_PATH)
    return target_pdsfile

def get_pdsfiles(paths, is_abspath=True):
    pdsfiles_arr = []
    if is_abspath:
        for path in paths:
            TESTFILE_PATH = pds4file.abspath_for_logical_path(path)
            target_pdsfile = pds4file.Pds4File.from_abspath(TESTFILE_PATH)
            pdsfiles_arr.append(target_pdsfile)
    else:
        for path in paths:
            TESTFILE_PATH = path
            target_pdsfile = pds4file.Pds4File.from_logical_path(TESTFILE_PATH)
            pdsfiles_arr.append(target_pdsfile)
    return pdsfiles_arr

def get_pdsgroups(paths_group, is_abspath=True):
    pdsgroups_arr = []
    for paths in paths_group:
        pdsfiles = get_pdsfiles(paths, is_abspath)
        pdsgroup = pds4file.PdsGroup(pdsfiles=pdsfiles)
        pdsgroups_arr.append(pdsgroup)
    return pdsgroups_arr

def opus_products_test(input_path, expected):
    target_pdsfile = instantiate_target_pdsfile(input_path)
    results = target_pdsfile.opus_products()
    # Note that messages are more useful if extra values are identified before
    # missing values. That's because extra items are generally more diagnostic
    # of the issue at hand.
    for key in results:
        assert key in expected, f'Extra key: {key}'
    for key in expected:
        assert key in results, f'Missing key: {key}'
    for key in results:
        result_paths = []       # flattened list of logical paths
        for pdsfiles in results[key]:
            result_paths += pds4file.Pds4File.logicals_for_pdsfiles(pdsfiles)
        for path in result_paths:
            assert path in expected[key], f'Extra file under key {key}: {path}'
        for path in expected[key]:
            assert path in result_paths, f'Missing file under key {key}: {path}'

def versions_test(input_path, expected):
    target_pdsfile = instantiate_target_pdsfile(input_path)
    res = target_pdsfile.all_versions()
    keys = list(res.keys())
    keys.sort()
    keys.reverse()
    for key in keys:
        assert key in expected, f'"{key}" not expected'
        assert res[key].logical_path == expected[key], f'value mismatch at "{key}": {expected[key]}'
    keys = list(expected.keys())
    keys.sort()
    keys.reverse()
    for key in keys:
        assert key in res, f'"{key}" missing'
