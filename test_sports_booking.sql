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


-- Run cleanup before tests to ensure a clean slate
CALL cleanup_test_data();


-- ============================================================
-- SECTION 3: insert_new_member
-- ============================================================

-- 3.1 Insert a valid new member creates the row
CALL insert_new_member('test_ins1', 'ValidPass1!', 'test_ins1@example.com');
CALL assert_int_eq('insert_new_member', '3.1 Valid insert - member row created',
    1, (SELECT COUNT(*) FROM members WHERE id = 'test_ins1'));


-- 3.2 Duplicate member ID raises an error
DROP PROCEDURE IF EXISTS _t;
DELIMITER $$
CREATE PROCEDURE _t()
BEGIN
    DECLARE v_err INT DEFAULT 0;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET v_err = 1;
    CALL insert_new_member('test_ins1', 'AnotherPass', 'other_ins@example.com');
    CALL assert_int_eq('insert_new_member', '3.2 Duplicate ID raises error', 1, v_err);
END$$
DELIMITER ;
CALL _t();
DROP PROCEDURE IF EXISTS _t;


-- 3.3 Member ID shorter than 3 characters raises a constraint error
DROP PROCEDURE IF EXISTS _t;
DELIMITER $$
CREATE PROCEDURE _t()
BEGIN
    DECLARE v_err INT DEFAULT 0;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET v_err = 1;
    CALL insert_new_member('ab', 'ValidPass1!', 'shortid@example.com');
    CALL assert_int_eq('insert_new_member', '3.3 ID shorter than 3 chars raises error', 1, v_err);
END$$
DELIMITER ;
CALL _t();
DROP PROCEDURE IF EXISTS _t;


-- 3.4 Invalid email format raises a constraint error
DROP PROCEDURE IF EXISTS _t;
DELIMITER $$
CREATE PROCEDURE _t()
BEGIN
    DECLARE v_err INT DEFAULT 0;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET v_err = 1;
    CALL insert_new_member('test_ins2', 'ValidPass1!', 'not-a-valid-email');
    CALL assert_int_eq('insert_new_member', '3.4 Invalid email format raises error', 1, v_err);
END$$
DELIMITER ;
CALL _t();
DROP PROCEDURE IF EXISTS _t;


-- ============================================================
-- SECTION 4: delete_member
-- ============================================================

-- Setup
CALL insert_new_member('test_del1', 'Pass123!', 'test_del1@example.com');


-- 4.1 Delete existing member removes the row
CALL delete_member('test_del1');
CALL assert_int_eq('delete_member', '4.1 Delete existing member - row removed',
    0, (SELECT COUNT(*) FROM members WHERE id = 'test_del1'));


-- 4.2 Delete a non-existent member raises an error
DROP PROCEDURE IF EXISTS _t;
DELIMITER $$
CREATE PROCEDURE _t()
BEGIN
    DECLARE v_err INT DEFAULT 0;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET v_err = 1;
    CALL delete_member('test_nobody');
    CALL assert_int_eq('delete_member', '4.2 Delete non-existent member raises error', 1, v_err);
END$$
DELIMITER ;
CALL _t();
DROP PROCEDURE IF EXISTS _t;


-- ============================================================
-- SECTION 5: update_member_password
-- ============================================================

-- Setup
CALL insert_new_member('test_pwd1', 'OldPass1!', 'test_pwd1@example.com');


-- 5.1 Update password of an existing member
CALL update_member_password('test_pwd1', 'NewPass2!');
CALL assert_eq('update_member_password', '5.1 Password updated successfully',
    'NewPass2!', (SELECT password FROM members WHERE id = 'test_pwd1'));


-- 5.2 Update password of a non-existent member raises an error
DROP PROCEDURE IF EXISTS _t;
DELIMITER $$
CREATE PROCEDURE _t()
BEGIN
    DECLARE v_err INT DEFAULT 0;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET v_err = 1;
    CALL update_member_password('test_nobody', 'SomePass1!');
    CALL assert_int_eq('update_member_password', '5.2 Non-existent member raises error', 1, v_err);
