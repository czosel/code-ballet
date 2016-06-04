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


def test_initial_board_not_solved():
    initial = Board.start(4)
    assert not initial.is_solved()


def test_full_target_board_solved():
    board = Board.start(4)
    board._home, board._target = board._target, board._home
    assert board.is_solved()
