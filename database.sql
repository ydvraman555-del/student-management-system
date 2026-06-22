-- ============================================================
-- STUDENT MANAGEMENT SYSTEM - database.sql
-- MySQL 8.0
-- ============================================================


-- ============================================================
-- 1. CREATE DATABASE
-- ============================================================

CREATE DATABASE IF NOT EXISTS student_db;
USE student_db;

-- Required for user-defined functions without SUPER privilege
SET GLOBAL log_bin_trust_function_creators = 1;


-- ============================================================
-- 2. DROP TABLES (FK-safe order)
-- ============================================================

DROP TABLE IF EXISTS audit_log;
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS marks;
DROP TABLE IF EXISTS subjects;
DROP TABLE IF EXISTS students;


-- ============================================================
-- 3. CREATE TABLE students
-- ============================================================

CREATE TABLE students (
    student_id     INT          PRIMARY KEY AUTO_INCREMENT,
    name           VARCHAR(100) NOT NULL,
    email          VARCHAR(100) UNIQUE,
    phone          VARCHAR(15),
    class          VARCHAR(10)  NOT NULL,
    age            INT          CHECK (age >= 5 AND age <= 30),
    admission_date DATE         DEFAULT (CURRENT_DATE),
    status         VARCHAR(10)  DEFAULT 'Active'
);


-- ============================================================
-- 4. CREATE TABLE subjects
-- ============================================================

CREATE TABLE subjects (
    subject_id   INT         PRIMARY KEY AUTO_INCREMENT,
    subject_name VARCHAR(50) UNIQUE NOT NULL,
    max_marks    INT         DEFAULT 100
);


-- ============================================================
-- 5. CREATE TABLE marks
-- ============================================================

CREATE TABLE marks (
    mark_id    INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    marks      INT CHECK (marks >= 0 AND marks <= 100),
    exam_date  DATE DEFAULT (CURRENT_DATE),
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE
);


-- ============================================================
-- 6. CREATE TABLE attendance
-- ============================================================

CREATE TABLE attendance (
    attend_id  INT        PRIMARY KEY AUTO_INCREMENT,
    student_id INT        NOT NULL,
    date       DATE       DEFAULT (CURRENT_DATE),
    status     VARCHAR(10) CHECK (status IN ('Present', 'Absent')),
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);


-- ============================================================
-- 7. CREATE TABLE audit_log
-- ============================================================

CREATE TABLE audit_log (
    log_id     INT          PRIMARY KEY AUTO_INCREMENT,
    action     VARCHAR(100),
    student_id INT,
    log_time   DATETIME     DEFAULT NOW(),
    details    TEXT
);


-- ============================================================
-- 8. CREATE INDEXES
-- ============================================================

CREATE INDEX idx_student_name  ON students(name);
CREATE INDEX idx_marks_student ON marks(student_id);


-- ============================================================
-- 9. INSERT INTO students
-- ============================================================

INSERT INTO students (name, email, phone, class, age, admission_date, status) VALUES
('Aarav Sharma', 'aarav@mail.com', '9876543210', '10A', 15, '2024-06-01', 'Active'),
('Diya Patel',   'diya@mail.com',  '9876543211', '10A', 14, '2024-06-01', 'Active'),
('Kartik Verma',  'kartik@mail.com', '9876543212', '10B', 16, '2024-06-01', 'Active'),
('Priya Singh',  'priya@mail.com', '9876543213', '10A', 15, '2024-06-01', 'Active'),
('Karan Kumar',  'karan@mail.com', '9876543214', '10B', 16, '2024-06-01', 'Active'),
('Neha Gupta',   'neha@mail.com',  '9876543215', '10C', 14, '2024-06-01', 'Active'),
('Arjun Reddy',  'arjun@mail.com', '9876543216', '10C', 15, '2024-06-01', 'Active');


-- ============================================================
-- 10. INSERT INTO subjects
-- ============================================================

INSERT INTO subjects (subject_name, max_marks) VALUES
('Maths',   100),
('Science', 100),
('English', 100),
('Hindi',   100);


