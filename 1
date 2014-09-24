__(+)__
// Найти названия всех фильмов снятых 'Steven Spielberg', отсортировать по алфавиту. 

SELECT DISTINCT title
FROM Movie
WHERE director = 'Steven Spielberg'
ORDER BY title; 

__(+)__
// Найти года в которых были фильмы с рейтингом 4 или 5, и отсортировать по возрастанию.

SELECT DISTINCT year 
FROM Movie JOIN Rating ON Movie.mID = Rating.mID
WHERE stars = 4 OR stars = 5
ORDER BY year;


__(+)__
// Найти названия всех фильмов которые не имеют рейтинга, отсортировать по алфавиту. 

SELECT DISTINCT title
FROM Movie 
LEFT JOIN Rating ON Movie.mID = Rating.mID 
WHERE Rating.mID IS NULL
ORDER BY title;

__(+)__
// Для каждой оценки, где эксперт тот же целовек что и режиссер, выбрать имя, название фильма и оценку, отсортировать по имени, названию фильма и оценке

SELECT name, title, stars 
FROM Rating 
JOIN Reviewer ON Rating.rID = Reviewer.rID
JOIN Movie ON Movie.mID = Rating.mID AND Reviewer.name = Movie.director
ORDER BY name, title, stars;

__(+)__
// Некоторые оценки не имеют даты. Найти имена всех экспертов, имеющих оценки без даты, отсортировать по алфавиту

SELECT DISTINCT name FROM Rating 
JOIN Reviewer ON Rating.rID = Reviewer.rID AND Rating.ratingDate IS NULL
ORDER BY name;

__(+)__
// Выберите названия всех фильмов, по алфавиту, которым не поставил оценку 'Chris Jackson'. 

SELECT DISTINCT title FROM Movie
WHERE Movie.mID NOT IN
(SELECT mID FROM Rating 
JOIN Reviewer ON Rating.rID = Reviewer.rID 
WHERE name = 'Chris Jackson')
ORDER BY title;

__(+)__
// Найти имена всех экспертов, которые поставили три или более оценок, сортировка по алфавиту.

SELECT name  FROM Rating 
JOIN Reviewer ON Rating.rID = Reviewer.rID
GROUP BY name
HAVING COUNT(*) >= 3
ORDER BY name;


__(+)__
// Найти имена всех экспертов, кто оценил "Gone with the Wind", отсортировать по алфавиту. 

SELECT DISTINCT name
FROM Movie
JOIN Rating ON Movie.mID = Rating.mID AND title = 'Gone with the Wind'
JOIN Reviewer ON Rating.rID = Reviewer.rID
ORDER BY name;

// Найти разницу между средней оценкой фильмов выпущенных до 1980 года, а средней оценкой фильмов выпущенных после 1980 года. (Убедитесь, что для расчета используете среднюю оценку для каждого фильма. Не просто среднюю оценку фильмов до и после 1980 года.) 

SELECT max(tmp2.stars) - min(tmp2.stars) as diff
FROM (
    SELECT avg(tmp1.stars) as stars
    FROM (
        SELECT avg(stars) as stars, mID
        FROM Rating
        GROUP BY mID
    ) AS tmp1
    JOIN Movie m ON tmp1.mID = m.mID
    GROUP BY m.year < 1980
) as tmp2;


__(+)__
// Для всех случаев когда один эксперт оценивал фильм дважды и указал лучший рейтинг второй раз, выведите имя эксперта и название фильма, отсортировав по имени, затем по названию фильма. 

SELECT name, title
FROM 
(SELECT rID, mID, max(stars) as max_stars, max(ratingDate) as max_ratingDate
    FROM Rating
    GROUP BY rID
    HAVING count(rID) = 2
) as tmp
JOIN Rating ra ON ra.rID = tmp.rID and ra.mID = tmp.mID
JOIN Movie m ON m.mID = tmp.mID
JOIN Reviewer re ON re.rID = tmp.rID
WHERE stars = max_stars AND ratingDate = max_ratingDate;

__(+)__
// Некоторые режиссеры сняли более чем один фильм. Для всех таких режиссеров, выбрать названия всех фильмов режиссера, его имя. Сортировка по имени режиссера. Пример: Titanic,Avatar | James Cameron 

SELECT
GROUP_CONCAT(DISTINCT title SEPARATOR ','), director
FROM Movie
GROUP BY director
HAVING count(*) > 1
ORDER BY director;


// Для каждого фильма, выбрать название и "разброс оценок", то есть, разницу между самой высокой и самой низкой оценками для этого фильма. Сортировать по "разбросу оценок" от высшего к низшему, и по названию фильма.

SELECT title, max(stars) - min(stars) AS diff
FROM Movie 
JOIN Rating ON Movie.mID = Rating.mID
GROUP BY title
ORDER BY diff DESC, title;


__(+)__
// Для каждого фильма, который имеет по крайней мере одну оценку, найти наибольшее количество звезд, которые фильм получил. Выбрать название фильма и количество звезд. Сортировать по названию фильма

SELECT title, max(stars)
FROM Movie 
JOIN Rating ON Movie.mID = Rating.mID
GROUP BY title
ORDER BY title;


__(+)__
// Напишите запрос возвращающий информацию о рейтингах в более читаемом формате: имя эксперта, название фильма, оценка и дата оценки.
// Отсортируйте данные по имени эксперта, затем названию фильма и наконец оценка 

SELECT name, title, stars, ratingDate
FROM Rating 
JOIN Reviewer ON Rating.rID = Reviewer.rID
JOIN Movie ON Movie.mID = Rating.mID
ORDER BY name, title, stars;


__(+)__
// Выбрать список названий фильмов и средний рейтинг, от самого низкого до самого высокого. Если два или более фильмов имеют одинаковый средний балл, перечислить их в алфавитном порядке 

SELECT title, avg(stars) as a
FROM Movie 
JOIN Rating ON Movie.mID = Rating.mID
GROUP BY title
ORDER BY a, title;


__(+)__
// Выберите всех экспертов и названия фильмов в едином списке в алфавитном порядке 

(SELECT name AS col FROM Reviewer)
UNION
(SELECT title AS col FROM Movie)
ORDER BY col;