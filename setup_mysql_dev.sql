CREATE DATABASE IF NOT EXISTS shoppers_db;
CREATE USER
    IF NOT EXISTS 'Shoppers'@'localhost';
    IDENTIFIED BY 'shoppers1996';
GRANT ALL PRIVILEGES
    ON Shoppers_db.*
    TO 'Shoppers'@'localhost';
GRANT SELECT
    ON performance_schema.*
    TO 'Shoppers'@'localhost';
FLUSH PRIVILEGES;
