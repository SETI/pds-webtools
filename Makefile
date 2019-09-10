.PHONY: clean test

ACTIVATE = source venv/bin/activate

dist : test
	$(ACTIVATE) && python setup.py sdist

test  : venv
	$(ACTIVATE) && pytest ./tests

venv : requirements.txt
	virtualenv --no-site-packages -p python2.7 $@
	$(ACTIVATE) && pip install -r requirements.txt

clean :
	-find . -name '*~' -delete
	-find . -name '#*' -delete
	-find . -name '*.pyc' -delete
	-rm -rf dist venv MANIFEST
