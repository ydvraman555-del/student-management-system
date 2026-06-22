# ============================================================
# STUDENT MANAGEMENT SYSTEM - app.py
# Flask Backend
# ============================================================

# 1. IMPORTS
from flask import Flask, render_template, request, redirect, url_for, flash
from connection import get_connection, execute_query
from datetime import datetime, date


# 2. FLASK APP
app = Flask(__name__)
app.secret_key = "student_secret_key"


# 3. JINJA2 GLOBALS — make enumerate available in all templates
app.jinja_env.globals.update(enumerate=enumerate)


# ============================================================
# 4. ROUTE → Dashboard "/"
# ============================================================

@app.route("/")
def dashboard():
    try:
        # a) Total students
        result         = execute_query("SELECT COUNT(*) AS cnt FROM students", fetch=True)
        total_students = result[0]["cnt"] if result else 0

        # b) Total subjects
        result         = execute_query("SELECT COUNT(*) AS cnt FROM subjects", fetch=True)
        total_subjects = result[0]["cnt"] if result else 0

        # c) Total present
        result        = execute_query(
            "SELECT COUNT(*) AS cnt FROM attendance WHERE status='Present'", fetch=True
        )
        total_present = result[0]["cnt"] if result else 0

        # d) Total absent
        result       = execute_query(
            "SELECT COUNT(*) AS cnt FROM attendance WHERE status='Absent'", fetch=True
        )
        total_absent = result[0]["cnt"] if result else 0

        # e) Top 5 students
        top_students = execute_query(
            """SELECT name, total_marks, avg_marks, grade
               FROM vw_student_performance
               ORDER BY total_marks DESC
               LIMIT 5""",
            fetch=True
        )

        # f) Class distribution
        class_data = execute_query(
            "SELECT class, COUNT(*) AS cnt FROM students GROUP BY class",
            fetch=True
        )

        # g) Subject average marks
        subject_data = execute_query(
            """SELECT sub.subject_name,
                      ROUND(AVG(m.marks), 2) AS avg_marks
               FROM marks m
               JOIN subjects sub ON m.subject_id = sub.subject_id
               GROUP BY sub.subject_name""",
            fetch=True
        )

        # h) Grade distribution
        grade_data = execute_query(
            "SELECT grade, COUNT(*) AS cnt FROM vw_student_performance GROUP BY grade",
            fetch=True
        )

        return render_template(
            "dashboard.html",
            now            = datetime.now(),
            total_students = total_students,
            total_subjects = total_subjects,
            total_present  = total_present,
            total_absent   = total_absent,
            top_students   = top_students   or [],
            class_data     = class_data     or [],
            subject_data   = subject_data   or [],
            grade_data     = grade_data     or []
        )

    except Exception as e:
        flash(f"❌ Error loading dashboard: {e}", "danger")
        return render_template(
            "dashboard.html",
            now            = datetime.now(),
            total_students = 0,
            total_subjects = 0,
            total_present  = 0,
            total_absent   = 0,
            top_students   = [],
            class_data     = [],
            subject_data   = [],
            grade_data     = []
        )


# ============================================================
# 5. ROUTE → Students "/students"
# ============================================================

@app.route("/students")
def students():
    try:
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '', type=str)
        per_page = 50
        offset = (page - 1) * per_page

        where_clause = ""
        params = []
        if search:
            where_clause = " WHERE name LIKE %s OR email LIKE %s OR class LIKE %s"
            params = [f"%{search}%", f"%{search}%", f"%{search}%"]

        total_count_res = execute_query(f"SELECT COUNT(*) as cnt FROM students {where_clause}", params=params, fetch=True)
        total_count = total_count_res[0]['cnt'] if total_count_res else 0

        students_list = execute_query(
            f"SELECT * FROM students {where_clause} ORDER BY student_id LIMIT %s OFFSET %s",
            params=params + [per_page, offset],
            fetch=True
        )
        total_pages = (total_count + per_page - 1) // per_page if total_count > 0 else 1

        return render_template(
            "students.html",
            students=students_list or [],
            page=page,
            total_pages=total_pages,
            search=search,
            total_records=total_count,
            per_page=per_page
        )
    except Exception as e:
        flash(f"❌ Error loading students: {e}", "danger")
        return render_template("students.html", students=[], page=1, total_pages=1, search='', total_records=0, per_page=50)


# ============================================================
# 6. ROUTE → Add Student "/add_student"
# ============================================================

@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    if request.method == "GET":
        return render_template("add_student.html", student=None)

    # POST
    name  = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    cls   = request.form.get("cls")
    age   = request.form.get("age")

    try:
        execute_query(
            "INSERT INTO students (name, email, phone, class, age) VALUES (%s, %s, %s, %s, %s)",
            params=(name, email, phone, cls, int(age))
        )
        flash("✅ Student Added Successfully!", "success")
        return redirect(url_for("students"))
    except Exception as e:
        flash(f"❌ Error: {e}", "danger")
        return redirect(url_for("add_student"))


