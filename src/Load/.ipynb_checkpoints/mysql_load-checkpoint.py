import mysql.connector
from sqlalchemy import create_engine
import pandas as pd

# Pour se connecter à mysql via mysql.connector
# https://www.kaggle.com/code/dilarabr/writing-pandas-dataframe-to-mysql
try:
    mydb = mysql.connector.connect(
        host="mysql",
        user="root",
        password="Password")
    print("Connection established")
    cursor = mydb.cursor()
    cursor.execute("create database if not exists new_db")
    mydb.commit()
    print("Database created successfully")
    cursor.execute("use new_db")
except mysql.connector.Error as err:
    print("An error occurred:", err)

# READ data extracted previously from the website Capterra and transformed
df = pd.read_csv("../../data_csv/capterra.csv")

# CREATE engine
hostname= "mysql"
database= "new_db"
username= "root"
password= "Password"
engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(host=hostname, db=database, user=username, pw=password))

# Load data into mysql
df.to_sql('table1', engine, if_exists='replace', index=False)

# READ data in from mysql
cursor.execute("use new_db")
cursor.execute('''  SELECT * from table1 ''')
rows = cursor.fetchall()
print("The last value of the first row is: {}".format(rows[0][-1]))
