
.PHONY: lint lint-fix test

lint:
	ruff --version
	ruff check src/
	mypy --version
	mypy --python-version 3.7 src/

lint-fix:
	ruff format src/

tests:
	pytest --version
	pytest
