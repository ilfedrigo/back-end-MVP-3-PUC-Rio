from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
from datetime import datetime
from werkzeug.exceptions import UnsupportedMediaType
import sqlite3

app = Flask(__name__)
CORS(app)

def connect_db():
    return sqlite3.connect('store.db')

def initialize_db():
    with connect_db() as connection:
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS checkout (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_user INTEGER,
        updated_at DATE,
        total FLOAT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS store (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT NOT NULL,
        price FLOAT NOT NULL,
        id_checkout INTEGER,
        FOREIGN KEY (id_checkout) REFERENCES checkout(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        """)

        connection.commit()

@app.route('/')
@cross_origin()
def login_page():
    return render_template('login.html')

@app.route('/checkout', methods=['POST'])
@cross_origin() 
def checkout():
    if request.headers.get('Content-Type') != 'application/json':
        raise UnsupportedMediaType('Only JSON format is supported')
    data = request.get_json()
    updated_at = datetime.now().date()
    id_user = 1
    if data and 'cart' in data: 
        try:
            with connect_db() as connection:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO checkout (id_user, updated_at) VALUES (?, ?)", 
                               (id_user, updated_at))
                checkout_id = cursor.lastrowid
                total = 0
                for item in data['cart']:
                    total += item['price']
                    cursor.execute("INSERT INTO store (item, price, id_checkout) VALUES (?, ?, ?)",
                           (item['item'], item['price'], checkout_id))
                cursor.execute("UPDATE checkout SET total = ? WHERE id = ?", 
                               (total, id_user))
                connection.commit()
                print(total)
                return jsonify({'message': 'Items added to the database successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid data format or no cart data received'}), 400

@app.route('/orders', methods=['GET'])
@cross_origin()
def orders():
    try:
        with connect_db() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, item, price FROM store")
            items = cursor.fetchall()
            item_list = [{'id': row[0], 'item': row[1], 'price': row[2]} for row in items]
            return jsonify(item_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/orders/<int:item_id>', methods=['DELETE'])
@cross_origin()
def delete_order(item_id):
    try:
        with connect_db() as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM store WHERE id = ?", (item_id,))
            connection.commit()
            return jsonify({'message': f'Item with id {item_id} deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/orders/<int:item_id>', methods=['PUT'])
@cross_origin()
def edit_order(item_id):
    data = request.get_json()
    if not data or ('item' not in data and 'price' not in data):
        return jsonify({'error': 'Invalid data format or no data received for update'}), 400

    try:
        with connect_db() as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE store SET item = ?, price = ? WHERE id = ?", (data.get('item'), data.get('price'), item_id))
            connection.commit()
            return jsonify({'message': f'Item with id {item_id} updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/login', methods=['POST'])
@cross_origin()
def login():    
    data = request.get_json() 
    username = data.get('username')
    password = data.get('password')
    
    try:
        with connect_db() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            user = cursor.fetchone()

            if user:
                if user[2] == password:
                    return jsonify({'success': True, 'redirect': 'admin.html' if user[1] == 'admin' else 'index.html'})
                else:
                    return jsonify({'success': False, 'message': 'Senha incorreta'}), 401
            else:
                return jsonify({'success': False, 'message': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/signup', methods=['POST'])
@cross_origin()
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    try:
        with connect_db() as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            connection.commit()
            return jsonify({'success': True, 'message': 'User created successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'message': 'Username already exists'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    initialize_db()
    app.run(host='0.0.0.0', port=5000)

