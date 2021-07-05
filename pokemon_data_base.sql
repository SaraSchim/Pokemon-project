use pokemon;
select * from type;
select * from pokemon;
select * from owner;
-- delete from type where name = "aa"
-- delete from type where pokemon_id = (select id from pokemon where name = 'aa');
-- insert into type(name, pokemon_id) values("aa", 15 )
-- select * from pokemon where name = "aaa"

-- insert into pokemon(id, name, height, weight) values(1111, "aaa", 10,20)



-- create table owner(
--     name varchar(20) PRIMARY KEY,
--     town varchar(20)
-- );


-- create table pokemon(
--     id int PRIMARY KEY,
--     name varchar(20),
--     height int,
--     weight int
-- );

-- create table type(
--     name varchar(20),
--     pokemon_id int,
--     primary key(name,pokemon_id),
--     FOREIGN KEY(pokemon_id) REFERENCES pokemon(id)
-- );
-- create table ownedBy(
--     pokemon_id int,
--     owner_name varchar(20),
--     primary key(pokemon_id,owner_name),
--     FOREIGN KEY (pokemon_id) REFERENCES pokemon(id),
--     FOREIGN KEY (owner_name) REFERENCES owner(name)
-- );

