from ezcode.Array.Utils import array_to_string


def test_array_to_string():
    assert array_to_string([0, [1], [1, 2, [0, 1, 2, 3]], [], [[[0, 1, 2], 0], 1, 2]]) == """
[
    0,
    [1],
    [
        1,
        2,
        [0, 1, 2, 3]
    ],
    [],
    [
        [
            [0, 1, 2],
            0
        ],
        1,
        2
    ]
]
"""[1:-1]
    array = [1, [2, 3, [4, 5, 6, [6, 7, 8, 9]]], [1, 2], [[[9, 8, 7, 6], 5, 4], 3], 2, 0]
    assert array_to_string(array, indent="    ", cell_size=None, with_bracket_and_comma=True, deepest_iterable_one_line=True) == """
[
    1,
    [
        2,
        3,
        [
            4,
            5,
            6,
            [6, 7, 8, 9]
        ]
    ],
    [1, 2],
    [
        [
            [9, 8, 7, 6],
            5,
            4
        ],
        3
    ],
    2,
    0
]
"""[1:-1]
    assert array_to_string(array, indent="    ", cell_size=None, with_bracket_and_comma=True, deepest_iterable_one_line=False) == """
[
    1,
    [
        2,
        3,
        [
            4,
            5,
            6,
            [
                6,
                7,
                8,
                9
            ]
        ]
    ],
    [
        1,
        2
    ],
    [
        [
            [
                9,
                8,
                7,
                6
            ],
            5,
            4
        ],
        3
    ],
    2,
    0
]
"""[1:-1]
    assert array_to_string(array, indent="    ", cell_size=None, with_bracket_and_comma=False, deepest_iterable_one_line=True) == """
1
    2
    3
        4
        5
        6
        6 7 8 9
1 2
        9 8 7 6
        5
        4
    3
2
0
"""[1:]
    assert array_to_string(array, indent="    ", cell_size=None, with_bracket_and_comma=False, deepest_iterable_one_line=False) == """
1
    2
    3
        4
        5
        6
            6
            7
            8
            9
    1
    2
            9
            8
            7
            6
        5
        4
    3
2
0
"""[1:]

    array = ["abcdef", ["abc", "de"]]
    assert array_to_string(array, indent="    ", cell_size=8, alignment="l", with_bracket_and_comma=True, deepest_iterable_one_line=True) == """
[
    abcdef  ,
    [abc     ,de      ]
]
"""[1:-1]
    assert array_to_string(array, indent="    ", cell_size=8, alignment="l", with_bracket_and_comma=True, deepest_iterable_one_line=False) == """
[
    abcdef  ,
    [
        abc     ,
        de      
    ]
]
"""[1:-1]
    assert array_to_string(array, indent="    ", cell_size=8, alignment="l", with_bracket_and_comma=False, deepest_iterable_one_line=True) == """
abcdef  
abc     de      
"""[1:]
    assert array_to_string(array, indent="    ", cell_size=8, alignment="l", with_bracket_and_comma=False, deepest_iterable_one_line=False) == """
abcdef  
    abc     
    de      
"""[1:]





