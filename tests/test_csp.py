import subprocess, sys
from src.csp import backtracking_search
from src.restoration_csp import VARIABLES, DOMAINS, build_constraints
from test_planner import is_valid_plan

def solve(seed=0, cap=4, all_solutions=False):
    return backtracking_search(VARIABLES, DOMAINS, build_constraints(tranche_cap=cap),
                               seed=seed, all_solutions=all_solutions)

def to_plan(assignment):
    return sorted(assignment, key=assignment.get)

def test_solution_is_valid():
    plan = to_plan(solve()[0])
    assert is_valid_plan(plan, tranche_cap=4)

def test_same_seed_same_plan():
    assert solve(seed=7) == solve(seed=7)

def test_solution_counts():
    # TODO: parametrize over the table in the self-check:
    # cap 4 -> 5 plans, cap 3 -> 1 plan, cap 2 -> 0 plans
    for cap, expected in [(4, 5), (3, 1), (2, 0)]:
        assert len(solve(cap=cap, all_solutions=True)) == expected

def test_old_oracle_gap_is_closed():
    bad = ["stabilize_base", "seal_crack", "clean_surface", "restore_pigment"]
    # TODO: assert your extended is_valid_plan rejects this plan at cap 4
    assert is_valid_plan(bad, tranche_cap=4) == False

def test_reproducible_across_processes():
    # TODO: run `src/main_csp.py` in a subprocess twice
    # (subprocess.run([sys.executable, "src/main_csp.py"], capture_output=True,
    # text=True, check=True).stdout) and assert the two outputs are identical.
    # An in-process test can't catch the trap from Part B. This one can.
    out1 = subprocess.run([sys.executable, "src/main_csp.py"], capture_output=True,
                          text=True, check=True).stdout
    out2 = subprocess.run([sys.executable, "src/main_csp.py"], capture_output=True,
                          text=True, check=True).stdout
    assert out1 == out2