from connection import connection

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


