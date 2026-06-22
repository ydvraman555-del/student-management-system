import mysql.connector


# ============================================================
# CONNECTION
# ============================================================

def get_connection():
    conn = mysql.connector.connect(
        host     = "localhost",
        user     = "root",
        password = "12345",
        database = "student_db"
    )
    return conn


# ============================================================
# EXECUTE QUERY (SELECT / INSERT / UPDATE / DELETE)
# ============================================================

def execute_query(query, params=None, fetch=False):
    conn   = None
    cursor = None
    try:
        conn   = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        if fetch:
            result = cursor.fetchall()
            cursor.close()
            return result
        else:
            conn.commit()
            cursor.close()
            return None
    except Exception as e:
        print(f"Query Error: {e}")
        return [] if fetch else None
    finally:
        if conn:
            conn.close()


# ============================================================
# EXECUTE STORED PROCEDURE
# ============================================================

def execute_procedure(proc_name, params=()):
    conn   = None
    cursor = None
    try:
        conn   = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc(proc_name, params)
        conn.commit()
    except Exception as e:
        print(f"Procedure Error: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    try:
        conn = get_connection()
        print("✅ Database Connected Successfully!")
        conn.close()
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
