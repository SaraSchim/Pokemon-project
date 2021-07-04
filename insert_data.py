import json
from connection import connection

def insert_data():
    with open("pokemon_data.json", "r") as pok_data:
        data = json.load(pok_data)
        try:
            with connection.cursor() as cursor:
                for pok in data:
                    query1 = "insert into pokemon(id, name, type, height, weight) values({},'{}','{}',{},{})".format(pok.get('id'), pok.get('name'), pok.get('type'), pok.get('height'), pok.get('weight'))
                    cursor.execute(query1)
                    for owner in pok.get('ownedBy'):
                        query2 = "insert into owner(name, town) select '{}','{}' where not EXISTS (select * from owner where name = '{}')".format(owner.get("name"), owner.get("town"), owner.get("name"), owner.get("town"))
                        cursor.execute(query2)
                        print("q2")
                        query3 = "insert into ownedBy(pokemon, owner) values('{}', '{}')".format(pok.get('id'), owner.get('name'))
                        cursor.execute(query3)
                        print("q3")
                    print("hi")
                    connection.commit()
        except:
            print("DB error")
