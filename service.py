from typing import Coroutine

from pymysql.cursors import Cursor
from connection import connection

def add_pokemon(id, name, height, weight, types):
    try:
        with connection.cursor() as cursor:
            cursor.execute("insert into pokemon(id, name, height, weight) values({}, '{}', {}, {})".format(id,name,height,weight))
            for i in range(len(types)):
                cursor.execute("insert into type(name, pokemon_id) values('{}', {})".format(types[i],id))
            connection.commit()
    except:
        print("DB Error")



def delete_pokemon(pokemon_name):
    try:
        with connection.cursor() as cursor:
            cursor.execute("delete from type where pokemon_id = (select id from pokemon where name = '{}')".format(pokemon_name))
            cursor.execute("delete from pokemon where name = '{}'".format(pokemon_name))
            connection.commit()
    except:
        print("DB Error")


def heaviest_pokemon():
    try:
        with connection.cursor() as cursor:
            cursor.execute( "select name from pokemon where weight = (SELECT MAX(weight) FROM pokemon);")
            result = cursor.fetchall()
            return result
    except:
        print("DB Error")


def find_by_type(type):
    try:
        with connection.cursor() as cursor:
            cursor.execute( "select pokemon.name FROM type join pokemon on pokemon.id=type.pokemon_id where type.name=(%s);",(type))
            result = cursor.fetchall()
            return [i['name'] for i in result]
    except:
        print("Error")



def find_owners(pokemon_name):
    try:
        with connection.cursor() as cursor:
            cursor.execute( "SELECT ownedBy.owner_name FROM pokemon JOIN ownedBy ON pokemon.id = ownedBy.pokemon_id where pokemon.name=(%s);",(pokemon_name))
            result = cursor.fetchall()
            return [i['owner_name'] for i in result]
    except:
        print("Error")



def find_roster(trainer_name):
    try:
        with connection.cursor() as cursor:
            cursor.execute( "SELECT pokemon.name FROM pokemon JOIN ownedBy ON pokemon.id = ownedBy.pokemon_id where ownedBy.owner_name=(%s);",(trainer_name))
            result = cursor.fetchall()
            return [i['name'] for i in result]
    except:
        print("Error")


def finds_most_owned():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT pokemon.name\
                FROM ownedBy JOIN pokemon on ownedBy.pokemon_id = pokemon.id\
                where ownedBy.pokemon_id in\
                    (select pokemon_id from ownedBy group by pokemon_id\
                        having count(pokemon_id) = (select count(pokemon_id) as c\
                            from ownedBy group by pokemon_id order by c desc limit 1))")
            result = cursor.fetchall()
            return [i['name'] for i in result]

    except:
        print("Error")



def update_types(name,types):
    try:
        with connection.cursor() as cursor:
            for i in types:
                cursor.execute( "SELECT id FROM pokemon where name=(%s)",(name))
                id=cursor.fetchall()[0].get('id')
                cursor.execute("INSERT INTO type values(%s,%s)",(i,id))
            connection.commit()
            return True
    except:
        return False


def evolve_pokemon(pokemon_name, trainer, evolves_to):
    try:
        with connection.cursor() as cursor:
            cursor.execute( "SELECT id FROM pokemon where name=(%s)",(evolves_to))
            evolves_id = cursor.fetchall()[0]['id']
            
            cursor.execute( "SELECT id FROM pokemon where name=(%s)",(pokemon_name))
            pokemon_id = cursor.fetchall()[0]['id']
            cursor.execute("select * from ownedby where pokemon_id = (%s) and owner_name = (%s)", (pokemon_id, trainer ))
            does_exist = cursor.fetchall()
            if not does_exist:
                return False
            cursor.execute("select * from ownedby where pokemon_id = (%s) and owner_name = (%s)", (evolves_id, trainer ))
            has_evolve = cursor.fetchall()
            if has_evolve:
                return True
            cursor.execute("UPDATE ownedBy SET pokemon_id =(%s)  where pokemon_id = (%s) and owner_name = (%s)", (evolves_id, pokemon_id, trainer ))
            connection.commit()
            return True
    except:
        return False


def does_pokemon_exist(pokemon_name):
    try:
        with connection.cursor() as cursor:
            pokemon = cursor.execute( "SELECT '{}' FROM pokemon".format(pokemon_name))
            return pokemon != 0
    except:
        print("Error")


