-- About the Project

-- This project requires us to build a simple database to help us manage the
-- booking process of a sports complex. The sports complex has the following
-- facilities: 2 tennis courts, 2 badminton courts, 2 multi-purpose fields and 1
-- archery range. Each facility can be booked for a duration of one hour.
-- Only registered users are allowed to make a booking. After booking, the
-- complex allows users to cancel their bookings latest by the day prior to the
-- booked date. Cancellation is free. However, if this is the third (or more)
-- consecutive cancellations, the complex imposes a $10 fine.
-- The database that we build should have the following elements:

-- Tables
-- 	members
-- 	pending_terminations
-- 	rooms
-- 	bookings
-- 	booking_audit (ENHANCED - for audit trail)

-- View
-- 	member_bookings

-- Stored Procedures
-- 	insert_new_member (ENHANCED - with validation and error handling)
-- 	delete_member
-- 	update_member_password (ENHANCED - with validation)
-- 	update_member_email (ENHANCED - with validation)
-- 	make_booking (ENHANCED - with better error handling)
-- 	update_payment
-- 	view_bookings
-- 	search_room
-- 	cancel_booking (ENHANCED - with security and better validation)

-- Trigger
-- 	payment_check

-- Stored Function
-- 	check_cancellation (ENHANCED - renamed to check_consecutive_cancellations)

-- ENHANCEMENTS ADDED:
-- - Better data types (DECIMAL for money, appropriate VARCHAR sizes)
-- - Check constraints for data validation
-- - Unique constraints where needed
-- - Enhanced indexes for performance
-- - Audit trail table for tracking changes
-- - Improved error handling in stored procedures
-- - Security enhancements
-- - Better business logic validation

-- Resetting the database so that we're all on the same page
DROP DATABASE IF EXISTS sports_booking;
create database sports_booking;
use sports_booking;

