-- Fix: Drop and recreate sp_add_student with correct 5 parameters
USE student_db;

DROP PROCEDURE IF EXISTS sp_add_student;
DROP PROCEDURE IF EXISTS sp_student_total_marks;

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

CREATE PROCEDURE sp_student_total_marks (
    IN p_student_id INT
)
BEGIN
    SELECT s.name, SUM(m.marks) AS total_marks
    FROM students s
    JOIN marks m ON s.student_id = m.student_id
    WHERE s.student_id = p_student_id
    GROUP BY s.name;
END//

DELIMITER ;

-- Verify
SHOW PROCEDURE STATUS WHERE Db = 'student_db';
