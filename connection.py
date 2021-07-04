import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="SH6520653",
    db="pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

