# 🔍 AI Missing Person Identification System

A professional AI-powered web application for managing and identifying missing persons using facial recognition technology.

---

## ✨ Features

### 🎯 Core Functionality
- **AI-Powered Face Matching** - Advanced facial recognition using MediaPipe (478 facial landmarks)
- **Three Access Levels** - Admin, Registered Public Users, and Public Viewing
- **Real-time Case Management** - Register, track, and manage missing person cases
- **Email Notifications** - Automated alerts for case updates and matches
- **Interactive Map** - Geographic visualization of cases across India
- **Secure Authentication** - Email verification and password hashing

### 👮 Admin Features
- Register missing person cases with photo upload
- View dashboard with statistics
- Run AI matching algorithms
- Manage all cases and submissions
- Send email notifications
- User management system
- Excel export functionality

### 👥 Public User Features
- Create account with email verification
- Submit sighting reports with photos
- Track submission status
- Secure login system

### 👁️ View Cases (No Login)
- Browse all registered cases
- Search and filter cases
- View case details and photos

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "Ai Missing Person Identification System"
   ```

2. **Install system dependencies (Linux only)**
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt-get update
   sudo apt-get install -y libgles2-mesa libgles2-mesa-dev libgl1-mesa-glx libglib2.0-0
   ```
   
   **Fedora/RHEL/CentOS:**
   ```bash
   sudo dnf install -y mesa-libGLES mesa-libGLES-devel
   ```
   
   **Arch Linux:**
   ```bash
   sudo pacman -S mesa
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure email (Required for user registration)**
   
   Edit `email_settings.txt`:
   ```
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   NOTIFY_EMAIL=your-email@gmail.com
   ```

5. **Run the application**
   
   **Windows:**
   ```cmd
   start.bat
   ```
   
   **Or directly:**
   ```bash
   python -m streamlit run Home.py
   ```

6. **Access the application**
   - Local: `http://localhost:8501`

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

#### Option 1: Automated Setup (Recommended)

**Linux/WSL:**
```bash
# Run the setup script
python3 setup.py

# Start the application
streamlit run Home.py
```

**Windows:**
```cmd
# Install dependencies
install_dependencies.bat

# Run the application
run_app.bat
```

#### Option 2: Manual Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "Ai Missing Person Identification System"
   ```

2. **Install system dependencies (Linux only)**
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt-get update
   sudo apt-get install -y libgles2-mesa libgles2-mesa-dev libgl1-mesa-glx libglib2.0-0
   ```
   
   **Fedora/RHEL/CentOS:**
   ```bash
   sudo dnf install -y mesa-libGLES mesa-libGLES-devel
   ```
   
   **Arch Linux:**
   ```bash
   sudo pacman -S mesa
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure email (Required for user registration)**
   
   Edit `email_settings.txt`:
   ```
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   NOTIFY_EMAIL=your-email@gmail.com
   ```

5. **Run the application**
   ```bash
   streamlit run Home.py
   ```

6. **Access the application**
   - Local: `http://localhost:8501`

---

## 🔐 Default Login

**Admin Access:**
- Username: `mit`
- Password: `123`

⚠️ **Change this password immediately after first login!**

---

## 📁 Project Structure

```
.
├── Home.py                           # Main application entry point
├── requirements.txt                  # Python dependencies
├── login_config.yml                  # Authentication configuration
├── email_settings.txt                # Email SMTP configuration
├── .env                              # Environment variables
│
├── backend/                          # Backend logic
│   ├── database/                     # Database queries
│   ├── models/                       # Data models
│   ├── services/                     # Business logic
│   └── utils/                        # Utility functions
│
├── frontend/                         # UI components
│   ├── pages/                        # Application pages
│   └── components/                   # Reusable UI elements
│
├── config/                           # Configuration
│   ├── sqlite_database.db            # SQLite database
│   ├── face_landmarker.task          # MediaPipe model
│   └── app_config.py                 # App configuration
│
├── email_system/                     # Email handling
├── assets/                           # Static files
├── resources/                        # Uploaded images
└── logs/                             # Application logs
```