END$$
DELIMITER ;
CALL _t();
DROP PROCEDURE IF EXISTS _t;


-- ============================================================
-- SECTION 6: update_member_email
-- ============================================================

-- Setup
CALL insert_new_member('test_eml1', 'Pass123!', 'test_eml1@example.com');


-- 6.1 Update email of an existing member
CALL update_member_email('test_eml1', 'updated_eml1@example.com');
CALL assert_eq('update_member_email', '6.1 Email updated successfully',
    'updated_eml1@example.com', (SELECT email FROM members WHERE id = 'test_eml1'));


-- 6.2 Update email of a non-existent member raises an error
DROP PROCEDURE IF EXISTS _t;
DELIMITER $$
CREATE PROCEDURE _t()
BEGIN
    DECLARE v_err INT DEFAULT 0;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET v_err = 1;
    CALL update_member_email('test_nobody', 'new@example.com');
    CALL assert_int_eq('update_member_email', '6.2 Non-existent member raises error', 1, v_err);
END$$
DELIMITER ;
CALL _t();
DROP PROCEDURE IF EXISTS _t;


-- 6.3 Update to an invalid email format raises a constraint error
DROP PROCEDURE IF EXISTS _t;
DELIMITER $$
CREATE PROCEDURE _t()
BEGIN
    DECLARE v_err INT DEFAULT 0;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET v_err = 1;
    CALL update_member_email('test_eml1', 'not-a-valid-email');
    CALL assert_int_eq('update_member_email', '6.3 Invalid email format raises error', 1, v_err);
END$$

DELIMITER ;
CALL _t();
DROP PROCEDURE IF EXISTS _t;


-- ============================================================
-- SECTION 7: make_booking
-- ============================================================

-- Setup
CALL insert_new_member('test_bk1', 'Pass123!', 'test_bk1@example.com');


-- 7.1 Valid booking returns SUCCESS
CALL make_booking('B2', '2030-06-01', '09:00:00', 'test_bk1', @bk_id, @bk_status, @bk_msg);
CALL assert_eq('make_booking', '7.1 Valid booking returns SUCCESS', 'SUCCESS', @bk_status);


-- 7.2 Valid booking increases member payment_due by the room price
CALL assert_decimal_eq('make_booking', '7.2 payment_due increases by room price (8.00)',
    8.00, (SELECT payment_due FROM members WHERE id = 'test_bk1'));


-- 7.3 Booking the same room/date/time again returns CONFLICT
CALL make_booking('B2', '2030-06-01', '09:00:00', 'test_bk1', @bk_id, @bk_status, @bk_msg);
CALL assert_eq('make_booking', '7.3 Duplicate room/date/time returns CONFLICT', 'CONFLICT', @bk_status);


-- 7.4 Non-existent room ID returns ROOM_NOT_FOUND
CALL make_booking('ZZZ', '2030-06-02', '10:00:00', 'test_bk1', @bk_id, @bk_status, @bk_msg);
CALL assert_eq('make_booking', '7.4 Invalid room ID returns ROOM_NOT_FOUND', 'ROOM_NOT_FOUND', @bk_status);


-- 7.5 Non-existent member returns MEMBER_NOT_FOUND
CALL make_booking('B2', '2030-06-03', '10:00:00', 'test_nobody', @bk_id, @bk_status, @bk_msg);
CALL assert_eq('make_booking', '7.5 Non-existent member returns MEMBER_NOT_FOUND', 'MEMBER_NOT_FOUND', @bk_status);


-- 7.6 Booking a past date returns INVALID_DATE
CALL make_booking('B2', '2000-01-01', '10:00:00', 'test_bk1', @bk_id, @bk_status, @bk_msg);
CALL assert_eq('make_booking', '7.6 Past date returns INVALID_DATE', 'INVALID_DATE', @bk_status);


