-- In 10.sql, write a SQL query to list the names of all people who have directed a movie that received a rating of at least 9.0.

SELECT name FROM people, directors, movies, ratings WHERE people.id = directors.person_id AND movies.id = directors.movie_id AND ratings.movie_id = movies.id AND rating >= 9 GROUP BY name;
