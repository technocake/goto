all:
	make clean
	make compile

everything:
	make clean
	make compile
	make test
	make testpublish
	make uninstall
	make install
	make install

compile:
	python setup.py build
	python setup.py sdist bdist_wheel

clean:
	python setup.py clean
	rm -rf dist build */*.egg-info *.egg-info

test:
	tox


endtoendtest:
	GOTOPATH=/tmp/.goto ./test_end_to_end.sh 
	
testpublish:
	make clean
	make compile
	make test
	make _testpublish

_testpublish:
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


circleci:
	# Testing circleci tests locally using cli:
	# https://circleci.com/docs/2.0/local-cli/
	circleci config validate
	circleci local execute



installpyenv:
	brew install pyenv
	pyenv install 3.7.2 
	pyenvinstall 3.6.8
