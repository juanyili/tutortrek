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
    unique(username)
    );

create table admin(
    admin_id int,
    foreign key (admin_id) references people.uid
    );

create table tutee(
    tutee_id int,
    foreign key (tutee_id) references people.uid
    );

create table tutor(
    tutor_id int,
    foreign key (tutor_id) references people.uid
    );

create table class(
    class_id int,
    title  varchar(50),
    primary key (class_id)
    );

create table session(
    sid int auto_increment primary key,
    class_id int,
    session_date date,
    length int,
    tutor_id int,
    foreign key (class_id) references class.class_id,
    foreign key (tutor_id) references tutor.tutor_id
    );

create table ratings(
    tutee_id int,
    sid int,
    rating_score enum ('Yes, I recommend', "No, I don't", 'I am neutral.'),
    primary key (tutee_id, sid),
    foreign key (sid) references session.sid,
    foreign key (tutee_id) references tutee.tutee_id
    );