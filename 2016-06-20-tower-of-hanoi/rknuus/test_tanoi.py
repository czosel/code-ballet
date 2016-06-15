from tanoi import Tower, Priests


def initialize_tower(home, interim, target):
    tower = Tower(len(home) + len(interim) + len(target))
    tower._home, tower._auxiliary, tower._target = home, interim, target
    return tower


def test_print_initial_single_tower():
    tower = initialize_tower([0], [], [])
    assert str(tower) == '  -  |     |     '


def test_print_initial_double_tower():
    tower = initialize_tower([1, 0], [], [])
    assert str(tower) == '   -   |       |       \n  ---  |       |       '


def test_print_initial_fiver_tower():
    tower = initialize_tower(list(reversed(range(0, 5))), [], [])
    assert str(tower) == ('      -      |             |             \n'
                          '     ---     |             |             \n'
                          '    -----    |             |             \n'
                          '   -------   |             |             \n'
                          '  ---------  |             |             ')


def test_print_arbitrary_tower():
    tower = initialize_tower([4], [5, 2, 0], [3, 1])
    assert str(tower) == ('               |               |               \n'
                          '               |               |               \n'
                          '               |               |               \n'
                          '               |       -       |               \n'
                          '               |     -----     |      ---      \n'
                          '   ---------   |  -----------  |    -------    ')


def test_initial_tower_not_solved():
    initial = initialize_tower(list(reversed(range(0, 4))), [], [])
    assert not initial.is_solved()


def test_full_target_tower_solved():
    tower = initialize_tower([], [], list(reversed(range(0, 4))))
    assert tower.is_solved()


def test_moves_from_initial_tower():
    tower = initialize_tower([0], [], [])
    expected_moves = {initialize_tower([], [0], []), initialize_tower([], [], [0])}
    assert set(tower.moves()) == expected_moves


def test_both_moves_from_auxiliary_tower():
    tower = initialize_tower([], [0], [])
    expected_moves = {initialize_tower([0], [], []), initialize_tower([], [], [0])}
    assert set(tower.moves()) == expected_moves


def test_both_moves_from_target_tower():
    tower = initialize_tower([], [], [0])
    expected_moves = {initialize_tower([0], [], []), initialize_tower([], [0], [])}
    assert set(tower.moves()) == expected_moves


def test_moves_if_home_to_auxiliary_illegal():
    tower = initialize_tower([1], [0], [])
    expected_moves = {initialize_tower([], [0], [1]),
                      initialize_tower([1], [], [0]),
                      initialize_tower([1, 0], [], [])}
    assert set(tower.moves()) == expected_moves


def test_moves_if_auxiliary_to_home_illegal():
    tower = initialize_tower([0], [1], [])
    expected_moves = {initialize_tower([], [1, 0], []),
                      initialize_tower([], [1], [0]),
                      initialize_tower([0], [], [1])}
    assert set(tower.moves()) == expected_moves


def test_moves_if_target_to_home_illegal():
    tower = initialize_tower([1], [], [0])
    expected_moves = {initialize_tower([], [1], [0]),
                      initialize_tower([1, 0], [], []),
                      initialize_tower([1], [0], [])}
    assert set(tower.moves()) == expected_moves
