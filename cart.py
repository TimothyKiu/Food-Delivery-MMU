from flask import Flask, request, session
import mysql.connector

#NOTE: STOP RUNNING PYTHON WHENEVER YOU WANNA ALTER SQL TABLES
db = mysql.connector.connect(
    host="localhost",
    user='root',
    passwd='Chan@125',
    database='customer'
)

mycursor = db.cursor(buffered=True)

app = Flask(__name__)


@app.route('/cart.py/remarks', methods=['POST'])
def remarks():
    if request.method == 'POST':

        remark = request.form.get('remark')

        cursor = db.cursor()
        cursor.execute("INSERT INTO customer (customer_name) VALUES (%s)", (remark))
        db.commit()
    return 'success' 


@app.route('/')
def home():
    return 'Cart Backend'  


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

app.run(debug=False)