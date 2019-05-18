all:
	make clean
	make compile

everything:
	make clean
	make compile
	make upload
	make uninstall
	make install
	make install

compile:
	python setup.py build
	python setup.py sdist

clean:
	rm dist/* || echo Nothing to clean
	rm -rf **/*.egg-info

upload:
	twine upload --repository testpypi dist/*

publish:
	make clean
	make compile
	twine upload dist/*

install:
	pip install --no-cache-dir --upgrade --force-reinstall --index-url https://test.pypi.org/simple/ magicgoto

uninstall:
	pip uninstall magicgoto

