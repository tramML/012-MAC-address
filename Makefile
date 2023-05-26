
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

format:
	black

lint: venv domain.yml data/
	. venv/bin/activate
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

clean:
	rm -f *.yml
	rm -rf actions/ data/ tests/ venv/

