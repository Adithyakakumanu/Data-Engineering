--Transactions:A Transaction is a sequence of SQL operations that are executed as a single logical unit, meaning all succeed or all fail.

CREATE TABLE accounts (
    account_id INT PRIMARY KEY,
    balance INT
);

START TRANSACTION;
UPDATE accounts SET balance = balance - 1000 WHERE account_id = 1;
UPDATE accounts SET balance = balance + 1000 WHERE account_id = 2;
COMMIT;

--ROLLBACK TRANSACTION:Undo all changes since transaction start.
START TRANSACTION;
UPDATE accounts SET balance = balance - 500 WHERE account_id = 1;
ROLLBACK;

--SAVEPOINTS:A Savepoint allows partial rollback inside a transaction.
START TRANSACTION;
UPDATE accounts SET balance = balance - 500 WHERE account_id = 1;
SAVEPOINT sp1;
UPDATE accounts SET balance = balance + 500 WHERE account_id = 2;
ROLLBACK TO sp1;
COMMIT;