DROP DATABASE IF EXISTS stockifyDB;
CREATE DATABASE stockifyDB;

USE stockifyDB;

CREATE TABLE file (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    iv BLOB NOT NULL,
    data LONGBLOB NOT NULL,
    uniqueLink boolean NOT NULL,
    expirationDate DATETIME NOT NULL,
    salt BLOB NOT NULL,
    token TEXT NOT NULL,
    file_size INTEGER
);