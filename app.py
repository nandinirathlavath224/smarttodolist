import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from database import init_db
from Home import show_home
from Task_Page import show_task_page
from Retrieve import show_retrieve
from History import show_history

# 1. Page Configuration
st.set_page_config(
    page_title="Smart Todo List",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Database Initialization
# Ensures folder/files tasks.json and history.json are created immediately
init_db()

# 3. Session State Navigation Setup
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home Dashboard"

# 4. Custom Sidebar UI
st.sidebar.markdown(
    """
    <div style="text-align: center; margin-bottom: 25px; padding-top: 10px;">
        <h1 style="color: #6366f1; margin: 0; font-size: 2.2rem; font-weight: 700; font-family: 'Outfit', sans-serif;">SmartTodo 📝</h1>
        <p style="color: #94a3b8; font-size: 0.9rem; margin-top: 5px; font-family: 'Outfit', sans-serif;">Modular Task Dashboard</p>
    </div>
    """,
    unsafe_allow_html=True
)

navigation_mapping = {
    "Home Dashboard 📊": "Home Dashboard",
    "Manage Tasks 📋": "Manage Tasks",
    "Advanced Search 🔍": "Advanced Search",
    "Audit Logs 🕰️": "Audit Logs"
}

# Determine default selected index
try:
    default_index = list(navigation_mapping.values()).index(st.session_state.current_page)
except ValueError:
    default_index = 0

selected_label = st.sidebar.radio(
    "NAVIGATION",
    options=list(navigation_mapping.keys()),
    index=default_index,
    label_visibility="visible"
)

# Update page route state
st.session_state.current_page = navigation_mapping[selected_label]

st.sidebar.markdown("<br><hr style='border-color: rgba(255,255,255,0.05);'><br>", unsafe_allow_html=True)
st.sidebar.markdown(
    """
    <div style="color: #64748b; font-size: 0.8rem; text-align: center; font-family: 'Outfit', sans-serif;">
        <p style="margin: 2px;">Smart Todo List v1.0.0</p>
        <p style="margin: 2px;">JSON Database System</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 5. Page Routing Controller
if st.session_state.current_page == "Home Dashboard":
    show_home()
elif st.session_state.current_page == "Manage Tasks":
    show_task_page()
elif st.session_state.current_page == "Advanced Search":
    show_retrieve()
elif st.session_state.current_page == "Audit Logs":
    show_history()
