import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="goto",
    version="1.3.0",
    author="Robin Aaberg",
    author_email="robin.garen@gmail.com",
    description="Magic goto - goto where you need to be, right now.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gotogoto.ninja",
    packages=['goto'],
    scripts=['bin/goto', 'bin/project']
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
   
