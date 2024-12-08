DROP DATABASE IF EXISTS stockifyDB;
CREATE DATABASE stockifyDB;

USE stockifyDB;

CREATE TABLE file (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    iv BLOB,
    data LONGBLOB
);

-- pour lancer le script
-- mysql -h stockifydb-stockifydb1.f.aivencloud.com -P 17500 -u avnadmin -p --ssl-mode=REQUIRED
-- password
-- source C:/projet_crypto/Stockify/src/models/SQL/BDD.sql;