# Installation

```bash
pip3 install --upgrade ezcode
```

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

# Contents
* [array](docs/array/readme.md)
* [dp](docs/dp.md)
* [graph](docs/graph/readme.md)
* [grid](docs/grid.md)
* [hash](docs/hash.md)
* [heap](docs/heap.md)
* [interval](docs/interval.md)
* [list](docs/list.md)
* [math](docs/math.md)
* [string](docs/string/readme.md)
* [tree](docs/tree.md)
