from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "edusupport-secret-key"

DATABASE = "edusupport.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    with open("sql/schema.sql", "r") as f:
        conn.executescript(f.read())

    # Demo users
    conn.execute("""
        INSERT OR IGNORE INTO users
        (id, name, email, password, role, department)
        VALUES
        (1, 'Amulya Student', 'student@college.com',
         'student123', 'STUDENT', 'Computer Science')
    """)

    conn.execute("""
        INSERT OR IGNORE INTO users
        (id, name, email, password, role, department)
        VALUES
        (2, 'Support Staff', 'staff@college.com',
         'staff123', 'STAFF', 'Administration')
    """)

    conn.execute("""
        INSERT OR IGNORE INTO users
        (id, name, email, password, role, department)
        VALUES
        (3, 'Admin User', 'admin@college.com',
         'admin123', 'ADMIN', 'Administration')
    """)

    conn.commit()
    staff_users = conn.execute("""
    SELECT id, name, email
    FROM users
    WHERE role = 'STAFF'
    ORDER BY name
""").fetchall()
    conn.close()


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()

        user = conn.execute("""
            SELECT * FROM users
            WHERE email = ? AND password = ?
        """, (email, password)).fetchone()

        conn.close()

        if user:

            session["user_id"] = user["id"]
            session["name"] = user["name"]
            session["role"] = user["role"]

            if user["role"] == "STUDENT":
                return redirect(url_for("dashboard"))

            elif user["role"] == "STAFF":
                return redirect(url_for("staff_dashboard"))

            elif user["role"] == "ADMIN":
                return redirect(url_for("admin_dashboard"))

        else:
            error = "Invalid email or password"

    return render_template("login.html", error=error)


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    tickets = conn.execute("""
        SELECT *
        FROM tickets
        WHERE student_id = ?
        ORDER BY created_at DESC
    """, (session["user_id"],)).fetchall()

    total = len(tickets)
    open_count = sum(1 for t in tickets if t["status"] == "OPEN")
    pending_count = sum(1 for t in tickets if t["status"] == "PENDING")
    resolved_count = sum(
        1 for t in tickets
        if t["status"] in ["RESOLVED", "CLOSED"]
    )

    conn.close()

    return render_template(
        "dashboard.html",
        tickets=tickets,
        total=total,
        open_count=open_count,
        pending_count=pending_count,
        resolved_count=resolved_count
    )

