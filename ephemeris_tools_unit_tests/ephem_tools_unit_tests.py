"""This script contains the PDS4 Ephemeris Tools Unit Tests.

These tests represent two operations: the creation and storage of 
"golden copies", and the comparison of current documents against these golden
copy counterparts. 

To correctly run this script, the structure is:
    
run ephem_tools_unit_test.py --run-test/current-ephemeris <path to directory 
containing the URL test files> <path leading to the golden_copies folder> 
--tools <chosen tools> --chosen-tests <start>:<end> --server <chosen server>

The "golden copy" generation takes the command line input of which tools to 
generate golden copies for. The attributed functions to those tools 
(viewer_replace, moon_tracker_replace, and ephemeris_generator_replace) take 
the input values for the ephemeris type, the path to the tests files, which 
tools to replace. The golden copies can only be generated from the staging 
server. These files are stored as their original (uncleaned) versions. 

The comparison feature generates files from a requested server utilizing the 
same method of generation as the golden files. The new version and the golden 
copy are matched via hex name and cleaned of contents that are constant between 
versions or are expected to change but have no impact on the final result. The
two cleaned files are then compared against one another in search of discrepancy.
The match results of all the files are noted in the log, whether or not they
match.
"""
import argparse
from datetime import datetime
import logging
import os
import re
import requests
import sys
import urllib3
import uuid
import warnings


class NotHTML():
    'URL does not pass quality check. Please verify that all URL tests end with'
    '"&output=HTML".'
    pass


class FileNotFound(FileNotFoundError):
    'File cannot be found within the designated golden copies directory.'
    pass


