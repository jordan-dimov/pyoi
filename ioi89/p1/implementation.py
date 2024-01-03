from typing import Literal

BOX_VALUE = Literal["A", "B", None]
STATE = list[BOX_VALUE]


class NoSolutionError(Exception):
    pass


def check_state(state_list: STATE) -> None:
    if len(state_list) < 2:
        raise ValueError("Invalid state")

    if len(state_list) % 2 != 0:
        raise ValueError("Invalid state")

    if state_list.count(None) != 2:
        raise ValueError("Invalid state")

    if len(state_list) > 2:
        if state_list.count("A") != state_list.count("B"):
            raise ValueError("Invalid state")

        # Check that the two None boxes are next to each other
        pos_n1 = state_list.index(None)
        pos_n2 = state_list.index(None, pos_n1 + 1)
        if pos_n2 - pos_n1 != 1:
            raise ValueError("Invalid state")



def exchange(state_list: STATE, pos: int) -> STATE:
    if not 0 <= pos < len(state_list) - 1:
        raise IndexError("Position out of range")

    l1, l2 = state_list[pos], state_list[pos + 1]
    if None in (l1, l2):
        raise ValueError("Invalid exchange")

    pos_n1 = state_list.index(None)

    if pos_n1 > pos:
        return state_list[:pos] + [None, None] + state_list[pos + 2 : pos_n1] + [l1, l2] + state_list[pos_n1 + 2 :]
    return state_list[:pos_n1] + [l1, l2] + state_list[pos_n1 + 2 : pos] + [None, None] + state_list[pos + 2 :]


def is_goal(state: STATE) -> bool:
    first_b = state.index("B")
    try:
        state.index("A", first_b)
    except ValueError:
        return True


def find_minimal_plan(state: STATE) -> list[STATE]:
    # Check input validity
    check_state(state)

    N = len(state) // 2

    if N == 1:
        return [state]
    elif N == 2:
        if is_goal(state):
            return [state]
        else:
            raise NoSolutionError

    plan = [state]

    plan += _solve_for_higher_n(state)

    return plan


def _solve_for_higher_n(state: STATE) -> list[STATE]:
    plan = []

    def do_exchange(pos: int) -> None:
        nonlocal state
        state = exchange(state, pos)
        if state in plan:
            raise NoSolutionError
        plan.append(state)

    while not is_goal(state):
        first_none = state.index(None)
        first_b = state.index("B")

        # Find the first A which follows a B after the empty boxes
        try:
            first_wrong_a = state.index("A", max(first_none, first_b))
            if first_wrong_a > first_b and first_wrong_a > first_none:
                try:
                    # Move the A left over the B
                    do_exchange(first_wrong_a)
                    continue
                except IndexError:
                    try:
                        # There may be one more way to move the A left over the B
                        do_exchange(first_wrong_a - 1)
                        continue
                    except (IndexError, ValueError):
                        raise NoSolutionError
        except ValueError:
            pass

        # See if there's still any A's to the right of a B
        try:
            state.index("A", first_b)
        except ValueError:
            raise NoSolutionError

        # If so, try to move a B to the right
        if first_b < first_none:
            try:
                do_exchange(first_b)
            except IndexError:
                raise NoSolutionError
        else:
            raise NoSolutionError

    return plan
