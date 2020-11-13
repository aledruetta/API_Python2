SHELL := /bin/bash

run:
	FLASK_APP=projeto/app FLASK_ENV=development flask run --host=0.0.0.0

install:
	# python3 -m venv .venv
	# source .venv/bin/activate
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

clean:
	rm -rf .venv
