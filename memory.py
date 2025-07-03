import json
import os

HISTORY_FILE = "recent_commands.json"

def save_command(command):
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    history.append(command)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history[-20:], f, indent=2)

def show_recent():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
        return "\n".join(f"🕘 {cmd}" for cmd in history[-10:])
    return "No recent commands found."