-- ============================================================
-- SECTION 8: update_payment
-- ============================================================

-- Setup: member with one booking
CALL insert_new_member('test_pay1', 'Pass123!', 'test_pay1@example.com');
CALL make_booking('T1', '2030-07-01', '09:00:00', 'test_pay1', @pay_bk_id, @s, @m);


-- 8.1 Valid payment returns SUCCESS
CALL update_payment(@pay_bk_id, @pay_status, @pay_msg);
CALL assert_eq('update_payment', '8.1 Valid payment returns SUCCESS', 'SUCCESS', @pay_status);


-- 8.2 Paying a booking reduces member payment_due to 0
CALL assert_decimal_eq('update_payment', '8.2 Payment reduces member payment_due to 0',
    0.00, (SELECT payment_due FROM members WHERE id = 'test_pay1'));


-- 8.3 Paying an already-paid booking returns ALREADY_PAID
CALL update_payment(@pay_bk_id, @pay_status, @pay_msg);
CALL assert_eq('update_payment', '8.3 Already paid booking returns ALREADY_PAID', 'ALREADY_PAID', @pay_status);


-- 8.4 Non-existent booking ID returns NOT_FOUND
CALL update_payment(999999, @pay_status, @pay_msg);
CALL assert_eq('update_payment', '8.4 Non-existent booking returns NOT_FOUND', 'NOT_FOUND', @pay_status);


-- 8.5 Paying a cancelled booking returns CANCELLED
CALL make_booking('T2', '2030-07-02', '10:00:00', 'test_pay1', @pay_bk_id2, @s, @m);
CALL cancel_booking(@pay_bk_id2, @cm);
CALL update_payment(@pay_bk_id2, @pay_status, @pay_msg);
CALL assert_eq('update_payment', '8.5 Cancelled booking returns CANCELLED status', 'CANCELLED', @pay_status);



-- ============================================================
-- SECTION 9: view_bookings
-- ============================================================

-- test_pay1 already has bookings from section 8


-- 9.1 Existing active member returns SUCCESS
CALL view_bookings('test_pay1', @vb_status, @vb_msg);
CALL assert_eq('view_bookings', '9.1 Existing member returns SUCCESS', 'SUCCESS', @vb_status);


-- 9.2 Non-existent member returns MEMBER_NOT_FOUND
CALL view_bookings('test_nobody', @vb_status, @vb_msg);
CALL assert_eq('view_bookings', '9.2 Non-existent member returns MEMBER_NOT_FOUND', 'MEMBER_NOT_FOUND', @vb_status);


-- ============================================================
-- SECTION 10: search_room
-- ============================================================


-- 10.1 Valid search with available rooms returns SUCCESS
CALL search_room('Tennis Court', '2030-08-01', '09:00:00', @sr_status, @sr_msg);
CALL assert_eq('search_room', '10.1 Available rooms found returns SUCCESS', 'SUCCESS', @sr_status);


-- 10.2 Past date returns INVALID_DATE
CALL search_room('Tennis Court', '2000-01-01', '09:00:00', @sr_status, @sr_msg);
CALL assert_eq('search_room', '10.2 Past date returns INVALID_DATE', 'INVALID_DATE', @sr_status);


-- 10.3 When all rooms of a type are booked returns NO_ROOMS
-- Setup: book both Tennis Courts at the same slot
CALL insert_new_member('test_sr1', 'Pass123!', 'test_sr1@example.com');
CALL make_booking('T1', '2030-08-10', '14:00:00', 'test_sr1', @sr_id1, @s, @m);
CALL make_booking('T2', '2030-08-10', '14:00:00', 'test_sr1', @sr_id2, @s, @m);
CALL search_room('Tennis Court', '2030-08-10', '14:00:00', @sr_status, @sr_msg);
CALL assert_eq('search_room', '10.3 All rooms of type booked returns NO_ROOMS', 'NO_ROOMS', @sr_status);


