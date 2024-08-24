import mysql.connector
# Replace these with your actual credentials
host = "localhost"
database = "proctorbook"
user = "root"
password = "violin123"

try:
    # Connect to the database
    connection = mysql.connector.connect(host=host, database=database, user=user, password=password)

    print("Successfully connected to the MySQL database!")

except mysql.connector.Error as err:
    print("Error connecting to the database:", err)
