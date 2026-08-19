import json
from models import AgentState
from pathlib import Path
from dataclasses import asdict
from datetime import datetime


STATE_FILE = Path("workdir") / "agent_state.json"

def initialize_state():
    STATE_FILE.parent.mkdir(parents = True , exist_ok = True)
    if STATE_FILE.exists():
        return
    state = AgentState()
    data = asdict(state)
    with STATE_FILE.open("w") as file:
        json.dump(data , file , indent= 4)

def load_state():
    with STATE_FILE.open("r") as file:
        data = json.load(file)
        state = AgentState(**data)
    return state

def save_state(state: AgentState):
    state.last_updated = datetime.now().isoformat()
    data = asdict(state)
    with STATE_FILE.open("w") as file:
        json.dump(data , file , indent = 4)






