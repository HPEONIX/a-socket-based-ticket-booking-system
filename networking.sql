show databases;
use booking;

Drop table event_list;
drop table seats;

create table if not exists event_list(
event_id int AUTO_INCREMENT unique,
event_name varchar(50),
phone varchar(20),
search_id varchar(100),
org_name varchar(20),
primary key(search_id)
);

create table if not exists seats (search_id varchar(100),total_seats int,seats_booked int);

show tables;

select * from event_list;
select * from seats;


