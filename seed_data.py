"""
seed_data.py — Insert 50 students per class/division
Classes : 10A, 10B, 10C, 11A, 11B, 11C, 12A, 12B, 12C
Total   : 9 classes x 50 students = 450 students
Marks   : 4 subjects per student  = 1800 mark records
Attendance: 10 days per student   = 4500 attendance records

Run: python seed_data.py
"""

import sys
import random
import mysql.connector
from datetime import date, timedelta

sys.stdout.reconfigure(encoding='utf-8')

# ── DB Connection ──────────────────────────────────────────────
conn = mysql.connector.connect(
    host="localhost", user="root", password="12345", database="student_db"
)
cursor = conn.cursor()
print("[INFO] Connected to student_db")

# ── Indian First Names ─────────────────────────────────────────
first_names = [
    "Aarav","Aditya","Akash","Alok","Amit","Ananya","Anjali","Ankit","Ankita","Anuj",
    "Arjun","Aryan","Ashish","Ayaan","Ayesha","Bhavna","Chetan","Deepak","Deepika","Dev",
    "Dhruv","Diya","Esha","Gaurav","Harshita","Himanshu","Ishaan","Ishika","Jatin","Karan",
    "Kavya","Kunal","Lakshmi","Lavanya","Manav","Manisha","Mayank","Meera","Mihir","Mohit",
    "Nandini","Neha","Nikhil","Nikita","Nitin","Pallavi","Pankaj","Payal","Pooja","Prachi",
    "Pranav","Priya","Rahul","Raj","Rajesh","Ravi","Riya","Kartik","Rohit","Sachin",
    "Sahil","Sanjay","Sara","Saurabh","Shivam","Shreya","Shruti","Simran","Sneha","Sonam",
    "Sunil","Suresh","Swati","Tanvi","Tarun","Tushar","Uday","Vandana","Varun","Vikas",
    "Vikram","Vinay","Vishal","Vivek","Yamini","Yash","Zara","Zoya","Kabir","Kiara",
    "Krish","Kriti","Madhav","Mahi","Navya","Nishant","Parth","Riddhi","Siddharth","Trisha"
]

# ── Indian Last Names ──────────────────────────────────────────
last_names = [
    "Sharma","Verma","Singh","Kumar","Gupta","Patel","Shah","Mehta","Joshi","Yadav",
    "Mishra","Pandey","Tiwari","Agarwal","Bhatia","Kapoor","Malhotra","Nair","Reddy","Iyer",
    "Pillai","Menon","Rao","Sinha","Dubey","Chauhan","Saxena","Shukla","Tripathi","Bansal",
    "Goyal","Jain","Khanna","Lal","Mathur","Naidu","Oberoi","Prasad","Qureshi","Rastogi",
    "Srivastava","Thakur","Upadhyay","Vora","Walia","Yadav","Zaveri","Anand","Bhatt","Chaudhary"
]

# ── Classes & Age Ranges ───────────────────────────────────────
classes = {
    "10A": (14, 16),
    "10B": (14, 16),
    "10C": (14, 16),
    "11A": (15, 17),
    "11B": (15, 17),
    "11C": (15, 17),
    "12A": (16, 18),
    "12B": (16, 18),
    "12C": (16, 18),
}

# ── Subject IDs (must match DB: 1=Maths, 2=Science, 3=English, 4=Hindi) ──────
subject_ids = [1, 2, 3, 4]

# ── Attendance Dates (10 school days) ─────────────────────────
att_dates = [
    "2025-06-02","2025-06-03","2025-06-04","2025-06-05","2025-06-06",
    "2025-06-09","2025-06-10","2025-06-11","2025-06-12","2025-06-13"
]

# ── Grade-based marks ranges ───────────────────────────────────
def random_marks(grade_type):
    if grade_type == "A":   return random.randint(80, 100)
    elif grade_type == "B": return random.randint(60, 79)
    elif grade_type == "C": return random.randint(40, 59)
    else:                   return random.randint(20, 39)

# ── Clear old seeded data (keep original 7 students safe) ─────
print("[INFO] Removing old seeded students (student_id > 7)...")
cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
cursor.execute("DELETE FROM attendance WHERE student_id > 7")
cursor.execute("DELETE FROM marks       WHERE student_id > 7")
cursor.execute("DELETE FROM students    WHERE student_id > 7")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
conn.commit()
print("[OK]  Old data cleared")

# ── Seed ──────────────────────────────────────────────────────
total_students  = 0
total_marks     = 0
total_attendance= 0
used_emails     = set()

for cls, (age_min, age_max) in classes.items():
    # Introduce random class size variation (e.g., between 120 and 240 students)
    class_size = random.randint(120, 240)
    print(f"\n[INFO] Inserting {class_size} students for Class {cls}...")
    count = 0

    while count < class_size:
        fname = random.choice(first_names)
        lname = random.choice(last_names)
        name  = f"{fname} {lname}"

        # Unique email
        email_base = f"{fname.lower()}.{lname.lower()}{random.randint(10,999)}"
        email = f"{email_base}@school.com"
        if email in used_emails:
            continue
        used_emails.add(email)

        phone  = f"9{random.randint(100000000, 999999999)}"
        age    = random.randint(age_min, age_max)
        adm    = f"2024-0{random.randint(1,6)}-{random.randint(1,28):02d}"
        status = "Active"

        # Insert student
        cursor.execute(
            "INSERT INTO students (name, email, phone, class, age, admission_date, status) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (name, email, phone, cls, age, adm, status)
        )
        student_id = cursor.lastrowid

        # Grade distribution: 40% A, 30% B, 20% C, 10% F
        grade_type = random.choices(["A","B","C","F"], weights=[40,30,20,10])[0]
        exam_date  = f"2025-03-{random.randint(10,25):02d}"

        for sub_id in subject_ids:
            m = random_marks(grade_type)
            
            # Introduce subject-specific variation
            if sub_id == 1:   # Maths (make it a bit tougher)
                m = max(10, m - random.randint(8, 16))
            elif sub_id == 3: # English (make it a bit easier/higher)
                m = min(100, m + random.randint(5, 12))
            elif sub_id == 2: # Science (slightly wider spread)
                m = max(0, min(100, m + random.randint(-5, 5)))
                
            cursor.execute(
                "INSERT INTO marks (student_id, subject_id, marks, exam_date) VALUES (%s,%s,%s,%s)",
                (student_id, sub_id, m, exam_date)
            )
            total_marks += 1

        # Attendance (10 days, ~80% present)
        for att_date in att_dates:
            att_status = random.choices(["Present","Absent"], weights=[80, 20])[0]
            cursor.execute(
                "INSERT INTO attendance (student_id, date, status) VALUES (%s,%s,%s)",
                (student_id, att_date, att_status)
            )
            total_attendance += 1

        count          += 1
        total_students += 1

    conn.commit()
    print(f"[OK]  Class {cls}: {class_size} students inserted")

# ── Final summary ──────────────────────────────────────────────
cursor.close()
conn.close()

print(f"""
============================================================
  SEEDING COMPLETE
============================================================
  Classes     : {len(classes)} (10A-10C, 11A-11C, 12A-12C)
  Students    : {total_students}
  Mark records: {total_marks}
  Attendance  : {total_attendance}
  Total DB rows added: {total_students + total_marks + total_attendance}
============================================================
  Now open: http://127.0.0.1:5000
============================================================
""")
