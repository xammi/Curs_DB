DROP DATABASE IF EXISTS forum_db;
CREATE DATABASE forum_db;
USE forum_db;

CREATE TABLE `User`(
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`username` CHAR (25),
    `email` CHAR (25) NOT NULL,

	`about` TEXT,
	`name` CHAR (25),
	`isAnonymous` BOOL NOT NULL DEFAULT False,

	PRIMARY KEY (`id`),
    UNIQUE KEY USING HASH (`email`),
    KEY USING HASH (`name`)
) ENGINE = MYISAM;


CREATE TABLE `Forum`(
	`id` INT(11) NOT NULL AUTO_INCREMENT,
    `short_name` CHAR (35) NOT NULL,
    `user` CHAR (25) NOT NULL,
	`name` NCHAR (35) NOT NULL,

	PRIMARY KEY (`id`),
    UNIQUE KEY USING HASH (`short_name`),
    UNIQUE KEY USING HASH (`name`),
    KEY USING HASH (`user`),
    CONSTRAINT FOREIGN KEY (`user`) REFERENCES `User` (`email`) ON DELETE CASCADE
) ENGINE = MYISAM;


CREATE TABLE `Thread` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `forum` CHAR (35) NOT NULL,
    `user` CHAR (25) NOT NULL,
    
    `title` NCHAR (50) NOT NULL,
    `date` DATETIME NOT NULL,
    `message` TEXT NOT NULL,
    `slug` CHAR (50) NOT NULL,

    `isDeleted` BOOL NOT NULL DEFAULT False,
    `isClosed` BOOL NOT NULL DEFAULT False, 
    `dislikes` SMALLINT NOT NULL DEFAULT 0,
    `likes` SMALLINT NOT NULL DEFAULT 0,
    `points` SMALLINT NOT NULL DEFAULT 0,
    `posts` SMALLINT NOT NULL DEFAULT 0,

    PRIMARY KEY (`id`),
    KEY USING HASH (`slug`),
    KEY USING HASH (`forum`),
    CONSTRAINT FOREIGN KEY (`forum`) REFERENCES `Forum` (`short_name`) ON DELETE CASCADE,
    CONSTRAINT FOREIGN KEY (`user`) REFERENCES `User` (`email`) ON DELETE CASCADE
) ENGINE = MYISAM;

ALTER TABLE `Thread` ADD INDEX idx_thread_ud (`user`, `date`);

CREATE TABLE `Post` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
    `thread` INT(11) NOT NULL,
    `user` CHAR (25) NOT NULL,
    `forum` CHAR (35) NOT NULL,

    `date` DATETIME NOT NULL,
    `message` TEXT NOT NULL,
    `dislikes` SMALLINT NOT NULL DEFAULT 0,
    `likes` SMALLINT NOT NULL DEFAULT 0,
    `points` SMALLINT NOT NULL DEFAULT 0,

	`parent` INT(11),
	`path` CHAR(50) NOT NULL DEFAULT '',
	`isHighlighted` BOOL NOT NULL DEFAULT False,
	`isApproved` BOOL NOT NULL DEFAULT False,
	`isEdited` BOOL NOT NULL DEFAULT False,
	`isSpam` BOOL NOT NULL DEFAULT False,
	`isDeleted` BOOL NOT NULL DEFAULT False,

	PRIMARY KEY (`id`),
    KEY (`parent`),
    CONSTRAINT FOREIGN KEY (`forum`) REFERENCES `Forum` (`short_name`) ON DELETE CASCADE,
    CONSTRAINT FOREIGN KEY (`user`) REFERENCES `User` (`email`) ON DELETE CASCADE,
    CONSTRAINT FOREIGN KEY (`thread`) REFERENCES `Thread` (`id`) ON DELETE CASCADE
) ENGINE = MYISAM;


ALTER TABLE `Post` ADD INDEX idx_post_fu (`forum`, `user`);
ALTER TABLE `Post` ADD INDEX idx_post_fd (`forum`, `date`);
ALTER TABLE `Post` ADD INDEX idx_post_td (`thread`, `date`);
ALTER TABLE `Post` ADD INDEX idx_post_ud (`user`, `date`);


DROP TRIGGER IF EXISTS ins_post;
CREATE TRIGGER ins_post
BEFORE INSERT ON `Post`
FOR EACH ROW
UPDATE `Thread` SET `posts` = `posts` + 1 WHERE `id` = NEW.`thread`;

DROP TRIGGER IF EXISTS del_post;

CREATE TABLE `Follow` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `follower` CHAR (25) NOT NULL,
    `followee` CHAR (25) NOT NULL,

    PRIMARY KEY (`id`),
    KEY USING HASH (`follower`),
    CONSTRAINT FOREIGN KEY (`follower`) REFERENCES `User` (`email`) ON DELETE CASCADE,
    KEY USING HASH (`followee`),
    CONSTRAINT FOREIGN KEY (`followee`) REFERENCES `User` (`email`) ON DELETE CASCADE
) ENGINE = MYISAM;

CREATE TABLE `Subscribe` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `user` CHAR (25) NOT NULL,
    `thread` INT(11) NOT NULL,

    PRIMARY KEY (`id`),
    KEY USING HASH (`user`),
    CONSTRAINT FOREIGN KEY (`user`) REFERENCES `User` (`email`) ON DELETE CASCADE,
    KEY (`thread`),
    CONSTRAINT FOREIGN KEY (`thread`) REFERENCES `Thread` (`id`) ON DELETE CASCADE
) ENGINE = MYISAM;