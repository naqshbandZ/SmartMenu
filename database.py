import sqlite3

def get_connection():
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

def get_menu_item():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('select * from menu_item')
    items = cursor.fetchall()
    conn.close()
    return items

import sqlite3 

def get_connection():
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    
    return conn

def get_menu_item():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('select * from menu_item')
    items = cursor.fetchall()
    conn.close()
    return items