-- 10.4 When only one of two rooms is booked, still returns SUCCESS (other is available)
CALL make_booking('T1', '2030-08-11', '14:00:00', 'test_sr1', @sr_id3, @s, @m);
CALL search_room('Tennis Court', '2030-08-11', '14:00:00', @sr_status, @sr_msg);
CALL assert_eq('search_room', '10.4 Partial availability still returns SUCCESS', 'SUCCESS', @sr_status);


-- ============================================================
-- SECTION 11: cancel_booking
-- ============================================================


-- Setup: member with a future booking
CALL insert_new_member('test_can1', 'Pass123!', 'test_can1@example.com');
CALL make_booking('AR', '2030-09-01', '10:00:00', 'test_can1', @can_bk_id1, @s, @m);


-- 11.1 Valid cancellation returns success message
CALL cancel_booking(@can_bk_id1, @can_msg);
CALL assert_eq('cancel_booking', '11.1 Valid cancellation returns success message',
    'Booking Cancelled', @can_msg);


-- 11.2 Cancelled booking status is set to CANCELLED
CALL assert_eq('cancel_booking', '11.2 Booking status set to CANCELLED',
    'CANCELLED', (SELECT payment_status FROM bookings WHERE id = @can_bk_id1));


-- 11.3 Cancelling an already-cancelled booking returns appropriate message
CALL cancel_booking(@can_bk_id1, @can_msg);
CALL assert_eq('cancel_booking', '11.3 Re-cancelling returns already cancelled message',
    'Booking has already been cancelled or paid', @can_msg);


-- 11.4 Cancelling an already-paid booking returns appropriate message
CALL insert_new_member('test_can2', 'Pass123!', 'test_can2@example.com');
CALL make_booking('AR', '2030-09-02', '10:00:00', 'test_can2', @can_bk_id2, @s, @m);
CALL update_payment(@can_bk_id2, @s, @m);
CALL cancel_booking(@can_bk_id2, @can_msg);
CALL assert_eq('cancel_booking', '11.4 Cancelling paid booking returns appropriate message',
    'Booking has already been cancelled or paid', @can_msg);


-- 11.5 Cancellation reduces member payment_due by the room price (no fine on 1st cancel)
CALL insert_new_member('test_can3', 'Pass123!', 'test_can3@example.com');
CALL make_booking('B1', '2030-09-03', '10:00:00', 'test_can3', @can_bk_id3, @s, @m);
-- payment_due is now 8.00; after cancel with no fine it should be 0.00
CALL cancel_booking(@can_bk_id3, @can_msg);
CALL assert_decimal_eq('cancel_booking', '11.5 Cancellation reduces payment_due (no fine on 1st)',
    0.00, (SELECT payment_due FROM members WHERE id = 'test_can3'));


-- 11.6 Cancelling a booking on the booked date itself returns appropriate message
-- (make_booking allows today; cancel_booking blocks cancellation on/after the date)
CALL insert_new_member('test_can4', 'Pass123!', 'test_can4@example.com');
CALL make_booking('MPF1', CURDATE(), '08:00:00', 'test_can4', @can_bk_id4, @s, @m);
CALL cancel_booking(@can_bk_id4, @can_msg);
CALL assert_eq('cancel_booking', '11.6 Cancel on booked date returns appropriate message',
    'Cancellation cannot be done on/after the booked date', @can_msg);


-- ============================================================
-- SECTION 12: Consecutive Cancellation Fine
--             (cancel_booking + check_cancellation function)
-- ============================================================
-- Direct inserts are used here to control datetime_of_booking ordering,
-- which determines what check_cancellation counts as "consecutive".
-- The function reads bookings DESC by datetime_of_booking and counts
-- consecutive CANCELLED statuses from the most recent outward.


CALL insert_new_member('test_fine', 'Pass123!', 'test_fine@example.com');
UPDATE members SET payment_due = 30.00 WHERE id = 'test_fine';


