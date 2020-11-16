SHELL := /bin/bash

run:
	FLASK_APP=projeto/app FLASK_ENV=development flask run --host=0.0.0.0

install:
	# python3 -m venv .venv
	# source .venv/bin/activate
	pip install -e .
	pip check

install-dev:
	pip install --upgrade pip
	pip install -e .['dev'] --use-feature=2020-resolver
	pip check

initdb:
	# flask db init
	# flask db migrate
	FLASK_APP=projeto/app flask db upgrade

clean:
	@find . -name '*.py[co]' -exec rm --force {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find . -name '*~' -exec rm --force {} \;
	@find . -name '__pycache__' -exec rm -rf {} \;
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf .tox/
	rm -rf docs/_build
