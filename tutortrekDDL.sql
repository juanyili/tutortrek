# CS304 Tutor Trek DDL
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
    tutor varchar(20),
    attendance int,
    foreign key (cid) references class.cid,
    foreign key (tutor) references people.username
    );

create table ratings(
    tutee varchar(20),
    sid int,
    rating_score enum ('1', '2', '3'),
    primary key (tutee, sid),
    foreign key (sid) references session.sid,
    foreign key (tutee) references people.username
    );