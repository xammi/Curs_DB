DROP DATABASE IF EXISTS forum_db;
CREATE DATABASE forum_db;
USE forum_db;

CREATE TABLE `User`(
	`id` INT NOT NULL AUTO_INCREMENT,
	`username` NVARCHAR (50) NOT NULL,
    `email` VARCHAR (50) NOT NULL,

	`about` TEXT NOT NULL DEFAULT '',
	`name` NVARCHAR (50) NOT NULL,
	`isAnonymous` BOOL NOT NULL DEFAULT False,

	PRIMARY KEY (`id`),
    UNIQUE KEY USING HASH (`username`),
    UNIQUE KEY USING HASH (`email`)
);


CREATE TABLE `Forum`(
	`id` INT NOT NULL AUTO_INCREMENT,
    `slug` VARCHAR (50) NOT NULL,
    `founder` VARCHAR (50) NOT NULL,
	`name` NVARCHAR (50) NOT NULL,

	PRIMARY KEY (`id`),
    UNIQUE KEY USING HASH (`slug`),
    KEY USING HASH (`founder`),
    CONSTRAINT FOREIGN KEY (`founder`) REFERENCES `User` (`email`)
);


CREATE TABLE `Thread` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `forum` VARCHAR (50) NOT NULL,
    `author` VARCHAR (50) NOT NULL,
    
    `title` NVARCHAR (50) NOT NULL,
    `date` DATETIME NOT NULL,
    `message` TEXT NOT NULL,
    `slug` VARCHAR (50) NOT NULL,

    `isDeleted` BOOL NOT NULL DEFAULT False,
    `isClosed` BOOL NOT NULL DEFAULT False, 
    `dislikes` INT NOT NULL DEFAULT 0,
    `likes` INT NOT NULL DEFAULT 0,

    PRIMARY KEY (`id`),
    KEY USING HASH (`forum`),
    CONSTRAINT FOREIGN KEY (`forum`) REFERENCES `Forum` (`slug`),
    KEY USING HASH (`author`),
    CONSTRAINT FOREIGN KEY (`author`) REFERENCES `User` (`email`)
);


CREATE TABLE `Post` (
	`id` INT NOT NULL AUTO_INCREMENT,	
    `thread` INT NOT NULL,
    `author` VARCHAR (50) NOT NULL,
    `forum` VARCHAR (50) NOT NULL,

    `date` DATETIME NOT NULL,
    `message` TEXT NOT NULL,
    `dislikes` INT NOT NULL DEFAULT 0,
    `likes` INT NOT NULL DEFAULT 0,

	`parent` VARCHAR (50) NOT NULL,
	`isHighlighted` BOOL NOT NULL DEFAULT False,
	`isApproved` BOOL NOT NULL DEFAULT False,
	`isEdited` BOOL NOT NULL DEFAULT False,
	`isSpam` BOOL NOT NULL DEFAULT False,
	`isDeleted` BOOL NOT NULL DEFAULT False,

	PRIMARY KEY (`id`),
    UNIQUE KEY (`parent`),
    KEY USING HASH (`forum`),
    CONSTRAINT FOREIGN KEY (`forum`) REFERENCES `Forum` (`slug`),
    KEY USING HASH (`author`),
    CONSTRAINT FOREIGN KEY (`author`) REFERENCES `User` (`email`),
    KEY (`thread`),
    CONSTRAINT FOREIGN KEY (`thread`) REFERENCES `Thread` (`id`)
);


