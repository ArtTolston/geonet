BEGIN;

DROP TABLE IF EXISTS service_t;
DROP TABLE IF EXISTS photos;
DROP TABLE IF EXISTS videos;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS groups;
DROP TABLE IF EXISTS users;


CREATE TABLE users (id serial primary key,
				login varchar(20) not null,
				passwd varchar(100) not null,
				avatar bytea,
				time timestamp default current_timestamp);


CREATE TABLE groups (id serial primary key,
				name varchar(100) not null,
				description text,
				time timestamp default current_timestamp);


CREATE TABLE service_t (usr int,
						grp int,
						PRIMARY KEY (usr, grp),
						FOREIGN KEY (usr) REFERENCES users (id),
						FOREIGN KEY (grp) REFERENCES groups (id));


CREATE TABLE events (id serial primary key,
				name varchar(100) not null,
				description text,
				grp int references groups (id),
				longtitude decimal not null,
				latitude decimal not null,
				time timestamp default current_timestamp);

CREATE TYPE mediatype AS ENUM ('photo', 'video'); 


CREATE TABLE media (id serial primary key,
				owner int references users (id),
				event int references events (id),
				type mediatype not null,
				path text not null,
				time timestamp default current_timestamp);

COMMIT;
