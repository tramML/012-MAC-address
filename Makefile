# Caveat: this Makefile will probably fail unless your "make" executable is GNU
# Make v4.1 or greater.

.ONESHELL:

.PHONY: help clean realclean format lint install test train run act zip

help:
	@echo "usage:"
	@echo "    make clean"
	@echo "    make realclean"
	@echo "    make install"
	@echo "    make venv"
	@echo "    make lint"
	@echo "    make train"
	@echo "    make test"
	@echo "    make test-stories"
	@echo "    make run"
	@echo "    make act"
	@echo "    make zip"

clean:
	rm -f *.zip
	rm -rf models/ results/ .rasa/

realclean:
	make clean
	rm -rf venv/

install: venv
	source venv/bin/activate
	pip3 --isolated install -r requirements.txt
	pip3 --isolated install --upgrade pip

venv: venv/touchfile

venv/touchfile: requirements.txt
	test -d venv || python3.9 -m venv venv
	source venv/bin/activate
	pip3 --isolated install --upgrade pip
	pip3 --isolated install -r requirements.txt
	touch venv/touchfile

format: venv actions/
	. venv/bin/activate
	black actions/ tests/
	isort actions/ tests/

lint: venv domain.yml data/
	. venv/bin/activate
	ruff check actions/ tests/
	rasa data validate

models/: train

train: venv domain.yml data/
	. venv/bin/activate
	rasa train

test: venv
	. venv/bin/activate
	pytest -vvv tests/

test-stories:
	. venv/bin/activate
	rasa test --stories tests/

run: venv domain.yml models/
	. venv/bin/activate
	rasa shell --debug

act: venv actions/
	. venv/bin/activate
	watchmedo auto-restart -d actions/ -p '*.py' rasa run actions

zip:
	zip -r macaddrbot.zip README.md Makefile requirements.txt actions/*.py data/ *.yml
