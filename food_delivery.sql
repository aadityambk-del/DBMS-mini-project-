create database aaditya;
use aaditya;

create table Customer
(
c_id int primary key,
c_fullname varchar(50) not null,
c_address varchar(100),
c_mobileno varchar(13) unique
);

create table Restaurant
(
r_regino int primary key,
r_gstino varchar(20) unique not null,
r_mobileno varchar(13),
r_address varchar(100),
c_id int,
foreign key (c_id) references Customer(c_id)
);

create table Delivery_Agent
(
da_contactno varchar(13) primary key,
da_id int unique not null,
da_tracking varchar(20) default 'Assigned' check (da_tracking in ('Assigned','Picked Up','On the Way','Delivered')),
da_otp int check (da_otp between 1000 and 9999),
r_regino int,
foreign key (r_regino) references Restaurant(r_regino)
);

create table Food
(
f_no int primary key,
f_description varchar(50) not null,
f_type varchar(10) check (f_type in ('Veg','Non-Veg')),
f_pricefilter decimal(10,2) check (f_pricefilter > 0),
c_id int,
da_contactno varchar(13),
foreign key (c_id) references Customer(c_id),
foreign key (da_contactno) references Delivery_Agent(da_contactno)
);

create table Hands_Out
(
r_regino int,
f_no int,
primary key (r_regino, f_no),
foreign key (r_regino) references Restaurant(r_regino),
foreign key (f_no) references Food(f_no)
);

create table Cart
(
ca_no int primary key,
ca_addon varchar(50),
ca_totalprice decimal(10,2),
ca_type varchar(20) default 'Delivery' check (ca_type in ('Delivery','Takeaway')),
c_id int,
foreign key (c_id) references Customer(c_id)
);

create table Offers
(
o_coupon varchar(20) primary key,
o_rewardpoints int default 0,
o_premium varchar(5) check (o_premium in ('Yes','No')),
o_discount int check (o_discount between 0 and 100),
c_id int,
ca_no int,
foreign key (c_id) references Customer(c_id),
foreign key (ca_no) references Cart(ca_no)
);

create table Review
(
c_id int,
r_regino int,
r_stars int check (r_stars between 1 and 5),
r_message varchar(100),
primary key (c_id, r_regino),
foreign key (c_id) references Customer(c_id),
foreign key (r_regino) references Restaurant(r_regino)
);

create table Payment
(
p_upiid varchar(30) primary key,
p_mode varchar(10) check (p_mode in ('Online','Offline')),
p_cod varchar(5) default 'No' check (p_cod in ('Yes','No')),
p_wallet varchar(20),
c_id int,
foreign key (c_id) references Customer(c_id)
);

create table Online
(
p_upiid varchar(30) primary key,
gpay varchar(30),
foreign key (p_upiid) references Payment(p_upiid)
);

create table Offline
(
p_upiid varchar(30) primary key,
cash decimal(10,2),
foreign key (p_upiid) references Payment(p_upiid)
);

create table Bill
(
b_no int primary key,
b_date date not null,
b_amt decimal(10,2),
b_time time,
ca_no int,
p_upiid varchar(30),
foreign key (ca_no) references Cart(ca_no),
foreign key (p_upiid) references Payment(p_upiid)
);

create table Customer_Care
(
cc_email varchar(50) primary key,
cc_refund varchar(10) default 'None' check (cc_refund in ('None','Initiated','Completed')),
cc_complaint varchar(100),
cc_paymentissue varchar(5) check (cc_paymentissue in ('Yes','No')),
c_id int,
da_contactno varchar(13),
foreign key (c_id) references Customer(c_id),
foreign key (da_contactno) references Delivery_Agent(da_contactno)
);
