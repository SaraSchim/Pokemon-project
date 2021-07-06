use pokemon;

create table owner(
    name varchar(20) PRIMARY KEY,
    town varchar(20)
);


create table pokemon(
    id int PRIMARY KEY,
    name varchar(20),
    height int,
    weight int
);


create table type(
    name varchar(20),
    pokemon_id int,
    primary key(name, pokemon_id),
    FOREIGN KEY(pokemon_id) REFERENCES pokemon(id)
);


create table ownedBy(
    pokemon_id int,
    owner_name varchar(20),
    primary key(pokemon_id,owner_name),
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(id),
    FOREIGN KEY (owner_name) REFERENCES owner(name)
);
