import mysql.connector

dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="matplotlib15"
)

#prepare cursor object
cursorObject = dataBase.cursor()

#create database
cursorObject.execute("CREATE DATABASE IF NOT EXISTS company")

print("All Done!")