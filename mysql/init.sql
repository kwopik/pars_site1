-- init.sql

USE mydatabase;

CREATE TABLE IF NOT EXISTS osnova (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price VARCHAR(50) NOT NULL
);