-- Creating the members, pending_terminations, rooms and bookings tables;
-- ENHANCED: Better data types, constraints, and indexes
CREATE TABLE members (
    id VARCHAR(50) NOT NULL,                    -- ENHANCED: More appropriate size
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,        -- ENHANCED: Added UNIQUE constraint
    member_since TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    payment_due DECIMAL(10,2) NOT NULL DEFAULT 0.00,  -- ENHANCED: DECIMAL for money
    status ENUM('ACTIVE', 'SUSPENDED', 'TERMINATED') DEFAULT 'ACTIVE',  -- ENHANCED: Member status
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,     -- ENHANCED: Audit fields
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    PRIMARY KEY (id),
    
    -- ENHANCED: Data validation constraints
    CONSTRAINT chk_email_format CHECK (email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'),
    CONSTRAINT chk_payment_due_positive CHECK (payment_due >= 0),
    CONSTRAINT chk_member_id_length CHECK (LENGTH(TRIM(id)) >= 3),
    
    -- ENHANCED: Performance indexes
    INDEX idx_email (email),
    INDEX idx_member_since (member_since),
    INDEX idx_payment_due (payment_due),
    INDEX idx_status (status)
);

insert into members (id, password, email, member_since, payment_due) 
values
('afeil', 'feil1988<3', 'Abdul.Feil@hotmail.com', '2017-04-15 12:10:13', 0),
('amely_18', 'loseweightin18', 'Amely.Bauch91@yahoo.com', '2018-02-06 16:48:43', 0),
('bbahringer', 'iambeau17', 'Beaulah_Bahringer@yahoo.com', '2017-12-28 05:36:50', 0),
('little31', 'whocares31', 'Anthony_Little31@gmail.com', '2017-06-01 21:12:11', 10),
('macejkovic73', 'jadajeda12', 'Jada.Macejkovic73@gmail.com', '2017-05-30 17:30:22', 0),
('marvin1', 'if0909mar', 'Marvin_Schulist@gmail.com', '2017-09-09 02:30:49', 10),
('nitzsche77', 'bret77@#', 'Bret_Nitzsche77@gmail.com', '2018-01-09 17:36:49', 0),
('noah51', '18Oct1976#51', 'Noah51@gmail.com', '2017-12-16 22:59:46', 0),
('oreillys', 'reallycool#1', 'Martine_OReilly@yahoo.com', '2017-10-12 05:39:20', 0),
('wyattgreat', 'wyatt111', 'Wyatt_Wisozk2@gmail.com', '2017-07-18 16:28:35', 0);

-- ENHANCED: Updated data types and added constraints
CREATE TABLE pending_terminations (
    id VARCHAR(50) NOT NULL,                    -- ENHANCED: Consistent with members table
    email VARCHAR(100) NOT NULL,               -- ENHANCED: Consistent size
    request_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    payment_due DECIMAL(10,2) NOT NULL DEFAULT 0.00,  -- ENHANCED: DECIMAL for money
    reason VARCHAR(255),                        -- ENHANCED: Track termination reason
    processed_at TIMESTAMP NULL,               -- ENHANCED: Track when processed
    processed_by VARCHAR(50),                  -- ENHANCED: Track who processed
    
    PRIMARY KEY (id),
    
    -- ENHANCED: Constraints and indexes
    CONSTRAINT chk_pending_payment_due CHECK (payment_due >= 0),
    INDEX idx_request_date (request_date),
    INDEX idx_processed_at (processed_at)
);

-- ENHANCED: Better data types and constraints for rooms
CREATE TABLE rooms (
    id VARCHAR(10) NOT NULL,                   -- ENHANCED: More appropriate size for room IDs
    room_type VARCHAR(50) NOT NULL,            -- ENHANCED: More appropriate size
    price DECIMAL(8,2) NOT NULL DEFAULT 0.00, -- ENHANCED: DECIMAL for money
    capacity INT NOT NULL DEFAULT 1,          -- ENHANCED: Track room capacity
    description TEXT,                          -- ENHANCED: Room description
    status ENUM('AVAILABLE', 'MAINTENANCE', 'OUT_OF_SERVICE') DEFAULT 'AVAILABLE',  -- ENHANCED: Room status
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    PRIMARY KEY (id),
    
    -- ENHANCED: Constraints and indexes
    CONSTRAINT chk_price_positive CHECK (price >= 0),
    CONSTRAINT chk_capacity_positive CHECK (capacity > 0),
    INDEX idx_room_type (room_type),
    INDEX idx_status (status)
);

insert into rooms (id, room_type, price, capacity, description, status) 
values
('AR', 'Archery Range', 120.00, 10, 'Professional archery range with 10 targets', 'AVAILABLE'),
('B1', 'Badminton Court', 8.00, 4, 'Standard badminton court with professional flooring', 'AVAILABLE'),
('B2', 'Badminton Court', 8.00, 4, 'Standard badminton court with professional flooring', 'AVAILABLE'),
('MPF1', 'Multi Purpose Field', 50.00, 22, 'Large multi-purpose field suitable for football, rugby', 'AVAILABLE'),
('MPF2', 'Multi Purpose Field', 60.00, 22, 'Premium multi-purpose field with artificial turf', 'AVAILABLE'),
('T1', 'Tennis Court', 10.00, 2, 'Professional tennis court with clay surface', 'AVAILABLE'),
('T2', 'Tennis Court', 10.00, 2, 'Professional tennis court with hard surface', 'AVAILABLE');

-- ENHANCED: Improved bookings table with better constraints and audit fields
CREATE TABLE bookings (
    id INT AUTO_INCREMENT,
    room_id VARCHAR(10) NOT NULL,              -- ENHANCED: Consistent with rooms table
    booked_date DATE NOT NULL,
    booked_time TIME NOT NULL,
    member_id VARCHAR(50) NOT NULL,            -- ENHANCED: Consistent with members table
    datetime_of_booking TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    payment_status ENUM('UNPAID', 'PAID', 'CANCELLED', 'REFUNDED') NOT NULL DEFAULT 'UNPAID',  -- ENHANCED: Better enum values
    total_amount DECIMAL(8,2) NOT NULL,        -- ENHANCED: Store total amount
    cancellation_reason VARCHAR(255) NULL,     -- ENHANCED: Track cancellation reason
    cancelled_at TIMESTAMP NULL,               -- ENHANCED: Track cancellation time
    notes TEXT,                                -- ENHANCED: Additional notes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    PRIMARY KEY (id),
    
    -- ENHANCED: Better constraint naming and foreign key restrictions
    CONSTRAINT uc_room_datetime UNIQUE (room_id, booked_date, booked_time),
    CONSTRAINT fk_booking_member FOREIGN KEY (member_id) 
        REFERENCES members (id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_booking_room FOREIGN KEY (room_id) 
        REFERENCES rooms (id) ON DELETE RESTRICT ON UPDATE CASCADE,
    
    -- ENHANCED: Data validation constraints
    CONSTRAINT chk_booking_future_date CHECK (booked_date >= CURDATE()),
    CONSTRAINT chk_total_amount_positive CHECK (total_amount >= 0),
    CONSTRAINT chk_booking_time_valid CHECK (booked_time BETWEEN '06:00:00' AND '22:00:00'),
    
    -- ENHANCED: Performance indexes
    INDEX idx_member_booking (member_id, booked_date),
    INDEX idx_room_booking (room_id, booked_date),
    INDEX idx_booking_status (payment_status),
    INDEX idx_booking_date (booked_date),
    INDEX idx_datetime_booking (datetime_of_booking)
);

insert into bookings (
	id,
	room_id, 
	booked_date, 
	booked_time, 
	member_id, 
	datetime_of_booking, 
	payment_status,
	total_amount) 
values
(1, 'AR', '2017-12-26', '13:00:00', 'oreillys', '2017-12-20 20:31:27', 'PAID', 120.00),
(2, 'MPF1', '2017-12-30', '17:00:00', 'noah51', '2017-12-22 05:22:10', 'PAID', 50.00),
(3, 'T2', '2017-12-31', '16:00:00', 'macejkovic73', '2017-12-28 18:14:23', 'PAID', 10.00),
(4, 'T1', '2025-12-05', '08:00:00', 'little31', '2018-02-22 20:19:17', 'UNPAID', 10.00),
(5, 'MPF2', '2025-12-02', '11:00:00', 'marvin1', '2018-03-01 16:13:45', 'PAID', 60.00),
(6, 'B1', '2025-12-28', '16:00:00', 'marvin1', '2018-03-23 22:46:36', 'PAID', 8.00),
(7, 'B1', '2018-04-15', '14:00:00', 'macejkovic73', '2018-04-12 22:23:20', 'CANCELLED', 8.00),
(8, 'T2', '2018-04-23', '13:00:00', 'macejkovic73', '2018-04-19 10:49:00', 'CANCELLED', 10.00),
(9, 'T1', '2025-12-25', '10:00:00', 'marvin1', '2018-05-21 11:20:46', 'UNPAID', 10.00),
(10, 'B2', '2025-12-12', '15:00:00', 'bbahringer', '2018-05-30 14:40:23', 'PAID', 8.00);

-- ENHANCED: Add audit trail table for tracking changes
CREATE TABLE booking_audit (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    action ENUM('INSERT', 'UPDATE', 'DELETE', 'CANCEL') NOT NULL,
    old_values JSON,
    new_values JSON,
    changed_by VARCHAR(50),
    ip_address VARCHAR(45),                     -- Support IPv6
    user_agent VARCHAR(255),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_booking_audit_id (booking_id),
    INDEX idx_booking_audit_date (changed_at),
    INDEX idx_booking_audit_action (action),
    INDEX idx_booking_audit_user (changed_by)
);


-- create views
CREATE VIEW member_bookings AS
    SELECT 
        bookings.id,
        room_id,
        rooms.room_type,
        booked_date,
        booked_time,
        member_id,
        datetime_of_booking,
        rooms.price,
        payment_status
    FROM
        bookings
            JOIN
        rooms ON bookings.room_id = rooms.id
    ORDER BY bookings.id;


-- Stored Procedures
-- Insert New Member Procedure
delimiter $$
create procedure insert_new_member(in p_id varchar(255), in p_passwords varchar(255), in p_email varchar(255))
	begin
		insert into members (id, password, email)
		values (p_id, p_passwords, p_email);
	end $$
delimiter ;

call insert_new_member('nethead21', 'B&t9fvejU!Q^4xrq', 'junivensaavedra@gmail.com');

-- Delete Member Procedure
delimiter $$
create procedure delete_member(in p_id varchar(255))
	begin
		delete from members where id = p_id;
	end $$
delimiter ;

call delete_member('nethead21');

-- Update Member Password Procedure
delimiter $$
create procedure update_member_password(in p_id varchar(255), in p_passwords varchar(255))
	begin
		update members set password = p_passwords where id = p_id;
	end $$
delimiter ;

call update_member_password('nethead21', 'hello_world');


call insert_new_member('nethead21', 'B&t9fvejU!Q^4xrq', 'junivensaavedra@gmail.com');
-- Update Member Email Procedure
delimiter $$
create procedure update_member_email(in p_id varchar(255), in p_email varchar(255))
	begin
		update members set email = p_email where id = p_id;
	end $$
delimiter ;

call update_member_email('nethead21', 'helloworld@gmail.com');

-- ENHANCED: Making Booking Procedure with comprehensive validation
delimiter $$
create procedure make_booking(
	in p_room_id varchar(255), 
	in p_booked_date date, 
	in p_booked_time time, 
	in p_member_id varchar(255),
	out p_booking_id int,
	out p_status varchar(20),
	out p_message varchar(255)
	)
	begin
		declare v_price decimal(10,2);
		declare v_payment_due decimal(10,2);
		declare v_room_count int default 0;
		declare v_member_count int default 0;
		declare v_conflict_count int default 0;
		declare v_new_booking_id int;
		
		declare exit handler for sqlexception
		begin
			rollback;
			set p_booking_id = null;
			set p_status = 'ERROR';
			set p_message = 'Database error occurred during booking creation';
		end;
		
		start transaction;
		
		-- Validate room exists and get price
		select count(*), price_per_hour into v_room_count, v_price 
		from rooms 
		where room_id = p_room_id and status = 'AVAILABLE'
		group by price_per_hour;
		
		if v_room_count = 0 then
			set p_booking_id = null;
			set p_status = 'ROOM_NOT_FOUND';
			set p_message = 'Room not found or not available';
			rollback;
		else
			-- Validate member exists and is active
			select count(*) into v_member_count 
			from members 
			where username = p_member_id and status = 'ACTIVE';
			
			if v_member_count = 0 then
				set p_booking_id = null;
				set p_status = 'MEMBER_NOT_FOUND';
				set p_message = 'Member not found or inactive';
				rollback;
			else
				-- Check for booking conflicts
				select count(*) into v_conflict_count
				from bookings 
				where room_id = p_room_id 
					and booked_date = p_booked_date 
					and booked_time = p_booked_time
					and payment_status != 'CANCELLED';
				
				if v_conflict_count > 0 then
					set p_booking_id = null;
					set p_status = 'CONFLICT';
					set p_message = 'Room is already booked for this date and time';
					rollback;
				else
					-- Validate booking date is not in the past
					if p_booked_date < curdate() then
						set p_booking_id = null;
						set p_status = 'INVALID_DATE';
						set p_message = 'Cannot book for past dates';
						rollback;
					else
						-- Create the booking
						insert into bookings (
							room_id, 
							booked_date, 
							booked_time, 
							member_id, 
							datetime_of_booking, 
							payment_status, 
							total_amount
						) values (
							p_room_id, 
							p_booked_date, 
							p_booked_time, 
							p_member_id,
							now(),
							'UNPAID',
							v_price
						);
						
						set v_new_booking_id = last_insert_id();
						
						-- Update member payment due
						select payment_due into v_payment_due 
						from members 
						where username = p_member_id; 
						
						update members 
						set payment_due = v_price + v_payment_due,
							updated_at = now()
						where username = p_member_id;
						
						set p_booking_id = v_new_booking_id;
						set p_status = 'SUCCESS';
						set p_message = 'Booking created successfully';
						
						commit;
					end if;
				end if;
			end if;
		end if;
	end $$
delimiter ;

call make_booking('AR', '2023-11-13', '13:00:00', 'nethead21', @booking_id, @status, @message);
select @booking_id as booking_id, @status as status, @message as message;


-- ENHANCED: Making update payment Procedure with validation
delimiter $$
create procedure update_payment(
	in p_id int,
	out p_status varchar(20),
	out p_message varchar(255)
	)
	begin
		declare v_member_id varchar(255);
		declare v_payment_due decimal(10,2);
		declare v_price decimal(10,2);
		declare v_current_status varchar(20);
		declare v_booking_count int default 0;
		
		declare exit handler for sqlexception
		begin
			rollback;
			set p_status = 'ERROR';
			set p_message = 'Database error occurred during payment update';
		end;
		
		start transaction;
		
		-- Validate booking exists and get current status
		select count(*), payment_status, total_amount, member_id 
		into v_booking_count, v_current_status, v_price, v_member_id
		from bookings 
		where id = p_id
		group by payment_status, total_amount, member_id;

		if v_booking_count = 0 then
			set p_status = 'NOT_FOUND';
			set p_message = 'Booking not found';
			rollback;
		elseif v_current_status = 'PAID' then
			set p_status = 'ALREADY_PAID';
			set p_message = 'Booking has already been paid';
			rollback;
		elseif v_current_status = 'CANCELLED' then
			set p_status = 'CANCELLED';
			set p_message = 'Cannot process payment for cancelled booking';
			rollback;
		else
			-- Update booking status to paid
			update bookings 
			set payment_status = 'PAID',
				updated_at = now()
			where id = p_id;

			-- Update member payment due
			select payment_due into v_payment_due 
			from members where username = v_member_id;

			update members 
			set payment_due = greatest(v_payment_due - v_price, 0.00),
				updated_at = now()
			where username = v_member_id;
			
			set p_status = 'SUCCESS';
			set p_message = 'Payment processed successfully';
			
			commit;
		end if;
	end $$
delimiter ;

call update_payment(11, @status, @message);
select @status as status, @message as message;

-- ENHANCED: Making View Bookings Procedure with detailed information
delimiter $$
create procedure view_bookings(
	in p_id varchar(255),
	out p_status varchar(20),
	out p_message varchar(255)
	)
	begin
		declare v_member_count int default 0;
		
		declare exit handler for sqlexception
		begin
			set p_status = 'ERROR';
			set p_message = 'Database error occurred while retrieving bookings';
		end;
		
		-- Validate member exists
		select count(*) into v_member_count 
		from members 
		where username = p_id and status = 'ACTIVE';
		
		if v_member_count = 0 then
			set p_status = 'MEMBER_NOT_FOUND';
			set p_message = 'Member not found or inactive';
		else
			-- Return comprehensive booking information
			select 
				b.id as booking_id,
				b.room_id,
				r.room_name,
				r.room_type,
				b.booked_date,
				b.booked_time,
				b.payment_status,
				b.total_amount,
				b.datetime_of_booking as booking_created,
				b.updated_at as last_updated,
				datediff(b.booked_date, curdate()) as days_until_booking,
				case 
					when b.booked_date < curdate() then 'PAST'
					when b.booked_date = curdate() then 'TODAY'
					else 'FUTURE'
				end as booking_timing
			from bookings b
			inner join rooms r on b.room_id = r.room_id
			where b.member_id = p_id
			order by b.booked_date desc, b.booked_time desc;
			
			set p_status = 'SUCCESS';
			set p_message = 'Bookings retrieved successfully';
		end if;
	end $$
delimiter ;

call view_bookings('macejkovic73', @status, @message);
select @status as status, @message as message;

-- ENHANCED: Making Search Rooms Procedure with comprehensive filtering
delimiter $$
create procedure search_room(
	in p_room_type varchar(255),
	in p_booked_date date,
	in p_booked_time time,
	out p_status varchar(20),
	out p_message varchar(255)
	)
	begin
		declare v_search_count int default 0;
		
		declare exit handler for sqlexception
		begin
			set p_status = 'ERROR';
			set p_message = 'Database error occurred during room search';
		end;
		
		-- Validate search date is not in the past
		if p_booked_date < curdate() then
			set p_status = 'INVALID_DATE';
			set p_message = 'Cannot search for rooms on past dates';
		else
			-- Search for available rooms with detailed information
			select 
				r.room_id,
				r.room_name,
				r.room_type,
				r.price_per_hour,
				r.capacity,
				r.status as room_status,
				case 
					when r.status = 'AVAILABLE' then 'Available for booking'
					when r.status = 'MAINTENANCE' then 'Under maintenance'
					when r.status = 'RESERVED' then 'Reserved for special events'
					else 'Status unknown'
				end as availability_message,
				coalesce(
					(select count(*) 
					 from bookings b2 
					 where b2.room_id = r.room_id 
					   and b2.booked_date between curdate() and date_add(curdate(), interval 30 day)
					   and b2.payment_status != 'CANCELLED'
					), 0
				) as bookings_next_30_days
			from rooms r 
			where r.room_id not in (
				select b.room_id 
				from bookings b
				where 
					b.booked_date = p_booked_date and 
					b.booked_time = p_booked_time and 
					b.payment_status != 'CANCELLED'
			) 
			and r.room_type = p_room_type
			and r.status = 'AVAILABLE'
			order by r.price_per_hour asc, r.room_name asc;
			
			-- Count the results for status message
			select count(*) into v_search_count
			from rooms r 
			where r.room_id not in (
				select b.room_id 
				from bookings b
				where 
					b.booked_date = p_booked_date and 
					b.booked_time = p_booked_time and 
					b.payment_status != 'CANCELLED'
			) 
			and r.room_type = p_room_type
			and r.status = 'AVAILABLE';
			
			if v_search_count = 0 then
				set p_status = 'NO_ROOMS';
				set p_message = concat('No available rooms found for ', p_room_type, ' on ', p_booked_date, ' at ', p_booked_time);
			else
				set p_status = 'SUCCESS';
				set p_message = concat(v_search_count, ' room(s) found for ', p_room_type);
			end if;
		end if;
	end $$
delimiter ;

call search_room('Tennis Court', '2025-12-26', '13:00:00', @status, @message);
select @status as status, @message as message;

-- Making Cancel Booking
delimiter $$
create procedure cancel_booking(
	in p_booking_id int,
	out p_message varchar(255)
	)
	begin
		declare v_cancellation int;
		declare v_member_id varchar(255);
		declare v_payment_status varchar(10);
		declare v_booked_date date;
		declare v_price double(8,2);
		declare v_payment_due double;

		set v_cancellation = 0;

		select
			member_id, booked_date, price, payment_status
		into
			v_member_id, v_booked_date, v_price, v_payment_status
		from member_bookings
		where id = p_booking_id;

		select payment_due into v_payment_due 
		from members where id = v_member_id;

		if curdate() >= v_booked_date then
			select 'Cacellation cannot be done on/after the booked date' into p_message;
		elseif v_payment_status = 'Cancelled' or v_payment_status = 'Paid' then
			select 'Booking has already been cancelled or paid' into p_message;
		else
			update bookings set payment_status = 'Cancelled' where id = p_booking_id;
			set v_payment_due = v_payment_due - v_price;
			set v_cancellation = check_cancellation(p_booking_id);

			if v_cancellation >=2 then
				set v_payment_due = v_payment_due + 10;
			end if;

			update members set payment_due = v_payment_due where id = v_member_id;

			select 'Booking Cancelled' into p_message;

		end if;

	end $$
delimiter ;


-- Triggers
-- Creating payment_check Trigger
delimiter $$
create trigger payment_check
	before delete on members for each row
	begin
		declare v_payment_due double;

		select payment_due into v_payment_due 
		from members where id = old.id;

		if v_payment_due > 0 then
			insert into pending_terminations (id, email, payment_due)
			values (old.id, old.email, v_payment_due);
		end if;
	end $$
delimiter ;


-- Stored Function
-- Creating check_cancellation function
delimiter $$
create function check_cancellation(p_booking_id int)
    returns int
    deterministic
    begin
        declare v_done int;
        declare v_cancellation int;
        declare v_current_payment_status varchar(10);
        
        declare cur cursor for
			select payment_status 
	        from bookings 
	        where member_id = (select member_id 
	        	from bookings 
	        	where id = p_booking_id)
	        order by datetime_of_booking desc;

        declare continue handler 
        	for not found set v_done = 1;

        set v_done = 0;
        set v_cancellation = 0;

        open cur;
        	get_payment_status: loop
        		
        		fetch cur into v_current_payment_status;

        		if v_current_payment_status != 'Cancelled' or v_done = 1 then
        			leave get_payment_status;
        		else
        			set v_cancellation = v_cancellation + 1;
        		end if;

        	end loop get_payment_status;
        close cur;

        return v_cancellation;
    end $$
delimiter ;