
import mysql.connector
import requests

connection = None
cursor = None

try:
    req = requests.get('http://spotprices.energyecs.frostbit.fi/api/v1/prices')
    prices = req.json()
    connection = mysql.connector.connect(database='electricity_price', user='root')
    cursor = connection.cursor(prepared=True, dictionary=True)

    query = ("INSERT INTO prices(time, price) VALUES((%s), (%s))")

    # Execute query for each price row and save to database
    # prices = [{'_time': 'YYYY-MM-DDTHH:MM:SSZ', 'value': float}, ...]
    for price in prices:
        cursor.execute(query, (price['_time'], price['value']))

    connection.commit()    

    print("Viimeinen rivi on: ", cursor.lastrowid)

except Exception as e:
    print(e)
    connection.rollback()

finally:
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()


