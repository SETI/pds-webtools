from distutils.core import setup

setup(
    name='pds-webtools',
    version='0.1.dev1',
    maintainer='Mark Showalter',
    maintainer_email='mshowalter@seti.org',
    url='http://github.com/SETI/pds-webtools',
    packages=['rules'],
    py_modules=['finder_colors', 'pdscache', 'pdsfile', 'pdsfile_rules',
                'pdsiterator', 'pdslogger', 'pdsviewable', 'translator'])



