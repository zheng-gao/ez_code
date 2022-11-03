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
* [Array](docs/array.md)
* [DP](docs/dp.md)
* [Graph](docs/graph.md)
* [Grid](docs/grid.md)
* [Hash](docs/hash.md)
* [Heap](docs/heap.md)
* [Interval](docs/interval.md)
* [List](docs/list.md)
* [Math](docs/math.md)
* [Tree](docs/tree.md)
