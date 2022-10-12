CREATE DATABASE IF NOT EXISTS advice_health_challenge;
USE advice_health_challenge;

create table if not exists owner
(
    owner_id   int auto_increment
        primary key,
    first_name varchar(60) not null,
    last_name  varchar(60) not null
);

create table if not exists car
(
    car_id   int auto_increment
        primary key,
    model    varchar(20) not null,
    color    varchar(20) not null,
    owner_id int         not null,
    constraint car_owner___fk
        foreign key (owner_id) references owner (owner_id)
);

insert ignore into owner VALUES (1, 'John', 'Doe');
insert ignore into car VALUES (1, 'hatch', 'yellow', 1);