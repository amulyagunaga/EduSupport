# EduSupport Testing Document

## 1. Testing Objective

The objective of testing is to verify that the major student support workflows work correctly and that users can only access functionality permitted by their role.

---

## 2. Authentication Testing

| Test Case | Expected Result | Result |
|---|---|---|
| Valid student login | Student dashboard opens | PASS |
| Valid staff login | Staff dashboard opens | PASS |
| Valid admin login | Admin dashboard opens | PASS |
| Invalid email/password | Error message displayed | PASS |
| Logout | Session is cleared and login page opens | PASS |

---

## 3. Student Ticket Testing

| Test Case | Expected Result | Result |
|---|---|---|
| Create ticket | Ticket is created successfully | PASS |
| Select category | Selected category is stored | PASS |
| Select priority | Selected priority is stored | PASS |
| Ticket number generation | Unique ticket number generated | PASS |
| SLA calculation | Due date generated according to priority | PASS |
| View own ticket | Student can view own ticket | PASS |
| Add comment | Comment appears in ticket | PASS |
| Reopen resolved ticket | Ticket changes to REOPENED | PASS |

---

## 4. Staff Testing

| Test Case | Expected Result | Result |
|---|---|---|
| Staff dashboard opens | Dashboard displayed | PASS |
| View ticket | Ticket details displayed | PASS |
| Assign ticket | Staff member assigned | PASS |
| Change status | Status updated | PASS |
| Change priority | Priority updated | PASS |
| Add comment | Comment added | PASS |
| View ticket history | Actions displayed | PASS |

---

## 5. Admin Testing

| Test Case | Expected Result | Result |
|---|---|---|
| Admin dashboard opens | Dashboard displayed | PASS |
| View total tickets | Correct count displayed | PASS |
| View category statistics | Category counts displayed | PASS |
| View recent tickets | Recent tickets displayed | PASS |
| Manage ticket | Ticket can be updated | PASS |

---

## 6. Access Control Testing

| Test Case | Expected Result | Result |
|---|---|---|
| Student accesses staff dashboard | Access denied | PASS |
| Student accesses admin dashboard | Access denied | PASS |
| Staff accesses admin dashboard | Access denied | PASS |
| Student opens another student's ticket | Access denied | PASS |
| Unauthenticated user accesses dashboard | Redirected to login | PASS |

---

## 7. SLA Testing

### Low Priority

Expected SLA:

72 hours

### Medium Priority

Expected SLA:

48 hours

### High Priority

Expected SLA:

24 hours

### Critical Priority

Expected SLA:

4 hours

The application calculates the ticket due time during ticket creation and checks whether the SLA deadline has passed.

---

## 8. Ticket Lifecycle Testing

The intended lifecycle is:

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

A resolved or closed ticket can also be reopened:

RESOLVED / CLOSED

↓

REOPENED

---

## 9. History Testing

The system records important ticket events including:

- Ticket Created
- Ticket Assigned
- Status Changed
- Priority Changed
- Comment Added
- Ticket Reopened

This allows the ticket lifecycle to be reviewed later.

---

## 10. Final Testing Status

All major workflows were manually tested through the browser using the Student, Staff and Admin demo accounts.

The prototype was tested by creating tickets, updating tickets, assigning staff, adding comments, changing status and priority, checking SLA information and reopening resolved tickets.