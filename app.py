from flask import Flask, render_template, request, session, redirect, url_for, flash
from database import (get_menu_item, get_category, add_category, add_menu, delete_category, delete_menu,
                       add_table, update_table_qr, show_table, delete_table,table_exists, add_orders,
                         add_order_item, get_orders,booking, show_booking,show_upcoming_bk,show_today_bk,
                         done_order,order_history)
from werkzeug.utils import secure_filename
from qr_generator import generate_qr
import os
from functools import wraps  # import wraps tool

def login_required(f):       # f = the function below @login_required
    @wraps(f)                # keep original function name
    def decorated(*args, **kwargs):  # catch ALL arguments Flask passes
        if not session.get('logged_in'):  # check if logged in
            return redirect('/login')      # not logged in → send to login
        return f(*args, **kwargs)          # logged in → run the real function
    return decorated                       # return the wrapped function


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
@login_required
def admin():
     
     orders = get_orders()
     orders_history = order_history()
     
     return render_template('admin.html', orders=orders,orders_history=orders_history)



# book table route
@app.route('/book-table')
def book_table():
    tables = show_table()
    return render_template('booking.html', tables=tables)

@app.route('/add_booking', methods=['POST'])
def add_table():
    cs_name = request.form.get("customer_name")
    cs_phone = request.form.get("customer_phone")
    date = request.form.get("date")
    time = request.form.get("time")
    guest = request.form.get("guests")
    table = int(request.form.get("table_id"))

    booking(cs_name,cs_phone,date,time,guest,table)
    return redirect('/book-table')



# menu route
@app.route('/menu/<int:table_id>')
def menu(table_id):
        items = get_menu_item()
        categories = get_category()
        session['table_id'] = table_id
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
            return redirect(f"/menu/{session.get('table_id', 1)}")
    
    session['cart'].append({
        'id': id,
        'name': name,
        'price': price,
        'quantity': 1,
        'image': image
    })
    session.modified = True
    return redirect(f"/menu/{session.get('table_id', 1)}")
#//-------------------------------new line
@app.route('/place_order', methods=['POST'])
def place_order():

    table_id = session.get('table_id')
    
    cart = session.get('cart',[])
    total = sum(float(item['price']) * item['quantity'] for item in cart)
    order_id = add_orders(table_id,total)

    for item in cart:
        note = request.form.get(f"note_{item['id']}", '')
        add_order_item(order_id, item['id'], item['quantity'], item['price'],note)

    session.pop('cart', None)
    flash('Order placed successfully!')
    return redirect(f"/menu/{session.get('table_id', 1)}")
  


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

# ------------------------ADMIN---------------------------------------------

@app.route('/admin/category/add', methods=['POST'])
@login_required
def admin_add_category():
    name = request.form.get('cate_name')
    add_category(name)
    return redirect('/admin/menu')

@app.route('/admin/delete/category', methods=['POST'])
def admin_delete_category():
    id = request.form.get('category_id')
    delete_category(id)
    return redirect('/admin/menu')

@app.route('/admin/done_order/<int:id>')
def done(id):
    done_order(id)
    return redirect('/admin')


@app.route('/admin/menu/add',  methods=['POST'])
@login_required
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
@login_required
def admin_delete_menu():
    id = request.form.get('menu_id')
    delete_menu(id)
    return redirect('/admin/menu')


@app.route('/admin/menu')
@login_required
def admin_menu():
    categories = get_category()
    menus = get_menu_item()
    return render_template('admin_menu.html', categories=categories, menus=menus)


# admin manage table booking 
@app.route('/admin/show_bookings')
@login_required
def show_bookings():
    bookings = show_booking()
    upcomings = show_upcoming_bk()
    todays = show_today_bk()

    return render_template('admin_booking.html', bookings=bookings,upcomings=upcomings,todays=todays)


@app.route('/admin/add/table', methods=['POST'])
@login_required
def admin_add_table():
    table_number=request.form.get('table_number')

    if table_exists(table_number):
        flash('Table already exists!')

    table_id = add_table(table_number)
    path = generate_qr(table_id, table_number)
    update_table_qr(table_id, path)
    
    return redirect('/admin/add_table')


@app.route('/admin/add_table')
@login_required
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
