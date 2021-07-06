from connection import connection


# add a new pokemon to the pokemon table
def add_pokemon(id, name, height, weight, types):
    try:
        with connection.cursor() as cursor:
            cursor.execute("insert into pokemon(id, name, height, weight) values({}, '{}', {}, {})".format(id,name,height,weight))
            for i in range(len(types)):
                cursor.execute("insert into type(name, pokemon_id) values('{}', {})".format(types[i],id))
            connection.commit()
    except:
        return "DB Error"


# delete a pokemon from the pokemon table
def delete_pokemon(pokemon_name):
    try:
        with connection.cursor() as cursor:
            if cursor.execute("select * from pokemon where name=(%s)",(pokemon_name))==0:
                return "pokemon doesn't exist"
            cursor.execute("delete from type where pokemon_id = (select id from pokemon where name = '{}')".format(pokemon_name))
            cursor.execute("delete from pokemon where name = '{}'".format(pokemon_name))
            connection.commit()
    except:
        return "DB Error"


# finds all owners of given pokemon
def find_owners(pokemon_name):
    try:
        with connection.cursor() as cursor:
            if cursor.execute("select * from pokemon where name=(%s)",(pokemon_name))==0:
                return "pokemon doesn't exist"
            cursor.execute( "SELECT ownedBy.owner_name FROM pokemon JOIN ownedBy ON pokemon.id = ownedBy.pokemon_id where pokemon.name=(%s);",(pokemon_name))
            result = cursor.fetchall()
            return [i['owner_name'] for i in result]
    except:
        return "DB Error"


# finds all pokemons of given trainer
def find_roster(trainer_name):
    try:
        with connection.cursor() as cursor:
            if cursor.execute("select * from owner where name=(%s)",(trainer_name))==0:
                return "trainer doesn't exist"
            cursor.execute( "SELECT pokemon.name FROM pokemon JOIN ownedBy ON pokemon.id = ownedBy.pokemon_id where ownedBy.owner_name=(%s);",(trainer_name))
            result = cursor.fetchall()
            return [i['name'] for i in result]
    except:
        return "DB Error"


# find all pokemons with the given type
def find_by_type(type):
    try:
        with connection.cursor() as cursor:
            cursor.execute( "select pokemon.name FROM type join pokemon on pokemon.id=type.pokemon_id where type.name=(%s);",(type))
            result = cursor.fetchall()
            if not result:
                return "type does not exist"
            return [i['name'] for i in result]
    except:
        return "DB Error"



# updates the types of the given pokemon
def update_types(name,types):
    try:
        with connection.cursor() as cursor:
            cursor.execute( "SELECT id FROM pokemon where name=(%s)",(name))
            id=cursor.fetchall()[0].get('id')
            for i in types:
                cursor.execute("INSERT INTO type values(%s,%s)",(i,id))
            connection.commit()
            return True
    except:
        return False


# evolves the given pokemon
def evolve_pokemon(pokemon_name, trainer, evolves_to):
    try:
        with connection.cursor() as cursor:
            cursor.execute( "SELECT id FROM pokemon where name=(%s)",(evolves_to))
            evolves_id = cursor.fetchall()[0]['id']
            
            cursor.execute( "SELECT id FROM pokemon where name=(%s)",(pokemon_name))
            pokemon_id = cursor.fetchall()[0]['id']

            if cursor.execute( "SELECT * FROM owner where name=(%s)",(trainer))==0:
                return "trainer doesn't exist"

            cursor.execute("select * from ownedby where pokemon_id = (%s) and owner_name = (%s)", (pokemon_id, trainer ))
            does_exist = cursor.fetchall()
            if not does_exist:
                return "the owner does not have this pokemon"

            cursor.execute("select * from ownedby where pokemon_id = (%s) and owner_name = (%s)", (evolves_id, trainer ))
            has_evolve = cursor.fetchall()
            if has_evolve:
                return "evolved pokemon already exists"
            cursor.execute("UPDATE ownedBy SET pokemon_id =(%s)  where pokemon_id = (%s) and owner_name = (%s)", (evolves_id, pokemon_id, trainer ))
            connection.commit()
    except:
        return "DB Error"


# checks if the given pokemon exists in the pokemon table
def does_pokemon_exist(pokemon_name):
    try:
        with connection.cursor() as cursor:
            pokemon = cursor.execute( "SELECT '{}' FROM pokemon".format(pokemon_name))
            return pokemon != 0
    except:
        return "DB Error"


# finds the heaviest pokemon
def heaviest_pokemon():
    try:
        with connection.cursor() as cursor:
            cursor.execute( "select name from pokemon where weight = (SELECT MAX(weight) FROM pokemon);")
            result = cursor.fetchall()
            return result
    except:
        return "DB Error"


# finds the pokemon who has the most owners
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



