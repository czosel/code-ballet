from tanoi import Board, Moves


def test_print_initial_boards():
    single = Board(Moves(1))
    assert str(single) == '  -  |     |     '

    double = Board(Moves(2))
    assert str(double) == '   -   |       |       \n  ---  |       |       '

    fiver = Board(Moves(5))
    assert str(fiver) == ('      -      |             |             \n'
                          '     ---     |             |             \n'
                          '    -----    |             |             \n'
                          '   -------   |             |             \n'
                          '  ---------  |             |             ')


def test_print_arbitrary_board():
    board = Board(Moves(5))
    board._home = [4]
    board._interim = [0, 2, 5]
    board._target = [1, 3]
    assert str(board) == ('             |             |             \n'
                          '             |             |             \n'
                          '             |      -      |             \n'
                          '             |    -----    |     ---     \n'
                          '  ---------  | ----------- |   -------   ')


def test_initial_board_not_solved():
    initial = Board(Moves(4))
    assert not initial.is_solved()


def test_full_target_board_solved():
    board = Board(Moves(4))
    board._home, board._target = board._target, board._home
    assert board.is_solved()
