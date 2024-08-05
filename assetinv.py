import mysql.connector
from mysql.connector import Error

'''
CREATE TABLE `scorecard`.`assetinv` (
  `hostname` VARCHAR(32) NOT NULL DEFAULT '',
  `ip` VARCHAR(15) NOT NULL DEFAULT '');
'''

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='tethys',
            database='scorecard',
            user='scorecard',
            password='scorecard'
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def insert_records(connection, hostname, ip):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO assetinv (hostname, ip) VALUES (%s, %s)"
        cursor.execute(query, (hostname, ip))
    except Error as e:
        print(f"Error: {e}")

def main():
    connection = connect_to_database()
    query = "INSERT INTO assetinv (hostname, ip) VALUES (%s, %s)"
    if connection is None:
        return

    try:
        with open('assetexport.csv', 'r') as file:
            lines = file.readlines()
            count = 0
            cursor = connection.cursor()
            for line in lines:
                hostname, ip = line.strip().split(',')
#                insert_records(connection, hostname, ip)
                cursor.execute(query, (hostname, ip))
                count += 1

                if count % 100 == 0:
                    connection.commit()
                    print(f"Committed 100 records")

            # Final commit and cleanup
            connection.commit()
            print(f"Final commit executed: ${count}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    main()