import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database='hakimqt',
    charset='utf8',
    use_unicode=True)

mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE if not exists hakimqt")


mycursor.execute("CREATE TABLE IF NOT EXISTS students (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), code VARCHAR(255), role VARCHAR(255), lessons VARCHAR(255), img VARCHAR(255))")