-- ============================================================
-- 11. INSERT INTO marks
-- ============================================================

INSERT INTO marks (student_id, subject_id, marks, exam_date) VALUES
-- Aarav Sharma
(1, 1, 85, '2025-03-10'), (1, 2, 78, '2025-03-11'), (1, 3, 90, '2025-03-12'), (1, 4, 88, '2025-03-13'),
-- Diya Patel
(2, 1, 92, '2025-03-10'), (2, 2, 89, '2025-03-11'), (2, 3, 95, '2025-03-12'), (2, 4, 91, '2025-03-13'),
-- Rohan Verma
(3, 1, 55, '2025-03-10'), (3, 2, 60, '2025-03-11'), (3, 3, 65, '2025-03-12'), (3, 4, 58, '2025-03-13'),
-- Priya Singh
(4, 1, 75, '2025-03-10'), (4, 2, 80, '2025-03-11'), (4, 3, 70, '2025-03-12'), (4, 4, 72, '2025-03-13'),
-- Karan Kumar
(5, 1, 40, '2025-03-10'), (5, 2, 45, '2025-03-11'), (5, 3, 50, '2025-03-12'), (5, 4, 42, '2025-03-13'),
-- Neha Gupta
(6, 1, 88, '2025-03-10'), (6, 2, 92, '2025-03-11'), (6, 3, 85, '2025-03-12'), (6, 4, 90, '2025-03-13'),
-- Arjun Reddy
(7, 1, 65, '2025-03-10'), (7, 2, 70, '2025-03-11'), (7, 3, 68, '2025-03-12'), (7, 4, 72, '2025-03-13');


-- ============================================================
-- 12. INSERT INTO attendance
-- ============================================================

INSERT INTO attendance (student_id, date, status) VALUES
-- Aarav Sharma
(1, '2025-06-02', 'Present'), (1, '2025-06-03', 'Present'), (1, '2025-06-04', 'Absent'),
(1, '2025-06-05', 'Present'), (1, '2025-06-06', 'Present'),
-- Diya Patel
(2, '2025-06-02', 'Present'), (2, '2025-06-03', 'Present'), (2, '2025-06-04', 'Present'),
(2, '2025-06-05', 'Absent'),  (2, '2025-06-06', 'Present'),
-- Rohan Verma
(3, '2025-06-02', 'Absent'),  (3, '2025-06-03', 'Present'), (3, '2025-06-04', 'Absent'),
(3, '2025-06-05', 'Present'), (3, '2025-06-06', 'Absent'),
-- Priya Singh
(4, '2025-06-02', 'Present'), (4, '2025-06-03', 'Absent'),  (4, '2025-06-04', 'Present'),
(4, '2025-06-05', 'Present'), (4, '2025-06-06', 'Present'),
-- Karan Kumar
(5, '2025-06-02', 'Absent'),  (5, '2025-06-03', 'Absent'),  (5, '2025-06-04', 'Present'),
(5, '2025-06-05', 'Absent'),  (5, '2025-06-06', 'Present'),
-- Neha Gupta
(6, '2025-06-02', 'Present'), (6, '2025-06-03', 'Present'), (6, '2025-06-04', 'Present'),
(6, '2025-06-05', 'Present'), (6, '2025-06-06', 'Absent'),
-- Arjun Reddy
(7, '2025-06-02', 'Present'), (7, '2025-06-03', 'Absent'),  (7, '2025-06-04', 'Present'),
(7, '2025-06-05', 'Present'), (7, '2025-06-06', 'Present');


-- ============================================================
-- 13. TRIGGER trg_after_student_insert
-- ============================================================

DROP TRIGGER IF EXISTS trg_after_student_insert;

DELIMITER //
CREATE TRIGGER trg_after_student_insert
AFTER INSERT ON students
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (action, student_id, log_time, details)
    VALUES (
        'NEW STUDENT ADDED',
        NEW.student_id,
        NOW(),
        CONCAT('Name: ', NEW.name, ' | Email: ', NEW.email, ' | Class: ', NEW.class)
    );
