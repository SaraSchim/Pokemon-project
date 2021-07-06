from connection import connection
import json

def insert():
    try:
        with open("pokemon_data.json","r") as pokemon:
            poekmon_list = json.load(pokemon)
        for i in poekmon_list:
                with connection.cursor() as cursor:
                    cursor.execute( "INSERT INTO pokemon values(%s,%s,%s,%s);",(i["id"],i["name"],i["height"],i["weight"]))
                    for j in i["ownedBy"]:
                        
                        if cursor.execute( "select name from owner where name=(%s);",(j["name"]))==0:
                            cursor.execute( "INSERT INTO owner values(%s,%s);",(j["name"],j["town"]))
                        cursor.execute( "INSERT INTO ownedBy values(%s,%s);",(i["id"],j["name"]))
                    connection.commit()
    except:
        print("Error")
insert()