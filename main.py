from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def connect_db():
    return sqlite3.connect('store.db')

def initialize_db():
    with connect_db() as connection:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS store (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            price FLOAT NOT NULL,
            item TEXT NOT NULL,
            category TEXT NOT NULL
        )
        """)
        connection.commit()

@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.get_json()  # Recebe os dados enviados pelo front-end
    if data and 'cart' in data:  # Verifica se 'cart' está presente nos dados recebidos
        try:
            with connect_db() as connection:
                cursor = connection.cursor()
                for item in data['cart']:
                    cursor.execute("INSERT INTO store (price, item, category) VALUES (?, ?, ?)",
                                   (item['price'], item['item'], item['category']))
                connection.commit()
                return jsonify({'message': 'Items added to the database successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid data format or no cart data received'}), 400

if __name__ == '__main__':
    initialize_db()  # Inicializa o banco de dados
    app.run(debug=True)
