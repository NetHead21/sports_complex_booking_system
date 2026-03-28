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
