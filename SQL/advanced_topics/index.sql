--Index:An Index is a database structure that speeds up data retrieval by allowing the database to find rows quickly without scanning the entire table

--SINGLE-COLUMN INDEX:Index created on one column.
CREATE INDEX idx_student_name
ON students(name);

--COMPOSITE (MULTI-COLUMN) INDEX:Index created on multiple columns together.
CREATE INDEX idx_class_marks
ON students(class, marks);

--UNIQUE INDEX:Ensures no duplicate values.
CREATE UNIQUE INDEX idx_unique_email
ON users(email);

--CLUSTERED INDEX:A clustered index defines the physical order of data in a table.
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    order_date DATE
);

--NON-CLUSTERED INDEX:Index stored separately from table data.
CREATE INDEX idx_order_date
ON orders(order_date);

--FULL-TEXT INDEX:Used for text searching.
CREATE FULLTEXT INDEX idx_content
ON articles(content);

--Drop Index
DROP INDEX idx_student_name ON students;
