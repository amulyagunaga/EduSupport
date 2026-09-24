# EduSupport - Approach

## 1. Problem Understanding

Educational institutions receive many student support requests related to fees, attendance, certificates, documents, examinations, hostel, transport and other administrative services.

Without a centralized system, these requests can become difficult to track, assign and resolve.

EduSupport addresses this problem through a centralized ticket management workflow.

---

## 2. Proposed Solution

EduSupport allows students to create support tickets and track their progress.

Support staff can:

- View tickets
- Assign tickets
- Change priority
- Update status
- Add comments
- Resolve tickets

Administrators can monitor overall ticket activity through a dashboard.

---

## 3. User Roles

### Student

Students can:

- Login
- Create tickets
- View their own tickets
- Add comments
- Track status
- Reopen resolved or closed tickets

### Staff

Staff members can:

- View support tickets
- Assign tickets
- Update status
- Change priority
- Add comments
- Resolve tickets

### Admin

Administrators can:

- View overall ticket statistics
- Monitor ticket activity
- Manage tickets
- Monitor priorities and SLA information

---

## 4. Ticket Lifecycle

The main workflow is:

OPEN

↓

ASSIGNED

↓

IN_PROGRESS

↓

PENDING

↓

RESOLVED

↓

CLOSED

If the student is not satisfied with the resolution:

RESOLVED / CLOSED

↓

REOPENED

---

## 5. Priority and SLA

Each ticket has a priority.

| Priority | SLA |
|---|---:|
| LOW | 72 hours |
| MEDIUM | 48 hours |
| HIGH | 24 hours |
| CRITICAL | 4 hours |

The due time is calculated when the ticket is created.

---

## 6. Ticket History

A separate ticket history table records important actions.

Examples:

- Ticket Created
- Ticket Assigned
- Status Changed
- Priority Changed
- Comment Added
- Ticket Reopened

This provides an audit trail of the ticket lifecycle.

---

## 7. Architecture

The application follows a simple three-layer flow:

Browser

↓

HTML / Bootstrap / JavaScript

↓

Flask Application

↓

SQLite Database

The architecture was intentionally kept simple because this project is a product engineering prototype.

---

## 8. Technology Choices

### Flask

Flask was selected because it provides a lightweight backend framework and allows rapid development of REST-style routes and server-rendered pages.

### SQLite

SQLite was selected because it is lightweight, requires no separate database server and is suitable for a local prototype.

### Bootstrap

Bootstrap was used to create a responsive interface without introducing unnecessary frontend complexity.

---

## 9. Validation

The solution was validated through manual testing of:

- Authentication
- Ticket creation
- Ticket assignment
- Priority updates
- Status updates
- Comments
- SLA tracking
- Ticket history
- Ticket reopening
- Role-based access control