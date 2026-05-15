"""
UI Helper functions for consistent styling and components
Provides reusable UI components and styling utilities
"""

import streamlit as st

# Color constants
COLORS = {
    "primary": "#1565c0",
    "primary_light": "#42a5f5",
    "primary_dark": "#0d47a1",
    "secondary": "#667eea",
    "secondary_light": "#9b59b6",
    "success": "#27ae60",
    "warning": "#f39c12",
    "danger": "#e74c3c",
    "info": "#3498db",
    "light": "#ecf0f1",
    "dark": "#2c3e50",
    "text": "#1a237e",
    "text_light": "#546e7a",
    "border": "#cfd8dc",
    "background": "#f5f7fa",
}


def render_header(title, subtitle="", icon="", gradient_colors=None):
    """
    Render a professional header with gradient background
    
    Args:
        title (str): Main title text
        subtitle (str): Optional subtitle text
        icon (str): Optional emoji icon
        gradient_colors (tuple): Optional (color1, color2) for gradient
    """
    if gradient_colors is None:
        gradient_colors = ("#1565c0", "#667eea")
    
    color1, color2 = gradient_colors
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {color1} 0%, {color2} 100%); 
                padding: 2rem; border-radius: 12px; margin-bottom: 2rem; 
                box-shadow: 0 4px 16px rgba(0,0,0,0.1);'>
        <h1 style='color: white; margin: 0; font-size: 2.5rem;'>{icon} {title}</h1>
        {f"<p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 1.1rem;'>{subtitle}</p>" if subtitle else ""}
    </div>
    """, unsafe_allow_html=True)


def render_sidebar_header(title, subtitle="", icon="", gradient_colors=None):
    """
    Render a professional sidebar header
    
    Args:
        title (str): Main title text
        subtitle (str): Optional subtitle text
        icon (str): Optional emoji icon
        gradient_colors (tuple): Optional (color1, color2) for gradient
    """
    if gradient_colors is None:
        gradient_colors = ("#1565c0", "#667eea")
    
    color1, color2 = gradient_colors
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {color1} 0%, {color2} 100%); 
                padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
        <h3 style='color: white; margin: 0; font-size: 1.3rem;'>{icon} {title}</h3>
        {f"<p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 0.9rem;'>{subtitle}</p>" if subtitle else ""}
    </div>
    """, unsafe_allow_html=True)


def render_info_card(content_dict, background_color=None):
    """
    Render an information card with key-value pairs
    
    Args:
        content_dict (dict): Dictionary of key-value pairs to display
        background_color (str): Optional background color
    """
    if background_color is None:
        background_color = "#f5f7fa"
    
    html_content = f"""
    <div style='background: {background_color}; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
    """
    
    for key, value in content_dict.items():
        html_content += f"""
        <p style='margin: 0.5rem 0; font-size: 0.9rem;'><strong>{key}:</strong> {value}</p>
        """
    
    html_content += "</div>"
    
    st.markdown(html_content, unsafe_allow_html=True)


