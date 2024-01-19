PYTHON = python3
DIR = infected/

run:
	$(PYTHON) stockholm.py

h:
	$(PYTHON) stockholm.py -h

help:
	$(PYTHON) stockholm.py --help

r:
	$(PYTHON) stockholm.py -r

reverse: filekey.key
	$(PYTHON) stockholm.py --reverse $$(cat filekey.key)

s:
	$(PYTHON) stockholm.py -s

silent:
	$(PYTHON) stockholm.py --silent

v:
	$(PYTHON) stockholm.py -v

version:
	$(PYTHON) stockholm.py --version
