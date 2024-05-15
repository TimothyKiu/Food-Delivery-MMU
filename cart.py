from flask import Flask, request, render_template
import mysql.connector

# ALLOWED_HOSTS = ['127.0.0.1']

#NOTE: STOP RUNNING PYTHON WHENEVER YOU WANNA ALTER SQL TABLES
db = mysql.connector.connect(
    host="localhost",
    user='root',
    passwd='Chan@125',
    database='customer'
)

app = Flask(__name__)

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/submit_remarks', methods=['POST'])
def submit_remarks():
    if request.method == 'POST':

        remarks = request.form.get('remarks')
        # exec(remarks)
        cursor = db.cursor()
        cursor.execute("INSERT INTO customer (customer_name) VALUES (%s)", (remarks))
        db.commit()
    return 'success' 


# @app.route('/')
# def home():
#     return 'Cart Backend'  


# @app.route('/addtocart', methods=['POST'])
# def addtocart():
#     item_name = request.form['item_name']
#     item_price = float(request.form['item_price'])
#     if 'cart' not in session:
#         session['cart'] = []
#     session['cart'].append({'name': item_name, 'price': item_price})
#     return 'Item added to cart'

# @app.route('/cart')
# def view_cart():
#     if 'cart' not in session:
#         return 'Cart is empty'
#     return ''.join([f'<li>{item["name"]} - RM{item["price"]}</li>' for item in session['cart']])

# @app.route('/clear_cart')
# def clear_cart():
#     session.pop('cart', None)
#     return 'Cart cleared'


# shopping_cart = [] 

# @app.route('/cart/add', methods=['GET'])
# def cart_add():
#     item_name = request.args.get('name', 'Item')
#     item_price = request.args.get('price', '0.00')
    
#     item = {'name': item_name, 'price': item_price}
#     shopping_cart.append(item) 
    
#     return f"Added {item_name} with {item_price} to the cart."

# shopping_cart = []

# @app.route('/cart', methods=['GET'])
# def cart_get():
#     cart_items = ", ".join([f"{item['name']} (RM{item['price']})" for item in shopping_cart])
    
#     return f"Cart contains: {cart_items}"


if __name__ == '__main__':
    app.run('0.0.0.0' , debug=True)