# ezcode
[![PyPi](https://img.shields.io/pypi/v/ezcode.svg)](https://pypi.python.org/pypi/ezcode)
[![Github](https://img.shields.io/badge/github-master-brightgreen)](https://github.com/roll/ez_code)
## Installation
```bash
pip3 install --upgrade ezcode
```
## Documentation
* [docs](docs/readme.md)
## PyPi Releases
https://pypi.org/project/ezcode/#history
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