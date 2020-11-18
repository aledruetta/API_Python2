SHELL := /bin/bash

install:
	# ln -s /vagrant_data prototipo
	# cd prototipo
	python3 -m venv ~/.venv
	( \
		source ~/.venv/bin/activate; \
		pip install -r requirements.txt; \
		pip check; \
	)

initdb:
	# flask db init
	# flask db migrate
	FLASK_APP=projeto/app flask db upgrade; \

shell:
	FLASK_APP=projeto/app flask shell

run:
	FLASK_APP=projeto/app FLASK_ENV=development flask run --host=0.0.0.0

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
	pip install -r requirements.txt
	pip check