---

## 🛠️ Technology Stack

### Core
- **Streamlit** - Web framework
- **Python 3.8+** - Programming language
- **SQLite** - Database
- **SQLModel** - ORM

### AI/ML
- **MediaPipe** - Face detection (478 landmarks)
- **scikit-learn** - KNN classifier
- **NumPy** - Numerical computations
- **OpenCV** - Image processing

### Additional
- **Folium** - Interactive maps
- **openpyxl** - Excel export
- **smtplib** - Email notifications

---

## 📊 Usage Guide

### For Administrators

1. **Login** - Use admin credentials
2. **Register Case** - Upload photo and fill details
3. **View Cases** - Browse and manage all cases
4. **Run Matching** - Use AI to find potential matches
5. **User Management** - Manage registered users
6. **Export Data** - Download user and submission data

### For Public Users

1. **Register** - Create account with email verification
2. **Login** - Access your portal
3. **Submit Report** - Upload photo and provide details
4. **Track Submissions** - View your submission history

### For Viewing Cases

1. **Browse** - View all cases without login
2. **Search** - Find specific cases
3. **View Details** - See case information

---

## 🔧 Configuration

### Email Setup (Gmail)

1. Enable 2-Factor Authentication on Gmail
2. Generate App Password: Google Account → Security → App Passwords
3. Update `email_settings.txt` with your credentials
4. Restart the application

### Face Matching Threshold

- **1.5 - 2.5**: Moderate (recommended)
- **2.5 - 4.0**: Lenient (more matches)
- **0.5 - 1.5**: Strict (fewer matches)

Default: 3.0

---

---

## 🐛 Troubleshooting

### Common Issues

**libGLESv2.so.2 error (Linux systems):**

If you see: `libGLESv2.so.2: cannot open shared object file: No such file or directory`

This is caused by missing OpenGL ES libraries required by MediaPipe. Install them based on your Linux distribution:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y libgles2-mesa libgles2-mesa-dev
```

**Fedora/RHEL/CentOS:**
```bash
sudo dnf install -y mesa-libGLES mesa-libGLES-devel
```

**Arch Linux:**
```bash
sudo pacman -S mesa
```

**Alternative solution (if above doesn't work):**
```bash
# Install full Mesa OpenGL libraries
sudo apt-get install -y libgl1-mesa-glx libglib2.0-0
```

After installation, restart the application.

**No face detected:**
- Use clear, front-facing photos
- Ensure good lighting
- Minimum resolution: 640x480

**Email not sending:**
- Verify SMTP credentials
- Use Gmail App Password (not regular password)
- Check port 587 is not blocked

**Database errors:**
- Check file permissions
- Ensure `config/sqlite_database.db` exists

**Matching not working:**
- Verify `config/face_landmarker.task` exists
- Ensure cases have valid face data
- Try adjusting threshold value

---

## 🔒 Security

### Best Practices
1. Change default admin password immediately
2. Use strong passwords (minimum 8 characters)
3. Keep `.env` file secure
4. Use HTTPS in production
5. Regular backups
6. Update dependencies regularly

### Authentication
- Email verification with 6-digit codes
- SHA-256 password hashing
- Session timeout: 30 minutes
- Role-based access control

---

## 📝 Development

### Setup Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run Home.py
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Add docstrings
- Keep functions focused

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 📧 Support

- Email: missingpersonidentificationsys@gmail.com
- Instagram: [@ai_mpis](https://www.instagram.com/ai_mpis/)

---

## ⚠️ Disclaimer

This system is an investigative tool only. Always verify matches manually and follow proper legal procedures. The AI provides suggestions based on facial similarity but is not definitive identification.

---

## 🔒 Privacy Notice

All data is stored locally in SQLite database. Follow data protection regulations (GDPR, CCPA) when deploying. Users can delete their submissions anytime.

---

**Last Updated:** May 7, 2026
