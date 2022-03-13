# Installation

```
pip3 install --upgrade ezcode
```

# PyPi Releases

https://pypi.org/project/ezcode/#history


# Development Workflow
```
git clone https://github.com/zheng-gao/ez_code.git && cd ez_code
./ez.sh --development
```

# Release Workflow

```
git clone https://github.com/zheng-gao/ez_code.git && cd ez_code
./ez.sh --release
```

# Unit Test
### Run all the tests
```
./ez.sh --operations test
```
### Run a single test
```
./ez.sh --operations test --arguments test_array.py::test_binary_search
```

# Contents
* [Array](src/ezcode/array/array.md)
* [Heap](src/ezcode/heap/heap.md)
* [Knapsack](src/ezcode/knapsack/knapsack.md)
* [List](src/ezcode/list/list.md)
* [Tree](src/ezcode/tree/tree.md)
* [Graph](src/ezcode/graph/graph.md)
* [Math](src/ezcode/math/math.md)


