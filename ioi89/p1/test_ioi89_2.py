import pytest
from implementation import exchange, find_minimal_plan, NoSolutionError, is_goal, check_state

def test_exchange_operation():
    initial_state = ["A", "B", "B", "A", None, None, "A", "B", "A", "B"]

    new_state = exchange(initial_state, 0)
    assert new_state == [None, None, "B", "A", "A", "B", "A", "B", "A", "B"]

    new_state = exchange(initial_state, 1)
    assert new_state == ["A", None, None, "A", "B", "B", "A", "B", "A", "B"]

    new_state = exchange(initial_state, 2)
    assert new_state == ["A", "B", None, None, "B", "A", "A", "B", "A", "B"]

    new_state = exchange(initial_state, 6)
    assert new_state == ["A", "B", "B", "A", "A", "B", None, None, "A", "B"]

    new_state = exchange(initial_state, 7)
    assert new_state == ["A", "B", "B", "A", "B", "A", "A", None, None, "B"]

    new_state = exchange(initial_state, 8)
    assert new_state == ["A", "B", "B", "A", "A", "B", "A", "B", None, None]


def test_boundary_conditions():
    initial_state = ["A", "B", "B", "A", None, None, "A", "B", "A", "B"]
    with pytest.raises(IndexError):
        exchange(initial_state, 9)
    with pytest.raises(IndexError):
        exchange(initial_state, 10)


def test_invalid_exchanges():
    initial_state = ["A", "B", "B", "A", None, None, "A", "B", "A", "B"]
    with pytest.raises(ValueError, match="Invalid exchange"):
        exchange(initial_state, 3)
    with pytest.raises(ValueError, match="Invalid exchange"):
        exchange(initial_state, 4)
    with pytest.raises(ValueError, match="Invalid exchange"):
        exchange(initial_state, 5)


def test_multiple_exchanges():
    initial_state = ["A", "B", "A", "B", "A", "B", None, None]
    new_state = exchange(initial_state, 3)
    assert new_state == ["A", "B", "A", None, None, "B", "B", "A"]
    final_state = exchange(new_state, 0)
    assert final_state == [None, None, "A", "A", "B", "B", "B", "A"]


def test_n1():
    initial_state = [None, None]
    with pytest.raises(ValueError, match="Invalid exchange"):
        exchange(initial_state, 0)
    with pytest.raises(IndexError):
        exchange(initial_state, 1)


def test_n2():
    initial_state = ["B", "A", None, None]
    new_state = exchange(initial_state, 0)
    assert new_state == [None, None, "B", "A"]


def test_n3():
    initial_state = ["B", None, None, "A", "B", "A"]
    new_state = exchange(initial_state, 3)
    assert new_state == ["B", "A", "B", None, None, "A"]
    new_state = exchange(initial_state, 4)
    assert new_state == ["B", "B", "A", "A", None, None]



@pytest.mark.timeout(10)
def test_minimal_plan_jury_1():
    initial_state = [None, None, "A", "B", "A", "B", "A", "B", "A", "B"]
    plan = find_minimal_plan(initial_state)
    assert plan[0] == initial_state
    last_state = plan[-1]
    assert is_goal(last_state)
    # assert len(plan) == 4 + 1
    # E.g:
    # A B _ _ A B A B A B
    # A B B A A _ _ B A B
    # A B B A A A B B _ _
    # A _ _ A A A B B B B   # All A's are to the left of B's.


@pytest.mark.timeout(10)
def test_minimal_plan_jury_2():
    initial_state = ["A", "B", "B", "A", None, None, "A", "B", "A", "B"]
    plan = find_minimal_plan(initial_state)
    assert plan[0] == initial_state
    last_state = plan[-1]
    assert is_goal(last_state)
    # assert len(plan) == 3 + 1  # 3 exchanges + initial state
    # E.g:
    # A B B A _ _ A B A B
    # A B B A B A A _ _ B
    # A _ _ A B A A B B B
    # A A A A B _ _ B B B   # All A's are to the left of B's.


@pytest.mark.timeout(10)
def test_minimal_plan_jury_3():
    initial_state = [None, None, "A", "B", "A", "B"]
    with pytest.raises(NoSolutionError):
        find_minimal_plan(initial_state)


@pytest.mark.timeout(10)
def test_minimal_plan_jury_4():
    initial_state = [None, "A", "B", "A", None, "B", "A", "B"]
    with pytest.raises(ValueError, match="Invalid state"):
        find_minimal_plan(initial_state)


def test_minimal_plan_n1():
    initial_state = [None, None]
    plan = find_minimal_plan(initial_state)
    assert len(plan) == 1
    assert plan[0] == initial_state


def test_minimal_plan_n2_1():
    initial_state = [None, None, "A", "B"]
    plan = find_minimal_plan(initial_state)
    assert len(plan) == 1
    assert plan[0] == initial_state


def test_minimal_plan_n2_2():
    initial_state = ["A", "B", None, None]
    plan = find_minimal_plan(initial_state)
    assert len(plan) == 1
    assert plan[0] == initial_state


def test_minimal_plan_n2_3():
    initial_state = ["A", None, None, "B"]
    plan = find_minimal_plan(initial_state)
    assert len(plan) == 1
    assert plan[0] == initial_state


def test_plan_n2_no_solution_1():
    initial_state = ["B", None, None, "A"]
    with pytest.raises(NoSolutionError):
        find_minimal_plan(initial_state)


def _generate_random_state(N: int) -> list:
    from random import shuffle

    state = [None, None]
    state += ["A"] * (N - 1)
    state += ["B"] * (N - 1)
    shuffle(state)
    # Make sure the None boxes are next to each other
    pos_n1 = state.index(None)
    if state[pos_n1 + 1] is not None:
        pos_n2 = state.index(None, pos_n1 + 1)
        tmp_box = state[pos_n1 + 1]
        state[pos_n1 + 1] = state[pos_n2]
        state[pos_n2] = tmp_box
    return state


@pytest.mark.timeout(10)
@pytest.mark.parametrize("N", [2, 3, 4, 5, 6, 7, 8, 9])
def test_minimal_plan_random(N: int):
    initial_state = _generate_random_state(N)
    assert check_state(initial_state) is None

    print(f"Testing random state: {initial_state}")

    # Try to find a solution and assert that it either raises NoSolutionError or returns a plan, whose last state is a goal state
    try:
        plan = find_minimal_plan(initial_state)
        assert plan[0] == initial_state
        last_state = plan[-1]
        assert is_goal(last_state)
        print(f"Found a solution: {last_state}")
    except NoSolutionError:
        print("No solution found")
