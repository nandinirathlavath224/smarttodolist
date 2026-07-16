import uuid
from datetime import datetime, date
from utils.database import TASKS_FILE, read_json, write_json
from utils.history_manager import log_action

def get_all_tasks():
    """
    Returns all tasks from the tasks.json file.
    """
    return read_json(TASKS_FILE)

def add_task(title, description, priority, category, due_date, important=False):
    """
    Adds a new task, saves it to database, and logs a creation history entry.
    """
    tasks = get_all_tasks()
    
    # Standardize due date as string
    if isinstance(due_date, (date, datetime)):
        due_date_str = due_date.strftime("%Y-%m-%d")
    else:
        due_date_str = str(due_date)
        
    task_id = str(uuid.uuid4())
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    new_task = {
        "id": task_id,
        "title": title.strip(),
        "description": description.strip(),
        "priority": priority,  # High, Medium, Low
        "category": category.strip() if category else "General",
        "due_date": due_date_str,
        "status": "Pending",
        "created_at": now_str,
        "updated_at": now_str,
        "important": bool(important),
        "archived": False
    }
    
    tasks.append(new_task)
    write_json(TASKS_FILE, tasks)
    log_action(task_id, new_task["title"], "Task Created")
    return new_task

def update_task(task_id, **kwargs):
    """
    Updates specific task attributes and logs changes to history.
    """
    tasks = get_all_tasks()
    task_index = next((i for i, t in enumerate(tasks) if t["id"] == task_id), None)
    
    if task_index is None:
        return None
        
    task = tasks[task_index]
    updated = False
    action_logged = False
    
    # Check fields
    if "title" in kwargs and kwargs["title"].strip() != task["title"]:
        task["title"] = kwargs["title"].strip()
        updated = True
        
    if "description" in kwargs and kwargs["description"].strip() != task["description"]:
        task["description"] = kwargs["description"].strip()
        updated = True
        
    if "priority" in kwargs and kwargs["priority"] != task["priority"]:
        task["priority"] = kwargs["priority"]
        updated = True
        
    if "category" in kwargs and kwargs["category"].strip() != task["category"]:
        task["category"] = kwargs["category"].strip()
        updated = True
        
    if "due_date" in kwargs:
        due_date = kwargs["due_date"]
        if isinstance(due_date, (date, datetime)):
            due_date_str = due_date.strftime("%Y-%m-%d")
        else:
            due_date_str = str(due_date)
        if due_date_str != task["due_date"]:
            task["due_date"] = due_date_str
            updated = True
            
    if "status" in kwargs and kwargs["status"] != task["status"]:
        task["status"] = kwargs["status"]
        updated = True
        # Log specific action
        log_action(task_id, task["title"], f"Task Completed" if task["status"] == "Completed" else "Task Restored to Pending")
        action_logged = True
        
    if "important" in kwargs and bool(kwargs["important"]) != task["important"]:
        task["important"] = bool(kwargs["important"])
        updated = True
        log_action(task_id, task["title"], f"Task marked Important" if task["important"] else "Task marked Normal")
        action_logged = True
        
    if "archived" in kwargs and bool(kwargs["archived"]) != task["archived"]:
        task["archived"] = bool(kwargs["archived"])
        updated = True
        log_action(task_id, task["title"], "Task Archived" if task["archived"] else "Task Restored")
        action_logged = True
        
    if updated:
        task["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tasks[task_index] = task
        write_json(TASKS_FILE, tasks)
        
        # Log general update if specific toggles were not already logged
        if not action_logged:
            log_action(task_id, task["title"], "Task Updated")
            
    return task

def delete_task(task_id):
    """
    Deletes a task from the database and logs a deletion history entry.
    """
    tasks = get_all_tasks()
    task_index = next((i for i, t in enumerate(tasks) if t["id"] == task_id), None)
    
    if task_index is None:
        return False
        
    task_title = tasks[task_index]["title"]
    
    # Remove task
    tasks.pop(task_index)
    write_json(TASKS_FILE, tasks)
    
    log_action(task_id, task_title, "Task Deleted")
    return True

def get_task_metrics():
    """
    Calculates summary metrics for all non-archived tasks.
    """
    all_tasks = get_all_tasks()
    active_tasks = [t for t in all_tasks if not t["archived"]]
    
    total = len(active_tasks)
    pending = len([t for t in active_tasks if t["status"] == "Pending"])
    completed = len([t for t in active_tasks if t["status"] == "Completed"])
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    today = len([t for t in active_tasks if t["due_date"] == today_str])
    
    completion_rate = round((completed / total * 100), 1) if total > 0 else 0.0
    
    return {
        "total": total,
        "pending": pending,
        "completed": completed,
        "today": today,
        "completion_rate": completion_rate
    }