@app.route("/create-ticket", methods=["GET", "POST"])
def create_ticket():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        category = request.form["category"]
        subject = request.form["subject"]
        description = request.form["description"]
        priority = request.form["priority"]

        import uuid
        from datetime import datetime, timedelta

        ticket_number = "TKT-" + str(uuid.uuid4())[:8].upper()

        if priority == "LOW":
            sla_hours = 72
        elif priority == "MEDIUM":
            sla_hours = 48
        elif priority == "HIGH":
            sla_hours = 24
        else:
            sla_hours = 4

        due_at = datetime.now() + timedelta(hours=sla_hours)

        conn = get_db()

        cursor = conn.execute("""
            INSERT INTO tickets
            (
                ticket_number,
                student_id,
                category,
                subject,
                description,
                priority,
                status,
                due_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ticket_number,
            session["user_id"],
            category,
            subject,
            description,
            priority,
            "OPEN",
            due_at
        ))

        ticket_id = cursor.lastrowid

        conn.execute("""
            INSERT INTO ticket_history
            (
                ticket_id,
                user_id,
                action,
                old_value,
                new_value
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            ticket_id,
            session["user_id"],
            "Ticket Created",
            None,
            "OPEN"
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    return render_template("create_ticket.html")

@app.route("/ticket/<int:ticket_id>", methods=["GET", "POST"])
def ticket_detail(ticket_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    ticket = conn.execute("""
        SELECT
            t.*,
            u.name AS student_name,
            s.name AS assigned_name
        FROM tickets t
        JOIN users u
            ON t.student_id = u.id
        LEFT JOIN users s
            ON t.assigned_to = s.id
        WHERE t.id = ?
    """, (ticket_id,)).fetchone()

    if not ticket:
        conn.close()
        return "Ticket not found", 404

    # Students can only view their own tickets
    if session["role"] == "STUDENT":
        if ticket["student_id"] != session["user_id"]:
            conn.close()
            return "Access denied", 403

    # Add comment
    if request.method == "POST":

        comment = request.form["comment"].strip()

        if comment:

            conn.execute("""
                INSERT INTO ticket_comments
                (
                    ticket_id,
                    user_id,
                    comment
                )
                VALUES (?, ?, ?)
            """, (
                ticket_id,
                session["user_id"],
                comment
            ))

            conn.execute("""
                INSERT INTO ticket_history
                (
                    ticket_id,
                    user_id,
                    action,
                    old_value,
                    new_value
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                ticket_id,
                session["user_id"],
                "Comment Added",
                None,
                comment
            ))

            conn.commit()

        conn.close()

        return redirect(
            url_for("ticket_detail", ticket_id=ticket_id)
        )

    # Get comments
    comments = conn.execute("""
        SELECT
            tc.*,
            u.name AS user_name,
            u.role
        FROM ticket_comments tc
        JOIN users u
            ON tc.user_id = u.id
        WHERE tc.ticket_id = ?
        ORDER BY tc.created_at ASC
    """, (ticket_id,)).fetchall()

    # Get ticket history
    history = conn.execute("""
        SELECT
            th.*,
            u.name AS user_name
        FROM ticket_history th
        JOIN users u
            ON th.user_id = u.id
        WHERE th.ticket_id = ?
        ORDER BY th.created_at DESC
    """, (ticket_id,)).fetchall()

    # Check SLA
    from datetime import datetime

    sla_breached = False

    if ticket["due_at"]:

        due_date = datetime.fromisoformat(ticket["due_at"])

        if (
            due_date < datetime.now()
            and ticket["status"] not in ["RESOLVED", "CLOSED"]
        ):
            sla_breached = True

    # Get staff members for assignment dropdown
    staff_users = conn.execute("""
        SELECT
            id,
            name,
            email
        FROM users
        WHERE role = 'STAFF'
        ORDER BY name
    """).fetchall()

    conn.close()

    return render_template(
        "ticket_detail.html",
        ticket=ticket,
        comments=comments,
        history=history,
        sla_breached=sla_breached,
        staff_users=staff_users
    )

@app.route("/staff-dashboard")
def staff_dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] not in ["STAFF", "ADMIN"]:
        return "Access denied", 403

    conn = get_db()

    # Get all tickets
    tickets = conn.execute("""
        SELECT
            t.*,
            u.name AS student_name,
            s.name AS assigned_name
        FROM tickets t
        JOIN users u
            ON t.student_id = u.id
        LEFT JOIN users s
            ON t.assigned_to = s.id
        ORDER BY
            CASE t.priority
                WHEN 'CRITICAL' THEN 1
                WHEN 'HIGH' THEN 2
                WHEN 'MEDIUM' THEN 3
                WHEN 'LOW' THEN 4
            END,
            t.created_at DESC
    """).fetchall()

    # Basic counts
    total = len(tickets)

    open_count = sum(
        1 for t in tickets
        if t["status"] == "OPEN"
    )

    assigned_count = sum(
        1 for t in tickets
        if t["status"] in ["ASSIGNED", "IN_PROGRESS"]
    )

    pending_count = sum(
        1 for t in tickets
        if t["status"] == "PENDING"
    )

    resolved_count = sum(
        1 for t in tickets
        if t["status"] in ["RESOLVED", "CLOSED"]
    )

    critical_count = sum(
        1 for t in tickets
        if t["priority"] == "CRITICAL"
    )

    high_count = sum(
        1 for t in tickets
        if t["priority"] == "HIGH"
    )

    # Check SLA breaches
    from datetime import datetime

    sla_breached_count = 0

    for ticket in tickets:

        if ticket["due_at"]:

            due_date = datetime.fromisoformat(
                ticket["due_at"]
            )

            if (
                due_date < datetime.now()
                and ticket["status"]
                not in ["RESOLVED", "CLOSED"]
            ):
                sla_breached_count += 1

    conn.close()

    return render_template(
        "staff_dashboard.html",
        tickets=tickets,
        total=total,
        open_count=open_count,
        assigned_count=assigned_count,
        pending_count=pending_count,
        resolved_count=resolved_count,
        critical_count=critical_count,
        high_count=high_count,
        sla_breached_count=sla_breached_count
    )

@app.route("/ticket/<int:ticket_id>/update", methods=["POST"])
def update_ticket(ticket_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    # Only staff and admin can update tickets
    if session["role"] not in ["STAFF", "ADMIN"]:
        return "Access denied", 403

    conn = get_db()

    # Get the current ticket
    ticket = conn.execute("""
        SELECT *
        FROM tickets
        WHERE id = ?
    """, (ticket_id,)).fetchone()

    if not ticket:
        conn.close()
        return "Ticket not found", 404

    # Get values submitted from the form
    new_status = request.form.get("status")
    assigned_to = request.form.get("assigned_to")
    new_priority = request.form.get("priority")

    # =========================================================
    # 1. STATUS UPDATE
    # =========================================================

    if new_status and new_status != ticket["status"]:

        conn.execute("""
            UPDATE tickets
            SET status = ?
            WHERE id = ?
        """, (
            new_status,
            ticket_id
        ))

        from datetime import datetime

        # Store resolved time
        if new_status == "RESOLVED":

            conn.execute("""
                UPDATE tickets
                SET resolved_at = ?
                WHERE id = ?
            """, (
                datetime.now(),
                ticket_id
            ))

        # Store closed time
        elif new_status == "CLOSED":

            conn.execute("""
                UPDATE tickets
                SET closed_at = ?
                WHERE id = ?
            """, (
                datetime.now(),
                ticket_id
            ))

        # Add status change to history
        conn.execute("""
            INSERT INTO ticket_history
            (
                ticket_id,
                user_id,
                action,
                old_value,
                new_value
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            ticket_id,
            session["user_id"],
            "Status Changed",
            ticket["status"],
            new_status
        ))

    # =========================================================
    # 2. ASSIGNMENT UPDATE
    # =========================================================

    if assigned_to:

        assigned_to = int(assigned_to)

        if assigned_to != ticket["assigned_to"]:

            old_assignee = ticket["assigned_to"]

            # ---------------------------------------------
            # Get old staff member's name
            # ---------------------------------------------

            old_assignee_name = "Unassigned"

            if old_assignee:

                old_user = conn.execute("""
                    SELECT name
                    FROM users
                    WHERE id = ?
                """, (old_assignee,)).fetchone()

                if old_user:
                    old_assignee_name = old_user["name"]

            # ---------------------------------------------
            # Get new staff member's name
            # ---------------------------------------------

            new_user = conn.execute("""
                SELECT name
                FROM users
                WHERE id = ?
            """, (assigned_to,)).fetchone()

            new_assignee_name = (
                new_user["name"]
                if new_user
                else "Unknown"
            )

            # ---------------------------------------------
            # Update ticket assignment
            # ---------------------------------------------

            conn.execute("""
                UPDATE tickets
                SET assigned_to = ?,
                    status = CASE
                        WHEN status = 'OPEN'
                        THEN 'ASSIGNED'
                        ELSE status
                    END
                WHERE id = ?
            """, (
                assigned_to,
                ticket_id
            ))

            # ---------------------------------------------
            # Add assignment to history
            # ---------------------------------------------

            conn.execute("""
                INSERT INTO ticket_history
                (
                    ticket_id,
                    user_id,
                    action,
                    old_value,
                    new_value
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                ticket_id,
                session["user_id"],
                "Ticket Assigned",
                old_assignee_name,
                new_assignee_name
            ))

    # =========================================================
    # 3. PRIORITY UPDATE
    # =========================================================

    if new_priority and new_priority != ticket["priority"]:

        conn.execute("""
            UPDATE tickets
            SET priority = ?
            WHERE id = ?
        """, (
            new_priority,
            ticket_id
        ))

        # Add priority change to history
        conn.execute("""
            INSERT INTO ticket_history
            (
                ticket_id,
                user_id,
                action,
                old_value,
                new_value
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            ticket_id,
            session["user_id"],
            "Priority Changed",
            ticket["priority"],
            new_priority
        ))

    # Save all changes
    conn.commit()

    # Close database connection
    conn.close()

    # Go back to ticket details
    return redirect(
        url_for(
            "ticket_detail",
            ticket_id=ticket_id
        )
    )

@app.route("/ticket/<int:ticket_id>/reopen", methods=["POST"])
def reopen_ticket(ticket_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    ticket = conn.execute("""
        SELECT *
        FROM tickets
        WHERE id = ?
    """, (ticket_id,)).fetchone()

    if not ticket:
        conn.close()
        return "Ticket not found", 404

    # Only the student who created the ticket
    # can reopen it
    if (
        session["role"] == "STUDENT"
        and ticket["student_id"] != session["user_id"]
    ):
        conn.close()
        return "Access denied", 403

    # Ticket must be resolved or closed
    if ticket["status"] not in ["RESOLVED", "CLOSED"]:
        conn.close()
        return "Only resolved or closed tickets can be reopened", 400

    # Change status
    conn.execute("""
        UPDATE tickets
        SET status = ?,
            resolved_at = NULL,
            closed_at = NULL
        WHERE id = ?
    """, (
        "REOPENED",
        ticket_id
    ))

    # Add history
    conn.execute("""
        INSERT INTO ticket_history
        (
            ticket_id,
            user_id,
            action,
            old_value,
            new_value
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        ticket_id,
        session["user_id"],
        "Ticket Reopened",
        ticket["status"],
        "REOPENED"
    ))

    conn.commit()
    conn.close()

    return redirect(
        url_for(
            "ticket_detail",
            ticket_id=ticket_id
        )
    )
@app.route("/admin-dashboard")
def admin_dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "ADMIN":
        return "Access denied", 403

    conn = get_db()

    total = conn.execute("""
        SELECT COUNT(*) AS count
        FROM tickets
    """).fetchone()["count"]

    open_count = conn.execute("""
        SELECT COUNT(*) AS count
        FROM tickets
        WHERE status = 'OPEN'
    """).fetchone()["count"]

    in_progress_count = conn.execute("""
        SELECT COUNT(*) AS count
        FROM tickets
        WHERE status IN ('ASSIGNED', 'IN_PROGRESS')
    """).fetchone()["count"]

    pending_count = conn.execute("""
        SELECT COUNT(*) AS count
        FROM tickets
        WHERE status = 'PENDING'
    """).fetchone()["count"]

    resolved_count = conn.execute("""
        SELECT COUNT(*) AS count
        FROM tickets
        WHERE status IN ('RESOLVED', 'CLOSED')
    """).fetchone()["count"]

    critical_count = conn.execute("""
        SELECT COUNT(*) AS count
        FROM tickets
        WHERE priority = 'CRITICAL'
    """).fetchone()["count"]

    high_count = conn.execute("""
        SELECT COUNT(*) AS count
        FROM tickets
        WHERE priority = 'HIGH'
    """).fetchone()["count"]

    category_data = conn.execute("""
        SELECT
            category,
            COUNT(*) AS count
        FROM tickets
        GROUP BY category
        ORDER BY count DESC
    """).fetchall()

    recent_tickets = conn.execute("""
        SELECT
            t.*,
            u.name AS student_name,
            s.name AS assigned_name
        FROM tickets t
        JOIN users u
            ON t.student_id = u.id
        LEFT JOIN users s
            ON t.assigned_to = s.id
        ORDER BY t.created_at DESC
        LIMIT 10
    """).fetchall()

    conn.close()

    return render_template(
        "admin_dashboard.html",
        total=total,
        open_count=open_count,
        in_progress_count=in_progress_count,
        pending_count=pending_count,
        resolved_count=resolved_count,
        critical_count=critical_count,
        high_count=high_count,
        category_data=category_data,
        recent_tickets=recent_tickets
    )

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)