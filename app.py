from flask import Flask
from flask import request
import mysql.connector
from datetime import datetime
import re

app = Flask(__name__)

def getMysqlConnection():
    return mysql.connector.connect(
        host="10.0.1.5",
        port='3306',
        user="root",
        password="SomeRootPassword1!",
        database="dev"
    )

@app.route('/', methods=['GET'])
def home():
    mydb = getMysqlConnection()
    try:
        sql = "SELECT * from key_value_table"
        cur = mydb.cursor()
        cur.execute(sql)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        mydb.close()
    return jsonify(results=output_json)

@app.route('/<key>', methods=['PUT'])
def addKey(key):
    content = request.json
    value = content['value']

    mydb = getMysqlConnection()
    mycursor = mydb.cursor()
    sql = "INSERT INTO key_value_table (keyValue, value) VALUES (%s, %s)"
    val = (key, value)
    mycursor.execute(sql, val)
    mydb.commit()
    mydb.close()

    print(mycursor.rowcount, "record inserted.")
    return "Add key value pair"

@app.route('/<key>', methods=['GET'])
def getKey(key):
    print(key, flush=True)
    return "Return key value pair " + key

@app.route('/<key>', methods=['DELETE'])
def deleteKey(key):
    return "Delete all key value pairs"

if __name__ == "__main__":
    app.run(debug=True)