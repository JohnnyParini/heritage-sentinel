# restoration_graph.py — problem definition only.
# planner.py must not know anything specific to this file.

LARGE_ACTIONS = {
    "Open Launcher": {"requires": set(), "cost": 5},
    "View Owned Champions": {"requires": {"Open Launcher"}, "cost": 1},
    "View Owned Skins": {"requires": {"Open Launcher"}, "cost": 1},
    "Buy Champion": {"requires": {"Open Launcher"}, "cost": 2},
    "Buy Skin": {"requires": {"Open Launcher"}, "cost": 2},
    "Message Friend": {"requires": {"Open Launcher"}, "cost": 1},
    "Create Lobby": {"requires": {"Open Launcher"}, "cost": 1},
    "Invite Friends": {"requires": {"Open Launcher", "Create Lobby"}, "cost": 1},
    "Start Queue": {"requires": {"Open Launcher", "Create Lobby"}, "cost": 1},
    "Accept Queue": {"requires": {"Open Launcher", "Create Lobby", "Start Queue"}, "cost": 1},
    "Ban Champion": {"requires": {"Open Launcher", "Create Lobby", "Start Queue", "Accept Queue"}, "cost": 4},
    "Select Champion": {"requires": {"Open Launcher", "Create Lobby", "Start Queue", "Accept Queue"}, "cost": 3},
    "Select Runes": {"requires": {"Open Launcher", "Create Lobby", "Start Queue", "Accept Queue"}, "cost": 3},
    "Select Summoner Spells": {"requires": {"Open Launcher", "Create Lobby", "Start Queue", "Accept Queue"}, "cost": 2},
    "Select Skin": {"requires": {"Open Launcher", "Create Lobby", "Start Queue", "Accept Queue", "Select Champion"}, "cost": 1},
    "Load Game": {"requires": {"Open Launcher", "Create Lobby", "Start Queue", "Accept Queue", "Select Champion"}, "cost": 3},
    "Buy Items": {"requires": {"Load Game"}, "cost": 2},
    "Move": {"requires": {"Load Game"}, "cost": 4},
    "Farm": {"requires": {"Load Game"}, "cost": 8},
    "Win": {"requires": {"Load Game"}, "cost": 10},
}

LARGE_GOAL = frozenset(LARGE_ACTIONS.keys())
LARGE_START = frozenset()

def large_available_actions(state):
    """Actions whose prerequisites are satisfied and not already done."""
    return [a for a, info in LARGE_ACTIONS.items()
            if a not in state and info["requires"].issubset(state)]

def large_apply_action(state, action):
    return state | {action}
