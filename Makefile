
.PHONY: lint lint-fix version-check test

lint:
	ruff --version
	ruff check src/
	mypy --version
	mypy --python-version 3.7 src/

lint-fix:
	ruff format src/

version-check:
	@API_VERSION=$$(grep -oP '__version__ = "\K(.*?)(?=")' src/woocommerceaio/api.py); \
    PYPROJECT_VERSION=$$(grep -oP 'version = "\K(.*?)(?=")' pyproject.toml); \
    if [ "$$API_VERSION" != "$$PYPROJECT_VERSION" ]; then \
        echo "Version drift detected:"; \
        echo " - pyproject.toml has $$PYPROJECT_VERSION"; \
        echo " - src/woocommerceaio/api.py has $$API_VERSION"; \
		exit 1; \
	fi; \
	if [ -n "$$DEPLOY_VERSION" ] && [ "$$DEPLOY_VERSION" != "$$PYPROJECT_VERSION" ]; then \
        echo "Version drift detected:"; \
        echo " - deploy version is $$DEPLOY_VERSION"; \
        echo " - code version is $$PYPROJECT_VERSION"; \
		exit 1; \
	fi; \
	echo "Version check passed";

tests:
	pytest --version
	pytest
