
import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="iam18leah",
    db="pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)