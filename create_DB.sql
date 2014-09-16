DROP DATABASE IF EXISTS forum_db;
CREATE DATABASE forum_db;
USE forum_db;

CREATE TABLE `User`(
	`id` INT NOT NULL AUTO_INCREMENT,
	`username` NVARCHAR (20) NOT NULL UNIQUE,
	`about` TEXT NOT NULL,
	`name` NVARCHAR (20) NOT NULL,
	`email` VARCHAR (30) NOT NULL UNIQUE,

	`isAnonymous` BOOL NOT NULL DEFAULT False,

	PRIMARY KEY (`id`)
);

ALTER TABLE `User`
	ADD INDEX (`username`),
	ADD INDEX (`email`);


CREATE TABLE `Forum`(
	`id` INT NOT NULL AUTO_INCREMENT,
	`name` NVARCHAR (50) NOT NULL,
	`short_name` NVARCHAR (15) NOT NULL UNIQUE,
	`user_id` INT NOT NULL,

	PRIMARY KEY (`id`)
);

ALTER TABLE `Forum`
	ADD INDEX (`user_id`),
	ADD CONSTRAINT FOREIGN KEY (`user_id`) REFERENCES `User` (`id`);


CREATE TABLE `Post`(
	`id` INT NOT NULL AUTO_INCREMENT,	
	`date` DATETIME NOT NULL,
	`thread` INT NOT NULL,
	`message` TEXT NOT NULL,
	`user` INT NOT NULL,
	`forum` INT NOT NULL,

	`parent` INT DEFAULT NULL,
	`isHighlighted` BOOL NOT NULL DEFAULT False,
	`isApproved` BOOL NOT NULL DEFAULT False,
	`isEdited` BOOL NOT NULL DEFAULT False,
	`isSpam` BOOL NOT NULL DEFAULT False,
	`isDeleted` BOOL NOT NULL DEFAULT False,

	PRIMARY KEY (`id`)
);

ALTER TABLE `Post`
	ADD INDEX (`parent`),
	ADD INDEX (`thread`),
	ADD CONSTRAINT FOREIGN KEY (`parent`) REFERENCES `Post` (`id`);


CREATE TABLE `Thread` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`forum` INT NOT NULL,
	`title` NVARCHAR (50) NOT NULL,
	`isClosed` BOOL NOT NULL DEFAULT False,
	`user` INT NOT NULL,
	`date` DATETIME NOT NULL,
	`message` TEXT NOT NULL,
	`slug` VARCHAR (20) NOT NULL,

	`isDeleted` BOOL NOT NULL DEFAULT False,

	PRIMARY KEY (`id`)
);

ALTER TABLE `Thread`
	ADD INDEX (`forum`),
	ADD INDEX (`user`),
	ADD CONSTRAINT FOREIGN KEY (`forum`) REFERENCES `Forum` (`id`);

