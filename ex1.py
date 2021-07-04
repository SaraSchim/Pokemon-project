from connection import connection


def heaviest_pokemon():
    try:
        with connection.cursor() as cursor:
            cursor.execute("select name from pokemon where weight = (SELECT MAX(weight) FROM pokemon);")
            result = cursor.fetchall()
            return result
    except:
        print("DB Error")