def compare(ephem, tools, subtests, golden_location, source_location, server):
    """Compares test versions to golden copies of chosen tools.
    
    This function takes arguments for the ephemeris type ("current" or "test"), 
    the tools you choose to compare, and the server from which you want to pull
    the test versions. A quality check is in place that ensures that test 
    URLs generate HTML files before modifying the tests to create PostScript or
    TAB files; an error is thrown if an original test does not end with 
    'output=HTML'. The correct tools are generated, cleaned, then matched
    against their golden copy versions. Returns the results in the generated 
    log file.
    """

    warnings.simplefilter('ignore', urllib3.exceptions.InsecureRequestWarning)
    tests_final = []

    for tool in tools:
        tests_file = os.path.join(source_location[0], tool)
        with open(tests_file, 'r') as test_urls:
            test_urls = test_urls.readlines()
            
        if 'viewer3' in test_urls[0]:
            viewer_tests = os.path.join(source_location[0], tool)
            with open(viewer_tests, 'r') as file:
                viewer_urls = file.readlines()
                viewer_urls = [url.strip() for url in viewer_urls]
                viewer_urls = [url.strip('https://staging.pds.seti.org/')
                               for url in viewer_urls]
                
                for url in viewer_urls:
                        if not url.endswith('&output=HTML'):
                            logging.warning(f'The URL {url} '
                                            f'does not end with "HTML"')
                            raise NotHTML
                            sys.exit(1)
                            
                # This check for HTML within the URLs is necessary to ensure that 
                # all tests will function as expected. If tests are derived from 
                # a format other than HTML, this program will end and with will 
                # return a logged warning.
                if subtests:
                    subtests = subtests[0].split(':')
                    if subtests[0] != subtests[-1]:
                        first_test = int(subtests[0]) - 1
                        last_test = int(subtests[-1]) - 1
                        viewer_urls = viewer_urls[first_test:last_test]
                    
                    else:
                        assert subtests[0] == subtests[-1]
                        single_test = int(subtests[0]) - 1
                        viewer_urls = viewer_urls[single_test:single_test + 1]
                        
                viewer_indices_ps =[]
                
                for urls in viewer_urls:
                    tests_final.append(urls)
                    ps_urls = urls.replace('&output=HTML', '&output=PS')
                    viewer_indices_ps.append(ps_urls)
                    tests_final.append(ps_urls)
        
        if 'tracker3' in test_urls[0]:
            tracker_tests = os.path.join(source_location[0], tool)
            with open(tracker_tests, 'r') as file:
                tracker_urls = file.readlines()
                tracker_urls = [url.strip() for url in tracker_urls]
                tracker_urls = [url.strip('https://staging.pds.seti.org/')
                                for url in tracker_urls]
                
                for url in tracker_urls:
                        if not url.endswith('&output=HTML'):
                            logging.warning(f'The URL {url} '
                                            f'does not end with "HTML"')
                            raise NotHTML
                            sys.exit(1)
                
                # This check for HTML within the URLs is necessary to ensure that 
                # all tests will function as expected. If tests are derived from 
                # a format other than HTML, this program will end and with will 
                # return a logged warning.
                if subtests:
                    subtests = subtests[0].split(':')
                    if subtests[0] != subtests[-1]:
                        first_test = int(subtests[0]) - 1
                        last_test = int(subtests[-1]) - 1
                        tracker_urls = tracker_urls[first_test:last_test]
                    
                    else:
                        assert subtests[0] == subtests[-1]
                        single_test = int(subtests[0]) - 1
                        tracker_urls = tracker_urls[single_test:single_test + 1]
                        
                # TAB files are currently paused until the tabular format 
                # bug is fixed.
                
                tracker_indices_ps =[]
                tracker_indices_tab = []
                
                for urls in tracker_urls:
                    tests_final.append(urls)
                    ps_urls = urls.replace('&output=HTML', '&output=PS')
                    tracker_indices_ps.append(ps_urls)
                    tests_final.append(ps_urls)
                    tab_urls = urls.replace('&output=HTML', '&output=TAB')
                    tracker_indices_tab.append(tab_urls)
                    tests_final.append(tab_urls)

        if 'ephem3' in test_urls[0]:
            ephemeris_tests = os.path.join(source_location[0], 
                                           'ephemeris-generator-unit-tests.txt')
            with open(ephemeris_tests, 'r') as file:
                ephemeris_urls = file.readlines()
                ephemeris_urls = [url.strip() for url in ephemeris_urls]
                ephemeris_urls = [url.strip('https://staging.pds.seti.org/')
                                  for url in ephemeris_urls]
                
                for url in ephemeris_urls:
                        if not url.endswith('&output=HTML'):
                            logging.warning(f'The URL {url} '
                                            f'does not end with "HTML"')
                            raise NotHTML
                            sys.exit(1)
                            
                # This check for HTML within the URLs is necessary to ensure that 
                # all tests will function as expected. If tests are derived from 
                # a format other than HTML, this program will end and with will 
                # return a logged warning.
                if subtests:
                    subtests = subtests[0].split(':')
                    if subtests[0] != subtests[-1]:
                        first_test = int(subtests[0]) - 1
                        last_test = int(subtests[-1]) - 1
                        ephemeris_urls = ephemeris_urls[first_test:last_test]
                    
                    else:
                        assert subtests[0] == subtests[-1]
                        single_test = int(subtests[0]) - 1
                        ephemeris_urls = ephemeris_urls[single_test:
                                                        single_test + 1]
                
                ephemeris_indices_tab = []
                
                for urls in ephemeris_urls:
                    tests_final.append(urls)
                    tab_urls = urls.replace('&output=HTML', '&output=TAB')
                    ephemeris_indices_tab.append(tab_urls)
                    tests_final.append(tab_urls)
                
    if server == 'staging':
        logging.info('Staging server chosen')
        selected_server = 'https://staging.pds.seti.org/'
    elif server == 'production':
        logging.info('Production server chosen')
        selected_server = 'https://pds-rings.seti.org/'
    else:
        assert server == 'other', 'not an accepted value for server'
        selected_server = str(input('type the URL prefix '
                                    'for the server you wish to use: '))
        logging.info(f'Alternative server chosen: {selected_server}')
        
    golden_path = golden_location[0]
    
    # Having a file_type variable ensures that the golden copy counterpart will
    # be cleaned with the correct cleaning code. Since the golden copy will
    # always be the same file type as the test copy, they will use the same
    # cleaning code.
    file_type = None
    tool_type = None

    logging.info('Beginning test file vs. golden copy comparison')
    
    for ephemeris_type in ephem:
        if ephemeris_type == 'test':
            suffix = '&ephem=+-1+TEST&sc_trajectory=+-1+TEST'
        else:
            assert ephemeris_type == 'current'
            suffix = ''

        for test in tests_final:
            if 'viewer3' in test:
                tool_type = 'Planet Viewer test'
                if 'output=HTML' in test:
                    index = list(viewer_urls).index(test) + 1
                else:
                    assert'output=PS' in test
                    index = viewer_indices_ps.index(test) + 1
            
            if 'tracker3' in test:
                tool_type = 'Moon Tracker test'
                if 'output=HTML' in test:
                    index = list(tracker_urls).index(test) + 1
                elif'output=PS' in test:
                    index = tracker_indices_ps.index(test) + 1
                else:
                    assert 'output=TAB' in test
                    index = tracker_indices_tab.index(test) + 1
            
            if 'ephem3' in test:
                tool_type = 'Ephemeris Generator test'
                if 'output=HTML' in test:
                    index = list(ephemeris_urls).index(test) + 1
                else:
                    assert'output=TAB' in test
                    index = ephemeris_indices_tab.index(test) + 1
            name = str(uuid.uuid5(uuid.NAMESPACE_URL, test))
            test = selected_server + test + suffix
            content = requests.get(test, verify=False).content
            content = content.decode('utf8')
            if 'output=HTML' in test:
                test_version = html_file_cleaner(ephem, content)
                file_type = 'html'
            elif 'output=PS' in test:
                test_version = ps_file_cleaner(ephem, content)
                file_type = 'ps'
            else:
                assert 'output=TAB' in test
                file_type = 'tab'
        
            try:
                with open(os.path.join(golden_path, name), 'r') as file_to_read:
                    golden_file = file_to_read.read()
            except FileNotFoundError:
                logging.warning(f'Filename {name} not found within directory')
                
            if file_type == 'html':
                golden_version = html_file_cleaner(ephem, golden_file)
            elif file_type == 'ps':
                golden_version = ps_file_cleaner(ephem, golden_file)
            if golden_version != test_version:
                logging.debug(f'{tool_type} {name} at line {index} does not match')
            else:
                logging.info(f'{tool_type} {name} at line {index} matches')


