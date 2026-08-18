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

def add_order_item(order_id,menu_item_id,quantity,price,note):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('insert into order_item(order_id, menu_item_id, quantity, price_at_order,note) values (?,?,?,?,?)', (order_id,menu_item_id,quantity,price,note))
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

def done_order(order_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('update orders set status = "done" where id = ?',(order_id,))
    conn.commit()
    conn.close()


def order_history():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('select * from orders where orders.status = "done" and date(orders.created_at) = date("now")')
    order_hist = cursor.fetchall()
    conn.close()
    return order_hist

def get_orders():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT orders.id, orders.table_id, orders.status, orders.total_amount,
               order_item.quantity, order_item.price_at_order,order_item.note,
               menu_item.name
        FROM orders
        JOIN order_item ON orders.id = order_item.order_id
        JOIN menu_item ON order_item.menu_item_id = menu_item.id
        WHERE orders.status = "pending"
    ''')
    rows = cursor.fetchall()
    conn.close()
    
    # group by order_id
    orders = {}
    for row in rows:
        order_id = row['id']
        if order_id not in orders:
            orders[order_id] = {
                'id': row['id'],
                'table_id': row['table_id'],
                'status': row['status'],
                'total_amount': row['total_amount'],
                'items': []
            }
        orders[order_id]['items'].append({
            'name': row['name'],
            'quantity': row['quantity'],
            'price': row['price_at_order'],
            'note': row['note']
        })
    
    return list(orders.values())

def delete_table(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('delete from restaurant_table where id = ?', (id,))
    conn.commit()
    conn.close()

def booking(name,phone,date,time,guest,table_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('insert into booking(customer_name,customer_phone,date,time,guests,table_id) values (?,?,?,?,?,?)', (name,phone,date,time,guest,table_id))
    conn.commit()
    conn.close()

def show_booking():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM booking')
    bookings = cursor.fetchall()
    conn.close()
    return bookings

def show_today_bk():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM booking WHERE date = date('now')")
    today_bookings = cursor.fetchall()
    conn.close()
    return today_bookings

def show_upcoming_bk():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM booking WHERE date > date('now')")
    upcoming_bookings = cursor.fetchall()
    conn.close()
    return upcoming_bookings

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

