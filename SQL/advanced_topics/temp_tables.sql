--Temp Table:A Temporary Table is a table that stores temporary data for a session or transaction and is automatically deleted after use.

CREATE TEMPORARY TABLE temp_students (
    id INT,
    name VARCHAR(50),
    marks INT
);

--Insert Direct values
INSERT INTO temp_students VALUES (1, 'Ram', 85);

--Insert from SELECT
INSERT INTO temp_students
SELECT id, name, marks
FROM students
WHERE class = 6;

--temp table with aggregation 
CREATE TEMPORARY TABLE class_summary AS
SELECT class, COUNT(*) AS total_students
FROM students
GROUP BY class;
