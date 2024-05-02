from flask import Flask, request	

app = Flask(__name__)

@app.route('/')
def home():
    return 'Cart Backend'  

shopping_cart = [] 

@app.route('/cart/add', methods=['GET'])
def cart_add():
  
    item_name = request.args.get('name', 'Item')
    item_price = request.args.get('price', '0.00')
    
    item = {'name': item_name, 'price': item_price}
    shopping_cart.append(item) 
    
    return f"Added {item_name} with {item_price} to the cart."

shopping_cart = []

@app.route('/cart', methods=['GET'])
def cart_get():
    cart_items = ", ".join([f"{item['name']} (RM{item['price']})" for item in shopping_cart])
    
    return f"Cart contains: {cart_items}"

