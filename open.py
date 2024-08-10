import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('form_data.db')
cursor = conn.cursor()

# Execute a query
cursor.execute('SELECT * FROM form_data')

# Fetch and print results
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()