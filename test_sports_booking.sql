-- ============================================================
-- Sports Booking - Comprehensive SQL Test Suite
-- ============================================================
-- How to use:
--   1. Run final_sql_project_sports_booking.sql first
--   2. Then run this file
--   3. Results are shown automatically at the end
-- ============================================================


USE sports_booking;

-- ============================================================
-- SECTION 1: TEST INFRASTRUCTURE
-- ============================================================


DROP TABLE IF EXISTS test_results;
CREATE TABLE test_results (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    test_group VARCHAR(100) NOT NULL,
    test_name  VARCHAR(255) NOT NULL,
    status     ENUM('PASS', 'FAIL') NOT NULL,
    message    VARCHAR(500),
    ran_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Logs a test result
DROP PROCEDURE IF EXISTS log_test;
DELIMITER $$
CREATE PROCEDURE log_test(
    IN p_group  VARCHAR(100),
    IN p_name   VARCHAR(255),
    IN p_status ENUM('PASS', 'FAIL'),
    IN p_msg    VARCHAR(500)
)
BEGIN
    INSERT INTO test_results (test_group, test_name, status, message)
    VALUES (p_group, p_name, p_status, p_msg);
END$$
DELIMITER ;


-- Assert two VARCHAR values are equal
DROP PROCEDURE IF EXISTS assert_eq;
DELIMITER $$
CREATE PROCEDURE assert_eq(
    IN p_group    VARCHAR(100),
    IN p_name     VARCHAR(255),
    IN p_expected VARCHAR(255),
    IN p_actual   VARCHAR(255)
)
BEGIN
    IF p_expected <=> p_actual THEN
        CALL log_test(p_group, p_name, 'PASS',
            CONCAT('Value = [', COALESCE(p_actual, 'NULL'), ']'));
    ELSE
        CALL log_test(p_group, p_name, 'FAIL',
            CONCAT('Expected [', COALESCE(p_expected, 'NULL'),
                   '] but got [', COALESCE(p_actual, 'NULL'), ']'));
    END IF;
END$$
DELIMITER ;


-- Assert two INT values are equal
DROP PROCEDURE IF EXISTS assert_int_eq;
DELIMITER $$
CREATE PROCEDURE assert_int_eq(
    IN p_group    VARCHAR(100),
    IN p_name     VARCHAR(255),
    IN p_expected INT,
    IN p_actual   INT
)
BEGIN
    IF p_expected <=> p_actual THEN
        CALL log_test(p_group, p_name, 'PASS',
            CONCAT('Value = ', COALESCE(p_actual, 'NULL')));
    ELSE
        CALL log_test(p_group, p_name, 'FAIL',
            CONCAT('Expected [', COALESCE(p_expected, 'NULL'),
                   '] but got [', COALESCE(p_actual, 'NULL'), ']'));
    END IF;
END$$
DELIMITER ;