def render_stat_card(label, value, icon="", color=None):
    """
    Render a professional statistic card
    
    Args:
        label (str): Label for the statistic
        value (str/int): Value to display
        icon (str): Optional emoji icon
        color (str): Optional color (default: primary blue)
    """
    if color is None:
        color = COLORS["primary"]
    
    # Extract gradient colors
    if isinstance(color, tuple):
        color1, color2 = color
        gradient = f"linear-gradient(135deg, {color1} 0%, {color2} 100%)"
    else:
        gradient = f"linear-gradient(135deg, {color} 0%, {color} 100%)"
    
    st.markdown(f"""
    <div style='background: {gradient}; 
                padding: 1.5rem; border-radius: 8px; text-align: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
        <p style='color: rgba(255,255,255,0.8); margin: 0; font-size: 0.9rem;'>{icon} {label}</p>
        <p style='color: white; margin: 0.5rem 0 0 0; font-size: 2rem; font-weight: bold;'>
            {value}
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_section_header(title, icon=""):
    """
    Render a section header
    
    Args:
        title (str): Section title
        icon (str): Optional emoji icon
    """
    st.markdown(f"### {icon} {title}")


def render_divider():
    """Render a professional divider"""
    st.markdown("---")


def render_success_message(message):
    """Render a success message"""
    st.success(f"✅ {message}")


def render_error_message(message):
    """Render an error message"""
    st.error(f"❌ {message}")


def render_warning_message(message):
    """Render a warning message"""
    st.warning(f"⚠️ {message}")


def render_info_message(message):
    """Render an info message"""
    st.info(f"ℹ️ {message}")


def render_form_section(title, icon=""):
    """
    Render a form section header
    
    Args:
        title (str): Section title
        icon (str): Optional emoji icon
    """
    st.markdown(f"**{icon} {title}**")


def render_two_column_form(left_label, right_label):
    """
    Create a two-column form layout
    
    Args:
        left_label (str): Label for left column
        right_label (str): Label for right column
        
    Returns:
        tuple: (left_col, right_col) Streamlit columns
    """
    col1, col2 = st.columns(2)
    return col1, col2


def render_three_column_layout():
    """
    Create a three-column layout
    
    Returns:
        tuple: (col1, col2, col3) Streamlit columns
    """
    col1, col2, col3 = st.columns([1, 2, 2])
    return col1, col2, col3


def render_case_card_header(name, location, status, status_emoji=""):
    """
    Render a case card header for expanders
    
    Args:
        name (str): Person's name
        location (str): Location
        status (str): Case status (FOUND/NOT FOUND)
        status_emoji (str): Status emoji
        
    Returns:
        str: Formatted header string
    """
    return f"{status_emoji} {name} - {location} ({status})"


def render_button_group(buttons_dict, use_container_width=True):
    """
    Render a group of buttons in a row
    
    Args:
        buttons_dict (dict): Dictionary of {button_label: button_key}
        use_container_width (bool): Whether to use full width
        
    Returns:
        dict: Dictionary of {button_key: button_clicked}
    """
    cols = st.columns(len(buttons_dict))
    results = {}
    
    for col, (label, key) in zip(cols, buttons_dict.items()):
        with col:
            results[key] = st.button(label, use_container_width=use_container_width)
    
    return results


def render_metric_row(metrics_dict):
    """
    Render a row of metrics
    
    Args:
        metrics_dict (dict): Dictionary of {label: value}
    """
    cols = st.columns(len(metrics_dict))
    
    for col, (label, value) in zip(cols, metrics_dict.items()):
        with col:
            st.metric(label, value)


def render_status_badge(status, status_type="default"):
    """
    Render a status badge
    
    Args:
        status (str): Status text
        status_type (str): Type of status (default, success, warning, danger)
        
    Returns:
        str: HTML badge
    """
    colors = {
        "default": "#1565c0",
        "success": "#27ae60",
        "warning": "#f39c12",
        "danger": "#e74c3c",
    }
    
    color = colors.get(status_type, colors["default"])
    
    return f"""
    <span style="background: {color}; color: white; padding: 6px 14px; 
                 border-radius: 20px; font-size: 12px; font-weight: 600; 
                 display: inline-block;">
        {status}
    </span>
    """


def render_empty_state(icon="", title="", message=""):
    """
    Render an empty state message
    
    Args:
        icon (str): Emoji icon
        title (str): Title text
        message (str): Message text
    """
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem; background: #f5f7fa; 
                border-radius: 8px; margin: 1rem 0;'>
        <p style='font-size: 2rem; margin: 0;'>{icon}</p>
        <p style='font-size: 1.2rem; font-weight: 600; color: #1a237e; margin: 0.5rem 0;'>{title}</p>
        <p style='color: #546e7a; margin: 0;'>{message}</p>
    </div>
    """, unsafe_allow_html=True)


def render_loading_spinner(message="Loading..."):
    """
    Render a loading spinner with message
    
    Args:
        message (str): Loading message
    """
    with st.spinner(message):
        pass


def render_confirmation_dialog(title, message, confirm_text="Confirm", cancel_text="Cancel"):
    """
    Render a confirmation dialog
    
    Args:
        title (str): Dialog title
        message (str): Dialog message
        confirm_text (str): Confirm button text
        cancel_text (str): Cancel button text
        
    Returns:
        bool: True if confirmed, False if cancelled
    """
    st.markdown(f"""
    <div style='background: white; padding: 2rem; border-radius: 8px; 
                box-shadow: 0 4px 16px rgba(0,0,0,0.15); margin: 1rem 0;'>
        <h3 style='color: #1a237e; margin: 0 0 1rem 0;'>{title}</h3>
        <p style='color: #546e7a; margin: 0 0 1.5rem 0;'>{message}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        confirmed = st.button(confirm_text, type="primary", use_container_width=True)
    with col2:
        cancelled = st.button(cancel_text, use_container_width=True)
    
    return confirmed


def render_progress_bar(current, total, label=""):
    """
    Render a progress bar
    
    Args:
        current (int): Current progress
        total (int): Total progress
        label (str): Optional label
    """
    percentage = (current / total) * 100 if total > 0 else 0
    
    if label:
        st.markdown(f"**{label}**")
    
    st.progress(percentage / 100)
    st.caption(f"{current} of {total} ({percentage:.1f}%)")


def render_alert_box(message, alert_type="info"):
    """
    Render an alert box
    
    Args:
        message (str): Alert message
        alert_type (str): Type of alert (info, success, warning, error)
    """
    icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌",
    }
    
    colors = {
        "info": "#3498db",
        "success": "#27ae60",
        "warning": "#f39c12",
        "error": "#e74c3c",
    }
    
    icon = icons.get(alert_type, "ℹ️")
    color = colors.get(alert_type, "#3498db")
    
    st.markdown(f"""
    <div style='background: {color}20; border-left: 4px solid {color}; 
                padding: 1rem; border-radius: 4px; margin: 1rem 0;'>
        <p style='color: {color}; margin: 0; font-weight: 600;'>
            {icon} {message}
        </p>
    </div>
    """, unsafe_allow_html=True)
