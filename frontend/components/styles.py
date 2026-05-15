"""
Common CSS styles for the application
Professional design system with consistent spacing, colors, and typography
"""

# Color Palette - Professional & Accessible
COLORS = {
    "primary": "#1565c0",           # Deep Blue
    "primary_light": "#42a5f5",     # Light Blue
    "primary_dark": "#0d47a1",      # Dark Blue
    "secondary": "#667eea",         # Purple
    "secondary_light": "#9b59b6",   # Light Purple
    "success": "#27ae60",           # Green
    "warning": "#f39c12",           # Orange
    "danger": "#e74c3c",            # Red
    "info": "#3498db",              # Info Blue
    "light": "#ecf0f1",             # Light Gray
    "dark": "#2c3e50",              # Dark Gray
    "text": "#1a237e",              # Text Color
    "text_light": "#546e7a",        # Light Text
    "border": "#cfd8dc",            # Border Color
    "background": "#f5f7fa",        # Background
}

# Typography
TYPOGRAPHY = {
    "font_family": "'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif",
    "h1_size": "2.5rem",
    "h2_size": "2rem",
    "h3_size": "1.5rem",
    "h4_size": "1.25rem",
    "body_size": "1rem",
    "small_size": "0.875rem",
}

# Spacing
SPACING = {
    "xs": "0.25rem",
    "sm": "0.5rem",
    "md": "1rem",
    "lg": "1.5rem",
    "xl": "2rem",
    "xxl": "3rem",
}

# Shadows
SHADOWS = {
    "sm": "0 2px 8px rgba(0, 0, 0, 0.1)",
    "md": "0 4px 16px rgba(0, 0, 0, 0.12)",
    "lg": "0 8px 32px rgba(0, 0, 0, 0.15)",
    "xl": "0 12px 40px rgba(0, 0, 0, 0.2)",
}

# Border Radius
BORDER_RADIUS = {
    "sm": "4px",
    "md": "8px",
    "lg": "12px",
    "xl": "16px",
    "full": "20px",
}

