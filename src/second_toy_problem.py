# restoration_graph.py — problem definition only.
# planner.py must not know anything specific to this file.

ACTIONS = {
    "Fry Tofu": {"requires": set(), "cost": 3},
    "Concoct Sauce": {"requires": set(), "cost": 2},
    "CONSUME FOOD": {"requires": {"Fry Tofu", "Concoct Sauce"}, "cost": 1},
}

GOAL = frozenset(ACTIONS.keys())
START = frozenset()

def available_actions(state):
    """Actions whose prerequisites are satisfied and not already done."""
    return [a for a, info in ACTIONS.items()
            if a not in state and info["requires"].issubset(state)]

def apply_action(state, action):
    return state | {action}
