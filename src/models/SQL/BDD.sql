DROP DATABASE IF EXISTS stockifyDB;
CREATE DATABASE stockifyDB;

USE stockifyDB;

CREATE TABLE file (
    id INT AUTO_INCREMENT PRIMARY KEY,
    path VARCHAR(255)
);