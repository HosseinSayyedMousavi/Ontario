import sqlite3

# Connect to the database (create it if it doesn't exist)
conn = sqlite3.connect('OCP.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the 'book.cfi.ir' table with the specified fields
cursor.execute('''CREATE TABLE Pages (
                Rawdata JSON
)''')

# Commit the changes and close the connection
conn.commit()
conn.close()