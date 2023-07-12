create table movies (
    id bigserial primary key,
    title varchar(50) not null,
    director varchar(50) not null,
    genre varchar(30)[] not null,
    runtime integer not null,
    imdb_rating double precision not null,
    release_year integer not null
);

insert into movies (title, director, genre, runtime, imdb_rating, release_year) values 
    ('Joker', 'Todd Phillips', '{Crime, Drama, Thriller}', 122, 8.5, 2019),
    ('Gladiator', 'Ridley Scott', '{Action, Adventure, Drama}', 155, 8.5, 2000),
    ('Spider-Man: Into the Spider-Verse', 'Bob Persichetti', '{Animation, Action, Adventure}', 117, 8.4, 2018);
