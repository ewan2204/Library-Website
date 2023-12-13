# Should be ran to setup the sqlite database with tables
import sqlite3

conn = sqlite3.connect('database.db')

print ("Opened database successfully")
# Clear Database
conn.execute("PRAGMA writable_schema = 1;")
conn.execute("delete from sqlite_master where type in ('table', 'index', 'trigger');")
conn.execute("PRAGMA writable_schema = 0;")

conn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, email TEXT, password TEXT)')
conn.execute('CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT, description TEXT, image_location TEXT)')
conn.execute('CREATE TABLE book_loans (book_id INTEGER, user_id INTEGER, start TIMESTAMP, end TIMESTAMP)')
print ("Table created successfully")

conn.commit()
conn.close()