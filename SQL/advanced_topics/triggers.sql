--Triggers:A Trigger automatically executes SQL when an event occurs on a table.

--Before Insert Trigger
CREATE TRIGGER before_student_insert
BEFORE INSERT ON students
FOR EACH ROW
BEGIN
    IF NEW.marks < 0 THEN
        SET NEW.marks = 0;
    END IF;
END;

--after insert trigger
CREATE TRIGGER after_student_insert
AFTER INSERT ON students
FOR EACH ROW
BEGIN
    INSERT INTO student_audit
    VALUES (NEW.id, 'INSERT', NOW());
END;

--BEFORE UPDATE TRIGGER
CREATE TRIGGER before_student_update
BEFORE UPDATE ON students
FOR EACH ROW
BEGIN
    IF NEW.marks > 100 THEN
        SET NEW.marks = 100;
    END IF;
END;

--AFTER UPDATE TRIGGER (TRACK CHANGES)
CREATE TRIGGER after_student_update
AFTER UPDATE ON students
FOR EACH ROW
BEGIN
    INSERT INTO student_audit
    VALUES (OLD.id, 'UPDATE', NOW());
END;

--DELETE TRIGGER

CREATE TRIGGER after_student_delete
AFTER DELETE ON students
FOR EACH ROW
BEGIN
    INSERT INTO student_audit
    VALUES (OLD.id, 'DELETE', NOW());
END;

--PREVENT DELETE USING TRIGGER
CREATE TRIGGER prevent_student_delete
BEFORE DELETE ON students
FOR EACH ROW
BEGIN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Delete not allowed';
END;

--MULTIPLE CONDITIONS IN TRIGGER
CREATE TRIGGER validate_student_marks
BEFORE INSERT ON students
FOR EACH ROW
BEGIN
    IF NEW.marks IS NULL THEN
        SET NEW.marks = 0;
    ELSEIF NEW.marks > 100 THEN
        SET NEW.marks = 100;
    END IF;
END;