# ============================================================
# 7. ROUTE → Update Student "/update_student/<sid>"
# ============================================================

@app.route("/update_student/<int:sid>", methods=["GET", "POST"])
def update_student(sid):
    if request.method == "GET":
        try:
            result  = execute_query(
                "SELECT * FROM students WHERE student_id = %s",
                params=(sid,),
                fetch=True
            )
            student = result[0] if result else None
            return render_template("add_student.html", student=student)
        except Exception as e:
            flash(f"❌ Error loading student: {e}", "danger")
            return redirect(url_for("students"))

    # POST
    name  = request.form.get("name")
    phone = request.form.get("phone")
    cls   = request.form.get("cls")

    try:
        execute_query(
            "UPDATE students SET name=%s, phone=%s, class=%s WHERE student_id=%s",
            params=(name, phone, cls, sid)
        )
        flash("✅ Student Updated!", "success")
        return redirect(url_for("students"))
    except Exception as e:
        flash(f"❌ Error updating student: {e}", "danger")
        return redirect(url_for("update_student", sid=sid))


# ============================================================
# 8. ROUTE → Delete Student "/delete_student/<sid>"
# ============================================================

@app.route("/delete_student/<int:sid>")
def delete_student(sid):
    try:
        execute_query(
            "DELETE FROM students WHERE student_id = %s",
            params=(sid,)
        )
        flash("🗑️ Student Deleted!", "danger")
    except Exception as e:
        flash(f"❌ Error deleting student: {e}", "danger")
    return redirect(url_for("students"))


# ============================================================
# 9. ROUTE → Marks "/marks"
# ============================================================

@app.route("/marks")
def marks():
    try:
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '', type=str)
        per_page = 50
        offset = (page - 1) * per_page

        query_base = """
            FROM marks m
            INNER JOIN students s   ON s.student_id   = m.student_id
            INNER JOIN subjects sub ON sub.subject_id = m.subject_id
        """

        where_clause = ""
        params = []
        if search:
            where_clause = " WHERE s.name LIKE %s OR sub.subject_name LIKE %s"
            params = [f"%{search}%", f"%{search}%"]

        total_count_res = execute_query(f"SELECT COUNT(*) as cnt {query_base} {where_clause}", params=params, fetch=True)
        total_count = total_count_res[0]['cnt'] if total_count_res else 0

        marks_data = execute_query(
            f"""SELECT s.name, sub.subject_name, m.marks, m.exam_date
               {query_base}
               {where_clause}
               ORDER BY s.name, sub.subject_name
               LIMIT %s OFFSET %s""",
            params=params + [per_page, offset],
            fetch=True
        )
        total_pages = (total_count + per_page - 1) // per_page if total_count > 0 else 1

        return render_template(
            "marks.html",
            marks=marks_data or [],
            page=page,
            total_pages=total_pages,
            search=search,
            total_records=total_count,
            per_page=per_page
        )
    except Exception as e:
        flash(f"❌ Error loading marks: {e}", "danger")
        return render_template("marks.html", marks=[], page=1, total_pages=1, search='', total_records=0, per_page=50)


# ============================================================
# 10. ROUTE → Attendance "/attendance"
# ============================================================

@app.route("/attendance")
def attendance():
    try:
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '', type=str)
        per_page = 50
        offset = (page - 1) * per_page

        where_clause = ""
        params = []
        if search:
            where_clause = " WHERE name LIKE %s"
            params = [f"%{search}%"]

        total_count_res = execute_query(f"SELECT COUNT(*) as cnt FROM vw_attendance_summary {where_clause}", params=params, fetch=True)
        total_count = total_count_res[0]['cnt'] if total_count_res else 0

        attendance_data = execute_query(
            f"SELECT * FROM vw_attendance_summary {where_clause} ORDER BY student_id LIMIT %s OFFSET %s",
            params=params + [per_page, offset],
            fetch=True
        )
        students_list = execute_query(
            "SELECT student_id, name FROM students ORDER BY name",
            fetch=True
        )
        total_pages = (total_count + per_page - 1) // per_page if total_count > 0 else 1

        return render_template(
            "attendance.html",
            attendance = attendance_data or [],
            students   = students_list   or [],
            today      = date.today().isoformat(),
            page=page,
            total_pages=total_pages,
            search=search,
            total_records=total_count,
            per_page=per_page
        )
    except Exception as e:
        flash(f"❌ Error loading attendance: {e}", "danger")
        return render_template(
            "attendance.html",
            attendance = [],
            students   = [],
            today      = date.today().isoformat(),
            page=1,
            total_pages=1,
            search='',
            total_records=0,
            per_page=50
        )