INSERT INTO bookings (room_id, booked_date, booked_time, member_id, datetime_of_booking, payment_status, total_amount)
VALUES
    ('T1', '2030-10-01', '09:00:00', 'test_fine', '2030-01-01 10:00:00', 'UNPAID', 10.00),
    ('T1', '2030-10-02', '09:00:00', 'test_fine', '2030-01-01 11:00:00', 'UNPAID', 10.00),
    ('T1', '2030-10-03', '09:00:00', 'test_fine', '2030-01-01 12:00:00', 'UNPAID', 10.00);


-- Grab each booking ID
SET @fine_bk1 = (SELECT id FROM bookings WHERE member_id = 'test_fine' AND booked_date = '2030-10-01');
SET @fine_bk2 = (SELECT id FROM bookings WHERE member_id = 'test_fine' AND booked_date = '2030-10-02');
SET @fine_bk3 = (SELECT id FROM bookings WHERE member_id = 'test_fine' AND booked_date = '2030-10-03');



-- 12.1 1st consecutive cancellation: no fine (cancel most recent booking first)
-- check_cancellation sees: bk3(CANCELLED), bk2(UNPAID) → stops → count = 1 → no fine
CALL cancel_booking(@fine_bk3, @can_msg);
CALL assert_decimal_eq('check_cancellation', '12.1 1st cancellation: no fine, payment_due = 20.00',
    20.00, (SELECT payment_due FROM members WHERE id = 'test_fine'));


-- 12.2 2nd consecutive cancellation: still no fine
-- check_cancellation sees: bk3(CANCELLED), bk2(CANCELLED), bk1(UNPAID) → count = 2 → no fine
CALL cancel_booking(@fine_bk2, @can_msg);
CALL assert_decimal_eq('check_cancellation', '12.2 2nd cancellation: no fine, payment_due = 10.00',
    10.00, (SELECT payment_due FROM members WHERE id = 'test_fine'));


-- 12.3 3rd consecutive cancellation: $10 fine is applied
-- check_cancellation sees: bk3(CANCELLED), bk2(CANCELLED), bk1(CANCELLED) → count = 3 → FINE!
-- payment_due: 10.00 - 10.00 (cancel) + 10.00 (fine) = 10.00
CALL cancel_booking(@fine_bk1, @can_msg);
CALL assert_decimal_eq('check_cancellation', '12.3 3rd cancellation: $10 fine applied, payment_due = 10.00',
    10.00, (SELECT payment_due FROM members WHERE id = 'test_fine'));


-- 12.4 check_cancellation resets the count when a non-cancelled booking is encountered
-- Booking history (DESC by datetime): 12:00=CANCELLED, 11:00=PAID, 10:00=CANCELLED
-- Expected count = 1 (stops at PAID)
CALL insert_new_member('test_chk1', 'Pass123!', 'test_chk1@example.com');
INSERT INTO bookings (room_id, booked_date, booked_time, member_id, datetime_of_booking, payment_status, total_amount)
VALUES
    ('T2', '2030-11-01', '09:00:00', 'test_chk1', '2030-01-01 10:00:00', 'CANCELLED', 10.00),
    ('T2', '2030-11-02', '09:00:00', 'test_chk1', '2030-01-01 11:00:00', 'PAID',      10.00),
    ('T2', '2030-11-03', '09:00:00', 'test_chk1', '2030-01-01 12:00:00', 'CANCELLED', 10.00);



SET @chk_bk = (SELECT id FROM bookings WHERE member_id = 'test_chk1' AND booked_date = '2030-11-03');
CALL assert_int_eq('check_cancellation', '12.4 Non-consecutive cancellations: count resets at non-cancelled',
    1, check_cancellation(@chk_bk));


-- ============================================================
-- SECTION 13: payment_check TRIGGER
-- ============================================================


-- 13.1 Deleting a member with payment_due > 0 inserts a row into pending_terminations
CALL insert_new_member('test_trg1', 'Pass123!', 'test_trg1@example.com');
UPDATE members SET payment_due = 15.00 WHERE id = 'test_trg1';
CALL delete_member('test_trg1');
CALL assert_int_eq('payment_check trigger',
    '13.1 Member with payment_due > 0 added to pending_terminations',
    1, (SELECT COUNT(*) FROM pending_terminations WHERE id = 'test_trg1'));
