from datetime import datetime
import json
from utils.database import HISTORY_FILE, read_json, write_json

def log_action(task_id, task_title, action):
    """
    Appends an action log to history.json.
    """
    history = read_json(HISTORY_FILE)
    
    entry = {
        "task_id": str(task_id),
        "task_title": task_title,
        "action": action,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Prepend to show latest logs first
    history.insert(0, entry)
    write_json(HISTORY_FILE, history)

def get_history():
    """
    Returns the complete list of history logs.
    """
    return read_json(HISTORY_FILE)

def clear_history():
    """
    Clears all logs from history.json.
    """
    write_json(HISTORY_FILE, [])

def export_history_json():
    """
    Exports the history as a JSON string for download.
    """
    history = get_history()
    return json.dumps(history, indent=4)
