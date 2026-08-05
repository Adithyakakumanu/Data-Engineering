create database seconddemo;
use seconddemo;
#tables
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    dob DATE,
    admission_date DATE,
    department_id INT
);
INSERT INTO students (student_id, first_name, last_name, email, dob, admission_date, department_id) VALUES
(1, 'Alice', 'Johnson', 'alice.johnson@example.com', '2000-05-12', '2023-01-15', 1),
(2, 'Bob', 'Smith', 'bob.smith@example.com', '1999-07-22', '2022-12-10', 2),
(3, 'Charlie', 'Davis', 'charlie.davis@example.com', '2001-02-03', '2023-03-20', 1);
alter table students add department_name varchar(100);
update students set department_name='Electronics' where department_id=2;
CREATE TABLE faculty (
    faculty_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    department_id INT
);

INSERT INTO faculty (faculty_id, first_name, last_name, email, department_id) VALUES
(1, 'Dr. Ramesh', 'Kumar', 'ramesh.kumar@example.com', 1),
(2, 'Dr. Priya', 'Sharma', 'priya.sharma@example.com', 2),
(3, 'Dr. Vishal', 'Mehta', 'vishal.mehta@example.com', 3);
CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(100),
    department_id INT,
    credits INT
);
INSERT INTO courses (course_id, course_name, department_id, credits) VALUES
(101, 'Database Systems', 1, 4),
(102, 'Circuit Analysis', 2, 3),
(103, 'Thermodynamics', 3, 4);

CREATE TABLE enrollments (
    enrollment_id INT PRIMARY KEY,
    student_id INT,
    course_id INT,
    marks INT
);
INSERT INTO enrollments (enrollment_id, student_id, course_id, marks) VALUES
(1, 1, 101, 85),
(2, 2, 102, 78),
(3, 3, 103, 88);

CREATE TABLE exams (
    exam_id INT PRIMARY KEY,
    exam_name VARCHAR(100),
    exam_date DATE,
    course_id INT
);
INSERT INTO exams (exam_id, exam_name, exam_date, course_id) VALUES
(1, 'Midterm Exam', '2023-05-15', 101),
(2, 'Final Exam', '2023-06-10', 102),
(3, 'Final Exam', '2023-06-20', 103);


CREATE TABLE exam_marks (
    exam_id INT,
    student_id INT,
    marks INT,
    PRIMARY KEY (exam_id, student_id)
);
INSERT INTO exam_marks (exam_id, student_id, marks) VALUES
(1, 1, 85),
(2, 2, 78),
(3, 3, 88);


-- 1. Display all students
select * from students;
-- 2. Show names and emails of all faculty members
select concat(first_name, " ",last_name) as name,email from faculty;
-- 3. List all departments
select department_name from students;
-- 4. Show all subjects offered in a course
select course_name from courses;
-- 5. Show student details admitted after 2023
select * from students
where admission_date>='2023-01-01';
-- 6. Find students whose name starts with 'A'
select * from students
where first_name like 'a%';
-- 7. Display all students sorted by admission date
select * from students
order by admission_date asc;
-- 8. List students belonging to the 'Computer Science' department
select * from students 
where department_name='Computer Science';
-- 9. List subjects having credits greater than 3
select course_name from courses where credits>3;
-- 10. Find the total number of students in each department
select count(*) from students
group by department_name;
-- 11. Average marks obtained in each exam
select avg(marks),c.course_name from exam_marks e join students s on e.student_id=s.student_id join courses c on c.department_id=s.department_id
group by course_name; 
-- 12. Count of subjects per course
select count(*) from courses
group by course_name;
-- 13. Number of faculty per department
select count(*) from faculty
group by department_id;
-- 14. Show student name, course name, and department
select concat(s.first_name," ",s.last_name) as name,c.course_name,s.department_name from students s join courses c on c.department_id=s.department_id;
-- 15. Show subjects and corresponding faculty names
select c.course_name,concat(f.first_name," ",f.last_name) from courses c join faculty f on c.department_id=f.department_id;
-- 16. Display students with subjects they are enrolled in
select c.course_name as subject ,concat(s.first_name," ",s.last_name) as student_name from courses c join enrollments e on c.course_id=e.course_id join students s on s.student_id=e.student_id; 

-- 17. Show students who have not enrolled in any subject
select concat(s.first_name," ",s.last_name) as student_name from students s  left join enrollments e on s.student_id=e.student_id
where e.enrollment_id is null;

-- 18. Students having marks greater than the average of their exam
select s.*,m.marks from students s join exam_marks m on s.student_id=m.student_id
where m.marks>(select avg(marks) from exam_marks);
-- 19. Find subjects taught by ‘Dr. Ramesh’
select course_name as subject from courses c join faculty f on f.department_id=c.department_id
where f.first_name='Dr. Ramesh'; 
-- 20. List students enrolled in “Database Systems”
select concat(s.first_name," ",s.last_name) as name from students s join courses c on s.department_id=s.department_id
join enrollments e on e.course_id=c.course_id where course_name='Database Systems';
-- 21. Departments having more than 10 students

-- 22. Find exams with average marks less than 40
select exam_name from exams e join exam_marks m on e.exam_id=m.exam_id
group by exam_name
having avg(marks)<40;
-- 23. Calculate student age
select datediff(current_date(),dob)/365 as age from students;
-- 24. Display current system date
select date_format(current_date(), '%d-%m-%y');
-- 25. Display exam schedule with day of week
SELECT e.exam_name, e.exam_date, DAYNAME(e.exam_date) AS day_of_week
FROM exams e;

-- 26. Rank students based on marks in an exam
select m.student_id,concat(s.first_name," ",s.last_name) as name ,m.marks,
rank() over(order by m.marks desc) as rnk from exam_marks m join students s on m.student_id=s.student_id
order by rnk
limit 2;


-- 27. Top 3 students in each exam
select  s.first_name from students s join exam_marks m on s.student_id=m.student_id
order by m.marks desc
limit 3;
-- 28. Increase marks by 5 for all students in exam 101
update exam_marks set marks=marks+5 where exam_id=1;
-- 29. Delete enrollments older than 2020
DELETE e
FROM enrollments e
JOIN students s ON e.student_id = s.student_id
WHERE s.admission_date < '2020-01-01';

-- 30. Commit and Rollback