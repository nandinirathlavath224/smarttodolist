import streamlit as st
from datetime import datetime, date
from utils.task_manager import get_all_tasks
from utils.ui_helper import inject_custom_css

def show_retrieve():
    """
    Renders the Retrieve page for advanced multi-criteria search
    on title, description, priority, category, date range, and status.
    """
    inject_custom_css()
    
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.title("Advanced Task Retrieval 🔍")
    st.markdown("Query and filter tasks across your database using multi-dimensional parameters.")
    st.write("")
    
    tasks = get_all_tasks()
    
    if not tasks:
        st.info("Your database is empty. Add tasks in the Task page to begin searching.")
        st.markdown('</div>', unsafe_allow_html=True)
        return
        
    st.markdown("### Search Filters")
    col1, col2 = st.columns(2)
    
    with col1:
        search_title = st.text_input("Search by Keywords", placeholder="Type title or description terms...")
        
    with col2:
        search_priority = st.multiselect("Filter by Priority", options=["High", "Medium", "Low"], default=["High", "Medium", "Low"])
        
    col3, col4 = st.columns(2)
    
    with col3:
        # Get unique categories
        categories = list(set([t["category"] for t in tasks if t.get("category")]))
        categories.sort()
        search_category = st.multiselect("Filter by Category", options=categories, default=categories)
        
    with col4:
        search_status = st.multiselect("Filter by Status", options=["Pending", "Completed"], default=["Pending", "Completed"])
        
    st.write("")
    st.markdown("**Due Date Range**")
    d_col1, d_col2 = st.columns(2)
    
    # Calculate min and max due dates
    due_dates = []
    for t in tasks:
        try:
            due_dates.append(datetime.strptime(t["due_date"], "%Y-%m-%d").date())
        except ValueError:
            pass
            
    min_date = min(due_dates) if due_dates else date.today()
    max_date = max(due_dates) if due_dates else date.today()
    
    # Pad ranges slightly to make them inclusive
    if min_date > date.today():
        min_date = date.today()
    if max_date < date.today():
        max_date = date.today()
        
    with d_col1:
        start_date = st.date_input("Start Date", value=min_date)
    with d_col2:
        end_date = st.date_input("End Date", value=max_date)
        
    st.write("---")
    
    # ------------------ FILTER QUERY LOGIC ------------------
    results = []
    for task in tasks:
        # Match search title
        if search_title:
            q = search_title.lower()
            if q not in task["title"].lower() and q not in task["description"].lower():
                continue
                
        # Match priority
        if task["priority"] not in search_priority:
            continue
            
        # Match category
        if task["category"] not in search_category:
            continue
            
        # Match status
        if task["status"] not in search_status:
            continue
            
        # Match due date range
        try:
            task_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
            if not (start_date <= task_date <= end_date):
                continue
        except ValueError:
            pass
            
        results.append(task)
        
    # ------------------ DISPLAY RESULTS ------------------
    st.subheader(f"Matching Results ({len(results)})")
    st.write("")
    
    if results:
        for task in results:
            try:
                due_parsed = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
                is_overdue = due_parsed < date.today() and task["status"] == "Pending"
            except ValueError:
                is_overdue = False
                
            badge_due_class = "badge-overdue" if is_overdue else "badge-due"
            due_label = f"⚠️ Overdue: {task['due_date']}" if is_overdue else f"📅 Due: {task['due_date']}"
            priority_class = f"badge-{task['priority'].lower()}"
            important_badge = '<span class="custom-badge badge-important">⭐ Important</span>' if task["important"] else ''
            
            # Status badge styling
            status_style = "background-color: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3);" if task["status"] == "Completed" else "background-color: rgba(249, 115, 22, 0.15); color: #fdba74; border: 1px solid rgba(249, 115, 22, 0.3);"
            
            task_container_class = f"task-container priority-{task['priority'].lower()}"
            
            st.markdown(
                f"""
                <div class="{task_container_class}">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div style="width: 100%;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <h4 style="margin: 0; padding: 0; font-size: 1.15rem; font-weight: 600; color: {'#94a3b8' if task['status'] == 'Completed' else '#f8fafc'}; text-decoration: {'line-through' if task['status'] == 'Completed' else 'none'};">
                                    {task['title']}
                                </h4>
                                <span class="custom-badge" style="{status_style} margin: 0;">{task['status']}</span>
                            </div>
                            <p style="margin: 6px 0 10px 0; color: #cbd5e1; font-size: 0.9rem; line-height: 1.4;">
                                {task['description']}
                            </p>
                            <div>
                                <span class="custom-badge {priority_class}">{task['priority']} Priority</span>
                                <span class="custom-badge badge-category">📂 {task['category']}</span>
                                <span class="custom-badge {badge_due_class}">{due_label}</span>
                                {important_badge}
                                <span class="custom-badge badge-due">📅 Created: {task['created_at'].split(' ')[0]}</span>
                            </div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.warning("No tasks found matching your search parameters.")
        
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_retrieve()
