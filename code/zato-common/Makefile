
.PHONY: test

PY_DIR=$(CURDIR)/../bin

run-tests:
	echo "Running unit-tests in zato-common"
	$(PY_DIR)/nosetests $(CURDIR)/test/zato/common/test_util.py -s

static-check:
	echo "Running static checks in zato-common"
	$(CURDIR)/../bin/flake8 --config=$(CURDIR)/../tox.ini $(CURDIR)/
