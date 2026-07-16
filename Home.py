import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.task_manager import get_all_tasks, get_task_metrics
from utils.history_manager import get_history
from utils.ui_helper import inject_custom_css, render_metric_card

def show_home():
    """
    Renders the Home Dashboard page with KPIs, progress tracker,
    dynamic Plotly charts, and recent activity logs.
    """
    inject_custom_css()
    
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.title("Smart Todo Dashboard 📊")
    st.markdown("Welcome to your Smart Todo List dashboard. Track your tasks, categories, and audit logs in real-time.")
    st.write("")
    
    # Fetch summary metrics
    metrics = get_task_metrics()
    
    # Layout KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card("Total Tasks", metrics["total"], "📝", "gradient-total")
    with col2:
        render_metric_card("Pending Tasks", metrics["pending"], "⏳", "gradient-pending")
    with col3:
        render_metric_card("Completed Tasks", metrics["completed"], "✅", "gradient-completed")
    with col4:
        render_metric_card("Today's Tasks", metrics["today"], "📅", "gradient-today")
        
    st.write("")
    
    # Completion Rate Progress Bar
    st.subheader("Task Completion Progress")
    progress_val = metrics["completion_rate"] / 100.0
    st.progress(progress_val)
    st.write(f"📊 **{metrics['completion_rate']}%** of your active tasks are completed.")
    
    st.write("")
    st.markdown("---")
    st.write("")
    
    # Charts Row
    st.subheader("Task Analytics")
    col_chart1, col_chart2 = st.columns(2)
    
    all_tasks = [t for t in get_all_tasks() if not t["archived"]]
    
    if all_tasks:
        df = pd.DataFrame(all_tasks)
        
        with col_chart1:
            st.markdown("### Tasks by Category 🏷️")
            category_counts = df["category"].value_counts().reset_index()
            category_counts.columns = ["Category", "Count"]
            
            fig_cat = px.pie(
                category_counts, 
                values="Count", 
                names="Category", 
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_cat.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f8fafc", family="Outfit"),
                legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
                margin=dict(t=10, b=10, l=10, r=10)
            )
            st.plotly_chart(fig_cat, use_container_width=True)
            
        with col_chart2:
            st.markdown("### Tasks by Priority ⚡")
            priority_order = ["High", "Medium", "Low"]
            # Reindex to ensure order and full representation
            priority_counts = df["priority"].value_counts().reindex(priority_order, fill_value=0).reset_index()
            priority_counts.columns = ["Priority", "Count"]
            
            # Match badge styling colors
            color_map = {"High": "#ef4444", "Medium": "#f59e0b", "Low": "#10b981"}
            
            fig_pri = px.bar(
                priority_counts, 
                x="Priority", 
                y="Count",
                color="Priority",
                color_discrete_map=color_map,
                category_orders={"Priority": priority_order}
            )
            fig_pri.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f8fafc", family="Outfit"),
                showlegend=False,
                xaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="Priority"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="Number of Tasks"),
                margin=dict(t=10, b=10, l=10, r=10)
            )
            st.plotly_chart(fig_pri, use_container_width=True)
    else:
        with col_chart1:
            st.info("No active tasks found. Add a task to display category data.")
        with col_chart2:
            st.info("No active tasks found. Add a task to display priority charts.")
            
    st.write("")
    st.markdown("---")
    st.write("")
    
    # Recent Activities Log
    st.subheader("Recent Activity Log 🕰️")
    history_logs = get_history()[:5]  # Retrieve last 5 actions
    
    if history_logs:
        for log in history_logs:
            # Format action badge style color
            action = log["action"]
            color = "#6366f1"  # default purple
            if "Created" in action:
                color = "#3b82f6"  # blue
            elif "Completed" in action:
                color = "#10b981"  # green
            elif "Deleted" in action:
                color = "#ef4444"  # red
            elif "Archived" in action:
                color = "#f59e0b"  # amber
                
            st.markdown(
                f"""
                <div style="background-color: #1e293b; padding: 12px 18px; border-radius: 10px; border-left: 5px solid {color}; margin-bottom: 10px; border-top: 1px solid rgba(255,255,255,0.03); border-right: 1px solid rgba(255,255,255,0.03); border-bottom: 1px solid rgba(255,255,255,0.03);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 600; color: #f8fafc; font-size: 1rem;">{log['task_title']}</span>
                        <span style="color: #64748b; font-size: 0.8rem; font-weight: 500;">{log['timestamp']}</span>
                    </div>
                    <div style="color: #cbd5e1; font-size: 0.85rem; margin-top: 4px;">
                        Action: <span style="color: {color}; font-weight: 600;">{action}</span>
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
    else:
        st.info("No actions logged in history yet.")
        
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_home()
