import sqlite3

def get_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row  # So you can access rows as dicts like user['id']
    return conn
