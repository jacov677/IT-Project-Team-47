-- Run once as the MySQL root user to create the database and a least-privilege
-- application account (Phase 4, sections 4.4.8 and 4.5).
--   mysql -u root -p < docs/mysql_setup.sql
-- Change the password, then put the same password in your .env file (DB_PASSWORD).

CREATE DATABASE IF NOT EXISTS wil_placement
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'wil_app'@'localhost' IDENTIFIED BY 'change-this-password';

-- Only what Django needs to run and migrate the one project database. No global rights.
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX, DROP, REFERENCES
  ON wil_placement.* TO 'wil_app'@'localhost';

-- Django's test runner creates and drops a separate test_wil_placement database.
GRANT ALL PRIVILEGES ON test_wil_placement.* TO 'wil_app'@'localhost';

FLUSH PRIVILEGES;
