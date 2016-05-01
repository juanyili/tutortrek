# CS304 P2 Tutor Trek DDL
# Author: Wanyi Li & Emma Howey

drop table if exists people;
drop table if exists class;
drop table if exists admin;
drop table if exists tutee;
drop table if exists tutor;
drop table if exists class;
drop table if exists session;
drop table if exists ratings;

create table people (
    uid int auto_increment,
    name varchar(50),
	username varchar(20),
    password char(15),
    primary key (uid),
    unique(username),
    role enum ('Admin', 'Tutor', 'Tutee')
    );

create table class(
    cid int,
    title  varchar(50),
    primary key (cid)
    );

create table session(
    sid int auto_increment primary key,
    cid int,
    session_date date,
    length FLOAT,
    tutor_id int,
    attendance int,
    foreign key (cid) references class.class_id,
    foreign key (tutor_id) references people.uid
    );

create table ratings(
    tutee_id int,
    sid int,
    rating_score enum ('1', '2', '3'),
    primary key (tutee_id, sid),
    foreign key (sid) references session.sid,
    foreign key (tutee_id) references people.uid
    );