from connection import connection

def find_by_type(type):
    try:
        with connection.cursor() as cursor:
            query = "select name from pokemon where type = '{}'".format(type)
            cursor.execute(query)
            result = cursor.fetchall()
            result = [i.get('name') for i in result]
            return result
    except:
        print("DB error")