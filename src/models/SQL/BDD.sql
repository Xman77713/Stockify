DROP DATABASE IF EXISTS stockifyDB;
CREATE DATABASE stockifyDB;

USE stockifyDB;

CREATE TABLE test (
   id INT AUTO_INCREMENT PRIMARY KEY,
   username VARCHAR(50) NOT NULL,
   email VARCHAR(100) NOT NULL
);

INSERT INTO test (username, email) VALUES ('test1', 'test1@example.com');
INSERT INTO test (username, email) VALUES ('test2', 'test2@example.com');