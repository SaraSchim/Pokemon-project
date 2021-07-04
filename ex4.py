from connection import connection


def find_roster(trainer_name):
    try:
        with connection.cursor() as cursor:
            query = "select name from pokemon join ownedBy on pokemon.id = ownedBy.pokemon where owner = '{}'".format(
                trainer_name)
            cursor.execute(query)
            result = cursor.fetchall()
            result = [i.get('name') for i in result]
            return result
    except:
        print("DB error")
