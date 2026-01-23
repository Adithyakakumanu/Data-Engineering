CREATE DATABASE firstdemo;
USE firstdemo;

CREATE TABLE customer (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    mail VARCHAR(50),
    phonenumber VARCHAR(20),
    address VARCHAR(200)
);

-- Insert sample data
INSERT INTO customer (id, name, mail, phonenumber, address) VALUES
(1, 'Adithya', 'adithya1@gmail.com', '9502681630', 'Hyderabad'),
(2, 'Raj', 'raj@example.com', '9502681640', 'Mumbai'),
(3, 'Pramod', 'pramod@example.com', '9502681650', 'Delhi'),
(4, 'Sandy', 'sandy@example.com', '9502681660', 'Kolkata'),
(5, 'Pankaj', 'pankaj@example.com', '9502681670', 'Bangalore');

select * from customer;


-- Calculate the average price of all the movies
CREATE TABLE movies (
    movie_id INT PRIMARY KEY,
    title VARCHAR(100),
    type VARCHAR(50),
    price FLOAT
);
alter table movies
add issue_date date;
alter table movies add return_date date;

-- Insert sample movie data
INSERT INTO movies (movie_id, title, type, price, issue_date, return_date) 
VALUES 
(1, 'LOVE', 'Romance', 100.00, '2023-07-15', '2023-08-15'),
(2, 'ROBOT', 'Action', 150.00, '2023-06-20', '2023-07-20'),
(3, 'COMEDY CENTRAL', 'Comedy', 120.00, '2023-07-10', '2023-08-10'),
(4, 'THRILLER NIGHT', 'Thriller', 180.00, '2023-07-05', '2023-08-05'),
(5, 'HOLIDAY FUN', 'Comedy', 130.00, '2023-07-12', '2023-08-12');


select * from movies;