def get_login_page_styles(bg_image_base64=""):
    """Get CSS styles for login page"""
    return f"""
        <style>
        /* ============================================
           GLOBAL STYLES & PERFORMANCE OPTIMIZATIONS
           ============================================ */
        
        * {{
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            box-sizing: border-box;
        }}
        
        html, body {{
            font-family: {TYPOGRAPHY['font_family']};
            color: {COLORS['text']};
            background: {COLORS['background']};
        }}
        
        /* Reduce repaints and reflows */
        .stApp {{
            will-change: auto;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.7) 0%, rgba(118, 75, 162, 0.7) 100%), 
                        url('data:image/png;base64,{bg_image_base64}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}
        
        /* GPU acceleration for animations */
        button, .login-card {{
            transform: translateZ(0);
            backface-visibility: hidden;
        }}
        
        /* Mobile-first responsive design */
        @media (max-width: 768px) {{
            .stApp {{
                padding: 0 !important;
            }}
            
            [data-testid="stAppViewContainer"] > .main {{
                padding: 0.5rem !important;
            }}
            
            .main-container {{
                padding: 0.5rem !important;
                margin: 0 !important;
            }}
            
            .login-banner {{
                background: #ffffff !important;
                padding: 1.5rem 1rem !important;
                margin: 0.5rem !important;
                border-radius: 12px !important;
            }}
            
            .login-banner h1 {{
                font-size: 1.8rem !important;
                line-height: 1.2 !important;
            }}
            
            .login-banner .tagline {{
                font-size: 0.9rem !important;
            }}
            
            .login-banner .badge {{
                font-size: 0.8rem !important;
                padding: 6px 12px !important;
            }}
            
            /* Mobile card layout - stack vertically */
            div[data-testid="column"] {{
                padding: 0.25rem !important;
                margin-bottom: 1rem !important;
            }}
            
            /* Force columns to stack on mobile */
            .row-widget.stHorizontal {{
                flex-direction: column !important;
            }}
            
            .row-widget.stHorizontal > div {{
                width: 100% !important;
                margin-bottom: 1rem !important;
            }}
            
            /* Mobile buttons - full width and better spacing */
            button[kind="secondary"][data-testid="stBaseButton-secondary"] {{
                min-height: 160px !important;
                padding: 1.5rem 1rem !important;
                font-size: 0.9rem !important;
                line-height: 1.4 !important;
                margin-bottom: 1rem !important;
                width: 100% !important;
            }}
            
            /* Mobile forms */
            div[data-testid="stForm"] {{
                padding: 1rem !important;
                margin: 0.5rem 0 !important;
                border-radius: 8px !important;
            }}
            
            /* Mobile text inputs - prevent zoom and improve touch */
            div[data-testid="stTextInput"] input {{
                padding: 12px !important;
                font-size: 16px !important; /* Prevents zoom on iOS */
                border-radius: 6px !important;
                min-height: 44px !important; /* Better touch target */
            }}
            
            /* Mobile password inputs */
            input[type="password"] {{
                font-size: 16px !important; /* Prevents zoom on iOS */
                min-height: 44px !important;
            }}
            
            /* Mobile form buttons */
            div[data-testid="stForm"] button {{
                padding: 12px !important;
                font-size: 16px !important;
                border-radius: 6px !important;
                margin-top: 1rem !important;
                min-height: 44px !important;
            }}
            
            /* Mobile tabs */
            div[data-baseweb="tab-list"] {{
                padding: 5px !important;
                flex-wrap: wrap !important;
                gap: 5px !important;
            }}
            
            div[data-baseweb="tab"] {{
                padding: 8px 12px !important;
                font-size: 0.85rem !important;
                margin: 2px !important;
                border-radius: 6px !important;
                flex: 1 !important;
                min-width: 80px !important;
                min-height: 44px !important; /* Better touch target */
            }}
            
            div[data-baseweb="tab-panel"] {{
                padding: 15px !important;
                border-radius: 0 0 8px 8px !important;
            }}
            
            /* Mobile-specific improvements */
            .stMarkdown {{
                font-size: 0.9rem !important;
            }}
            
            /* Better touch targets for all interactive elements */
            button, input, select, textarea {{
                min-height: 44px !important;
            }}
            
            /* Prevent horizontal scroll */
            .main {{
                overflow-x: hidden !important;
            }}
            
            /* Mobile selectbox improvements */
            div[data-testid="stSelectbox"] > div > div {{
                min-height: 44px !important;
                font-size: 16px !important;
            }}
            
            /* Mobile file uploader */
            div[data-testid="stFileUploader"] {{
                padding: 1rem !important;
            }}
            
            div[data-testid="stFileUploader"] button {{
                min-height: 44px !important;
                padding: 12px !important;
            }}
            
            /* Mobile expander headers */
            div[data-testid="stExpander"] summary {{
                min-height: 44px !important;
                padding: 12px !important;
            }}
            
            /* Mobile metric containers */
            div[data-testid="metric-container"] {{
                padding: 1rem 0.5rem !important;
            }}
            
            /* Mobile image containers */
            div[data-testid="stImage"] {{
                text-align: center !important;
            }}
            
            /* Mobile alert boxes */
            div[data-testid="stAlert"] {{
                padding: 1rem !important;
                margin: 0.5rem 0 !important;
            }}
        }}
        
        /* Tablet responsive */
        @media (max-width: 1024px) and (min-width: 769px) {{
            .main-container {{
                padding: 1.5rem !important;
            }}
            
            .login-banner {{
                background: #ffffff !important;
                padding: 2rem 2rem !important;
            }}
            
            .login-banner h1 {{
                font-size: 2.2rem !important;
            }}
            
            button[kind="secondary"][data-testid="stBaseButton-secondary"] {{
                min-height: 220px !important;
                padding: 2rem 1.5rem !important;
            }}
        }}

        /* Hide default Streamlit header on login page */
        [data-testid="stHeader"] {{
            background: transparent !important;
        }}
        
        /* Mobile-specific header improvements */
        @media (max-width: 768px) {{
            [data-testid="stHeader"] {{
                height: 0 !important;
                min-height: 0 !important;
            }}
            
            /* Improve mobile toolbar */
            [data-testid="stToolbar"] {{
                display: none !important;
            }}
        }}

        /* Apply background to main app container */
        .stApp {{
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.7) 0%, rgba(118, 75, 162, 0.7) 100%), 
                        url('data:image/png;base64,{bg_image_base64}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}
        
        /* Ensure main block is transparent */
        [data-testid="stAppViewContainer"] {{
            background: transparent;
        }}
        
        .main {{
            background: transparent;
        }}
        
        /* Main container */
        .main-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}

        /* Login cards container */
        .login-cards {{
            display: flex;
            gap: 2rem;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 2rem;
        }}

        /* Individual login card */
        .login-card {{
            flex: 1;
            min-width: 350px;
            max-width: 450px;
            padding: 2.5rem 2rem;
            border-radius: 16px;
            background: #ffffff;
            box-shadow: 0 8px 32px rgba(0,0,0,0.15);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
            will-change: transform;
        }}

        .login-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0,0,0,0.2);
        }}

        /* Banner */
        .login-banner {{
            text-align: center;
            padding: 2.5rem 3rem;
            background: #ffffff;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
            margin-bottom: 2rem;
            border: 2px solid rgba(255, 255, 255, 0.8);
            transition: all 0.3s ease;
        }}
        .login-banner:hover {{
            background: #ffffff;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
            transform: translateY(-2px);
        }}
        .login-banner h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            color: #1a237e;
            margin-bottom: 0.5rem;
            text-shadow: none;
        }}
        .login-banner .tagline {{
            font-size: 1.1rem;
            color: #1a237e;
            margin-top: 0;
            font-weight: 600;
            text-shadow: none;
        }}
        .login-banner .badge {{
            display: inline-block;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
            color: white;
            border-radius: 20px;
            padding: 8px 20px;
            font-size: 0.9rem;
            font-weight: 600;
            margin-top: 0.8rem;
            letter-spacing: 0.5px;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}

        /* Card headers */
        .card-header {{
            text-align: center;
            margin-bottom: 2rem;
        }}
        .card-header h2 {{
            font-size: 1.5rem;
            font-weight: 600;
            color: #1a237e;
            margin-bottom: 0.5rem;
        }}
        .card-header p {{
            color: #546e7a;
            margin: 0;
            font-size: 0.95rem;
        }}

        /* Style all text inputs inside the form */
        div[data-testid="stTextInput"] input {{
            border-radius: 8px !important;
            border: 1.5px solid #cfd8dc !important;
            padding: 10px 14px !important;
            font-size: 0.97rem !important;
            background: white !important;
            autocomplete: off !important;
            transition: border-color 0.1s ease, box-shadow 0.1s ease !important;
        }}
        div[data-testid="stTextInput"] input:focus {{
            border-color: #1565c0 !important;
            box-shadow: 0 0 0 2px rgba(21,101,192,0.15) !important;
            outline: none !important;
        }}

        /* Form container background with instant dropdown animation */
        div[data-testid="stForm"] {{
            background: rgba(255, 255, 255, 0.95) !important;
            padding: 1.5rem !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;
            backdrop-filter: blur(10px) !important;
            margin-top: 1rem !important;
            animation: slideDown 0.15s ease-out forwards !important;
            transform-origin: top !important;
            will-change: transform, opacity !important;
        }}
        
        /* Fast dropdown animation keyframes */
        @keyframes slideDown {{
            0% {{
                opacity: 0;
                transform: translateY(-10px);
            }}
            100% {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        /* Style the submit button */
        div[data-testid="stForm"] button[kind="primaryFormSubmit"],
        div[data-testid="stForm"] button[type="submit"],
        div[data-testid="stForm"] button[kind="secondaryFormSubmit"] {{
            background-color: #1565c0 !important;
            color: white !important;
            border-radius: 8px !important;
            width: 100% !important;
            padding: 0.75rem !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            border: none !important;
            transition: all 0.1s ease !important;
            cursor: pointer !important;
            will-change: transform, background-color !important;
        }}
        div[data-testid="stForm"] button[kind="primaryFormSubmit"]:hover,
        div[data-testid="stForm"] button[type="submit"]:hover,
        div[data-testid="stForm"] button[kind="secondaryFormSubmit"]:hover {{
            background-color: #0d47a1 !important;
            transform: translateY(-1px) !important;
        }}
        div[data-testid="stForm"] button[kind="primaryFormSubmit"]:active,
        div[data-testid="stForm"] button[type="submit"]:active,
        div[data-testid="stForm"] button[kind="secondaryFormSubmit"]:active {{
            transform: translateY(0) !important;
            transition: all 0.05s ease !important;
        }}
        
        /* Form markdown text styling */
        div[data-testid="stForm"] .stMarkdown {{
            color: #1a237e !important;
        }}

        /* Admin card special styling */
        .admin-card {{
            border-top: 4px solid #ff6b6b;
        }}
        
        /* Public card special styling */
        .public-card {{
            border-top: 4px solid #4ecdc4;
        }}

        /* Toggle button styling - Make them look like cards */
        button[kind="secondary"][data-testid="stBaseButton-secondary"] {{
            background: white !important;
            color: #1a237e !important;
            border: none !important;
            padding: 2.5rem 2rem !important;
            border-radius: 16px !important;
            font-weight: 400 !important;
            margin-top: 0 !important;
            transition: all 0.15s ease !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15) !important;
            text-align: center !important;
            min-height: 250px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            white-space: pre-line !important;
            line-height: 1.6 !important;
            will-change: transform !important;
            cursor: pointer !important;
        }}
        
        button[kind="secondary"][data-testid="stBaseButton-secondary"]:hover {{
            transform: translateY(-5px) !important;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2) !important;
        }}
        
        button[kind="secondary"][data-testid="stBaseButton-secondary"]:active {{
            transform: translateY(-2px) !important;
            transition: all 0.05s ease !important;
        }}
        
        /* Admin card button - red top border */
        button[key="admin_card_btn"] {{
            border-top: 4px solid #ff6b6b !important;
        }}
        
        /* Public card button - teal top border */
        button[key="public_card_btn"] {{
            border-top: 4px solid #4ecdc4 !important;
        }}
        
        /* Complainant card button - purple top border */
        button[key="complainant_card_btn"] {{
            border-top: 4px solid #9b59b6 !important;
        }}

        /* Icon styling */
        .role-icon {{
            font-size: 3rem;
            text-align: center;
            margin-bottom: 1rem;
        }}
        
        /* Tab styling - add transparent background */
        div[data-baseweb="tab-list"] {{
            background: rgba(255, 255, 255, 0.95) !important;
            padding: 10px !important;
            border-radius: 10px 10px 0 0 !important;
            backdrop-filter: blur(10px) !important;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1) !important;
        }}
        
        div[data-baseweb="tab"] {{
            background: transparent !important;
            color: #1a237e !important;
            font-weight: 600 !important;
            padding: 12px 24px !important;
            border-radius: 8px !important;
            transition: all 0.15s ease !important;
        }}
        
        div[data-baseweb="tab"]:hover {{
            background: rgba(102, 126, 234, 0.1) !important;
        }}
        
        div[data-baseweb="tab"][aria-selected="true"] {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
        }}
        
        div[data-baseweb="tab-panel"] {{
            background: rgba(255, 255, 255, 0.95) !important;
            padding: 20px !important;
            border-radius: 0 0 10px 10px !important;
            backdrop-filter: blur(10px) !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;
        }}
        </style>
        """


