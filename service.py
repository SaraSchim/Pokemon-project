from connection import connection

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
            cursor.execute( "SELECT name FROM pokemon where type=(%s);",(type))
            result = cursor.fetchall()
            return result
    except:
        print("Error")

def find_owners(pokemon_name):
    try:
        with connection.cursor() as cursor:
            cursor.execute( "SELECT ownedBy.owner_name FROM pokemon JOIN ownedBy ON pokemon.id = ownedBy.pokemon_id where pokemon.name=(%s);",(pokemon_name))
            result = cursor.fetchall()
            return result
    except:
        print("Error")

def find_roster(trainer_name):
    try:
        with connection.cursor() as cursor:
            cursor.execute( "SELECT pokemon.name FROM pokemon JOIN ownedBy ON pokemon.id = ownedBy.pokemon_id where ownedBy.owner_name=(%s);",(trainer_name))
            result = cursor.fetchall()
            return result
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
            return result
    except:
        print("Error")




