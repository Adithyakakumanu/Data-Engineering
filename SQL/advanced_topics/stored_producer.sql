--Stored Producers:A Stored Procedure is a precompiled set of SQL statements stored in the database and executed as a single unit.

CREATE PROCEDURE procedure_name ()
BEGIN
    -- SQL statements
END;

--SIMPLE STORED PROCEDURE (NO PARAMETERS)
CREATE PROCEDURE get_all_students()
BEGIN
    SELECT * FROM students;
END;

--Call Procedure
CALL get_all_students();

--STORED PROCEDURE WITH INPUT PARAMETERS:To pass values into procedure dynamically.
CREATE PROCEDURE get_students_by_class(
    IN class_no INT
)
BEGIN
    SELECT id, name, marks
    FROM students
    WHERE class = class_no;
END;

--Call Procedure
CALL get_students_by_class(6);

--STORED PROCEDURE WITH OUTPUT PARAMETERS:To return values from procedure.
CREATE PROCEDURE get_student_count(
    IN class_no INT,
    OUT total_students INT
)
BEGIN
    SELECT COUNT(*)
    INTO total_students
    FROM students
    WHERE class = class_no;
END;

--Call Procedure
CALL get_student_count(6, @count);
SELECT @count;

--IN, OUT, INOUT PARAMETERS
CREATE PROCEDURE increment_value(
    INOUT num INT
)
BEGIN
    SET num = num + 1;
END;

--Call
SET @n = 10;
CALL increment_value(@n);
SELECT @n;

--STORED PROCEDURE WITH CONDITIONS (IF / ELSE)
CREATE PROCEDURE check_result(
    IN marks INT
)
BEGIN
    IF marks >= 40 THEN
        SELECT 'PASS' AS result;
    ELSE
        SELECT 'FAIL' AS result;
    END IF;
END;

--STORED PROCEDURE WITH LOOPS
CREATE PROCEDURE print_numbers()
BEGIN
    DECLARE i INT DEFAULT 1;
    WHILE i <= 5 DO
        SELECT i;
        SET i = i + 1;
    END WHILE;
END;

CREATE PROCEDURE loop_example()
BEGIN
    DECLARE counter INT DEFAULT 1;

    simple_loop: LOOP
        SELECT counter;
        SET counter = counter + 1;
        IF counter > 5 THEN
            LEAVE simple_loop;
        END IF;
    END LOOP;
END;

--STORED PROCEDURE WITH TRANSACTIONS

CREATE PROCEDURE transfer_marks()
BEGIN
    START TRANSACTION;
    UPDATE students SET marks = marks - 5 WHERE id = 1;
    UPDATE students SET marks = marks + 5 WHERE id = 2;
    COMMIT;
END;

--ERROR HANDLING IN STORED PROCEDURES:Handle runtime errors safely.
CREATE PROCEDURE safe_insert()
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;
    INSERT INTO students VALUES (10, 'Test', 6, 80);
    COMMIT;
END;