from flask import Flask, render_template, request, session, redirect, url_for
from database import get_menu_item, get_category

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


# logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
