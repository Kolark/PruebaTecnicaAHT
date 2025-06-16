-- create database if not exists aht_db;

-- use aht_db;

create table if not exists Inventory(
	id int not null primary key auto_increment,
	name          varchar(30) not null,
	price         int         not null,
	mac_address   varchar(17) not null,
	serial_number varchar(20) not null,
	manufacturer  varchar(15) not null,
	description   varchar(255)not null);

-- drop table if exists Inventory;

--Show all
-- select * from Inventory;
--Add item
insert into Inventory(name, price, mac_address, serial_number, manufacturer, description)
values('computer dell', 15000, '00:1A:2B:3C:4D:5E', 'DH1VVUHJ002D9NCK0051','dell', 'a computer');

insert into Inventory(name, price, mac_address, serial_number, manufacturer, description)
values('computer apple', 25000, '00:1A:2B:3C:4D:5E', 'DH1IIUD0002D9NCK0051','apple', 'a computer');

insert into Inventory(name, price, mac_address, serial_number, manufacturer, description)
values('computer hp', 35000, '00:1A:2B:3C:4D:5E', 'DH1VVUFF002D9NCK0051','hewlet packer', 'a computer');

insert into Inventory(name, price, mac_address, serial_number, manufacturer, description)
values('computer asus', 25000, '00:1A:2B:3C:4D:5E', 'DH1VDFD0002D9NCK0051','asus', 'a computer');

-- #delete
-- delete from Inventory i WHERE i.manufacturer = "dell";

-- #update
-- UPDATE Inventory i
-- set price=50000
-- where i.manufacturer = 'apple';

