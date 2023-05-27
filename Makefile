
.ONESHELL:

.PHONY: help clean install test

help:
	@echo "usage:"
	@echo "    make install"
	@echo "    make lint"
	@echo "    make train"
	@echo "    make test"
	@echo "    make run"
	@echo "    make clean"

install: venv
	source venv/bin/activate
	pip3 --isolated install -r requirements.txt
	pip3 --isolated install --upgrade pip

venv: venv/touchfile

venv/touchfile: requirements.txt
	test -d venv || python3.8 -m venv venv
	source venv/bin/activate
	pip3 --isolated install --upgrade pip
	pip3 --isolated install -r requirements.txt
	touch venv/touchfile

format: actions/
	black actions/

lint: venv domain.yml data/
	. venv/bin/activate
	black actions/
	rasa data validate

train: venv domain.yml data/
	. venv/bin/activate
	rasa train

test: venv domain.yml data/
	. venv/bin/activate
	rasa test

run: venv domain.yml models/
	. venv/bin/activate
	rasa shell --debug

act: venv actions/
	. venv/bin/activate
	watchmedo auto-restart -d actions/ -p '*.py' rasa run actions

clean:
	rm -rf venv/
