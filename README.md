# Smart Todo List Application 📝

A modern, responsive, and beautiful **Smart Todo List** application built with Python and Streamlit, featuring a JSON file-based database architecture, advanced sorting/filtering mechanisms, dynamic status statistics, and an automated audit trail logging system.

---

## 🌟 Key Features

1. **Home Dashboard**
   - Live KPI Metrics: Total Tasks, Pending Tasks, Completed Tasks, and Today's Due Tasks.
   - Interactive Progress Bar visualizing task completion percentage.
   - Dynamic charts powered by Plotly (Donut Chart for category breakdown and Bar Chart for priority counts).
   - Recent Activities Ticker showcasing the latest 5 operations instantly.

2. **Task Management (CRUD & Actions)**
   - Add new tasks with description, priority level (High, Medium, Low), due date, custom categories, and importance marker.
   - Edit inline details using prepopulated forms.
   - Toggle status directly via checkbox (instantly logs status transitions).
   - Mark as important (star indicator).
   - Archive/Restore tasks to clean the dashboard view.
   - Real-time search query matching.
   - Comprehensive sorting options (by Due Date, Priority, or Created Date) and filter parameters (Status, Priority, Category).

3. **Advanced Retrieval Directory**
   - Powerful multi-criteria real-time search engine.
   - Match fields simultaneously using category tags, priority weights, status values, date ranges, and title text matches.

4. **Audit History Log**
   - Automated logger tracking all lifecycle updates (Task Created, Task Updated, Task Completed, Task Deleted, Task Archived, Task Restored).
   - Shows action labels, task names, and exact datetime stamps.
   - Filter history by event category and keyword search logs.
   - Clear history logs securely.
   - Export full log history as a formatted JSON file with one click.

---

## 🛠️ Project Structure

```
SmartTodo/
│── app.py                 # Main entry point & routing hub
│── requirements.txt       # Dependencies list
│── .env                   # Configuration variables
│── .streamlit/
│   └── config.toml        # Streamlit theme & sidebar routing configuration
│── database/
│   ├── tasks.json         # Tasks JSON database file (auto-created)
│   └── history.json       # Actions JSON database file (auto-created)
│── pages/
│   ├── Home.py            # Home Dashboard layout & charts
│   ├── Task_Page.py       # Task CRUD operations & view lists
│   ├── Retrieve.py        # Advanced multi-criteria search page
│   └── History.py         # Audit trail viewer & exporter
└── utils/
    ├── database.py        # Database init, read, and write operations
    ├── task_manager.py    # Tasks CRUD & metrics utilities
    ├── history_manager.py # Logging audit actions & export logic
    └── ui_helper.py       # Custom CSS variables, fonts, gradients & animations
```

---

## 🚀 Setup & Execution Guide

### Prerequisites
- Python 3.8+ installed on your computer.

### Step 1: Install Dependencies
Run the following command in your terminal to install the necessary libraries:
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
Start the Streamlit application using:
```bash
streamlit run app.py
```
This will start a local server and automatically open the application in your browser at `http://localhost:8501`.

---

## 📂 Database & Fields

The application uses local JSON files inside the `database/` directory. If the directory or files do not exist, they will be created automatically on application launch.

### `tasks.json` structure
- `id` (string, UUID): Unique task ID
- `title` (string): Title of the task
- `description` (string): Summary description
- `priority` (string): High, Medium, or Low
- `category` (string): Custom category tag
- `due_date` (string): Due Date (YYYY-MM-DD)
- `status` (string): Pending or Completed
- `created_at` (string): Datetime created
- `updated_at` (string): Datetime updated
- `important` (boolean): Starred status
- `archived` (boolean): Archived status

### `history.json` structure
- `task_id` (string): Targeted task ID
- `task_title` (string): Name of task
- `action` (string): Action performed
- `timestamp` (string): Datetime stamp
