all:
	make clean
	make compile

everything:
	make clean
	make compile
	make test
	make upload
	make uninstall
	make install
	make install

compile:
	python setup.py build
	python setup.py sdist

clean:
	python setup.py clean
	rm dist/* || echo Nothing to clean
	rm -rf **/*.egg-info

test:
	make unittest
	make endtoendtest

unittest:
	tox

endtoendtest:
	GOTOPATH=/tmp/.goto goto/tests/test_end_to_end.sh 
	
upload:
	twine upload --repository testpypi dist/*

publish:
	make clean
	make compile
	make test
	twine upload dist/*

install:
	pip install -e .

testinstall:
	# Not all dependencies are available in testpypi, adding pypi
	# see: https://packaging.python.org/guides/using-testpypi/
	pip install --no-cache-dir --upgrade --force-reinstall \
		--index-url https://test.pypi.org/simple/ magicgoto \
		--extra-index-url https://pypi.org/simple/

uninstall:
	pip uninstall magicgoto


testcircleci:
	# Testing circleci tests locally using cli:
	# https://circleci.com/docs/2.0/local-cli/
	circleci config validate
	circleci local execute
