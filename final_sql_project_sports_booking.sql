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

-- View
-- 	member_bookings

-- Stored Procedures
-- 	insert_new_member
-- 	delete_member
-- 	update_member_password
-- 	update_member_email
-- 	make_booking
-- 	update_payment
-- 	view_bookings
-- 	search_room
-- 	cancel_booking

-- Trigger
-- 	payment_check

-- Stored Function
-- 	check_cancellation

-- Resetting the database so that we're all on the same page
DROP DATABASE IF EXISTS sports_booking;
create database sports_booking;
use sports_booking;

-- Creating the members, pending_terminations, rooms and bookings tables;
CREATE TABLE members (
    id VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    member_since TIMESTAMP NOT NULL DEFAULT NOW(),
    payment_due DOUBLE NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
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

CREATE TABLE pending_terminations (
    id VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    request_date TIMESTAMP NOT NULL DEFAULT NOW(),
    payment_due DOUBLE NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
);

CREATE TABLE rooms (
    id VARCHAR(255) NOT NULL,
    room_type VARCHAR(255) NOT NULL,
    price DOUBLE(8 , 2 ) NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
);

insert into rooms (id, room_type, price) 
values
('AR', 'Archery Range', 120),
('B1', 'Badminton Court', 8),
('B2', 'Badminton Court', 8),
('MPF1', 'Multi Purpose Field', 50),
('MPF2', 'Multi Purpose Field', 60),
('T1', 'Tennis Court', 10),
('T2', 'Tennis Court', 10);

CREATE TABLE bookings (
    id INT AUTO_INCREMENT,
    room_id VARCHAR(255) NOT NULL,
    booked_date DATE NOT NULL,
    booked_time TIME NOT NULL,
    member_id VARCHAR(255) NOT NULL,
    datetime_of_booking TIMESTAMP NOT NULL DEFAULT NOW(),
    payment_status VARCHAR(10) NOT NULL DEFAULT 'Unpaid',
    CONSTRAINT uc1 UNIQUE (room_id , booked_date , booked_time),
    CONSTRAINT fk1 FOREIGN KEY (member_id)
        REFERENCES members (id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk2 FOREIGN KEY (room_id)
        REFERENCES rooms (id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (id)
);

insert into bookings (
	id,
	room_id, 
	booked_date, 
	booked_time, 
	member_id, 
	datetime_of_booking, 
	payment_status) 
values
(1, 'AR', '2017-12-26', '13:00:00', 'oreillys', '2017-12-20 20:31:27', 'Paid'),
(2, 'MPF1', '2017-12-30', '17:00:00', 'noah51', '2017-12-22 05:22:10', 'Paid'),
(3, 'T2', '2017-12-31', '16:00:00', 'macejkovic73', '2017-12-28 18:14:23', 'Paid'),
(4, 'T1', '2018-03-05', '08:00:00', 'little31', '2018-02-22 20:19:17', 'Unpaid'),
(5, 'MPF2', '2018-03-02', '11:00:00', 'marvin1', '2018-03-01 16:13:45', 'Paid'),
(6, 'B1', '2018-03-28', '16:00:00', 'marvin1', '2018-03-23 22:46:36', 'Paid'),
(7, 'B1', '2018-04-15', '14:00:00', 'macejkovic73', '2018-04-12 22:23:20', 'Cancelled'),
(8, 'T2', '2018-04-23', '13:00:00', 'macejkovic73', '2018-04-19 10:49:00', 'Cancelled'),
(9, 'T1', '2018-05-25', '10:00:00', 'marvin1', '2018-05-21 11:20:46', 'Unpaid'),
(10, 'B2', '2018-06-12', '15:00:00', 'bbahringer', '2018-05-30 14:40:23', 'Paid');


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

-- Making Booking Procedure
delimiter $$
create procedure make_booking(
	in p_room_id varchar(255), 
	in p_booked_date date, 
	in p_booked_time time, 
	in p_member_id varchar(255)
	)
	begin
		declare v_price double(8,2);
		declare v_payment_due double;

		select price into v_price from rooms where id = p_room_id;
		
		insert into bookings (room_id, booked_date, booked_time, member_id)
		values (p_room_id, p_booked_date, p_booked_time, p_member_id);

		select payment_due into v_payment_due from members where id = p_member_id;

		update members set payment_due = v_price + v_payment_due where id = p_member_id;
	end $$
delimiter ;

call make_booking('AR', '2023-11-13', '13:00:00', 'nethead21');


-- Making update payment Procedure
delimiter $$
create procedure update_payment(
	in p_id int
	)
	begin
		declare v_member_id varchar(255);
		declare v_payment_due double;
		declare v_price double(8,2);

		update bookings set payment_status = 'Paid' where id = p_id;

		select
			member_id, price
		into 
			v_member_id, v_price
		from member_bookings where id = p_id;

		select payment_due into v_payment_due 
		from members where id = v_member_id;

		update members set payment_due = v_payment_due - v_price 
		where id = v_member_id;

	end $$
delimiter ;

call update_payment(11);

-- Making View Bookings Procedure
delimiter $$
create procedure view_bookings(
	in p_id varchar(255)
	)
	begin
		select * from member_bookings where 
		member_id = p_id;
	end $$
delimiter ;

call view_bookings('macejkovic73');

-- Making Search Rooms Procedure
delimiter $$
create procedure search_room(
	in p_room_type varchar(255),
	in p_booked_date date,
	in p_booked_time time
	)
	begin
		select * from rooms where id not in (
			select room_id 
			from bookings 
			where 
				booked_date = p_booked_date and 
				booked_time = p_booked_time and 
				payment_status != 'cancelled'
		) and room_type = p_room_type;
	end $$
delimiter ;

call search_room('Tennis Court', '2017-12-26', '13:00:00');

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