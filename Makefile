dist:
	python setup.py sdist bdist_wheel

lint:
	autoflake --in-place --recursive --remove-unused-variables --remove-all-unused-imports .
	isort -rc .
	black -l 120 .

upload: dist
	twine upload dist/*

.PHONY: dist lint upload
