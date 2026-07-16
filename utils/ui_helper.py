import streamlit as st

def inject_custom_css():
    """
    Injects custom styles for cards, scrollbars, list items, and modern dashboard enhancements.
    Uses glassmorphism and subtle gradient elements.
    """
    st.markdown(
        """
        <style>
        /* General styling resets and animations */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
        
        /* Modernized Streamlit defaults */
        .stApp {
            background-color: #0f172a;
        }
        
        h1, h2, h3, p, span, div, label {
            font-family: 'Outfit', sans-serif !important;
        }

        /* Glassmorphic Metric Cards */
        .dashboard-card {
            padding: 1.5rem;
            border-radius: 16px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            margin-bottom: 1rem;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            color: #ffffff;
        }
        
        .dashboard-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.3);
            border-color: rgba(255, 255, 255, 0.15);
        }

        /* Gradients for KPI Metrics */
        .gradient-total {
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        }
        .gradient-pending {
            background: linear-gradient(135deg, #ea580c 0%, #f97316 100%);
        }
        .gradient-completed {
            background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        }
        .gradient-today {
            background: linear-gradient(135deg, #db2777 0%, #ec4899 100%);
        }

        .card-value {
            font-size: 2.2rem;
            font-weight: 700;
            line-height: 1;
            margin: 0.5rem 0;
        }

        .card-label {
            font-size: 0.9rem;
            font-weight: 500;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* Task Cards */
        .task-container {
            background: #1e293b;
            border-radius: 12px;
            padding: 1.2rem;
            margin-bottom: 1rem;
            border-left: 6px solid #475569;
            transition: all 0.2s ease-in-out;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            border-top: 1px solid rgba(255, 255, 255, 0.03);
            border-right: 1px solid rgba(255, 255, 255, 0.03);
            border-bottom: 1px solid rgba(255, 255, 255, 0.03);
        }
        
        .task-container:hover {
            transform: scale(1.01);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            background: #233048;
        }

        /* Priority Colors */
        .priority-high {
            border-left-color: #ef4444 !important;
        }
        .priority-medium {
            border-left-color: #f59e0b !important;
        }
        .priority-low {
            border-left-color: #10b981 !important;
        }
        
        /* Custom badges */
        .custom-badge {
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-block;
            margin-right: 5px;
            margin-bottom: 5px;
        }
        .badge-high {
            background-color: rgba(239, 68, 68, 0.15);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }
        .badge-medium {
            background-color: rgba(245, 158, 11, 0.15);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.3);
        }
        .badge-low {
            background-color: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }
        .badge-important {
            background-color: rgba(236, 72, 153, 0.15);
            color: #f472b6;
            border: 1px solid rgba(236, 72, 153, 0.3);
        }
        .badge-category {
            background-color: rgba(99, 102, 241, 0.15);
            color: #818cf8;
            border: 1px solid rgba(99, 102, 241, 0.3);
        }
        .badge-due {
            background-color: rgba(148, 163, 184, 0.15);
            color: #cbd5e1;
            border: 1px solid rgba(148, 163, 184, 0.3);
        }
        .badge-overdue {
            background-color: rgba(239, 68, 68, 0.2);
            color: #fca5a5;
            border: 1px solid rgba(239, 68, 68, 0.5);
            animation: pulse 2s infinite;
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: .7; }
        }
        
        .fade-in {
            animation: fadeIn 0.4s ease-out forwards;
        }
        
        /* Modern form formatting */
        div[data-testid="stForm"] {
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            background-color: #1e293b !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
        }

        /* Sidebar modification */
        section[data-testid="stSidebar"] {
            background-color: #1e293b !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        }
        
        </style>
        """,
        unsafe_allow_html=True
    )

def render_metric_card(label, value, icon, gradient_class):
    """
    Renders a custom gradient metric card.
    """
    st.markdown(
        f"""
        <div class="dashboard-card {gradient_class} fade-in">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="card-label">{label}</span>
                <span style="font-size: 1.8rem;">{icon}</span>
            </div>
            <div class="card-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
