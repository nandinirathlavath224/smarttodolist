import os
import json
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "database"
TASKS_FILE = DB_DIR / "tasks.json"
HISTORY_FILE = DB_DIR / "history.json"

def init_db():
    """
    Initializes the database directory and files.
    Automatically creates tasks.json and history.json if they do not exist.
    """
    # Ensure the directory exists
    DB_DIR.mkdir(parents=True, exist_ok=True)
    
    # Initialize tasks.json if it doesn't exist or is empty
    if not TASKS_FILE.exists() or TASKS_FILE.stat().st_size == 0:
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)
            
    # Initialize history.json if it doesn't exist or is empty
    if not HISTORY_FILE.exists() or HISTORY_FILE.stat().st_size == 0:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)

def read_json(file_path):
    """
    Reads data from a JSON file.
    Returns an empty list if file not found or corrupted.
    """
    init_db()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # Re-initialize to clean state if JSON is corrupt
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)
        return []

def write_json(file_path, data):
    """
    Writes data to a JSON file.
    """
    init_db()
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
