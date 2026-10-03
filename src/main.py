from restoration_graph import START, GOAL, available_actions, apply_action
from planner import bfs_search
from csp import backtracking_search
from restoration_csp import build_constraints, VARIABLES, DOMAINS
if __name__ == "__main__":
    # plan = bfs_search(START, GOAL, available_actions, apply_action)
    # print("Restoration plan:", plan)
    
    constraints = build_constraints()
    solutions = backtracking_search(VARIABLES, DOMAINS, constraints, all_solutions=True)
    print("Number of solutions found: ", len(solutions))
    constraints = build_constraints(tranche_cap=3)
    solutions = backtracking_search(VARIABLES, DOMAINS, constraints, all_solutions=True)
    print("Number of solutions found: ", len(solutions))
    constraints = build_constraints(tranche_cap=2)
    solutions = backtracking_search(VARIABLES, DOMAINS, constraints, all_solutions=True)
    print("Number of solutions found: ", len(solutions))