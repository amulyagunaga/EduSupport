# EduSupport

## Student Support & Ticket Management System

EduSupport is a web-based student support and ticket management prototype designed for educational institutions.

The system provides a centralized workflow for students to raise support requests and for staff to assign, prioritize, process and resolve those requests.

---

# Features

## Student

- Secure login flow
- Create support tickets
- Select ticket category
- Set ticket priority
- View own tickets
- Track ticket status
- Add comments
- View ticket history
- Reopen resolved or closed tickets

## Staff

- Staff dashboard
- View student tickets
- Assign tickets
- Change priority
- Update status
- Add comments
- Track SLA
- View ticket history
- Resolve tickets

## Admin

- Admin dashboard
- Overall ticket statistics
- Priority overview
- Category overview
- Recent ticket monitoring
- Ticket management

---

# Ticket Categories

- Fees
- Attendance
- ID Card
- Certificate
- Documents
- Exam
- Hostel
- Transport
- Other

---

# Priority and SLA

| Priority | SLA |
|---|---:|
| LOW | 72 hours |
| MEDIUM | 48 hours |
| HIGH | 24 hours |
| CRITICAL | 4 hours |

---

# Ticket Statuses

- OPEN
- ASSIGNED
- IN_PROGRESS
- PENDING
- RESOLVED
- CLOSED
- REOPENED

---

# Technology Stack

- Python
- Flask
- SQLite
- HTML
- CSS
- Bootstrap
- JavaScript

---

# Architecture

Browser

↓

HTML + Bootstrap + JavaScript

↓

Flask Backend

↓

SQLite Database

---

# Project Structure

```text
EduSupport/
│
├── app.py
├── database.py
├── requirements.txt
├── edusupport.db
├── README.md
│
├── templates/
├── static/
├── sql/
│
└── docs/
    ├── approach.md
    ├── assumptions.md
    ├── testing.md
    └── ai-usage-report.md

Installation
1. Clone the repository
git clone <repository-url>
2. Enter the project
cd EduSupport
3. Create virtual environment
python -m venv venv
4. Activate virtual environment

Windows:

venv\Scripts\activate
5. Install dependencies
pip install -r requirements.txt
6. Run application
python app.py
7. Open browser
http://127.0.0.1:5000
Demo Accounts
Student

Email:

student@college.com

Password:

student123
Staff

Email:

staff@college.com

Password:

staff123
Admin

Email:

admin@college.com

Password:

admin123
Future Improvements

A production version could include:

Password hashing
Email notifications
File attachments
Search and filtering
Pagination
PostgreSQL/MySQL
Automated tests
Background SLA monitoring
Business-hour SLA calculations
Cloud deployment
More advanced role-based authorization
AI Usage

AI assistance was used during development for requirement understanding, product brainstorming, implementation assistance, debugging, testing ideas and documentation.

All AI-assisted code was reviewed and tested manually.

Detailed information is available in:

docs/ai-usage-report.md




Clone
  ↓
cd EduSupport
  ↓
Create virtual environment
  ↓
Activate virtual environment
  ↓
pip install -r requirements.txt
  ↓
python app.py
  ↓
Open http://127.0.0.1:5000
  ↓
Login