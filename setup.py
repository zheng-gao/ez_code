from pathlib import Path
from setuptools import setup, find_packages


long_description = """
# ezcode
[![PyPi](https://img.shields.io/pypi/v/ezcode.svg)](https://pypi.python.org/pypi/ezcode)
[![Github](https://img.shields.io/badge/github-master-brightgreen)](https://github.com/zheng-gao/ez_code)
## Installation
```bash
pip3 install --upgrade ezcode
```
## Documentation
* [docs](https://github.com/zheng-gao/ez_code/blob/main/docs)
## Development Workflow
```bash
git clone https://github.com/zheng-gao/ez_code.git
ez_code/ez.sh -d/--development
```
## Release Workflow
```bash
git clone https://github.com/zheng-gao/ez_code.git
ez_code/ez.sh -r/--release
```
## Unit Test
### Run all the tests
```bash
ez_code/ez.sh -o/--operations test
```
### Run a single test
```bash
ez_code/ez.sh -o/--operations test -a/--arguments test_array.py::test_binary_search
```
"""


setup(
    name="ezcode",
    version="1.0.5",
    author="Zheng Gao",
    author_email="mail.zheng.gao@gmail.com",
    description="Easy Algorithm & Data Structure",
    url="https://github.com/zheng-gao/ez_code",
    project_urls={
        "Documentation": "https://github.com/zheng-gao/ez_code/blob/main/docs/readme.md",
        "Bug Tracker": "https://github.com/zheng-gao/ez_code/issues",
    },
    long_description=long_description,  # open(file=Path(__file__).parent/"readme.md", mode="r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                            # Information to filter the project on PyPi website
    python_requires=">=3.7",                      # Minimum version requirement of the package
    py_modules=["ezcode"],                        # Name of the python package
    package_dir={"": "src"},                      # Directory of the source code of the package
    packages=find_packages(where="src"),          # List of all python modules to be installed
    install_requires=[]                           # Install other dependencies if any
)
