# Installation

```bash
pip3 install --upgrade ezcode
```

# PyPi Releases

https://pypi.org/project/ezcode/#history


# Development Workflow
```bash
git clone https://github.com/zheng-gao/ez_code.git && cd ez_code
./ez.sh -d/--development
```

# Release Workflow

```bash
git clone https://github.com/zheng-gao/ez_code.git && cd ez_code
./ez.sh -r/--release
```

# Unit Test
### Run all the tests
```bash
./ez.sh -o/--operations test
```
### Run a single test
```bash
./ez.sh -o/--operations test -a/--arguments test_array.py::test_binary_search
```

# Contents
* [Array](docs/array.md)
* [Graph](docs/graph.md)
* [Grid](docs/grid.md)
* [Hash](docs/hash.md)
* [Heap](docs/heap.md)
* [Interval](docs/interval.md)
* [Knapsack](docs/knapsack.md)
* [List](docs/list.md)
* [Math](docs/math.md)
* [Tree](docs/tree.md)
