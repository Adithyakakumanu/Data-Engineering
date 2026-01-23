create database thirddemo;
use thirddemo;
CREATE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL,
    location VARCHAR(100)
);
INSERT INTO departments (dept_id, dept_name, location) VALUES
(10, 'HR', 'New York'),
(20, 'IT', 'Bangalore'),
(30, 'Finance', 'London'),
(40, 'Marketing', 'Los Angeles'),
(50, 'Engineering', 'San Francisco');

CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(100) NOT NULL,
    salary DECIMAL(10,2),
    hire_date DATE,
    job_title VARCHAR(100),
    dept_id INT,
    manager_id INT,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id),
    FOREIGN KEY (manager_id) REFERENCES employees(emp_id)
);
INSERT INTO employees (emp_id, emp_name, salary, hire_date, job_title, dept_id, manager_id) VALUES
(1, 'John Doe', 90000, '2018-05-01', 'Manager', 10, NULL),
(2, 'Mary Jones', 75000, '2019-07-15', 'Developer', 20, 1),
(3, 'Sam Smith', 85000, '2020-01-20', 'Developer', 30, 1),
(4, 'Jane Lee', 60000, '2021-09-10', 'HR Specialist', 10, 1),
(5, 'Robert Brown', 120000, '2017-11-30', 'Director', 40, NULL),
(6, 'Lucy White', 95000, '2019-02-25', 'Developer', 50, 5),
(7, 'David Black', 70000, '2020-06-12', 'HR Specialist', 10, 1),
(8, 'Peter Green', 110000, '2020-03-01', 'Manager', 20, NULL),
(9, 'Emily Clarke', 92000, '2021-08-23', 'Developer', 30, 8),
(10, 'Nina Black', 67000, '2021-05-14', 'Developer', 50, 5);

CREATE TABLE projects (
    project_id INT PRIMARY KEY,
    project_name VARCHAR(100),
    dept_id INT,
    budget DECIMAL(12,2),
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);
INSERT INTO projects (project_id, project_name, dept_id, budget) VALUES
(1, 'HR System Upgrade', 10, 50000),
(2, 'Cloud Migration', 20, 200000),
(3, 'Financial Forecasting', 30, 150000),
(4, 'Brand Strategy', 40, 80000),
(5, 'New Website Launch', 50, 100000);



-- Find the total number of employees.
select count(*) from employees;
-- Find the total and average salary per department.
select dept_id,sum(salary),avg(salary) from employees 
group by dept_id;
-- Find the highest and lowest salary in the company.
select max(salary),min(salary) from employees;
-- Display departments having more than 2 employees.
select d.* from departments as d join employees as e on d.dept_id=e.dept_id
group by e.dept_id
having count(e.dept_id)>2;
-- Count employees hired each year.
select year(hire_date),count(*) from employees
group by year(hire_date);
-- Find total budget allocated per department from the projects table.
select sum(budget),dept_id from projects
group by dept_id;
-- Display average salary by job title.
select avg(salary),job_title from employees
group by job_title;
-- Find the department with the maximum average salary.
select dept_name from departments  d join employees  e on d.dept_id=e.dept_id
where salary=(select max(salary) from employees);
-- Find employees earning more than department average salary (subquery).  
select dept_name,d.dept_id,salary from departments  d join employees  e on d.dept_id=e.dept_id
where e.salary=(select avg(e2.salary) from employees e2 where e2.dept_id=e.dept_id);
-- Display the percentage contribution of each employee’s salary to department total.select dept_id 
select e.dept_id,(e.salary/sum(e.salary))*100 as percent from employees e
group by e.dept_id;
SELECT e.dept_id,e.emp_name, e.salary, (e.salary / dept_total.total_salary) * 100 AS salary_percentage
FROM employees e JOIN (SELECT dept_id, SUM(salary) AS total_salary FROM employees GROUP BY dept_id) dept_total 
ON e.dept_id = dept_total.dept_id
ORDER BY e.dept_id, e.emp_name;

-- Display employee name, department name, and location.
select e.emp_name,d.dept_name,location from employees e join departments d on d.dept_id=e.dept_id;
-- List all projects with their corresponding department names.
select project_name,dept_name from projects p join departments d on p.dept_id=d.dept_id;
-- Show all employees along with their manager names (self join).
select e.emp_name,e1.emp_name as managername,e.dept_id from employees e left join employees e1 on e1.emp_id=e.manager_id;
-- Display department names with number of employees.
select count(*),dept_name from employees e join departments d on d.dept_id=e.dept_id
group by dept_name;
-- List employees working in ‘Finance’ department.
select emp_name from employees e join departments d on e.dept_id=d.dept_id
where dept_name='finance';
-- Display employees earning between 50,000 and 80,000.
select * from employees where salary>50000 and salary<80000;
-- Show employees who belong to either HR or IT department.
select emp_name from employees e join departments d on e.dept_id=d.dept_id
where dept_name='hr' or dept_name='it';
-- Display employees whose name ends with ‘a’.
select * from employees
where emp_name like'%a';
-- Show employees hired in 2020.
select * from employees
where year(hire_date)=2020;
-- Display employees whose salary is not between 55,000 and 75,000.
select * from employees 
where salary<55000 or salary>75000;
-- Show all employees from departments 10 and 30.
select * from employees
where dept_id=10 or dept_id=30;
-- Display the top 3 highest-paid employees.
select * from employees
order by salary desc
limit 3;
-- Find employees whose salary is greater than the average salary.
select * from employees where salary>(select avg(salary) from employees);
-- Show the department of employee ‘Mary Jones’.
select d.dept_name from departments d join employees e on e.dept_id=d.dept_id
where emp_name='Mary Jones';

-- Display the length of each employee’s name.
select emp_name,length(emp_name) from employees;
-- Display all employee details.
select * from employees;
-- Show employee names and their salaries.
select emp_name,salary from employees;
-- List employees hired after 2018.
select * from employees
where year(hire_date)>2018;
-- Display employees whose job title is ‘Developer’.
select * from employees 
where job_title='Developer';
-- Show all departments located in ‘Bangalore’.
select * from departments
where location='Bangalore';
-- List employees sorted by salary in descending order.
select * from employees
order by salary desc;
-- Display distinct job titles in the organization.
select distinct job_title from employees;
-- Show names and annual salaries of all employees.
select emp_name,salary*12 as annual_salary from employees;
-- Display employees who have no manager (manager_id IS NULL).
select * from employees
where manager_id is not null;
-- Find employees whose name starts with ‘N’.
select * from employees
where emp_name like 'n%';