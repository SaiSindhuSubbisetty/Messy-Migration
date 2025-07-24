import sqlite3
from utils.security import hash_password  # make sure the path is correct

# Connect to the SQLite database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# Sample users with hashed passwords
users = [
    ('John Doe', 'john@example.com', hash_password('password123')),
    ('Jane Smith', 'jane@example.com', hash_password('secret456')),
    ('Bob Johnson', 'bob@example.com', hash_password('qwerty789')),
]

# Insert users
cursor.executemany("INSERT OR IGNORE INTO users (name, email, password) VALUES (?, ?, ?)", users)

conn.commit()
conn.close()

print("Database initialized with hashed sample data.")
