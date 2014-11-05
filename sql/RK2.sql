# RK_2

SELECT * FROM TBL WHERE A=5 AND B=6
SELECT * FROM TBL WHERE A>5 AND B=6

Какой индекс необходимо построить
A
B
AB
BA *OK*

#----------------------------------------------------------
    
CREATE INDEX tab_idx ON tbl (a, date_column);

SELECT date_column, count(*)
FROM tbl
WHERE a = 123
AND b = 42
GROUP BY date_column;

Отличный запрос
Что-то не так *OK*

#-----------------------------------------------------------

CREATE INDEX tab_idx ON tbl (a, date_column);

SELECT date_column, count(*)
FROM tbl
WHERE a = 123
GROUP BY date_column;


Отличный запрос *OK*
Что-то не так

#-----------------------------------------------------------

CREATE INDEX tab_idx ON tbl (date_column, a);

SELECT date_column, count(*)
FROM tbl
WHERE a = 123
AND b = 42
GROUP BY date_column;

Отличный запрос *OK*
Что-то не так

#-----------------------------------------------------------

 CREATE INDEX tbl_idx ON tbl (a, date_column);

SELECT id, a, date_column
FROM tbl
WHERE a = ?
ORDER BY date_column DESC
LIMIT 1;
Отличный запрос *OK*
Что-то не так

#-----------------------------------------------------------

 Какой из запросов наиболее высокопроизводителен?

SELECT * FROM Orders WHERE TO_DAYS(CURRENT_DATE()) - TO_DAYS(order_created) <= 7;
SELECT * FROM Orders WHERE order_created >= '20070211' INTERVAL 7 DAY; *OK*
SELECT * FROM Orders WHERE order_created >= CURRENT_DATE() INTERVAL 7 DAY;

#-----------------------------------------------------------

 Разложение JOIN на отдельные запросы и выполнение на стороне приложения:

Всегда эффективно, но усложняет понимание логики приложения
Может быть эффективно в некоторых случаях *OK*
Не эффективно, увеличивает кол-во запросов


#-------------------------------------------------------------

 Пусть есть таблица t1 с тремя столбцами c1,c2,c3 (тип данных char(32)). Создан составной индекс по трем этим полям
CREATE INDEX ind1 ON t1(c1,c2,c3);

Какие из нижеприведённых SELECT будут использовать этот индекс, хотя бы частично:
SELECT * FROM t1 WHERE c1='Василий' AND c2='Иванович' AND c3='Чапаев';
SELECT * FROM t1 WHERE (c1='Василий' OR c1='Петька') AND c2='Иванович';
SELECT * FROM t1 WHERE c3='Петька';
SELECT count(*) FROM t1 WHERE c3='Чапаев';
SELECT count(*) FROM t1 WHERE c1 LIKE 'Васил%' AND c3='Чапаев';

#---------------------------------------------------------------

 KEY (A,B)

Выберите лучший вариант
SELECT * FROM TBL WHERE A BETWEEN 2 AND 4 AND B=5
SELECT * FROM TBL WHERE A IN (2,3,4) AND B=5 *OK*
SELECT * FROM TBL WHERE A > 1 AND A < 5 AND B=5

#----------------------------------------------------------------

 KEY(A,B)

Выберите лучший вариант
SELECT * FROM TBL WHERE A IN (1,2) ORDER BY B LIMIT 5;
(SELECT * FROM TBL WHERE A=1 ORDER BY B LIMIT 5) UNION ALL (SELECT * FROM TBL WHERE A=2 ORDER BY B LIMIT 5) ORDER BY B LIMIT 5; *OK*

#----------------------------------------------------------------

 Учитывая уникальный ключ: my_key (a_field, b_field, c_field). Какие из следующих запросов будет использовать ключ, чтобы сортировать результаты?
SELECT .. FROM .. WHERE a_field='abc' ORDER BY b_field,c_field *OK*
SELECT .. FROM .. WHERE a_field='abc' ORDER BY b_field *OK*
SELECT .. FROM .. WHERE a_field > 'abc' ORDER BY b_field,c_field
SELECT .. FROM .. WHERE a_field > 'abc' ORDER BY a_field,b_field,c_field *OK*
SELECT .. FROM .. WHERE a_field='abc' ORDER BY b_field DESC,c_field ASC
SELECT .. FROM .. WHERE a_field='abc' ORDER BY c_field

#-----------------------------------------------------------------

 KEY (GENDER,CITY)

Выберите лучший вариант
SELECT * FROM PEOPLE WHERE CITY=“NEW YORK”
SELECT * FROM PEOPLE WHERE GENDER IN (“M”,”F”) AND CITY=“NEW YORK” *OK*

#-----------------------------------------------------------------

 Верно ли что оптимизация запросов со столбцами использующими null значения сложнее, чем без них.
Да *OK*
Нет

#-----------------------------------------------------------------

 CREATE INDEX tbl_idx ON tbl (date_column);

SELECT text, date_column
FROM tbl
WHERE TO_CHAR(date_column, 'YYYY') = '2012';
Отличный запрос
Что-то не так *OK*

#------------------------------------------------------------------

 Следующие два запроса возвращают одинаковый результат. Первый использует LIKE а второй использует функции LEFT. Какой вариант лучше, учитывая, что в столбец "title" индексируется?
SELECT * FROM film WHERE title LIKE 'Tr%'; *OK*
SELECT * FROM film WHERE LEFT(title,2) = 'Tr'

#---------------------------------------------------------

 CREATE INDEX tbl_idx ON tbl (date_column, state);

SELECT id, date_column, state
FROM tbl
WHERE date_column >= CURRENT_DATE - INTERVAL '5' YEAR
AND state = 'X';

(365 rows)


При следующем распределение:

SELECT count(*)
FROM tbl
WHERE date_column >= CURRENT_DATE - INTERVAL '5' YEAR;

count
-------
1826

SELECT count(*)
FROM tbl
WHERE state = 'X';

count
-------
10000
Отличный запрос
Что-то не так *OK*

#-------------------------------------------------------

 Какую часть индекса ABCD, MySQL будет использовать для следующего запроса:
Select A,B,C from my_table where A=x and B like "my string%" and C=y
ABCD
ABC
AB *OK*
A
MySQLне будет использовать индекс *OK*

#--------------------------------------------------------

 CREATE INDEX tbl_idx ON tbl (text);

SELECT id, text
FROM tbl
WHERE text LIKE '%TERM%';
Отличный запрос
Что-то не так *OK*

#---------------------------------------------------------

 CREATE INDEX tbl_idx ON tbl (a, b);

SELECT id, a, b
FROM tbl
WHERE a = ?
AND b = ?;


SELECT id, a, b
FROM tbl
WHERE b = ?;
Отличный запрос
Что-то не так