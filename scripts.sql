USE `forum_db`;

SELECT `id` FROM `User` WHERE `email` = 'ex@ex.ru';

INSERT INTO `Forum` (`name`, `short_name`, `user_id`) 
VALUES ('people', 'peo', 5);