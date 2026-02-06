import json
from threading import Lock

attempts_lock = Lock()
commands_lock = Lock()

def log_attempt(event):
    with attempts_lock:
        with open("logs/attempts.json", "a") as f:
            json.dump(event, f)
            f.write("\n")

def log_command(event):
    with commands_lock:
        with open("logs/commands.json", "a") as f:
            json.dump(event, f)
            f.write("\n")