def html_file_cleaner(ephem, raw_content):
    """Cleans HTML products of all material that is negligible between tests.
    
    Input parameter is the content of a file generated from the URL test via 
    the requests module.This cleaning code covers all three tools. The return 
    value is the cleaned version of the input string.
    """
    clean = re.sub('/></a><br/>',
                   '',
                   raw_content)
    clean = re.sub(r'<title>'
                   r'(Jupiter|Saturn|Uranus|Neptune|Pluto|Mars) '
                   r'(Viewer|Moon Tracker|Ephemeris Generator) \d.\d '
                   r'Results</title>',
                   '',
                   clean)
    clean = re.sub(r'<h1>(Jupiter|Saturn|Uranus|Neptune|Pluto|Mars) '
                   r'(Viewer|Moon Tracker|Ephemeris Generator) \d.\d '
                   r'Results</h1>',
                   '',
                   clean)
    clean = re.sub(r'<a target="blank" href="'
                   r'/work/(viewer|tracker|ephem)\d_'
                   r'(jup|sat|ura|nep|plu|mar)_\d{1,15}.pdf"><image '
                   r'src="/work/(viewer|tracker|ephem)\d_'
                   r'(jup|sat|ura|nep|plu|mar)_'
                   r'\d{1,10}tn.jpg"',
                   '',
                   clean)
    clean = re.sub(r'<a target="blank" href="/work/'
                   r'(viewer|tracker|ephem)\d_'
                   r'(jup|sat|ura|nep|plu|mar)_\d{1,15}.pdf\'><image '
                   r'src="/work/(viewer|tracker|ephem)\d_'
                   r'(jup|sat|ura|nep|plu|mar)_\d{1,10}tn.jpg"',
                   '',
                   clean)
    clean = re.sub(r'<p>Click <a target="blank" href="/work/'
                   r'(viewer|tracker|ephem)3_'
                   r'(jup|sat|ura|nep|plu|mar)_'
                   r'\d{1,15}.pdf">here</a>',
                   '',
                   clean)
    clean = re.sub(r'to download diagram \(PDF, \d{1,15} bytes\).</p>',
                   '',
                   clean)
    clean = re.sub(r'<p>Click <a target="blank" href="/work/'
                   r'(viewer|tracker|ephem)\d_'
                   r'(jup|sat|ura|nep|plu|mar)_'
                   r'(\d{1,15}|\d{1,15}\w).jpg">here</a>',
                   '',
                   clean)
    clean = re.sub(r'to download diagram \(JPEG format, '
                   r'\d{1,15} bytes\).</p>',
                   '',
                   clean)
    clean = re.sub(r'<p>Click <a target="blank" href="/work'
                   r'/(viewer|tracker|ephem)\d_'
                   r'(jup|sat|ura|nep|plu|mar)_'
                   r'\d{1,15}.ps">here</a>',
                   '',
                   clean)
    clean = re.sub(r'to download diagram \(PostScript format, \d{1,15} '
                   r'bytes\).</p>',
                   '',
                   clean)
    clean = re.sub(r'<p>Click <a target="blank" href="/work/'
                   r'(viewer|tracker|ephem)\d_'
                   r'(jup|sat|ura|nep|plu|mar)_'
                   r'\d{1,15}.tab">here</a>',
                   '',
                   clean)
    clean = re.sub(r'to download table \(ASCII format, '
                   r'\d{1,15} bytes\).</p>',
                   '',
                   clean)
    clean = re.sub(r'Click <a href="/work/(ephem|viewer)\d_' 
                   r'(jup|sat|ura|nep|plu|mar)_\d{1,15}.tab">here</a>',
                   '',
                   clean)
    clean = re.sub(r'to download table \(ASCII format, '
                   r'\d{1,15} bytes\).',
                   '',
                   clean)
    if 'test' in ephem:
        clean = re.sub(r'Ephemeris: .+',
                       '',
                       clean)
        clean = re.sub(r'Viewpoint: .+',
                       '',
                       clean)
    clean_content = re.sub(r'<a href=\'/tools/(viewer|tracker|ephem)'
                           r'\d_\w(jup|sat|ura|nep|plu|mar).shtml\'>'
                           r'(Jupiter|Saturn|Uranus|Neptune|Pluto|Mars) '
                           r'(Viewer|Moon Tracker|Ephemeris Generator) '
                           r'Form</a> \|',
                           '',
                           clean)
    
    return clean_content


