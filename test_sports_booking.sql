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


-- Assert two DECIMAL values are equal
DROP PROCEDURE IF EXISTS assert_decimal_eq;
DELIMITER $$
CREATE PROCEDURE assert_decimal_eq(
    IN p_group    VARCHAR(100),
    IN p_name     VARCHAR(255),
    IN p_expected DECIMAL(10,2),
    IN p_actual   DECIMAL(10,2)
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


-- ============================================================
-- SECTION 2: CLEANUP HELPER
-- ============================================================
-- Note: seed data bookings (IDs 1-10) were inserted BEFORE triggers
-- were created, so booking_audit only contains records from test runs.

DROP PROCEDURE IF EXISTS cleanup_test_data;
DELIMITER $$
CREATE PROCEDURE cleanup_test_data()
BEGIN
    -- Remove audit records for test bookings that still exist
    DELETE FROM booking_audit
    WHERE booking_id IN (SELECT id FROM bookings WHERE member_id LIKE 'test%');
    -- Remove any orphaned audit records from test bookings that were deleted
    DELETE FROM booking_audit
    WHERE booking_id NOT IN (SELECT id FROM bookings);
    -- Remove test bookings (FK: must go before members)
    DELETE FROM bookings      WHERE member_id LIKE 'test%';
    DELETE FROM pending_terminations WHERE id LIKE 'test%';
    DELETE FROM members       WHERE id LIKE 'test%';
END$$
DELIMITER ;