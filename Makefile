# Project management tasks only.

CLION_BUILD = 231.8770.66
CLION_PYTEST = ~/Library/Application\ Support/JetBrains/Toolbox/apps/CLion/ch-1/$(CLION_BUILD)/CLion.app/Contents/plugins/python-ce/helpers/pycharm/_jb_pytest_runner.py

VENV = .venv
PYTHON = . $(VENV)/bin/activate && python
TEST_PATH = test_pytest.py


$(VENV)/.make-update: requirements-dev.txt
	python -m venv $(VENV)
	for req in $^; do $(PYTHON) -m pip install -r "$$req"; done
	touch $@


.PHONY: dev
dev: $(VENV)/.make-update


.PHONY: pytest
pytest: dev
	$(PYTHON) -m pytest -v $(TEST_PATH)


.PHONY: pytest-jb
pytest-jb: dev
	$(PYTHON) $(CLION_PYTEST) --path $(TEST_PATH) -- -v