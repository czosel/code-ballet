from tanoi import Board, Moves


def test_print_initial_single_board():
    board = Board(Moves(1))
    assert str(board) == '  -  |     |     '


def test_print_initial_double_board():
    board = Board(Moves(2))
    assert str(board) == '   -   |       |       \n  ---  |       |       '


def test_print_initial_fiver_board():
    board = Board(Moves(5))
    assert str(board) == ('      -      |             |             \n'
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


def test_moves_from_initial_board():
    board = Board(Moves(1))
    assert list(board.moves()) == [[-1, 1, 0], [-1, 0, 1]]


def test_both_moves_from_interim_board():
    board = Board(Moves(1))
    board._home, board._interim = board._interim, board._home
    assert list(board.moves()) == [[1, -1, 0], [0, -1, 1]]


def test_both_moves_from_target_board():
    board = Board(Moves(1))
    board._home, board._target = board._target, board._home
    assert list(board.moves()) == [[1, 0, -1], [0, 1, -1]]


def test_moves_if_home_to_intermediate_illegal():
    board = Board(Moves(2))
    board._home = [1]
    board._interim = [0]
    assert list(board.moves()) == [[-1, 0, 1], [1, -1, 0], [0, -1, 1]]


def test_moves_if_intermediate_to_home_illegal():
    board = Board(Moves(2))
    board._home = [0]
    board._interim = [1]
    assert list(board.moves()) == [[-1, 1, 0], [-1, 0, 1], [0, -1, 1]]


def test_moves_if_target_to_home_illegal():
    board = Board(Moves(2))
    board._home = [1]
    board._target = [0]
    assert list(board.moves()) == [[-1, 1, 0], [1, 0, -1], [0, 1, -1]]
