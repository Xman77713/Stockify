DROP DATABASE IF EXISTS stockifyDB;
CREATE DATABASE stockifyDB;

USE stockifyDB;

CREATE TABLE file (
    id INT AUTO_INCREMENT PRIMARY KEY,
    path VARCHAR(255),
    name VARCHAR(255),
    extension VARCHAR(16)
);

-- pour lancer le script
-- mysql -h stockifydb-stockifydb1.f.aivencloud.com -P 17500 -u avnadmin -p --ssl-mode=REQUIRED
-- password
-- source C:/projet_crypto/Stockify/src/models/SQL/BDD.sql;