# ============================================================
# 11. ROUTE → Mark Attendance "/mark_attendance"
# ============================================================

@app.route("/mark_attendance", methods=["POST"])
def mark_attendance():
    student_id = request.form.get("student_id")
    status     = request.form.get("status")
    att_date   = request.form.get("date") or date.today().isoformat()

    try:
        execute_query(
            "INSERT INTO attendance (student_id, status, date) VALUES (%s, %s, %s)",
            params=(student_id, status, att_date)
        )
        flash("✅ Attendance Marked!", "success")
    except Exception as e:
        flash(f"❌ Error marking attendance: {e}", "danger")
    return redirect(url_for("attendance"))


# ============================================================
# 12. ROUTE → Reports "/reports"
# ============================================================

@app.route("/reports")
def reports():
    try:
        # a) Performance view
        performance = execute_query(
            "SELECT * FROM vw_student_performance ORDER BY total_marks DESC",
            fetch=True
        )

        # b) Window function ranking
        ranking = execute_query(
            """SELECT name, total_marks,
                      RANK()       OVER (ORDER BY total_marks DESC) AS rnk,
                      DENSE_RANK() OVER (ORDER BY total_marks DESC) AS dense_rnk,
                      ROW_NUMBER() OVER (ORDER BY total_marks DESC) AS row_num
               FROM vw_student_performance""",
            fetch=True
        )

        # c) CTE — avg marks > 70
        cte_top = execute_query(
            """WITH top_students AS (
                   SELECT s.name,
                          ROUND(AVG(m.marks), 2) AS avg_m
                   FROM students s
                   JOIN marks m ON s.student_id = m.student_id
                   GROUP BY s.student_id, s.name
               )
               SELECT * FROM top_students
               WHERE avg_m > 70
               ORDER BY avg_m DESC""",
            fetch=True
        )

        # d) Subquery — above average
        above_avg = execute_query(
            """SELECT name FROM students
               WHERE student_id IN (
                   SELECT student_id FROM marks
                   GROUP BY student_id
                   HAVING AVG(marks) > 70
               )""",
            fetch=True
        )

        return render_template(
            "reports.html",
            performance = performance or [],
            ranking     = ranking     or [],
            cte_top     = cte_top     or [],
            above_avg   = above_avg   or []
        )

    except Exception as e:
        flash(f"❌ Error loading reports: {e}", "danger")
        return render_template(
            "reports.html",
            performance = [],
            ranking     = [],
            cte_top     = [],
            above_avg   = []
        )


# ============================================================
# 13. ROUTE → Audit Log "/audit"
# ============================================================

@app.route("/audit")
def audit():
    try:
        logs = execute_query(
            "SELECT * FROM audit_log ORDER BY log_time DESC",
            fetch=True
        )
        return render_template("audit.html", logs=logs or [])
    except Exception as e:
        flash(f"❌ Error loading audit log: {e}", "danger")
        return render_template("audit.html", logs=[])


# ============================================================
# 14. ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def page_not_found(e):
    return f"""
    <div style='text-align:center; padding:80px; font-family:Segoe UI, sans-serif;
                background:#f0f2f5; min-height:100vh;'>
        <div style='background:white; padding:50px; border-radius:16px;
                    display:inline-block; box-shadow:0 4px 20px rgba(0,0,0,0.1)'>
            <h1 style='color:#1a237e; font-size:5rem; margin:0;'>404</h1>
            <h2 style='color:#444;'>Page Not Found</h2>
            <p style='color:#888;'>The page you are looking for does not exist.</p>
            <a href='/' style='background:#1a237e; color:white; padding:12px 30px;
                               border-radius:8px; text-decoration:none;
                               font-weight:600;'>🏠 Go to Dashboard</a>
        </div>
    </div>
    """, 404


@app.errorhandler(500)
def internal_error(e):
    return f"""
    <div style='text-align:center; padding:80px; font-family:Segoe UI, sans-serif;
                background:#f0f2f5; min-height:100vh;'>
        <div style='background:white; padding:50px; border-radius:16px;
                    display:inline-block; box-shadow:0 4px 20px rgba(0,0,0,0.1)'>
            <h1 style='color:#c0392b; font-size:5rem; margin:0;'>500</h1>
            <h2 style='color:#444;'>Server Error</h2>
            <p style='color:#888;'>Something went wrong. Please try again.</p>
            <a href='/' style='background:#1a237e; color:white; padding:12px 30px;
                               border-radius:8px; text-decoration:none;
                               font-weight:600;'>🏠 Go to Dashboard</a>
        </div>
    </div>
    """, 500


# ============================================================
# 15. RUN APP
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)