def ps_file_cleaner(ephem, raw_content):
    """Cleans PostScript products of all material that is negligible between 
    tests.
    
    Input parameter is the content of a file generated from the URL test via 
    the requests module. This cleaning code covers all three tools. The return 
    value is the cleaned version of the string.
    """
    
    clean = re.sub(r'\(Generated by .+\)', '', raw_content)
    if 'test' in ephem:
        clean = re.sub(r'\((JUP|SAT|URA|NEP|PLU|MAR).+[0-9]\)',
                       '',
                       clean)
        clean = re.sub(r' \\\(TEST\\\)',
                       '',
                       clean)
        clean = re.sub(r'\(TEST\)',
                       '',
                       clean)
    clean_content = re.sub(r'%%Title: (viewer|tracker)\d_'
                           r'(jup|sat|ura|nep|plu|mar)_\d{1,10}.ps',
                           '',
                           clean)
         
    return clean_content

    
def replace(ephem, tools, source_location, golden_copies_location):
            
    def ephemeris_generator_replace(ephem, ephemeris_tool_path, 
                                    golden_copies_path):
        """Generates golden copies for the ephemeris generator tool. 
        
        Input parameters are the chosen ephemeris, the path to the raw URL test 
        files, and the chosen path to put the golden_copies. For this tool, the 
        file types generated are HTML and TAB. These files are stored in their 
        original format and are not cleaned of content.
        """
        #FIXIT: Make this filename the default, add option for input 
        ephemeris_tests = ephemeris_tool_path
        
        logging.info('Now pulling raw URL tests from ephemeris-generator-unit'
                     '-tests.txt')
       
        with open(ephemeris_tests, 'r') as urls_fp: 
            ephemeris_urls = urls_fp.readlines()
            ephemeris_urls = [url.strip() for url in ephemeris_urls]
            ephemeris_urls = [url.strip('https://staging.pds.seti.org/')
                              for url in ephemeris_urls]
                        
        # This check for HTML within the URLs is necessary to ensure that all tests
        # Will function as expected. If tests are derived from a format other than
        # HTML, this program will end and with will return a logged warning.
        for url in ephemeris_urls: 
            if not url.endswith('&output=HTML'):
                logging.warning(f'The URL {url} '
                                f'does not end with "HTML"')
                raise NotHTML
                sys.exit(1)
    
        logging.info('Compatibility check successful')
        
        tab_versions = []
        all_urls = ephemeris_urls[:]
        number_of_base_tests = str(len(all_urls))
        logging.info(f'Golden copies of the Ephemeris Generator Tool '
                     f'requested. Now generating {number_of_base_tests} '
                     f'golden copies')
        
        logging.info(f'HTML test versions generated. Now generating '
                     f'{number_of_base_tests} TAB file versions')
        for url in ephemeris_urls: 
            url = url.replace('output=HTML', 'output=TAB')
            tab_versions.append(url)
            all_urls.append(url)
            
        for file in all_urls: 
            if file.endswith('&output=HTML'): 
                index = list(ephemeris_urls).index(file) + 1
            if file.endswith('&output=TAB'): 
                index = tab_versions.index(file) + 1
            if 'test' in ephem:
                file += '&ephem=+-1+TEST&sc_trajectory=+-1+TEST'
            name = str(uuid.uuid5(uuid.NAMESPACE_URL, file))
            file = 'https://staging.pds.seti.org/' + file
            grab = requests.get(file, verify=False)
            content = grab.content
            content = content.decode('utf8')
            with open(golden_copies_path[0] + '/' + name, 'w') as golden_file: 
                golden_file.write(content)
                logging.info(f'Generated file {name} from line {index}')
    
    def moon_tracker_replace(ephem, moon_tracker_tests_path, 
                             golden_copies_path):
        """Generates golden copies for the moon tracker tool. 
        
        For this tool, the file types generated are HTML, PostScript, and TAB. 
        These files are stored in their original format and are not cleaned of 
        content.
        """
        
        tracker_tests = moon_tracker_tests_path
        
        logging.info('Now pulling raw URL tests from '
                     'moon-tracker-unit-tests.txt')
        
        with open(tracker_tests, 'r') as urls_fp: 
            tracker_urls = urls_fp.readlines()
            tracker_urls = [url.strip() for url in tracker_urls]
            tracker_urls = [url.strip('https://staging.pds.seti.org/')
                            for url in tracker_urls]
            
        for url in tracker_urls: 
            if not url.endswith('&output=HTML'):
                logging.warning(f'The URL {url} '
                                f'does not end with "HTML"')
                raise NotHTML
                sys.exit(1)
                    
        # This check for HTML within the URLs is necessary to ensure that all tests
        # Will function as expected. If tests are derived from a format other than
        # HTML, this program will end and with will return a logged warning.
        logging.info('Compatibility check successful')
        
        ps_versions = []
        tab_versions = []
        all_urls = list(tracker_urls[:])
        number_of_base_tests = len(all_urls)
        logging.info(f'Golden copies of the Moon Tracker Tool requested. Now '
                     f'generating {number_of_base_tests} golden copies')
    
        logging.info(f'HTML test versions generated. Now generating '
                     f'{number_of_base_tests} PostScript file versions')
        for url in tracker_urls: 
            url = url.replace('output=HTML', 'output=PS')
            ps_versions.append(url)
            all_urls.append(url)
            
        logging.info(f'Postscript test versions generated. Now generating '
                     f'{number_of_base_tests} TAB file versions')
        for url in tracker_urls:
            url = url.replace('output=HTML', 'output=TAB')
            tab_versions.append(url)
            all_urls.append(url)
        
        for file in all_urls: 
            if file.endswith('&output=HTML'): 
                index = list(tracker_urls).index(file) + 1
            elif file.endswith('&output=PS'): 
                index = ps_versions.index(file) + 1
            else:
                assert file.endswith('&output=TAB') 
                index = tab_versions.index(file) + 1
            if 'test' in ephem:
                file += '&ephem=+-1+TEST&sc_trajectory=+-1+TEST'
            name = uuid.uuid5(uuid.NAMESPACE_URL, file)
            file = 'https://staging.pds.seti.org/' + file
            grab = requests.get(file, verify=False)
            content = grab.content
            content = content.decode('utf8')
            with open(golden_copies_path[0] + '/' + str(name),
                      'w') as golden_file:
                golden_file.write(content)
                logging.info(f'File {name} located at line {index} generated')
    
    def viewer_replace(ephem, viewer_tool_path, golden_copies_path):
        """Generates golden copies for the planet viewer tool. 
        
        For this tool, the file types generated are HTML and PostScript. 
        These files are stored in their original format and are not cleaned 
        of content.
        """
        
        viewer_tests = viewer_tool_path
        
        logging.info('Now pulling raw URL tests from viewer-unit-tests.txt')
                       
        with open(viewer_tests, 'r') as urls_fp: 
            viewer_urls = urls_fp.readlines()
            viewer_urls = [url.strip() for url in viewer_urls]
            viewer_urls = [url.strip('https://staging.pds.seti.org/')
                           for url in viewer_urls]
    
        for url in viewer_urls: 
                if not url.endswith('output=HTML'): 
                    logging.warning(f'The URL {url} '
                                    f'does not end with "HTML"')
                    raise NotHTML
                    sys.exit(1)
                    
        # This check for HTML within the URLs is necessary to ensure that all tests
        # Will function as expected. If tests are derived from a format other than
        # HTML, this program will end and will return a logged warning.
        logging.info('Compatibility check successful')
            
        ps_files = []
        all_urls = list(viewer_urls)
        number_of_base_tests = str(len(all_urls))
        logging.info(f'Golden copies of the Planet Viewer Tool requested. Now '
                     f'generating {number_of_base_tests} HTML file versions')
    
        logging.info(f'HTML test versions generated. Now generating '
                     f'{number_of_base_tests} PostScript file versions')
        
        for url in viewer_urls: 
            url = url.replace('output=HTML', 'output=PS')
            ps_files.append(url)
            all_urls.append(url)
    
        for file in all_urls:  
            if file.endswith('output=HTML'):
                index = list(viewer_urls).index(file) + 1
            else:
                assert file.endswith('output=PS')
                index = ps_files.index(file) + 1
            name = uuid.uuid5(uuid.NAMESPACE_URL, file)
            file = 'https://staging.pds.seti.org/' + file
            if 'test' in ephem:
                file += '&ephem=+-1+TEST&sc_trajectory=+-1+TEST'
            grab = requests.get(file, verify=False)
            content = grab.content
            content = content.decode('utf8')
            with open(golden_copies_path[0] + '/' + str(name),
                      'w') as golden_file:
                golden_file.write(content)
                logging.info(f'File {name} at line {index} generated')
            
    for tool in tools:
        tests_file = os.path.join(source_location[0], tool)
        with open(tests_file, 'r') as test_urls:
            test_urls = test_urls.readlines()
    
        if 'viewer3' in test_urls[0]:
            viewer_replace(ephem, tests_file, golden_copies_location)
        if 'tracker3' in test_urls[0]:
            moon_tracker_replace(ephem, tests_file, golden_copies_location)
        if 'ephem3' in test_urls[0]:
            ephemeris_generator_replace(ephem, tests_file, 
                                        golden_copies_location)
            
