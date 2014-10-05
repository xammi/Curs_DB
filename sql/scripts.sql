USE `forum_db`;

SELECT `id` FROM `User` WHERE `email` = 'ex@ex.ru';
SELECT * FROM Forum;

SELECT `id`, `date`, `message`, `parent`, 
`isApproved`, `isDeleted`,`isEdited`, `isHighlighted`, `isSpam`,
`User`.`email`
FROM `Post` 
JOIN `Forum` ON `forum` = `Forum`.`id`
JOIN `User` ON `user` = `User`.`id`
WHERE `forum` = 2;

INSERT INTO `Forum` (`name`, `short_name`, `user_id`) 
VALUES ('chicks', 'chicks', 1);

