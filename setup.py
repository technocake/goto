import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("POST_INSTALL_INSTRUCTIONS.txt", "r") as fh:
    post_install_instructions = fh.read()


setuptools.setup(
    name="magicgoto",
    version="1.3.3",
    author="Robin Aaberg",
    author_email="robin.garen@gmail.com",
    description="Magic goto - goto where you need to be, right now.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gotogoto.ninja",
    packages=['goto'],
    scripts=[
        'bin/goto',
        'bin/project',
        'bin/_gotoutils',
        'bin/start_goto',
        'bin/install_goto',
    ],
    entry_points={
        'console_scripts': ['the_real_goto.py=goto.the_real_goto:main']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
   
print(post_install_instructions)