DELETE FROM pending_terminations WHERE id = 'test_trg1';


-- 13.2 Deleting a member with payment_due = 0 does NOT insert into pending_terminations
CALL insert_new_member('test_trg2', 'Pass123!', 'test_trg2@example.com');
-- payment_due defaults to 0.00
CALL delete_member('test_trg2');
CALL assert_int_eq('payment_check trigger',
    '13.2 Member with payment_due = 0 not added to pending_terminations',
    0, (SELECT COUNT(*) FROM pending_terminations WHERE id = 'test_trg2'));


-- ============================================================
-- SECTION 14: booking_audit TRIGGERS
-- ============================================================

-- Setup
CALL insert_new_member('test_aud1', 'Pass123!', 'test_aud1@example.com');


-- 14.1 INSERT trigger: making a new booking creates an INSERT audit record
CALL make_booking('B1', '2030-12-01', '09:00:00', 'test_aud1', @aud_bk_id, @s, @m);
CALL assert_int_eq('booking_audit triggers',
    '14.1 INSERT trigger: new booking creates INSERT audit record',
    1, (SELECT COUNT(*) FROM booking_audit
        WHERE booking_id = @aud_bk_id AND action = 'INSERT'));


-- 14.2 UPDATE trigger: updating a booking creates an UPDATE audit record
UPDATE bookings SET notes = 'test update' WHERE id = @aud_bk_id;
CALL assert_int_eq('booking_audit triggers',
    '14.2 UPDATE trigger: booking update creates UPDATE audit record',
    1, (SELECT COUNT(*) FROM booking_audit
        WHERE booking_id = @aud_bk_id AND action = 'UPDATE'));


-- 14.3 CANCEL detection: cancelling a booking creates a CANCEL audit record (not UPDATE)
CALL cancel_booking(@aud_bk_id, @can_msg);
CALL assert_int_eq('booking_audit triggers',
    '14.3 Cancel detection: cancellation creates CANCEL audit record',
    1, (SELECT COUNT(*) FROM booking_audit
        WHERE booking_id = @aud_bk_id AND action = 'CANCEL'));


-- 14.4 DELETE trigger: deleting a booking creates a DELETE audit record
SET @del_bk_id = @aud_bk_id;
DELETE FROM bookings WHERE id = @del_bk_id;
CALL assert_int_eq('booking_audit triggers',
    '14.4 DELETE trigger: deleting a booking creates DELETE audit record',
    1, (SELECT COUNT(*) FROM booking_audit
        WHERE booking_id = @del_bk_id AND action = 'DELETE'));



-- ============================================================
-- SECTION 15: RESULTS & CLEANUP
-- ============================================================

-- Full results
SELECT
    id,
    test_group,
    test_name,
    status,
    message
FROM test_results
ORDER BY id;


-- Summary
SELECT
    COUNT(*)                                                  AS total_tests,
    SUM(status = 'PASS')                                      AS passed,
    SUM(status = 'FAIL')                                      AS failed,
    CONCAT(ROUND(SUM(status = 'PASS') / COUNT(*) * 100, 1), '%') AS pass_rate
FROM test_results;


-- Cleanup all test data
CALL cleanup_test_data();
DELETE FROM pending_terminations WHERE id LIKE 'test%';


-- Cleanup test infrastructure
DROP PROCEDURE IF EXISTS log_test;
DROP PROCEDURE IF EXISTS assert_eq;
DROP PROCEDURE IF EXISTS assert_int_eq;
DROP PROCEDURE IF EXISTS assert_decimal_eq;
DROP PROCEDURE IF EXISTS cleanup_test_data;
-- Keep test_results so you can review results after running:
--   SELECT * FROM test_results ORDER BY id;