CREATE TABLE INVOICE (
    inv_no int PRIMARY KEY,
    id INT,
    movie_id INT,
    issue_date DATE,
    return_date DATE,
    price DECIMAL(10, 2),
    FOREIGN KEY (id) REFERENCES customer(id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
);

INSERT INTO INVOICE (inv_no, id, movie_id, issue_date, return_date, price) 
VALUES
(1, 1, 1, '2023-07-15', '2023-08-15', 100.00),
(2, 2, 2, '2023-06-20', '2023-07-20', 150.00),
(3, 3, 3, '2023-07-10', '2023-08-10', 120.00),
(4, 4, 4, '2023-07-05', '2023-08-05', 180.00),
(5, 5, 5, '2023-07-12', '2023-08-12', 130.00);
select * from invoice;

-- Count separately the number of movies in the ‘comedy’ and ‘thriller’ type

select type,count(*) from movies
where type="Comedy" or type="Thriller"
group by type;
-- Find the customer’s name and area with cust_id ‘A05’
select name,address from customer
where id ='5';
-- Change the area of cust_id ‘a03’ to ‘vs’
update customer set address="vs" where id=3;
-- Retrieve the list of fname & the area of all the customers
select name,address from customer; #select substring_index(name,' ',1) as fnmae from customer;
-- Count the number of movies having price greater than equal to 150
select count(*),type from movies
where price>=150;
-- Find the number of movies in each type
select count(*),type from movies
group by type;
-- Find the names and movie number of all the customers who has been issued movies
SELECT 
    c.name AS customer_name, 
    i.movie_id AS movie_number
FROM 
    INVOICE i
JOIN 
    customer c ON i.id = c.id
JOIN 
    movies m ON i.movie_id = m.movie_id;

-- Change the issue date of cust_date of cust_id ‘a01’ to 24/07/93
-- Find the names of all customers
select name from customer;
-- Count the total numbers of customers
select count(*) from customer;
-- Count the average price for each movie type that has a maximum price of 150
select avg(price) as ap,type,count(*) from movies
where price>=150
group by type;
-- Display the movie number and day on which customers were issued movies
select i.movie_id as movienumber,m.issue_date from invoice as i join movies as m
on i.issue_date=m.issue_date;
-- Change the telephone number of ‘Pramod’ to 466389
update customer set phonenumber=466389 where name='pramod';
-- List the various movie types available from the movie table
select type from movies;
-- Calculate the total price of all the movies
select sum(price) from movies;
-- Print the type and average price of each movie
select type ,avg(price) as avg from movies
group by type;
-- Find out the movie number which has been issued to ‘Issued’

-- Change the price of ‘LOVE’ movie to Rs.250.00
update movies set price='250' where title="LOVE";
-- Find the lname of all customers that begin with ‘P’
select name from customer
where name like 'p%';
-- Calculate the average price of all movies where type is ‘comedy’ or ‘thriller and price greater than equal to 150
select avg(price),type as av from movies
where type='comedy' or type='thriller' and price>=150
group by type;
-- Find out the title and type of the movies that have been issued to Sandy
select m.title,m.type from movies as m join invoice i on m.movie_id=i.movie_id join customer c on c.id=i.id
where name='sandy';
-- Delete the record with invoice number ‘i08’ from INVOICE table
delete from invoice where inv_no=8;
-- Find the list of all customers who stay in area ‘DA’ or area ‘MU’ or area ‘GH’
select * from customer
where address='MU' or address='GH' or address='DA';
-- Determine the maximum and minimum movie price
select max(price),min(price) from movies;
-- Find the number of movies in each type
select count(*),type from movies
group by type;
-- Find the names of customers who have been issued movie of type ‘comedy’
-- Delete all the records having return date between 10th July 93
delete from invoice where return_date between '1993-07-10' AND '1993-07-15';
-- Find out which customers have been issued movie number ‘M09’
select c.* from customer c join invoice i on c.id=i.id join movies m on m.movie_id=i.movie_id
where m.movie_id='9';
-- Change the return date of invoice number ‘i07 to 16-08-93
update invoice set return_date='16-08-93' where inv_no=7;
-- Calculate the square root of the price of each movie
select price*price from movies;
-- Find the name of the movies issued to ‘Raj’ and ‘Prashant’
select title from movies m join invoice i on m.movie_id=i.movie_id join customer c on c.id=i.id
where name='raj' and name='prashant';
-- Change the issue date of cust_date of cust_id ‘a01’ to 22/07/93

-- Find the name of all customers having ‘a’ as the second letter in their fname
select * from customer
where name like '_a%';

-- Print the Title and average price of each movie
select title,avg(price) from movies
group by title;
-- Find the lname and fname that have been issued movie
-- Change the price of ‘robot’ to Rs.280.00
update movies set price='280' where title='robot';
-- Find out the customers who stay in areas whose second letter is ‘M’
select * from customer
where address like '_M%';
-- Count the average price for each type that has a maximum price of 190
select avg(price) from movies
group by type
having max(price)=190;
-- Find the movie whose price is greater than 100 and less than or equal to 180
select * from movies
where price>100 and price<=180;
-- Count the average price for each type that has a maximum price of 150
select avg(price),type from movies
where price>150
group by type;
-- Find out if the movie starring ‘LOVE’ is issued to any customer and print the cust_id to whom it is issued
SELECT 
    i.id AS cust_id
FROM 
    INVOICE i
JOIN 
    movies m ON i.movie_id = m.movie_id
WHERE 
    m.title = 'LOVE'; 
-- Find the movie of type ‘action’ and ‘comedy’
select * from movies
where type='action' and type='comedy';
-- Calculate the average price of all movies where type is ‘comedy’ or ‘thriller’ and price greater than equal to 100
select avg(price) from movies
where type="comedy" or type="thriller" and price>=100;
-- Find all customers name and phone numbers that have been issue movie before the month of August
select name,phonenumber from customer c join invoice i on c.id=i.id join movies m on m.movie_id=i.movie_id
where m.issue_date<'2023-8-01';
-- Change the area of cust_id ‘a01’ to ’jk’
update customer set address='jk' where id=1;
-- Find the movie whose price is greater than 170.
select * from movies
where price>170;
-- Find the number of movies in each type
select count(*),type from movies
group by type;
-- Delete the record with invoice number ‘i07’ from INVOICE table
delete from invoice where inv_no=9; 
-- Divide the cost of movie ‘robot’ by difference between its price and 100
select (price-100)/price from movies
where title='robot';
-- Print the type and average price of each movie
select type,avg(price) from movies

group by type;
-- List the movie number and movie names issued to all customers
select m.title as moviename,m.movie_id as movienumber from movies m join invoice i on i.movie_id=i.movie_id join customer c on c.id=i.id
;
-- List the movie in the sorted order of their title
select * from movies
order by title asc;
-- Calculate the total price of all the movies
select sum(price) from movies;
-- Find the number of movies in each type
select count(*),type from movies
group by type;
-- Change the telephone number of ‘Ravi’ to 789546
update customer set phonenumber=789546 where name='ravi';
-- Print information from INVOICE table of customer who have been issued movie
select i.* from invoice i join customer c on i.id=c.id;
-- Calculate the average price of all the movies
select avg(price) from movies;
-- Count separately the number of movies in the ‘Romance’ and ‘Suspence’ type
select count(*),type from movies
where type="romance" or type="suspence"
group by type;
/*SELECT type, COUNT(*) AS movie_count
FROM movies
WHERE type = 'Romance'
GROUP BY type
UNION
SELECT 'Suspence' AS type, 0 AS movie_count
FROM dual
WHERE NOT EXISTS (SELECT 1 FROM movies WHERE type = 'Suspence');*/

-- Change the return date of invoice number ‘i07’ to 28-FEB-20
update invoice set return_date='2000-02-28' where inv_no=3;
-- List the movie in the descending sorted order of their title
select * from movies
order by type desc;
-- Count the total number of customers
select count(*) from customer;
-- Display Return date of movie
select return_date from movies;
-- Delete all the record having return date before 14-MAR-20
delete from movies where return_date<'2000-04-14';
-- Display the INVOICE table information for cust_id ‘A01’and ‘A02’
select i.* from invoice i join customer c on i.id=c.id
where c.id='1' or c.id='2';
-- Count the average price for each type that has a maximum price of 140
select avg(price),type from movies
group by type
having max(price)=140;
-- Display the cust_id and issue_date
select c.id,issue_date from invoice i join customer c on c.id=i.id;
-- Print the name and types of all the movies accept action movies
select title,type from movies
where type!='action';
-- Count the number of movies having price greater than equal to 190
select count(*) from movies
where price>=190;

-- Count the average price for each type that has a maximum price of 250
select avg(price),type from movies
where price>=250
group by type;
-- List the movie_no and inv_no of customers having mv_no less than ‘M05’ 
select m.movie_id as movie_no,inv_no from movies m join invoice i on m.movie_id=i.movie_id
where m.movie_id<5;
-- Calculate the average price of all movies where type is ‘Action’ or ‘thriller’ and price greater than equal to 100
select avg(price) from movies
where type='action' or type='thriller' and price>=100;
-- Display the issue_date in the format dd-mm-yy
select date_format(issue_date, '%d-%m-%y') as formated from invoice; #tochar(issuedate,'DD-MM-YY'),format(issue_date,'dd-mm-yy')
-- Select the title,cust_id,and mv_no for all the movies that are issued
select title,i.id as cust_id,m.movie_id as mv_no from movies m join invoice i on m.movie_id=i.movie_id;
-- Find out if the movie starring ‘Tom Cruise’ is issued to any customer and print the cust_id to whom it is issued
SELECT i.id AS cust_id
FROM INVOICE i
JOIN movies m ON i.movie_id = m.movie_id
WHERE m.title LIKE '%Tom Cruise%';

-- Find the date 15 days after the current date
select date_add(current_date(), interval 15 day) as date; 
select date