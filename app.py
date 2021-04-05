from flask import Flask, render_template,request, redirect, url_for
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('database.db',  check_same_thread=False)

# data = conn.execute("SELECT * FROM Persons")

# print(data)

# for i in data:
#     print(i)



@app.route('/')
def hello_world():
    data = conn.execute("SELECT * FROM Category")
    return render_template('index.html', categories=data)

@app.route('/admin')
def admin():
    conn = sqlite3.connect('database.db')
    data = conn.execute("SELECT * FROM food")
    return render_template('admin.html',categories=data)

@app.route('/forms', methods=['GET', 'POST'])
def forms():
    if request.method == "POST":
        conn = sqlite3.connect('database.db')
        itemName = request.form.get('item-name')
        price = request.form.get('price')
        category = request.form.get('category')
        conn.execute("INSERT INTO food (name,price,category) VALUES (?,?,?)", (itemName,price,category,) )
        conn.commit()
        return redirect(url_for('admin'))
    conn = sqlite3.connect('database.db')
    data = conn.execute("SELECT * FROM Category")
    return render_template('forms.html',categories=data)

@app.route('/category', methods=['GET', 'POST'])
def categoryForm():
    if request.method == "POST":
        conn = sqlite3.connect('database.db')
        category = request.form.get('category')        
        conn.execute("INSERT INTO Category (category) VALUES (?)", (category,) )
        conn.commit()
        return render_template('admin.html')
    return render_template('category-form.html')

@app.route('/menu/<name>')
def menu(name):
    conn = sqlite3.connect('database.db')
    menu = conn.execute("SELECT * FROM food where category = ?",[name])
    return render_template('menu.html',menu = menu)

@app.route('/cart/<name>', methods=['GET', 'POST'])
def cart(name):
    conn = sqlite3.connect('database.db')
    menu = conn.execute("SELECT * FROM food where name = ?",[name])
    for i in menu:
        item = i[0]
        price = i[1]
    conn.execute("INSERT INTO cart (item,price) VALUES (?,?)", (item,price) )
    conn.commit()
    data = conn.execute("SELECT * FROM cart")
    return render_template('cart.html', data = data)

@app.route('/buy')
def buy():
    return render_template('buy.html')