END//
DELIMITER ;


-- ============================================================
-- 14. TRIGGER trg_after_student_delete
-- ============================================================

DROP TRIGGER IF EXISTS trg_after_student_delete;

DELIMITER //
CREATE TRIGGER trg_after_student_delete
AFTER DELETE ON students
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (action, student_id, log_time, details)
    VALUES (
        'STUDENT DELETED',
        OLD.student_id,
        NOW(),
        CONCAT('Name: ', OLD.name, ' | Email: ', OLD.email, ' | Class: ', OLD.class)
    );
END//
DELIMITER ;


-- ============================================================
-- 15. TRIGGER trg_before_marks_update
-- ============================================================

DROP TRIGGER IF EXISTS trg_before_marks_update;

DELIMITER //
CREATE TRIGGER trg_before_marks_update
BEFORE UPDATE ON marks
FOR EACH ROW
BEGIN
    IF NEW.marks < 0   THEN SET NEW.marks = 0;   END IF;
    IF NEW.marks > 100 THEN SET NEW.marks = 100;  END IF;
END//
DELIMITER ;


-- ============================================================
-- 16. PROCEDURE sp_add_student
-- ============================================================

DROP PROCEDURE IF EXISTS sp_add_student;

DELIMITER //
CREATE PROCEDURE sp_add_student (
    IN p_name  VARCHAR(100),
    IN p_email VARCHAR(100),
    IN p_phone VARCHAR(15),
    IN p_class VARCHAR(10),
    IN p_age   INT
)
BEGIN
    INSERT INTO students (name, email, phone, class, age)
    VALUES (p_name, p_email, p_phone, p_class, p_age);
END//
DELIMITER ;


-- ============================================================
-- 17. PROCEDURE sp_student_total_marks
-- ============================================================

DROP PROCEDURE IF EXISTS sp_student_total_marks;

DELIMITER //
CREATE PROCEDURE sp_student_total_marks (
    IN p_student_id INT
)
BEGIN
    SELECT
        s.name,
        SUM(m.marks) AS total_marks
    FROM students s
    JOIN marks m ON s.student_id = m.student_id
    WHERE s.student_id = p_student_id
    GROUP BY s.name;
END//
DELIMITER ;


-- ============================================================
-- 18. FUNCTION fn_get_grade
-- ============================================================

DROP FUNCTION IF EXISTS fn_get_grade;

DELIMITER //
CREATE FUNCTION fn_get_grade (p_marks INT)
RETURNS VARCHAR(15)
DETERMINISTIC
BEGIN
    IF p_marks >= 80 THEN RETURN 'Excellent';
    ELSEIF p_marks >= 60 THEN RETURN 'Good';
    ELSEIF p_marks >= 40 THEN RETURN 'Average';
    ELSE RETURN 'Fail';
    END IF;
END//
DELIMITER ;


-- ============================================================
-- 19. VIEW vw_student_performance
-- ============================================================

CREATE OR REPLACE VIEW vw_student_performance AS
SELECT
    s.student_id,
    s.name,
    s.class,
    SUM(m.marks)                        AS total_marks,
    ROUND(AVG(m.marks), 2)              AS avg_marks,
    fn_get_grade(ROUND(AVG(m.marks), 2)) AS grade
FROM students s
JOIN marks m ON s.student_id = m.student_id
GROUP BY s.student_id, s.name, s.class;


-- ============================================================
-- 20. VIEW vw_attendance_summary
-- ============================================================

CREATE OR REPLACE VIEW vw_attendance_summary AS
SELECT
    s.student_id,
    s.name,
    COUNT(CASE WHEN a.status = 'Present' THEN 1 END) AS total_present,
    COUNT(CASE WHEN a.status = 'Absent'  THEN 1 END) AS total_absent
FROM students s
LEFT JOIN attendance a ON s.student_id = a.student_id
GROUP BY s.student_id, s.name;
