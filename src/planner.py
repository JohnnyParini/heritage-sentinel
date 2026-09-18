# planner.py — search algorithm only. No mention of statues, cracks, or pigment allowed here.
from collections import deque

def bfs_search(start, goal, available_actions, apply_action):
    frontier = deque([(start, [])])
    visited = {start}
    while frontier:
        state, path = frontier.popleft()
        if state == goal:
            return path
        
        for action in available_actions(state):
            new_state = apply_action(state, action)

            if new_state not in visited:
                new_path = path + [action]
                frontier.append((new_state, new_path))
            
        visited.add(state)

        # TODO: for each action available from `state`, compute the next
        # state, and if it hasn't been visited, add it to the frontier
        # with the updated path.
        ...
    return None  # no valid sequence exists