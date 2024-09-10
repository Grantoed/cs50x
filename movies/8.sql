-- In 8.sql, write a SQL query to list the names of all people who starred in Toy Story.

SELECT name FROM movies, people, stars WHERE movies.id = stars.movie_id AND people.id = stars.person_id AND movies.title = 'Toy Story';
