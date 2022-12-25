format:
	flake8 setup.py mppsolar tests

test: tests/*.py
	pytest -sv

t: test

pypi:
	rm -rf dist/*
	poetry build
	ls -l dist/

pypi-upload:
	twine upload dist/*
