format:
	pre-commit run -a

test: tests/*.py
	pytest -sv

t: test

build:
	poetry build

release:
	poetry publish
