USE `forum_db`;

SELECT * FROM `Forum`;
SELECT * FROM `User`;
SELECT * FROM `Thread`;
SELECT * FROM `Post`;

UPDATE `Post`
SET `isDeleted` = True
WHERE `id` = 0;