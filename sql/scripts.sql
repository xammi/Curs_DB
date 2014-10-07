USE `forum_db`;

SELECT * FROM `Forum`;
SELECT * FROM `User`;
SELECT * FROM `Thread`;
SELECT * FROM `Post`;

INSERT INTO `Thread` (`forum`, `title`, `user`, `date`, `message`, `slug`)
VALUES (5, 'Python', 1, '2014-01-01', 'Python language', 'python');

INSERT INTO `Thread` (`forum`, `title`, `user`, `date`, `message`, `slug`)
VALUES (5, 'C++', 1, '2014-01-01', 'C++ language', 'cpp');

INSERT INTO `Post` (`date`, `thread`, `message`, `user`, `forum`)
VALUES ('2014-01-01', 2, 'Template metaprogramming', 1, 5);