from flask import Flask
from flask import request
from flask import jsonify
import mysql.connector
from datetime import datetime
import re

app = Flask(__name__)

def getMysqlConnection():
    return mysql.connector.connect(
        #host="10.0.1.5",
        host="192.168.1.5",
        port='3306',
        user="root",
        password="SomeRootPassword1!",
        database="dev"
    )

@app.route('/', methods=['GET'])
def home():
    mydb = getMysqlConnection()
    status = 200
    try:
        sql = "SELECT * FROM key_value_table"
        cur = mydb.cursor()
        cur.execute(sql)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
        status = 500
    finally:
        mydb.close()
    return jsonify(output_json), status

@app.route('/<key>', methods=['PUT'])
def addKey(key):
    content = request.json
    value = content['value']
    mydb = getMysqlConnection()
    status = 201

    try:
        mycursor = mydb.cursor()
        sql = "INSERT INTO key_value_table (keyValue, value) VALUES (%s, %s)"
        val = (key, value)
        mycursor.execute(sql, val)
        mydb.commit()
    except Exception as e:
        print("Error in SQL:\n", e)
        status = 500
    finally:
        mydb.close()

    print(mycursor.rowcount, "record inserted.")
    return jsonify([key, value]), status

@app.route('/<key>', methods=['GET'])
def getKey(key):

    mydb = getMysqlConnection()
    status = 200
    try:
        sql = "SELECT * FROM key_value_table WHERE keyValue = %s"
        cur = mydb.cursor()
        cur.execute(sql, (key,))
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
        status = 500
    finally:
        mydb.close()
    return jsonify(output_json), status

@app.route('/<key>', methods=['DELETE'])
def deleteKey(key):

    mydb = getMysqlConnection()
    status = 200
    try:
        sql = "DELETE FROM key_value_table WHERE keyValue = %s"
        cur = mydb.cursor()
        cur.execute(sql, (key,))
        mydb.commit()
    except Exception as e:
        print("Error in SQL:\n", e)
        status = 500
    finally:
        mydb.close()
    return "", status

if __name__ == "__main__":
    app.run(debug=True)