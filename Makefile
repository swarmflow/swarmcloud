.PHONY: install test lint clean build publish

install:
	poetry install

test:
	poetry run pytest src/tests/ -v --cov=aiswarm --cov-report=term-missing

lint:
	poetry run black src/
	poetry run isort src/
	poetry run flake8 src/
	poetry run mypy src/

clean:
	rm -rf dist/
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +

build: clean
	poetry build

publish: build
	poetry publish

setup-dev: install
	poetry run pre-commit install