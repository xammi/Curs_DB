USE `forum_db`;

INSERT INTO `User` (`username`, `email`, `name`) 
VALUES ('xammi', 'xammi@yandex.ru', 'Kislenko Maksim');

INSERT INTO `User` (`username`, `email`, `name`) 
VALUES ('eugene', 'eugene@mail.ru', 'Eugeniy Kislenko');

#--------------------------------------------------------------------------------------------------

INSERT INTO `Forum` (`slug`, `founder`, `name`)
VALUES ('progs', 'xammi@yandex.ru', 'Programming');

INSERT INTO `Forum` (`slug`, `founder`, `name`)
VALUES ('cars', 'xammi@yandex.ru', 'Cars');

INSERT INTO `Forum` (`slug`, `founder`, `name`)
VALUES ('toys', 'eugene@mail.ru', 'Computer toys');

INSERT INTO `Forum` (`slug`, `founder`, `name`)
VALUES ('books', 'eugene@mail.ru', 'Interesting Books');

#--------------------------------------------------------------------------------------------------

INSERT INTO `Thread` (`forum`, `title`, `author`, `date`, `message`, `slug`)
VALUES ('progs', 'Python', 'xammi@yandex.ru', '2014-01-01', 'Python language', 'python');

INSERT INTO `Thread` (`forum`, `title`, `author`, `date`, `message`, `slug`)
VALUES ('progs', 'C++', 'eugene@mail.ru', '2014-01-02', 'C++ language', 'cpp');

INSERT INTO `Post` (`date`, `thread`, `message`, `author`, `forum`)
VALUES ('2014-01-03', 1, 'Template metaprogramming', 'xammi@yandex.ru', 'progs');