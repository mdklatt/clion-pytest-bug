# Project management tasks only.

VENV = .venv
PYTHON = . $(VENV)/bin/activate && python
TEST_PATH = test_pytest.py


$(VENV)/.make-update: requirements-dev.txt
	python -m venv $(VENV)
	for req in $^; do $(PYTHON) -m pip install -r "$$req"; done
	touch $@


.PHONY: image
image:
	docker build --tag clion-pytest-bug:latest .

.PHONY: dev
dev: $(VENV)/.make-update image


.PHONY: test
pytest: dev
	$(PYTHON) -m pytest -v $(TEST_PATH)