def get_main_app_styles():
    """Get CSS styles for main application"""
    return """
    <style>
    /* Performance optimizations */
    * {
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    /* GPU acceleration */
    .stButton > button, .stSelectbox, .stTextInput {
        transform: translateZ(0);
        backface-visibility: hidden;
    }
    
    /* Reduce layout shifts */
    img {
        content-visibility: auto;
    }
    
    /* Mobile responsiveness for main app */
    @media (max-width: 768px) {
        /* Main content area */
        .main .block-container {
            padding: 1rem 0.5rem !important;
            max-width: 100% !important;
        }
        
        /* Sidebar adjustments */
        .css-1d391kg {
            padding: 1rem 0.5rem !important;
        }
        
        /* Headers */
        h1 {
            font-size: 1.5rem !important;
            line-height: 1.2 !important;
        }
        
        h2 {
            font-size: 1.3rem !important;
        }
        
        h3 {
            font-size: 1.1rem !important;
        }
        
        /* Buttons */
        .stButton > button {
            width: 100% !important;
            padding: 0.75rem !important;
            font-size: 0.9rem !important;
            min-height: 44px !important;
        }
        
        /* Select boxes */
        .stSelectbox > div > div {
            font-size: 16px !important; /* Prevents zoom on iOS */
            min-height: 44px !important;
        }
        
        /* Text inputs */
        .stTextInput > div > div > input {
            font-size: 16px !important; /* Prevents zoom on iOS */
            padding: 0.75rem !important;
            min-height: 44px !important;
        }
        
        /* Text areas */
        .stTextArea > div > div > textarea {
            font-size: 16px !important; /* Prevents zoom on iOS */
            padding: 0.75rem !important;
        }
        
        /* Number inputs */
        .stNumberInput > div > div > input {
            font-size: 16px !important; /* Prevents zoom on iOS */
            min-height: 44px !important;
        }
        
        /* Date inputs */
        .stDateInput > div > div > input {
            font-size: 16px !important; /* Prevents zoom on iOS */
            min-height: 44px !important;
        }
        
        /* Time inputs */
        .stTimeInput > div > div > input {
            font-size: 16px !important; /* Prevents zoom on iOS */
            min-height: 44px !important;
        }
        
        /* File uploader */
        .stFileUploader > div {
            padding: 0.5rem !important;
        }
        
        .stFileUploader button {
            min-height: 44px !important;
            padding: 0.75rem !important;
        }
        
        /* Columns - stack on mobile */
        .row-widget.stHorizontal > div {
            flex-direction: column !important;
        }
        
        /* Expanders */
        .streamlit-expanderHeader {
            font-size: 0.9rem !important;
            padding: 0.75rem !important;
            min-height: 44px !important;
        }
        
        .streamlit-expanderContent {
            padding: 0.5rem !important;
        }
        
        /* Images */
        img {
            max-width: 100% !important;
            height: auto !important;
        }
        
        /* Tables */
        .dataframe {
            font-size: 0.8rem !important;
            overflow-x: auto !important;
        }
        
        /* Metrics */
        .metric-container {
            padding: 0.5rem !important;
        }
        
        /* Forms */
        .stForm {
            padding: 1rem 0.5rem !important;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.25rem !important;
            flex-wrap: wrap !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0.75rem !important;
            font-size: 0.85rem !important;
            min-height: 44px !important;
        }
        
        /* Map container */
        .folium-map {
            width: 100% !important;
            height: 400px !important;
        }
        
        /* Alert boxes */
        .stAlert {
            padding: 0.75rem !important;
            font-size: 0.9rem !important;
        }
        
        /* Progress bars */
        .stProgress > div {
            height: 8px !important;
        }
        
        /* Sidebar on mobile */
        .css-1d391kg {
            width: 100% !important;
            margin-left: 0 !important;
        }
        
        /* Hide sidebar toggle on mobile when open */
        .css-1rs6os {
            display: none !important;
        }
        
        /* Radio buttons */
        .stRadio > div {
            flex-direction: column !important;
        }
        
        .stRadio > div > label {
            padding: 0.5rem !important;
            margin: 0.25rem 0 !important;
        }
        
        /* Checkboxes */
        .stCheckbox > label {
            padding: 0.5rem !important;
        }
        
        /* Download buttons */
        .stDownloadButton > button {
            min-height: 44px !important;
            padding: 0.75rem !important;
        }
        
        /* Spinner */
        .stSpinner > div {
            margin: 1rem auto !important;
        }
        
        /* Success/Error/Warning/Info messages */
        .stSuccess, .stError, .stWarning, .stInfo {
            padding: 1rem !important;
            margin: 0.5rem 0 !important;
            border-radius: 8px !important;
        }
        
        /* Container spacing */
        .element-container {
            margin-bottom: 1rem !important;
        }
        
        /* Prevent text selection on buttons for better mobile UX */
        button {
            -webkit-user-select: none !important;
            -moz-user-select: none !important;
            -ms-user-select: none !important;
            user-select: none !important;
        }
        
        /* Improve mobile touch scrolling and performance */
        @media (max-width: 768px) {
            * {
                -webkit-tap-highlight-color: rgba(102, 126, 234, 0.2) !important;
            }
            
            .main {
                -webkit-overflow-scrolling: touch !important;
                overflow-x: hidden !important;
            }
            
            /* Prevent zoom on double tap */
            * {
                touch-action: manipulation !important;
            }
            
            /* Smooth scrolling */
            html {
                scroll-behavior: smooth !important;
            }
        }
    }
    
    /* Tablet responsive */
    @media (max-width: 1024px) and (min-width: 769px) {
        .main .block-container {
            padding: 1.5rem 1rem !important;
        }
        
        h1 {
            font-size: 2rem !important;
        }
        
        .stButton > button {
            padding: 0.6rem 1.2rem !important;
        }
    }
    
    /* Ensure touch targets are large enough */
    @media (max-width: 768px) {
        button, input, select, textarea {
            min-height: 44px !important;
        }
        
        /* Make clickable areas larger */
        .stCheckbox > label {
            padding: 0.5rem !important;
        }
        
        .stRadio > label {
            padding: 0.5rem !important;
        }
        
        /* Improve tap highlighting */
        button, input, select, textarea {
            -webkit-tap-highlight-color: rgba(102, 126, 234, 0.3) !important;
        }
        
        /* Better focus states for accessibility */
        button:focus, input:focus, select:focus, textarea:focus {
            outline: 2px solid #667eea !important;
            outline-offset: 2px !important;
        }
    }
    </style>
    """
