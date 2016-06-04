from tanoi import Board


def test_print_initial_boards():
    single = Board.start(1)
    assert str(single) == '  -  |     |     '

    double = Board.start(2)
    assert str(double) == '   -   |       |       \n  ---  |       |       '

    fiver = Board.start(5)
    assert str(fiver) == ('      -      |             |             \n'
                          '     ---     |             |             \n'
                          '    -----    |             |             \n'
                          '   -------   |             |             \n'
                          '  ---------  |             |             ')


def test_print_arbitrary_board():
    board = Board([4], [0, 2, 5], [1, 3])
    assert str(board) == ('             |             |             \n'
                          '             |             |             \n'
                          '             |      -      |             \n'
                          '             |    -----    |     ---     \n'
                          '  ---------  | ----------- |   -------   ')
