from flask import Flask, render_template, request, session, redirect, url_for, flash
from database import get_menu_item, get_category, add_category, add_menu, delete_category, delete_menu, add_table, update_table_qr, show_table, delete_table,table_exists
from werkzeug.utils import secure_filename
from qr_generator import generate_qr
import os

app = Flask(__name__)

app.secret_key = 'x7k#mP9$qL2nR5vW'  # Replace with a real secret key

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

@app.route('/')
def index():
    return render_template('index.html')

# login route
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
         username = request.form['username']
         password = request.form['password']
         if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
             session['logged_in'] = True
             return redirect('admin')
         else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')



# admin page route, 
@app.route('/admin')
def admin():
     print("session:", session)
     if not session.get('logged_in'):
         return redirect('login.html')
     return render_template('admin.html')

# book table route
@app.route('/book-table')
def book_table():
    return render_template('book-table.html')

# menu route
@app.route('/menu')
def menu():
        items = get_menu_item()
        categories = get_category()
        return render_template('menu.html', items=items,categories=categories, error="No menu items found" if not items else None)

# add cart
@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    id = request.form.get('item_id')
    name = request.form.get('item_name')
    price = request.form.get('item_price')
    image = request.form.get('item_image')
    
    if 'cart' not in session:
        session['cart'] = []

    for item in session['cart']:
        if item['id'] == id:
            flash('Item already in cart! Change quantity from cart.')
            session.modified = True
            return redirect('/menu')
    
    session['cart'].append({
        'id': id,
        'name': name,
        'price': price,
        'quantity': 1,
        'image': image
    })
    session.modified = True
    return redirect('/menu')

@app.route('/cart/increase/<item_id>')
def increase_quantity(item_id):
    for item in session['cart']:
        if item['id'] == item_id:
            # increase quantity by 1
            item['quantity'] += 1
            # set session.modified
            session.modified = True
            break
    return redirect('/cart')

@app.route('/cart/decrease/<item_id>')
def decrease_quantity(item_id):
    for item in session['cart']:
        if item['id'] == item_id:
            item['quantity'] -= 1
            if item['quantity'] == 0:
                session['cart'].remove(item)
            break
    session.modified = True
    return redirect('/cart')

@app.route('/cart')
def cart_page():
    # get cart from session
    cart = session.get('cart',[])
    total = sum(float(item['price']) * item['quantity'] for item in cart)
    # pass it to cart.html
    return render_template('cart.html', cart=cart,total=total)


@app.route('/admin/category/add', methods=['POST'])
def admin_add_category():
    name = request.form.get('cate_name')
    add_category(name)
    return redirect('/admin/menu')

@app.route('/admin/delete/category', methods=['POST'])
def admin_delete_category():
    id = request.form.get('category_id')
    delete_category(id)
    return redirect('/admin/menu')

@app.route('/admin/menu/add',  methods=['POST'])
def admin_add_menu():
    name = request.form.get('menu_name')
    description = request.form.get('description')
    price = request.form.get('price')
    category = request.form.get('category')
    image = request.files['image_path']
    filename = secure_filename(image.filename)
    image.save(os.path.join('static/images', filename))
    image_path = '/static/images/' + filename 

    add_menu(name,description,price,category,image_path)
    return redirect('/admin/menu')

@app.route('/admin/delete/menu', methods=['POST'])
def admin_delete_menu():
    id = request.form.get('menu_id')
    delete_menu(id)
    return redirect('/admin/menu')


@app.route('/admin/menu')
def admin_menu():
    categories = get_category()
    menus = get_menu_item()
    return render_template('admin_menu.html', categories=categories, menus=menus)

@app.route('/admin/add/table', methods=['POST'])
def admin_add_table():
    table_number=request.form.get('table_number')

    if table_exists(table_number):
        flash('Table already exists!')

    table_id = add_table(table_number)
    path = generate_qr(table_id, table_number)
    update_table_qr(table_id, path)
    
    return redirect('/admin/add_table')


@app.route('/admin/add_table')
def admin_table():
    tables = show_table()
    return render_template("add_table.html", tables=tables)

@app.route('/admin/delete/table/<int:id>')
def admin_delete_tb(id):
    delete_table(id)

    return redirect('/admin/add_table')



@app.route('/clear')
def clear():
    session.clear()
    return redirect('/menu')


# logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
