from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

def initialize_database():
    with sqlite3.connect('chocolate_database.db') as connection:
        connection.execute('''CREATE TABLE IF NOT EXISTS seasonal_flavors (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                flavor TEXT NOT NULL UNIQUE)''')
        connection.execute('''CREATE TABLE IF NOT EXISTS ingredient_inventory (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                ingredient TEXT NOT NULL UNIQUE,
                                stock INTEGER NOT NULL CHECK(stock >= 0))''')
        connection.execute('''CREATE TABLE IF NOT EXISTS customer_suggestions (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                flavor TEXT NOT NULL,
                                allergy_concerns TEXT)''')
        connection.commit()

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/add_flavor', methods=['GET', 'POST'])
def add_flavor():
    if request.method == 'POST':
        new_flavor_name = request.form.get('flavor')
        if not new_flavor_name:
            return render_template('add_flavor.html', error='Flavor name cannot be empty')

        with sqlite3.connect('chocolate_database.db') as connection:
            cursor = connection.execute("SELECT * FROM seasonal_flavors WHERE flavor = ?", (new_flavor_name,))
            if cursor.fetchone():
                return render_template('add_flavor.html', error='Flavor already exists')

            connection.execute("INSERT INTO seasonal_flavors (flavor) VALUES (?)", (new_flavor_name,))
            connection.commit()
        return render_template('add_flavor.html', message='Flavor added successfully')

    return render_template('add_flavor.html')

@app.route('/list_flavors')
def list_flavors():
    with sqlite3.connect('chocolate_database.db') as connection:
        cursor = connection.execute("SELECT * FROM seasonal_flavors")
        flavor_list = [{'id': row[0], 'flavor': row[1]} for row in cursor.fetchall()]
    return render_template('list_flavors.html', flavors=flavor_list)

@app.route('/delete_flavor/<int:flavor_id>', methods=['POST'])
def delete_flavor(flavor_id):
    with sqlite3.connect('chocolate_database.db') as connection:
        connection.execute("DELETE FROM seasonal_flavors WHERE id = ?", (flavor_id,))
        connection.commit()
    return redirect(url_for('list_flavors'))

@app.route('/add_ingredient', methods=['GET', 'POST'])
def add_ingredient():
    if request.method == 'POST':
        ingredient_name = request.form.get('ingredient')
        ingredient_stock = request.form.get('stock')
        if not ingredient_name or ingredient_stock is None:
            return render_template('add_ingredient.html', error='Ingredient name and stock are required')

        with sqlite3.connect('chocolate_database.db') as connection:
            cursor = connection.execute("SELECT * FROM ingredient_inventory WHERE ingredient = ?", (ingredient_name,))
            if cursor.fetchone():
                return render_template('add_ingredient.html', error='Ingredient already exists')

            connection.execute("INSERT INTO ingredient_inventory (ingredient, stock) VALUES (?, ?)", 
                               (ingredient_name, ingredient_stock))
            connection.commit()
        return render_template('add_ingredient.html', message='Ingredient added successfully')

    return render_template('add_ingredient.html')

@app.route('/list_ingredients')
def list_ingredients():
    with sqlite3.connect('chocolate_database.db') as connection:
        cursor = connection.execute("SELECT * FROM ingredient_inventory")
        ingredient_list = [{'id': row[0], 'ingredient': row[1], 'stock': row[2]} for row in cursor.fetchall()]
    return render_template('list_ingredients.html', ingredients=ingredient_list)

@app.route('/delete_ingredient/<int:ingredient_id>', methods=['POST'])
def delete_ingredient(ingredient_id):
    with sqlite3.connect('chocolate_database.db') as connection:
        connection.execute("DELETE FROM ingredient_inventory WHERE id = ?", (ingredient_id,))
        connection.commit()
    return redirect(url_for('list_ingredients'))

@app.route('/add_suggestion', methods=['GET', 'POST'])
def add_suggestion():
    if request.method == 'POST':
        customer_name = request.form.get('name')
        suggested_flavor = request.form.get('flavor')
        if not customer_name or not suggested_flavor:
            return render_template('add_suggestion.html', error='Name and flavor are required')

        with sqlite3.connect('chocolate_database.db') as connection:
            connection.execute("INSERT INTO customer_suggestions (name, flavor) VALUES (?, ?)",
                               (customer_name, suggested_flavor))
            connection.commit()
        return render_template('add_suggestion.html', message='Suggestion added successfully')

    return render_template('add_suggestion.html')

@app.route('/list_suggestions')
def list_suggestions():
    with sqlite3.connect('chocolate_database.db') as connection:
        cursor = connection.execute("SELECT * FROM customer_suggestions")
        suggestion_list = [{'id': row[0], 'name': row[1], 'flavor': row[2]} for row in cursor.fetchall()]
    return render_template('list_suggestions.html', suggestions=suggestion_list)

@app.route('/delete_suggestion/<int:suggestion_id>', methods=['POST'])
def delete_suggestion(suggestion_id):
    with sqlite3.connect('chocolate_database.db') as connection:
        connection.execute("DELETE FROM customer_suggestions WHERE id = ?", (suggestion_id,))
        connection.commit()
    return redirect(url_for('list_suggestions'))

if __name__ == '__main__':
    initialize_database()  
    app.run(debug=True)
