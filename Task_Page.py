import streamlit as st
from datetime import datetime, date
from utils.task_manager import get_all_tasks, add_task, update_task, delete_task
from utils.ui_helper import inject_custom_css

def show_task_page():
    """
    Renders the Task Management page with task creation, editing,
    searching, filtering, sorting, and inline card operations.
    """
    inject_custom_css()
    
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.title("Manage Tasks 📋")
    st.markdown("Add, edit, structure, search, and update details for all of your tasks here.")
    st.write("")
    
    # Initialize edit task state
    if "editing_task_id" not in st.session_state:
        st.session_state.editing_task_id = None
        
    tasks = get_all_tasks()
    
    # ------------------ TASK EDITING PANEL ------------------
    if st.session_state.editing_task_id:
        task_to_edit = next((t for t in tasks if t["id"] == st.session_state.editing_task_id), None)
        if task_to_edit:
            st.markdown("### ✏️ Edit Task")
            with st.form("edit_task_form", clear_on_submit=False):
                edit_title = st.text_input("Title*", value=task_to_edit["title"])
                edit_description = st.text_area("Description", value=task_to_edit["description"])
                
                col_p, col_c, col_d = st.columns(3)
                with col_p:
                    try:
                        p_index = ["High", "Medium", "Low"].index(task_to_edit["priority"])
                    except ValueError:
                        p_index = 1
                    edit_priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=p_index)
                with col_c:
                    edit_category = st.text_input("Category", value=task_to_edit["category"])
                with col_d:
                    try:
                        due_val = datetime.strptime(task_to_edit["due_date"], "%Y-%m-%d").date()
                    except ValueError:
                        due_val = date.today()
                    edit_due_date = st.date_input("Due Date", value=due_val)
                    
                edit_important = st.checkbox("Important Task", value=task_to_edit["important"])
                
                col_save, col_cancel = st.columns(2)
                with col_save:
                    save_btn = st.form_submit_button("Save Changes")
                with col_cancel:
                    cancel_btn = st.form_submit_button("Cancel")
                    
                if save_btn:
                    if not edit_title.strip():
                        st.error("Task title is required!")
                    else:
                        update_task(
                            task_to_edit["id"],
                            title=edit_title,
                            description=edit_description,
                            priority=edit_priority,
                            category=edit_category if edit_category else "General",
                            due_date=edit_due_date,
                            important=edit_important
                        )
                        st.session_state.editing_task_id = None
                        st.success("Task updated successfully!")
                        st.rerun()
                elif cancel_btn:
                    st.session_state.editing_task_id = None
                    st.rerun()
            st.write("---")
            
    # ------------------ TASK CREATION EXPANDER ------------------
    else:
        with st.expander("➕ Add New Task", expanded=False):
            with st.form("new_task_form", clear_on_submit=True):
                title = st.text_input("Task Title*", placeholder="What needs to be done?")
                description = st.text_area("Task Description", placeholder="Enter task details (optional)...")
                
                col_p, col_c, col_d = st.columns(3)
                with col_p:
                    priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=1)
                with col_c:
                    category = st.text_input("Category", placeholder="e.g. Work, Personal, Life")
                with col_d:
                    due_date = st.date_input("Due Date", value=date.today())
                    
                important = st.checkbox("Mark as Important")
                
                submitted = st.form_submit_button("Add Task")
                if submitted:
                    if not title.strip():
                        st.error("Task title is required!")
                    else:
                        add_task(
                            title=title,
                            description=description,
                            priority=priority,
                            category=category.strip() if category.strip() else "General",
                            due_date=due_date,
                            important=important
                        )
                        st.success("Task added successfully!")
                        st.rerun()
        st.write("")

    # ------------------ SEARCH, FILTER & SORT PANEL ------------------
    st.write("### Filter & Sort Tasks 🔍")
    f_col1, f_col2, f_col3, f_col4 = st.columns([2, 1, 1, 1])
    
    with f_col1:
        search_query = st.text_input("Search query", placeholder="Search tasks by title or description...", label_visibility="collapsed")
    with f_col2:
        status_filter = st.selectbox("Filter by Status", ["All Active", "Pending", "Completed", "Archived", "All Tasks"])
    with f_col3:
        priority_filter = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
    with f_col4:
        # Extract existing categories
        all_t = get_all_tasks()
        categories = list(set([t["category"] for t in all_t if t.get("category")]))
        categories.sort()
        category_filter = st.selectbox("Filter by Category", ["All"] + categories)

    s_col1, s_col2 = st.columns(2)
    with s_col1:
        sort_by = st.selectbox("Sort By", ["Due Date", "Priority", "Created Date"])
    with s_col2:
        sort_order = st.selectbox("Sort Order", ["Ascending", "Descending"])

    st.write("---")

    # ------------------ FILTERING & SORTING LOGIC ------------------
    filtered_tasks = get_all_tasks()

    # Apply Status Filter
    if status_filter == "All Active":
        filtered_tasks = [t for t in filtered_tasks if not t["archived"]]
    elif status_filter == "Pending":
        filtered_tasks = [t for t in filtered_tasks if t["status"] == "Pending" and not t["archived"]]
    elif status_filter == "Completed":
        filtered_tasks = [t for t in filtered_tasks if t["status"] == "Completed" and not t["archived"]]
    elif status_filter == "Archived":
        filtered_tasks = [t for t in filtered_tasks if t["archived"]]

    # Apply Priority Filter
    if priority_filter != "All":
        filtered_tasks = [t for t in filtered_tasks if t["priority"] == priority_filter]

    # Apply Category Filter
    if category_filter != "All":
        filtered_tasks = [t for t in filtered_tasks if t["category"] == category_filter]

    # Apply Search Query
    if search_query:
        q = search_query.lower()
        filtered_tasks = [t for t in filtered_tasks if q in t["title"].lower() or q in t["description"].lower()]

    # Sort Tasks
    priority_weights = {"High": 3, "Medium": 2, "Low": 1}
    
    def sort_key(t):
        if sort_by == "Due Date":
            return t["due_date"]
        elif sort_by == "Priority":
            return priority_weights.get(t["priority"], 0)
        else: # Created Date
            return t["created_at"]

    reverse = (sort_order == "Descending")
    filtered_tasks.sort(key=sort_key, reverse=reverse)

    # ------------------ TASK LIST RENDER ------------------
    if filtered_tasks:
        for task in filtered_tasks:
            # Determine due date badge classes
            try:
                due_parsed = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
                is_overdue = due_parsed < date.today() and task["status"] == "Pending"
            except ValueError:
                is_overdue = False
                
            badge_due_class = "badge-overdue" if is_overdue else "badge-due"
            due_label = f"⚠️ Overdue: {task['due_date']}" if is_overdue else f"📅 Due: {task['due_date']}"
            priority_class = f"badge-{task['priority'].lower()}"
            important_badge = '<span class="custom-badge badge-important">⭐ Important</span>' if task["important"] else ''
            
            task_container_class = f"task-container priority-{task['priority'].lower()}"
            
            # Start UI container
            st.markdown(f'<div class="{task_container_class}">', unsafe_allow_html=True)
            
            # Outer grid mapping
            col_check, col_text, col_actions = st.columns([0.6, 6.4, 3.0])
            
            with col_check:
                st.write("")  # Margin
                # Render completion checkbox
                is_checked = st.checkbox("", value=(task["status"] == "Completed"), key=f"chk_{task['id']}", label_visibility="collapsed")
                db_checked = (task["status"] == "Completed")
                if is_checked != db_checked:
                    new_status = "Completed" if is_checked else "Pending"
                    update_task(task["id"], status=new_status)
                    st.rerun()
                    
            with col_text:
                # Text section
                title_style = "text-decoration: line-through; color: #64748b; font-style: italic;" if task["status"] == "Completed" else "color: #f8fafc;"
                st.markdown(
                    f"""
                    <div style="margin-bottom: 5px;">
                        <h4 style="margin: 0; padding: 0; font-size: 1.15rem; font-weight: 600; {title_style}">
                            {task['title']}
                        </h4>
                        <p style="margin: 4px 0 8px 0; color: #94a3b8; font-size: 0.9rem; line-height: 1.4;">
                            {task['description']}
                        </p>
                        <div>
                            <span class="custom-badge {priority_class}">{task['priority']} Priority</span>
                            <span class="custom-badge badge-category">📂 {task['category']}</span>
                            <span class="custom-badge {badge_due_class}">{due_label}</span>
                            {important_badge}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
            with col_actions:
                st.write("") # Vertical offset
                sub_col1, sub_col2, sub_col3 = st.columns(3)
                
                with sub_col1:
                    # Toggle Starred/Important
                    star_lbl = "⭐" if task["important"] else "☆"
                    if st.button(star_lbl, key=f"star_btn_{task['id']}", help="Toggle Importance"):
                        update_task(task["id"], important=not task["important"])
                        st.rerun()
                with sub_col2:
                    # Edit Task
                    if st.button("✏️", key=f"edit_btn_{task['id']}", help="Edit Task Details"):
                        st.session_state.editing_task_id = task["id"]
                        st.rerun()
                with sub_col3:
                    # Archive/Restore Task
                    arch_lbl = "📤" if task["archived"] else "📥"
                    arch_hlp = "Restore Task" if task["archived"] else "Archive Task"
                    if st.button(arch_lbl, key=f"arch_btn_{task['id']}", help=arch_hlp):
                        update_task(task["id"], archived=not task["archived"])
                        st.rerun()
                        
                # Delete task button
                if st.button("🗑️ Delete Task", key=f"del_btn_{task['id']}", use_container_width=True):
                    delete_task(task["id"])
                    st.rerun()
                    
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No matching tasks found. Create a task or adjust your filters!")
        
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_task_page()
