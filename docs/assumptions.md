# EduSupport - Assumptions

The assignment intentionally leaves several implementation decisions open. The following assumptions were made while designing the prototype.

## 1. Authentication

Users authenticate using an email address and password.

## 2. User Roles

The system contains three roles:

- STUDENT
- STAFF
- ADMIN

## 3. Ticket Ownership

Each ticket belongs to one student.

Students can view only their own tickets.

## 4. Ticket Categories

The prototype uses predefined categories:

- Fees
- Attendance
- ID Card
- Certificate
- Documents
- Exam
- Hostel
- Transport
- Other

## 5. Priority

Tickets have four priority levels:

- LOW
- MEDIUM
- HIGH
- CRITICAL

## 6. SLA

The priority determines the target resolution time.

- LOW: 72 hours
- MEDIUM: 48 hours
- HIGH: 24 hours
- CRITICAL: 4 hours

## 7. Staff Assignment

A ticket can be assigned to a staff member.

## 8. Ticket Reopening

A student can reopen a resolved or closed ticket when the issue has not actually been resolved.

## 9. Database

SQLite was selected because the assignment is a prototype and does not require a production database server.

## 10. Password Security

The current prototype uses simple password storage to keep the assessment implementation straightforward.

A production version should use secure password hashing such as Argon2 or bcrypt.

## 11. Notifications

Email/SMS notifications were considered outside the initial prototype scope.

A production system could notify students when:

- A ticket is assigned
- Status changes
- A ticket is resolved
- An SLA is approaching or breached

## 12. File Attachments

File attachments are not included in the initial prototype.

They could be added for documents such as receipts, screenshots or certificates.

## 13. Time Calculation

SLA calculations use elapsed time from ticket creation.

A production implementation could additionally consider business hours, holidays and institutional working calendars.