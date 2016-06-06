from tanoi import Board, Moves


def initialize_board(home, interim, target):
    board = Board(Moves(len(home) + len(interim) + len(target)))
    board._home, board._interim, board._target = home, interim, target
    return board


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
    board = initialize_board([4], [5, 2, 0], [3, 1])
    assert str(board) == ('               |               |               \n'
                          '               |               |               \n'
                          '               |               |               \n'
                          '               |       -       |               \n'
                          '               |     -----     |      ---      \n'
                          '   ---------   |  -----------  |    -------    ')


def test_initial_board_not_solved():
    initial = Board(Moves(4))
    assert not initial.is_solved()


def test_full_target_board_solved():
    board = Board(Moves(4))
    board._home, board._target = board._target, board._home
    assert board.is_solved()


def test_moves_from_initial_board():
    board = Board(Moves(1))
    expected_moves = {initialize_board([], [0], []), initialize_board([], [], [0])}
    assert set(board.moves()) == expected_moves


def test_both_moves_from_interim_board():
    board = Board(Moves(1))
    board._home, board._interim = board._interim, board._home
    expected_moves = {initialize_board([0], [], []), initialize_board([], [], [0])}
    assert set(board.moves()) == expected_moves


def test_both_moves_from_target_board():
    board = Board(Moves(1))
    board._home, board._target = board._target, board._home
    expected_moves = {initialize_board([0], [], []), initialize_board([], [0], [])}
    assert set(board.moves()) == expected_moves


def test_moves_if_home_to_intermediate_illegal():
    board = initialize_board([1], [0], [])
    expected_moves = {initialize_board([], [0], [1]),
                      initialize_board([1], [], [0]),
                      initialize_board([1, 0], [], [])}
    assert set(board.moves()) == expected_moves


def test_moves_if_intermediate_to_home_illegal():
    board = initialize_board([0], [1], [])
    expected_moves = {initialize_board([], [1, 0], []),
                      initialize_board([], [1], [0]),
                      initialize_board([0], [], [1])}
    assert set(board.moves()) == expected_moves


def test_moves_if_target_to_home_illegal():
    board = initialize_board([1], [], [0])
    expected_moves = {initialize_board([], [1], [0]),
                      initialize_board([1, 0], [], []),
                      initialize_board([1], [0], [])}
    assert set(board.moves()) == expected_moves
