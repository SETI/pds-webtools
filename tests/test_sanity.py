'''Simple sanity tests.  Currently these tests simply import the
modules and packages to ensure that they load.  These tests should be
expanded to test functionality.'''

import pytest

# module tests

def test_finder_colors():
    import finder_colors

def test_pdscache():
    import pdscache

def test_pdsfile():
    import pdsfile

def test_pdsfile_rules():
    import pdsfile_rules

def test_pdsiterator():
    import pdsiterator

def test_pdslogger():
    import pdslogger

def test_pdsviewable():
    import pdsviewable

def test_translator():
    import translator

# package tests

def test_rules():
    import rules

