# 🎓 SemStar - Academic Resource Portal (Version 1.0)

A Django-based centralized platform for students to share and access academic resources like notes, model papers, and career guidance materials with an admin approval system.

---

## 📋 Table of Contents

- [Overview](#overview)
- [What's New in Version 1.0](#whats-new-in-version-10)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Interview Preparation](#interview-preparation)

---

## 🌟 Overview

SemStar is an academic resource portal that enables students to:
- Upload and share educational materials
- Access approved documents organized by branch and category
- Search and filter resources efficiently
- Receive email notifications for document approvals

Administrators can:
- Review and approve/reject submitted documents
- Manage user accounts
- View contact queries from students
- Monitor platform statistics

---

## 🆕 What's New in Version 1.0

This version includes major improvements over the original project:

### ✅ **Critical Bug Fixes**
1. Fixed HTML typo in `view_allnotes.html` (`</ssth>` → `</th>`)
2. Fixed model `__str__` method bug (incorrect attribute reference)
3. Fixed password change security - now verifies old password
4. Added file upload validation to prevent malicious files

### 🚀 **New Features**

#### **1. Django Forms Implementation**
- Replaced raw POST data handling with Django ModelForms
- Automatic validation and error handling
- Better security with built-in CSRF protection
- Forms for: Signup, Document Upload, Contact, Profile Edit, Password Change, Search/Filter

#### **2. Advanced Search & Filtering**
- Search documents by subject, description, or uploader name
- Filter by branch, category, and file type
- Combined search and filter functionality
- Optimized database queries using Django Q objects

#### **3. Pagination**
- All document lists now paginated (10-15 items per page)
- Improves page load performance
- Better user experience with large datasets

#### **4. Email Notification System**
- Welcome email on registration
- Document status notifications (approved/rejected)
- Contact form confirmation emails
- Configurable: console backend for dev, SMTP for production

#### **5. Enhanced Models**
- Proper field types (DateField instead of CharField for dates)
- Field choices for status, category, branch, file type
- Better `__str__` representations
- Added `downloads` field to track document popularity
- Model Meta classes with ordering and verbose names

#### **6. Security Improvements**
- Environment variables for SECRET_KEY and sensitive config
- Proper DEBUG and ALLOWED_HOSTS configuration
- Session security settings
- Production-ready security headers
- Better password validation
- File upload whitelist and size limits

#### **7. Logging System**
- Configured logging to console and file
- Different log levels for development and production
- Error tracking for debugging
- User activity monitoring

#### **8. Code Quality**
- Specific exception handling instead of generic `except:`
- Docstrings for all functions
- Better variable naming
- DRY (Don't Repeat Yourself) principles
- Comments explaining complex logic

---

## ✨ Features

### For Students:
- ✅ User registration and authentication
- ✅ Upload documents (PDF, PPT, DOC, Images, ZIP/RAR)
- ✅ View own uploaded documents with status
- ✅ Browse all approved documents
- ✅ Advanced search and filtering
- ✅ Download academic resources
- ✅ Update profile information
- ✅ Change password securely
- ✅ Email notifications

### For Administrators:
- ✅ Separate admin login portal
- ✅ Dashboard with statistics
- ✅ Review and approve/reject documents
- ✅ User management
- ✅ Contact query management
- ✅ Email notification to users on status change

### Resource Categories:
- 📚 **Notes:** Study materials and lecture notes
- 📝 **Model Papers:** Previous year question papers
- 🎯 **Guidance:** Career guidance and tips

### Supported Branches:
- Computer Science
- Mechanical Engineering
- Civil Engineering
- Electronics Engineering
- Electrical Engineering
- Information Technology

---

## 🛠️ Tech Stack

### Backend:
- **Framework:** Django 3.1.1
- **Language:** Python 3.x
- **Database:** SQLite3 (development), PostgreSQL/MySQL compatible

### Frontend:
- **HTML5 & CSS3**
- **JavaScript & jQuery 3.6.0**
- **Bootstrap 4.3.1**
- **DataTables Plugin**
- **Chart.js** (for admin analytics)

### Additional Libraries:
- Pillow 7.2.0 (image handling)
- WhiteNoise 5.2.0 (static file serving)
- Gunicorn 20.0.4 (WSGI server for production)

---

## 📦 Installation

### Prerequisites:
- Python 3.7 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Steps:

1. **Clone or download the project:**
```bash
cd "Version 1"
```

2. **Create and activate virtual environment:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requriements.txt
```

4. **Apply database migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create admin user:**
```bash
python manage.py createsuperuser
```
Follow prompts to create your admin account.

6. **Run development server:**
```bash
python manage.py runserver
```

7. **Access the application:**
- Student Portal: http://127.0.0.1:8000/
- Admin Portal: http://127.0.0.1:8000/login_admin
- Django Admin: http://127.0.0.1:8000/admin

---

## ⚙️ Configuration

### Environment Variables:

Create a `.env` file in the project root (copy from `.env.example`):

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Configuration (for production)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@semstar.com
```

### Email Setup:

**For Development (Default):**
Emails are printed to console. No configuration needed.

**For Production:**
1. Get Gmail App Password:
   - Go to Google Account → Security → 2-Step Verification → App Passwords
   - Generate app-specific password
2. Update `.env` with your email and app password
3. Change `EMAIL_BACKEND` in settings

---

## 🎯 Usage

### As a Student:

1. **Register:**
   - Click "Sign Up" on homepage
   - Fill in your details (name, email, contact, branch)
   - Submit and check email for welcome message

2. **Login:**
   - Use your email and password
   - Access student dashboard

3. **Upload Documents:**
   - Go to "Upload Notes"
   - Select branch, category, subject
   - Choose file and add description
   - Submit (goes to pending status)
   - Receive email when approved/rejected

4. **Browse Resources:**
   - Click "View All Notes"
   - Use search bar or filters
   - Download approved documents

5. **Manage Profile:**
   - View/edit profile information
   - Change password

### As an Administrator:

1. **Login:**
   - Go to `/login_admin`
   - Use superuser credentials

2. **Dashboard:**
   - View statistics (pending, accepted, rejected documents)
   - Total users count

3. **Review Documents:**
   - Click "Pending Notes"
   - Review submitted documents
   - Assign status (Accept/Reject)
   - System sends email notification automatically

4. **Manage Users:**
   - View all registered users
   - Delete user accounts if needed

5. **Handle Queries:**
   - View unread contact queries
   - Mark as read after responding

---

## 📁 Project Structure

```
Version 1/
├── NotesSharingProject/          # Django project configuration
│   ├── settings.py               # Project settings (now with env variables)
│   ├── urls.py                   # URL routing
│   ├── wsgi.py & asgi.py        # Server config
├── notes/                        # Main Django app
│   ├── models.py                 # Database models (improved)
│   ├── views.py                  # Business logic (500+ lines)
│   ├── forms.py                  # Django Forms (NEW!)
│   ├── email_utils.py            # Email functions (NEW!)
│   ├── admin.py                  # Django admin config
│   ├── templates/                # HTML templates (29 files)
│   ├── static/                   # CSS, JS, images
│   └── migrations/               # Database migrations
├── media/                        # User-uploaded files
│   └── notes/                    # Organized document storage
├── staticfiles/                  # Collected static files (production)
├── db.sqlite3                    # SQLite database
├── manage.py                     # Django management
├── requriements.txt              # Python dependencies
├── .env.example                  # Environment variables template (NEW!)
├── README.md                     # This file (NEW!)
├── INTERVIEW_GUIDE.md            # Interview prep guide (NEW!)
└── debug.log                     # Application logs (generated)
```

---

## 📊 Database Models

### **Signup (User Profile)**
- Extends Django User model
- Stores: contact number, branch, role
- One-to-one relationship with User

### **Notes (Documents)**
- Links to User (uploader)
- Fields: branch, subject, category, file, file type, description
- Status workflow: pending → Accept/Reject
- Tracks: upload date, download count

### **Contact (Queries)**
- Stores: name, email, mobile, subject, message
- Tracks: date, read status
- Helps admin manage student queries

---

## 🎤 Interview Preparation

**Comprehensive interview guide available in `INTERVIEW_GUIDE.md`**

This guide covers:
- Common interview questions with answers
- Technical architecture explanations
- Security considerations
- Performance optimizations
- Future enhancement ideas
- Technical terminology

**Key topics to review:**
1. Django MTV pattern
2. ORM and database queries
3. Form validation
4. File upload security
5. Authentication vs Authorization
6. Search implementation (Q objects)
7. Pagination benefits
8. Email integration
9. Security best practices
10. Scaling strategies

---

## 🔒 Security Features

1. ✅ CSRF protection on all forms
2. ✅ SQL injection prevention (ORM-only queries)
3. ✅ XSS protection (template auto-escaping)
4. ✅ Secure password storage (PBKDF2 hashing)
5. ✅ File upload validation (whitelist + size limit)
6. ✅ Environment variable configuration
7. ✅ Session security
8. ✅ Production security headers

---

## 🐛 Known Issues & Limitations

1. **Email:** Requires SMTP configuration for production
2. **File Storage:** Currently local storage; consider cloud (S3) for scaling
3. **No Document Versioning:** Updates create new documents
4. **No User Ratings:** Can't rate document quality yet
5. **No Real-time Notifications:** Email-only notifications

These are intentional scope limitations and make great talking points for "future enhancements" in interviews.

---

## 🚀 Deployment

For production deployment:

1. Set `DEBUG=False` in environment
2. Configure `ALLOWED_HOSTS`
3. Use PostgreSQL instead of SQLite
4. Configure email SMTP settings
5. Collect static files: `python manage.py collectstatic`
6. Use Gunicorn as WSGI server
7. Set up Nginx as reverse proxy
8. Configure SSL certificate
9. Set up logging and monitoring

---

## 📝 Testing

### Manual Testing Checklist:

**Student Features:**
- [ ] Registration with email validation
- [ ] Login/logout functionality
- [ ] Upload document (check all file types)
- [ ] Search and filter documents
- [ ] Download documents
- [ ] Edit profile
- [ ] Change password
- [ ] Receive email notifications

**Admin Features:**
- [ ] Admin login
- [ ] Dashboard statistics
- [ ] Approve/reject documents
- [ ] Delete documents
- [ ] View users
- [ ] Delete users
- [ ] View contact queries
- [ ] Mark queries as read

**Security Tests:**
- [ ] Try uploading non-whitelisted file type
- [ ] Try uploading file > 50MB
- [ ] Try accessing admin pages as student
- [ ] Try changing password without old password
- [ ] Verify CSRF token on forms

---

## 📄 License

This is an academic project. Feel free to use for learning purposes.

---

## 👨‍💻 Developer

**Your Name**
- B.Tech Student
- Project Duration: January 2024 - April 2024

---

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap Team
- Stack Overflow Community
- Academic Institution for project opportunity

---

## 📞 Support

For interview preparation or technical questions, refer to `INTERVIEW_GUIDE.md`.

---

**Last Updated:** November 2024
**Version:** 1.0 (Enhanced)

---

## Quick Start Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requriements.txt
python manage.py migrate
python manage.py createsuperuser

# Run
python manage.py runserver

# Test email (console backend)
# Emails will print to console during development
```

Happy Learning! 🚀
