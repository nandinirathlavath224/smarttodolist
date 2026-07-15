import streamlit as st
from utils.history_manager import get_history, clear_history, export_history_json
from utils.ui_helper import inject_custom_css

def show_history():
    """
    Renders the History log page, providing filters, searching,
    history clearing (with confirmation), and JSON export options.
    """
    inject_custom_css()
    
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.title("Audit Trail & Action History 🕰️")
    st.markdown("Track updates, completions, deletions, and additions for your tasks.")
    st.write("")
    
    history_logs = get_history()
    
    if not history_logs:
        st.info("No logs found. Perform actions on your tasks to generate entries.")
        st.markdown('</div>', unsafe_allow_html=True)
        return
        
    # Actions panel
    col_dl, col_clr = st.columns([3, 2])
    
    with col_dl:
        json_str = export_history_json()
        st.download_button(
            label="📥 Export History as JSON",
            data=json_str,
            file_name="task_history.json",
            mime="application/json",
            use_container_width=True
        )
        
    with col_clr:
        # Secure clear mechanism via Streamlit popover
        with st.popover("🗑️ Clear History Logs", use_container_width=True):
            st.warning("This action is permanent and will clear all logged events.")
            if st.button("Yes, Clear History", type="primary", use_container_width=True):
                clear_history()
                st.success("History cleared!")
                st.rerun()
                
    st.write("")
    st.markdown("---")
    st.write("")
    
    # Search and Filter
    st.subheader("Filter Audit Logs")
    f_col1, f_col2 = st.columns([3, 2])
    
    with f_col1:
        search_query = st.text_input("Search query logs", placeholder="Search by task title or keyword...", label_visibility="collapsed")
        
    with f_col2:
        actions_list = list(set([h["action"] for h in history_logs]))
        actions_list.sort()
        action_filter = st.selectbox("Action Type Filter", ["All Actions"] + actions_list, label_visibility="collapsed")
        
    # Filtering logic
    filtered_history = history_logs
    if search_query:
        q = search_query.lower()
        filtered_history = [h for h in filtered_history if q in h["task_title"].lower() or q in h["action"].lower()]
        
    if action_filter != "All Actions":
        filtered_history = [h for h in filtered_history if h["action"] == action_filter]
        
    st.write("")
    
    # Render logs
    if filtered_history:
        for log in filtered_history:
            action = log["action"]
            
            # Select icon and badge colors based on action type
            icon = "📝"
            color = "#818cf8"  # Slate indigo
            if "Created" in action:
                icon = "➕"
                color = "#3b82f6"  # Blue
            elif "Completed" in action:
                icon = "✅"
                color = "#10b981"  # Emerald Green
            elif "Deleted" in action:
                icon = "🗑️"
                color = "#ef4444"  # Red
            elif "Archived" in action:
                icon = "📥"
                color = "#f59e0b"  # Amber
            elif "Restored" in action:
                icon = "📤"
                color = "#06b6d4"  # Cyan
            elif "Important" in action:
                icon = "⭐"
                color = "#ec4899"  # Pink
                
            st.markdown(
                f"""
                <div style="background-color: #1e293b; padding: 12px 18px; border-radius: 10px; border-left: 5px solid {color}; margin-bottom: 10px; border-top: 1px solid rgba(255,255,255,0.03); border-right: 1px solid rgba(255,255,255,0.03); border-bottom: 1px solid rgba(255,255,255,0.03);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 600; color: #f8fafc; font-size: 1.05rem;">{icon} {log['task_title']}</span>
                        <span style="color: #64748b; font-size: 0.8rem; font-weight: 500;">{log['timestamp']}</span>
                    </div>
                    <div style="color: #cbd5e1; font-size: 0.85rem; margin-top: 4px;">
                        Event: <span style="color: {color}; font-weight: 600;">{action}</span>
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
    else:
        st.warning("No records found matching filters.")
        
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_history()
