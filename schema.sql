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
				utime timestamp default current_timestamp);


CREATE TABLE groups (id serial primary key,
				name varchar(100) not null,
				description text,
				gtime timestamp default current_timestamp);


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
				etime timestamp default current_timestamp);


CREATE TABLE photos (id serial primary key,
				owner int references users (id),
				event int references events (id),
				photo_path text not null,
				ptime timestamp default current_timestamp);


CREATE TABLE videos (id serial primary key,
				owner int references users (id),
				event int references events (id),
				video_path text not null,
				ptime timestamp default current_timestamp);


COMMIT;
