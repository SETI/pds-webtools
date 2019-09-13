.PHONY: clean test

ACTIVATE = source venv/bin/activate
TEST_DIR = /Volumes/golden_000x
CMD = python -c 'from tests.mk_golden_db import make_db; make_db();'

dist : test
	$(ACTIVATE) && python setup.py sdist

test  : venv tests/golden.db
	# Run all tests (including golden tests) without pickles;
	# repeat golden tests with pickles.
	$(ACTIVATE) && \
	PDS_WEBTOOLS_TEST_DIR=$(TEST_DIR) \
	    PDS_WEBTOOLS_USE_PICKLES=0 pytest ./tests && \
	PDS_WEBTOOLS_TEST_DIR=$(TEST_DIR) \
	    PDS_WEBTOOLS_USE_PICKLES=1 pytest -k '_golden_' ./tests

tests/golden.db : venv
	# build the data without pickles, then the data with pickles.
	$(ACTIVATE) && \
	    PDS_WEBTOOLS_TEST_DIR=$(TEST_DIR) \
		PDS_WEBTOOLS_USE_PICKLES=0 $(CMD)
	    PDS_WEBTOOLS_TEST_DIR=$(TEST_DIR) \
		PDS_WEBTOOLS_USE_PICKLES=1 $(CMD)

venv : requirements.txt
	virtualenv --no-site-packages -p python2.7 $@
	$(ACTIVATE) && pip install -r requirements.txt

clean :
	-find . -name '*~' -delete
	-find . -name '#*' -delete
	-find . -name '*.pyc' -delete
	-rm -rf dist venv MANIFEST
