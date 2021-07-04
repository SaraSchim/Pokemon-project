use pokemon;

drop table ownedBy;
drop table pokemon;
drop table owner;

create table owner(
    name varchar(20),
    town varchar(20),
    primary key(name)
);


create table pokemon(
    id int primary key,
    name varchar(20),
    type varchar(20),
    height int,
    weight int
);


create table ownedBy(
    pokemon int,
    owner varchar(20),
    primary key(pokemon, owner),

    foreign key (pokemon) references pokemon(id),
    foreign key (owner) references owner(name)
);

