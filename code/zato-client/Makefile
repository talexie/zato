
.PHONY: test

default: upload

upload2: PYTHON_BIN = python2
upload3: PYTHON_BIN = python3

upload:
	$(MAKE) upload2
	$(MAKE) upload3

clean:
	rm -rf $(CURDIR)/dist/ && rm -rf $(CURDIR)/build

twine:
	twine upload $(CURDIR)/dist/*

upload2 upload3:
	$(MAKE) clean
	$(PYTHON_BIN) setup.py clean && $(PYTHON_BIN) setup.py bdist_wheel
	$(MAKE) twine

static-check:
	echo "Running static checks in zato-client"
	$(CURDIR)/../bin/flake8 --config=$(CURDIR)/../tox.ini $(CURDIR)/