current_time = datetime.now().strftime('%H:%M:%S')
logging.basicConfig(filename=f'ephem_tools_unit_test_{current_time}.log',
                    encoding='utf-8',
                    level=logging.DEBUG, 
                    format='%(asctime)s | %(levelname)s | %(message)s',
                    datefmt='%y-%m-%d %H:%M:%S',
                    force=True)
    
warnings.simplefilter('ignore', urllib3.exceptions.InsecureRequestWarning)
logging.getLogger('urllib3').setLevel(logging.WARNING)

parser = argparse.ArgumentParser()
parser.add_argument('--run-test-ephemeris', dest='chosenephems', 
                    action='append_const', const='test',
                    help='Runs your chosen action with the "test" '
                         'extension implemented to force all tests to operate '
                         'with the most recent ephemeris.')

parser.add_argument('--run-current-ephemeris', dest='chosenephems', 
                    action='append_const', const='current',
                    help='Runs your chosen action in the current active '
                         'version of the server.')

parser.add_argument('tool_directory', type=str, nargs=1,
                    help='The location of the URL source files that will '
                         'generate the results. All files called must be '
                         'within the same location within the directory. '
                         'Do not include the file name within the path. '
                         'Do not end the path with a /.')

parser.add_argument('golden_directory', type=str, nargs=1, 
                    help='Path to the golden_files storage.')

