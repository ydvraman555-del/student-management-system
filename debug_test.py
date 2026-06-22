"""
Debug script - Student Management System
Run: python debug_test.py
"""
import sys
import mysql.connector

sys.stdout.reconfigure(encoding='utf-8')

SEP = "=" * 60

def ok(msg):  print(f"  [OK]  {msg}")
def fail(msg): print(f"  [ERR] {msg}")
def warn(msg): print(f"  [!]   {msg}")

# ── 1. Test connection ─────────────────────────────────────────
print(f"\n{SEP}\nTEST 1: Database Connection\n{SEP}")
try:
    conn = mysql.connector.connect(
        host="localhost", user="root", password="12345", database="student_db"
    )
    ok("Connected to student_db")
    cursor = conn.cursor(dictionary=True)
except Exception as e:
    fail(f"Connection failed: {e}")
    exit()

# ── 2. Check tables ────────────────────────────────────────────
print(f"\n{SEP}\nTEST 2: Tables\n{SEP}")
cursor.execute("SHOW TABLES")
rows   = cursor.fetchall()
tables = [row[list(row.keys())[0]] for row in rows]
print(f"  Found tables: {tables}")
for t in ['students','subjects','marks','attendance','audit_log']:
    (ok if t in tables else fail)(t)

# ── 3. Check views ─────────────────────────────────────────────
print(f"\n{SEP}\nTEST 3: Views\n{SEP}")
cursor.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW'")
rows  = cursor.fetchall()
views = [row[list(row.keys())[0]] for row in rows]
print(f"  Found views: {views}")
for v in ['vw_student_performance','vw_attendance_summary']:
    (ok if v in views else fail)(v)

# ── 4. Check stored procedures ─────────────────────────────────
print(f"\n{SEP}\nTEST 4: Stored Procedures\n{SEP}")
cursor.execute("SHOW PROCEDURE STATUS WHERE Db='student_db'")
procs = [row['Name'] for row in cursor.fetchall()]
print(f"  Found procedures: {procs}")
for p in ['sp_add_student','sp_student_total_marks']:
    (ok if p in procs else fail)(p)

# ── 5. Check function ──────────────────────────────────────────
print(f"\n{SEP}\nTEST 5: Functions\n{SEP}")
cursor.execute("SHOW FUNCTION STATUS WHERE Db='student_db'")
funcs = [row['Name'] for row in cursor.fetchall()]
print(f"  Found functions: {funcs}")
(ok if 'fn_get_grade' in funcs else fail)('fn_get_grade')

# ── 6. Check triggers ──────────────────────────────────────────
print(f"\n{SEP}\nTEST 6: Triggers\n{SEP}")
cursor.execute("SHOW TRIGGERS")
trigs = [row['Trigger'] for row in cursor.fetchall()]
print(f"  Found triggers: {trigs}")
for t in ['trg_after_student_insert','trg_after_student_delete','trg_before_marks_update']:
    (ok if t in trigs else fail)(t)

# ── 7. Test sp_add_student directly ───────────────────────────
print(f"\n{SEP}\nTEST 7: sp_add_student (direct call)\n{SEP}")
try:
    cursor.callproc('sp_add_student',
                    ('Debug Student','debug@test.com','9999999999','10A', 15))
    conn.commit()
    ok("callproc executed without error")
    cursor.execute("SELECT * FROM students WHERE email='debug@test.com'")
    row = cursor.fetchone()
    if row:
        ok(f"Row found in DB: {row}")
        cursor.execute("DELETE FROM students WHERE email='debug@test.com'")
        conn.commit()
        ok("Test row cleaned up")
    else:
        fail("Row NOT found after callproc - procedure may be missing")
except Exception as e:
    fail(f"sp_add_student error: {e}")

# ── 8. Test fn_get_grade ───────────────────────────────────────
print(f"\n{SEP}\nTEST 8: fn_get_grade\n{SEP}")
for marks_val, expected in [(85,'A'),(70,'B'),(45,'C'),(20,'F')]:
    try:
        cursor.execute(f"SELECT fn_get_grade({marks_val}) AS grade")
        grade = cursor.fetchone()['grade']
        result = "OK" if grade == expected else "WRONG"
        print(f"  [{result}] fn_get_grade({marks_val}) = {grade} (expected {expected})")
    except Exception as e:
        fail(f"fn_get_grade({marks_val}): {e}")

# ── 9. Test vw_student_performance ────────────────────────────
print(f"\n{SEP}\nTEST 9: vw_student_performance\n{SEP}")
try:
    cursor.execute("SELECT * FROM vw_student_performance LIMIT 3")
    rows = cursor.fetchall()
    if rows:
        for r in rows:
            ok(f"{r['name']} | Total:{r['total_marks']} | Avg:{r['avg_marks']} | Grade:{r['grade']}")
    else:
        warn("View returned 0 rows - marks table may be empty")
except Exception as e:
    fail(f"vw_student_performance: {e}")

# ── 10. Test vw_attendance_summary ────────────────────────────
print(f"\n{SEP}\nTEST 10: vw_attendance_summary\n{SEP}")
try:
    cursor.execute("SELECT * FROM vw_attendance_summary LIMIT 3")
    rows = cursor.fetchall()
    if rows:
        for r in rows:
            ok(f"{r['name']} | Present:{r['total_present']} | Absent:{r['total_absent']}")
    else:
        warn("View returned 0 rows")
except Exception as e:
    fail(f"vw_attendance_summary: {e}")

# ── 11. Row counts ─────────────────────────────────────────────
print(f"\n{SEP}\nTEST 11: Row Counts\n{SEP}")
for table in ['students','subjects','marks','attendance','audit_log']:
    try:
        cursor.execute(f"SELECT COUNT(*) AS cnt FROM {table}")
        cnt = cursor.fetchone()['cnt']
        (ok if cnt > 0 else warn)(f"{table}: {cnt} rows")
    except Exception as e:
        fail(f"{table}: {e}")

# ── 12. Direct INSERT test (bypass procedure) ──────────────────
print(f"\n{SEP}\nTEST 12: Direct INSERT into students\n{SEP}")
try:
    cursor.execute(
        "INSERT INTO students (name,email,phone,class,age) VALUES (%s,%s,%s,%s,%s)",
        ('Direct Insert Test','direct@test.com','8888888888','10B',16)
    )
    conn.commit()
    ok("Direct INSERT succeeded")
    cursor.execute("DELETE FROM students WHERE email='direct@test.com'")
    conn.commit()
    ok("Cleaned up test row")
except Exception as e:
    fail(f"Direct INSERT failed: {e}")

cursor.close()
conn.close()
print(f"\n{SEP}\nDEBUG COMPLETE\n{SEP}\n")
