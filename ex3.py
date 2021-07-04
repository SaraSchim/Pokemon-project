from connection import connection

def find_owners(pokemon_name):
    try:
        with connection.cursor() as cursor:
            cursor.execute( "SELECT ownedBy.owner_name FROM pokemon JOIN ownedBy ON pokemon.id = ownedBy.pokemon_id where pokemon.name=(%s);",(pokemon_name))
            result = cursor.fetchall()
            return result
    except:
        print("DB Error")