parser.add_argument('--comparison', action='store_true',
                    help='Compares results of chosen ephemeris tools to '
                         'their stored golden version counterparts. '
                         'The generated results are pulled from your '
                         'chosen server.')

parser.add_argument('--replacement', dest='folderaction', action='store_false',
                    help='Replaces stored versions of chosen ephemeris '
                         'tools. All versions stored are generated from the '
                         'current staging server.')

parser.set_defaults(folderaction=True)

parser.add_argument('--tools', type=str, nargs='+',
                    help='The ephemeris tool file(s) you wish to utilize. '
                         'Any combination of tools is allowed.')

parser.add_argument('--chosen-tests', dest='testsubset', action='store', nargs='+',
                    help='The indices to specify which subset of tests to run '
                         'within a set of URL tests. Refer to the indices '
                         'within the log file to determine which tests to '
                         'rerun.')

parser.set_defaults(testsubset=None)

parser.add_argument('--server', type=str, choices=['staging', 'production',
                                                     'other'],
                    help='The server you wish to generate the current tests '
                         'for comparison. If you choose "other", please enter '
                         'the URL prefix for the sever you wish to use.')

args = parser.parse_args()

if not args.folderaction: 
    replace(args.chosenephems, 
            args.tools, 
            args.tool_directory, 
            args.golden_directory)
else: 
    compare(args.chosenephems, 
            args.tools, 
            args.testsubset,
            args.golden_directory,
            args.tool_directory, args.server)