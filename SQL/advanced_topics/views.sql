--see that students table have to be there and created
--views:It is a virtual table created from a SELECT query that stores logic, not data.
CREATE VIEW class6_students AS
SELECT id, name, marks
FROM students
WHERE class = 6;

select * from class6_students;

--Alter table
ALTER VIEW class6_students AS
SELECT id, name
FROM students
WHERE class = 6;

--drop table
DROP VIEW IF EXISTS class6_students;

--Materialized View:A Materialized View stores actual data, not just logic.

CREATE MATERIALIZED VIEW class_summary AS
SELECT class, COUNT(*) total
FROM students
GROUP BY class;

REFRESH MATERIALIZED VIEW class_summary;


