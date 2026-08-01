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

def get_category():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('select * from category')
    categories = cursor.fetchall()
    conn.close()
    return categories



def get_connection():
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    
    return conn

def add_category(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('insert into category (name) values (?)', (name,))
    conn.commit()
    conn.close()

def delete_category(idd):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM category WHERE id=(?)', (idd,))
    conn.commit()
    conn.close()

def add_menu(name,description,price,category_id,image_path):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('insert into menu_item(name, description, price, category_id, image_path) values (?,?,?,?,?)',
                   (name, description, price, category_id, image_path))
    conn.commit()
    conn.close()

def delete_menu(idd):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('delete from menu_item where id =(?)', (idd,))
    conn.commit()
    conn.close()

def add_table(table_number):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('insert into restaurant_table(table_number) values (?)', (table_number,))
    conn.commit()
    table_id = cursor.lastrowid
    conn.close()
    return table_id

def add_orders(table_id,total_amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('insert into orders(table_id, total_amount) values (?,?)', (table_id, total_amount))
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return order_id

def add_order_item(order_id,menu_item_id,quantity,price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('insert into order_item(order_id, menu_item_id, quantity, price_at_order) values (?,?,?,?)', (order_id,menu_item_id,quantity,price))
    conn.commit()
    conn.close()


def update_table_qr(table_id,path):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE restaurant_table SET qr_image_path = ? WHERE id = ?', (path, table_id))
    conn.commit()
    conn.close()

def show_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('select * from restaurant_table ')
    tables = cursor.fetchall()
    conn.close()
    return tables

def delete_table(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('delete from restaurant_table where id = ?', (id,))
    conn.commit()
    conn.close()


def table_exists(table_number):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM restaurant_table WHERE table_number = ?', (table_number,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def get_menu_item():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('select * from menu_item')
    items = cursor.fetchall()
    conn.close()
    return items

