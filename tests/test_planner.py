# tests/test_planner.py
from src.restoration_graph import ACTIONS, START, GOAL, available_actions, apply_action
from src.planner import bfs_search

def is_valid_plan(plan, actions=ACTIONS):
    """A plan is valid if every action's prerequisites are satisfied by
    the actions before it, and every required action appears exactly once."""
    completed = set()
    for action in plan:
        if action in completed:
            return False          # duplicate action
        if not actions[action]["requires"].issubset(completed):
            return False          # prerequisite violated
        completed.add(action)
    return completed == set(actions.keys())


def test_finds_a_valid_plan():
    plan = bfs_search(START, GOAL, available_actions, apply_action)
    assert plan is not None
    assert is_valid_plan(plan)


def test_trivial_already_done():
    # start == goal: the plan should be empty, not None, not a crash
    plan = bfs_search(GOAL, GOAL, available_actions, apply_action)
    assert plan == []


def test_plan_has_no_duplicate_actions():
    plan = bfs_search(START, GOAL, available_actions, apply_action)
    assert len(plan) == len(set(plan))


def test_no_solution_returns_none():
    # TODO: this is your job. Construct a problem where the goal is
    # unreachable — e.g. a goal that includes an action name not in
    # ACTIONS, or an action whose "requires" set can never be satisfied
    # (a circular or impossible prerequisite). Then assert that
    # bfs_search returns None instead of crashing or hanging forever.
    
    new_set = set(ACTIONS.keys).add("FAIL NODE")
    plan = bfs_search(START, new_set, available_actions, apply_action)
    assert plan is None



def test_large_action_set_terminates():
    # TODO: build a bigger synthetic ACTIONS dict (15-20 actions, chained
    # prerequisites) and assert bfs_search still returns within a couple
    # of seconds. This isn't about speed — it's about proving the search
    # actually terminates instead of looping.
    ...