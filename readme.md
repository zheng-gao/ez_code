![Python Logo](https://www.python.org/static/community_logos/python-logo.png)
# Installation
```bash
pip3 install --upgrade ezcode
```
# Documentation
* [docs](docs/readme.md)
# PyPi Releases
https://pypi.org/project/ezcode/#history
# Development Workflow
```bash
git clone https://github.com/zheng-gao/ez_code.git
ez_code/ez.sh -d/--development
```
# Release Workflow
```bash
git clone https://github.com/zheng-gao/ez_code.git
ez_code/ez.sh -r/--release
```
# Unit Test
### Run all the tests
```bash
ez_code/ez.sh -o/--operations test
```
### Run a single test
```bash
ez_code/ez.sh -o/--operations test -a/--arguments test_array.py::test_binary_search
```