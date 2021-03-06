USE `forum_db`;

INSERT INTO `User` (`username`, `email`, `name`) 
VALUES ('xammi', 'xammi@yandex.ru', 'Kislenko Maksim');

INSERT INTO `User` (`username`, `email`, `name`) 
VALUES ('eugene', 'eugene@mail.ru', 'Eugeniy Kislenko');

-- --------------------------------------------------------------------------------------------------

INSERT INTO `Forum` (`short_name`, `user`, `name`)
VALUES ('progs', 'xammi@yandex.ru', 'Programming');

INSERT INTO `Forum` (`short_name`, `user`, `name`)
VALUES ('cars', 'xammi@yandex.ru', 'Cars');

INSERT INTO `Forum` (`short_name`, `user`, `name`)
VALUES ('toys', 'eugene@mail.ru', 'Computer toys');

INSERT INTO `Forum` (`short_name`, `user`, `name`)
VALUES ('books', 'eugene@mail.ru', 'Interesting Books');

-- --------------------------------------------------------------------------------------------------

INSERT INTO `Thread` (`forum`, `title`, `user`, `date`, `message`, `slug`)
VALUES ('progs', 'Python', 'xammi@yandex.ru', '2014-01-01', 'Python language', 'python');

INSERT INTO `Thread` (`forum`, `title`, `user`, `date`, `message`, `slug`)
VALUES ('progs', 'C++', 'eugene@mail.ru', '2014-01-02', 'C++ language', 'cpp');

INSERT INTO `Thread` (`forum`, `title`, `user`, `date`, `message`, `slug`)
VALUES ('toys', 'Civilization', 'eugene@mail.ru', '2014-01-02', 'Sid Meyers Civilization', 'civ');

-- --------------------------------------------------------------------------------------------------

INSERT INTO `Post` (`date`, `thread`, `message`, `user`, `forum`)
VALUES ('2014-01-03', 1, 'Template metaprogramming', 'xammi@yandex.ru', 'progs');


INSERT INTO `Post` (`date`, `thread`, `message`, `user`, `forum`)
VALUES ('2014-01-03', 1, 'Unit', 'eugene@mail.ru', 'toys');

-- flat ASC

SELECT *
FROM `Post`
WHERE `forum` = %s AND `date` > %s
ORDER BY `date` ASC
LIMIT 3;

-- flat DESC

SELECT *
FROM `Post`
WHERE `forum` = %s AND `date` > %s
ORDER BY `date` DESC
LIMIT 3;

-- tree ASC

SELECT *
FROM `Post`
WHERE `forum` = %s AND `date` > %s
ORDER BY `date` DESC, `path` ASC
LIMIT 3;

-- tree DESC

SELECT *
FROM `Post`
WHERE `forum` = %s AND `date` > %s
ORDER BY `date` DESC, `path` DESC
LIMIT 3;

-- parent_tree ASC

SELECT *
FROM `Post`
WHERE `forum` = %s AND `date` > %s AND `path` LIKE ''
ORDER BY `date` DESC, `path` ASC
LIMIT 3;

-- parent_tree DESC

SELECT *
FROM `Post`
WHERE `forum` = %s AND `date` > %s AND `path` LIKE ''
ORDER BY `date` DESC, `path` DESC
LIMIT 3;

SELECT *
FROM `Post`
WHERE id = INT(LEFT(path, '%.'))
ORDER BY `date` DESC;