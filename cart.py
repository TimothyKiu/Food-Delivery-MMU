from flask import Flask, request, render_template,redirect, url_for
import os
import mysql.connector


#NOTE: STOP RUNNING PYTHON WHENEVER YOU WANNA ALTER SQL TABLES
db = mysql.connector.connect(
    host="localhost",
    user='root',
    passwd='Chan@125',
    database='customer'
)

cursor = db.cursor()

app = Flask(__name__)
app.secret_key = "oisdsaoidiosad"

deen_food = [
    {'name': 'CHICKEN CHOP COMBO (Rice)', 'price': 7.00, 'category': 'Western'},
    {'name': 'CHICKEN CHOP COMBO (Fried Rice)', 'price': 8.50, 'category': 'Western'},
    {'name': 'ROTI BAKAR', 'price': 1.50, 'category': 'Western'},
    {'name': 'SANDWICH AYAM', 'price': 2.50, 'category': 'Western'},
    {'name': 'SANDWICH SARDIN', 'price': 2.50, 'category': 'Western'},
    {'name': 'ROT JOHN', 'price': 5.00, 'category': 'Western'},
    {'name': 'FRIES', 'price': 5.00, 'category': 'Western'},
    {'name': 'WET FRIES', 'price': 5.00, 'category': 'Western'},
    {'name': 'FISH & CHIPS', 'price': 11.00, 'category': 'Western'},
    {'name': 'CHICKEN CHOP (REGULAR)', 'price': 12.00, 'category': 'Western'},
    {'name': 'CHICKEN GRILL', 'price': 15.00, 'category': 'Western'},
    {'name': 'LAMB CHOP', 'price': 18.00, 'category': 'Western'},
    {'name': 'FRIED NOODLES', 'price': 5.00, 'category': 'Chinese'},
    {'name': 'KUEY TIAU GOREN', 'price': 5.00, 'category': 'Chinese'},
    {'name': 'BIHUN GOREN', 'price': 5.00, 'category': 'Chinese'},
    {'name': 'BIHUN SINGAPORE', 'price': 5.00, 'category': 'Chinese'},
    {'name': 'MEE GOREN', 'price': 5.00, 'category': 'Chinese'},
    {'name': 'MEE GORENG MAMAK', 'price': 5.00, 'category': 'Chinese'},
    {'name': 'MAGGIE GOREN', 'price': 5.00, 'category': 'Chinese'},
    {'name': 'YEE MEE GOREN', 'price': 6.00, 'category': 'Chinese'},
    {'name': 'HOKKIEN MEE', 'price': 6.00, 'category': 'Chinese'},
    {'name': 'MAGGIE GORENG XLR', 'price': 7.00, 'category': 'Chinese'},
    {'name': 'CHINESE STYLE', 'price': 0.00, 'category': 'Chinese'},  # Header for Chinese-style dishes
    {'name': 'NASI BUTTER CHICKEN', 'price': 8.00, 'category': 'Chinese'},
    {'name': 'NASI BUTTER FISH', 'price': 8.00, 'category': 'Chinese'},
    {'name': 'NASI BUTTER PRAWN', 'price': 9.00, 'category': 'Chinese'},
    {'name': 'NASI BUTTER SQUID', 'price': 9.00, 'category': 'Chinese'},
    {'name': 'NASI BUTTER CAMPUR', 'price': 10.00, 'category': 'Chinese'},
    {'name': 'NASI BUTTER MILK (CN)', 'price': 10.00, 'category': 'Chinese'},
    {'name': 'TOM YAM SOUP + RICE', 'price': 7.00, 'category': 'Soups'},
    {'name': 'TOM YAM SOUP (CENDAWAN)', 'price': 7.00, 'category': 'Soups'},
    {'name': 'TOM YAM SOUP (AYAM)', 'price': 7.00, 'category': 'Soups'},
    {'name': 'TOM YAM SOUP (DAGING)', 'price': 8.00, 'category': 'Soups'},
    {'name': 'TOM YAM SOUP (SEA FOOD)', 'price': 8.00, 'category': 'Soups'},
    {'name': 'TOM YAM SOUP (CAMPUR)', 'price': 8.50, 'category': 'Soups'},
    {'name': 'MAGGIE SOUP', 'price': 5.00, 'category': 'Soups'},
    {'name': 'KUEY TIAU SOUP', 'price': 5.00, 'category': 'Soups'},
    {'name': 'BIHUN SOUP', 'price': 5.00, 'category': 'Soups'},
    {'name': 'VEGETARIAN + NASI', 'price': 6.00, 'category': 'Soups'},
    {'name': 'CENDAWAN + NASI', 'price': 6.00, 'category': 'Soups'},
    {'name': 'AYAM + NASI', 'price': 6.00, 'category': 'Soups'},  # Likely a mistake on the menu, assuming this should not be Vegetarian
    {'name': 'DAGING + NASI', 'price': 7.00, 'category': 'Soups'},  # Likely a mistake on the menu, assuming this should not be Vegetarian
    {'name': 'KAMBING + NASI', 'price': 10.00, 'category': 'Soups'},
    {'name': 'NASI GORENG / FRIED RICE', 'price': 0.00, 'category': 'Nasi Goreng'},  # Header for Nasi Goreng dishes
    {'name': 'NASI GORENG BIASA (RM5)', 'price': 5.00, 'category': 'Nasi Goreng'},  # Assuming "BIASA" means "Normal"
    {'name': 'NASI GORENG KAMPUNG', 'price': 6.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG CIN', 'price': 5.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG MAMAK', 'price': 5.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG TELUR (EGG)', 'price': 5.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG CILI API', 'price': 5.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG SAUSAGE', 'price': 5.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG TOMYAM', 'price': 6.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG SARDIN', 'price': 6.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG PATTAYA', 'price': 6.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG IKAN MASIN', 'price': 6.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG TOMATO', 'price': 6.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG CENDAWAN', 'price': 6.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG DAGING', 'price': 7.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG SEA FOOD', 'price': 7.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG AYAM (CHICKEN)', 'price': 8.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG PAPRIK AYAM', 'price': 8.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG MSA (EGG)', 'price': 9.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG THAI', 'price': 9.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG KAMBING', 'price': 12.00, 'category': 'Nasi Goreng'},
    {'name': 'PASTA SPECIAL', 'price': 0.00, 'category': 'Pasta'},  # Header for Pasta dishes
    {'name': 'CARBONARA', 'price': 10.00, 'category': 'Pasta'},
    {'name': 'CHICKEN ALFRED', 'price': 10.00, 'category': 'Pasta'},
    {'name': 'BOLONESE', 'price': 10.00, 'category': 'Pasta'},
    {'name': 'PASTA VEGETARIAN', 'price': 10.00, 'category': 'Pasta'},
    {'name': 'MARINARA', 'price': 12.00, 'category': 'Pasta'},
    {'name': 'CHICKEN SPICY', 'price': 12.00, 'category': 'Pasta'},
    {'name': 'HOT PLATE', 'price': 0.00, 'category': 'Other'},  # Header for Hot Plate dishes
    {'name': 'CHAR KUEY TIAU', 'price': 6.00, 'category': 'Other'},
    {'name': 'SIZZLING RICE', 'price': 6.00, 'category': 'Other'},
    {'name': 'MEE BANDUNG', 'price': 6.00, 'category': 'Other'},
    {'name': 'SIZZLING YEE MEE', 'price': 6.50, 'category': 'Other'},
    {'name': 'CANTONESE YEE MEE', 'price': 7.00, 'category': 'Other'},
    {'name': 'CANTONESE JUEY TIAU', 'price': 7.00, 'category': 'Other'},
    {'name': 'YING YONG', 'price': 8.00, 'category': 'Other'},
    {'name': 'TEH TARIK', 'price': 2.00, 'category': 'Drinks'},  # Assuming Teh refers to Tea
    {'name': 'TEH O', 'price': 1.50, 'category': 'Drinks'},
    {'name': 'TEH O LIMAU', 'price': 2.00, 'category': 'Drinks'},
    {'name': 'TEH O LAICI', 'price': 3.50, 'category': 'Drinks'},
    {'name': 'NESCAFE', 'price': 2.50, 'category': 'Drinks'},
    {'name': 'NESCAFE O', 'price': 2.00, 'category': 'Drinks'},
    {'name': 'NESLO', 'price': 3.00, 'category': 'Drinks'},
    {'name': 'WHITE COFFEE', 'price': 3.00, 'category': 'Drinks'},
    {'name': 'KOPI', 'price': 2.00, 'category': 'Drinks'},
    {'name': 'KOPI O', 'price': 1.50, 'category': 'Drinks'},
    {'name': 'MILO', 'price': 2.50, 'category': 'Drinks'},
    {'name': 'MILO O', 'price': 2.50, 'category': 'Drinks'},
    {'name': 'BARLEY', 'price': 2.00, 'category': 'Drinks'},
    {'name': 'HORLICKS', 'price': 3.00, 'category': 'Drinks'},
    {'name': 'LIMAU PANAS', 'price': 2.00, 'category': 'Drinks'},
    {'name': 'LAICI', 'price': 3.00, 'category': 'Drinks'},  # Assuming referring to juice
    {'name': 'SIRAP BANDUNG', 'price': 2.00, 'category': 'Drinks'},
    {'name': 'FRUIT JUICE', 'price': 0.00, 'category': 'Drinks'},  # Header for Fruit Juices
    {'name': 'ORANGE JUICE', 'price': 4.00, 'category': 'Drinks'},
    {'name': 'APPLE JUICE', 'price': 4.00, 'category': 'Drinks'},
    {'name': 'WATERMELON JUICE', 'price': 4.00, 'category': 'Drinks'},
    {'name': 'EXTRA JASS', 'price': 3.50, 'category': 'Drinks'},
    {'name': 'CARROT JUICE', 'price': 4.00, 'category': 'Drinks'},
]

htc_food = [
    {'name': 'GORENG-GORENG', 'price': 0.00, 'category': 'Goreng'},  # Header for goreng dishes
    {'name': 'NASI GORENG', 'price': 4.50, 'category': 'Goreng'},
    {'name': 'NASI GORENG DOUBLE', 'price': 6.00, 'category': 'Goreng'},
    {'name': 'NASI GORENG CILI PADIR', 'price': 6.00, 'category': 'Goreng'},
    {'name': 'NASI GORENG CINAR', 'price': 5.00, 'category': 'Goreng'},
    {'name': 'NASI GORENG KAMPUNG', 'price': 6.00, 'category': 'Goreng'},
    {'name': 'NASI GORENG AYAM', 'price': 8.00, 'category': 'Goreng'},
    {'name': 'NASI GORENG KAMPUNG [AYAM]', 'price': 9.00, 'category': 'Goreng'},
    {'name': 'NASI GORENG PATTAYA', 'price': 6.00, 'category': 'Goreng'},
    {'name': 'MAGGI', 'price': 4.50, 'category': 'Goreng'},
    {'name': 'MAGGI DOUBLE', 'price': 7.00, 'category': 'Goreng'},
    {'name': 'MAGGI DOUBLE AYAM', 'price': 10.00, 'category': 'Goreng'},
    {'name': 'MEE', 'price': 4.50, 'category': 'Goreng'},
    {'name': 'BIHUN', 'price': 4.50, 'category': 'Goreng'},
    {'name': 'KUEY TEOW', 'price': 4.50, 'category': 'Goreng'},
    {'name': 'ROJAK', 'price': 4.50, 'category': 'Goreng'},
    {'name': 'TELUR MATA', 'price': 1.00, 'category': 'Goreng'},
    {'name': 'TELUR DADAR', 'price': 1.50, 'category': 'Goreng'},
    {'name': 'MEE/KUE TEOW/BIHUN', 'price': 4.50, 'category': 'Goreng'},  # Assuming this refers to a combo
    {'name': 'MEE/NASI GORENG', 'price': 4.50, 'category': 'Goreng'},  # Assuming this refers to a combo
    {'name': 'KUE TEOW/BIHUN GORENG', 'price': 4.50, 'category': 'Goreng'},  # Assuming this refers to a combo
    {'name': 'ROJAK BIASA', 'price': 5.50, 'category': 'Goreng'},
    {'name': 'ROJAK TELUR', 'price': 5.50, 'category': 'Goreng'},
    {'name': 'ROJAK MEE/MEE', 'price': 5.50, 'category': 'Goreng'},  # Assuming this is a typo and should be "ROJAK MEE/BIHUN"
    {'name': 'ROTI CANAI', 'price': 0.00, 'category': 'Roti'},  # Header for Roti dishes
    {'name': 'BIAS', 'price': 1.20, 'category': 'Roti'},
    {'name': 'TELUR', 'price': 2.50, 'category': 'Roti'},
    {'name': 'TELUR BAWANG', 'price': 3.00, 'category': 'Roti'},
    {'name': 'BAWANG', 'price': 2.00, 'category': 'Roti'},
    {'name': 'PLANTAR', 'price': 2.50, 'category': 'Roti'},
    {'name': 'BOOM', 'price': 2.50, 'category': 'Roti'},
    {'name': 'CHEESE', 'price': 3.00, 'category': 'Roti'},
    {'name': 'TELUR CHEESE', 'price': 4.00, 'category': 'Roti'},
    {'name': 'SARDINE', 'price': 4.00, 'category': 'Roti'},
    {'name': 'KAYA', 'price': 2.50, 'category': 'Roti'},
    {'name': 'MADU', 'price': 2.50, 'category': 'Roti'},
    {'name': 'PISANG', 'price': 3.00, 'category': 'Roti'},
    {'name': 'TOSAI', 'price': 0.00, 'category': 'Tosai'},  # Header for Tosai dishes
    {'name': 'BIAS', 'price': 2.00, 'category': 'Tosai'},
    {'name': 'TELUR', 'price': 3.00, 'category': 'Tosai'},
    {'name': 'BAWANG', 'price': 3.00, 'category': 'Tosai'},
    {'name': 'MASALA', 'price': 3.50, 'category': 'Tosai'},
    {'name': 'GHEE', 'price': 3.00, 'category': 'Tosai'},
    {'name': 'MURTABAK', 'price': 4.50, 'category': 'Murtabak'},
    {'name': 'CAPATI', 'price': 2.00, 'category': 'Others'},
    {'name': 'SPECIAL', 'price': 0.00, 'category': 'Others'},  # Header for Special dishes
    {'name': 'ROTI BAKAR', 'price': 1.50, 'category': 'Others'},
    {'name': 'ROTI BAKAR TELUR', 'price': 3.00, 'category': 'Others'},
    {'name': 'ROTI BAKAR SARDIN', 'price': 4.00, 'category': 'Others'},
    {'name': 'MINUMAN', 'price': 0.00, 'category': 'Drinks'},  # Header for Drinks
    {'name': 'AIS TEH', 'price': 2.30, 'category': 'Drinks'},
    {'name': 'TEH O', 'price': 2.00, 'category': 'Drinks'},
    {'name': 'KOPI', 'price': 2.30, 'category': 'Drinks'},
    {'name': 'KOPI O', 'price': 2.00, 'category': 'Drinks'},
    {'name': 'MILO', 'price': 2.80, 'category': 'Drinks'},
    {'name': 'MILO O', 'price': 2.50, 'category': 'Drinks'},
    {'name': 'NESCAFE O', 'price': 2.50, 'category': 'Drinks'},
    {'name': 'NESCAFE', 'price': 2.80, 'category': 'Drinks'},
    {'name': 'BRU', 'price': 3.00, 'category': 'Drinks'},
    {'name': 'HORLICKS', 'price': 3.00, 'category': 'Drinks'},
    {'name': 'TEH LIMAU', 'price': 2.30, 'category': 'Drinks'},
    {'name': 'AIR SIRAP', 'price': 2.30, 'category': 'Drinks'},
    {'name': 'SIRAP LIMAU', 'price': 2.30, 'category': 'Drinks'},
    {'name': 'JUS BUAH-BUAHAN', 'price': 0.00, 'category': 'Drinks'},  # Header for Fruit Juices
    {'name': 'OREN/EPAL', 'price': 3.50, 'category': 'Drinks'},
    {'name': 'BELIMBING', 'price': 3.50, 'category': 'Drinks'},
    {'name': 'MANGGA/KAROT', 'price': 3.50, 'category': 'Drinks'},
    {'name': 'ASAM JAWA', 'price': 2.80, 'category': 'Drinks'},
    {'name': 'BARLI', 'price': 2.80, 'category': 'Drinks'}
]

bakery_food = [
    {'name': 'VANILLA CHOCO TIWIST', 'price': 4.50, 'category': 'Pastry'},
    {'name': 'CHICKEN CURRY PUFF', 'price': 4.50, 'category': 'Pastry'},
    {'name': 'TUNA PUFF', 'price': 4.50, 'category': 'Pastry'},
    {'name': 'BANANA BAR', 'price': 3.80, 'category': 'Pastry'},
    {'name': 'CHICKEN SAUSAGE DONUT', 'price': 4.50, 'category': 'Pastry'},
    {'name': 'GARLIC SAUSAGE ROLL', 'price': 5.50, 'category': 'Pastry'},
    {'name': 'BBQ SAUSAGE ROLL', 'price': 5.50, 'category': 'Pastry'},
    {'name': 'MINI CROISSANT', 'price': 2.00, 'category': 'Pastry'},
    {'name': 'MINI CHICKEN MUSHROOM PIE', 'price': 5.50, 'category': 'Pastry'},
    {'name': 'FIRE CRACKER SAUSAGE', 'price': 7.50, 'category': 'Pastry'},
    {'name': 'CHOCOLATE ROLL', 'price': 3.00, 'category': 'Pastry'},
    {'name': 'CHOCOLATE MUFFIN', 'price': 6.50, 'category': 'Pastry'},
    {'name': 'BLUEBERRY MUFFIN', 'price': 6.50, 'category': 'Pastry'},
    {'name': 'MINI MUFFIN RED VELVET', 'price': 2.50, 'category': 'Pastry'},
    {'name': 'MINI MUFFIN BUTTERSCOTCH', 'price': 2.50, 'category': 'Pastry'},
    {'name': 'CHOCOLATE CHIP COOKIES', 'price': 4.50, 'category': 'Pastry'},
    {'name': 'DOUBLE CHOCO CHIP COOKIES', 'price': 4.50, 'category': 'Pastry'},
    {'name': 'SPICY TUNA EGG SANDWICH', 'price': 4.00, 'category': 'Pastry'},
    {'name': 'EGG MAYO SANDWICH', 'price': 3.50, 'category': 'Pastry'},
    {'name': 'BIHUN GORENG', 'price': 5.00, 'category': 'Pastry'},
    {'name': 'NASI GORENG', 'price': 5.00, 'category': 'Pastry'},
    {'name': 'NASI LEMAK', 'price': 4.00, 'category': 'Pastry'},
    {'name': 'COFFEE', 'price': 0.00, 'category': 'Coffee'},  # Header for Coffee category
    {'name': 'S BLACK COFFEE', 'price': 4.00, 'category': 'Coffee'},
    {'name': 'WHITE COFFEE', 'price': 4.00, 'category': 'Coffee'},
    {'name': 'PREMIUM COFFEE', 'price': 0.00, 'category': 'Coffee'},  # Sub-header for Premium Coffee
    {'name': 'ESPRESSO', 'price': 5.50, 'category': 'Coffee'},
    {'name': 'AMERICAN', 'price': 6.50, 'category': 'Coffee'},
    {'name': 'LATTE', 'price': 7.50, 'category': 'Coffee'},
    {'name': 'CAPPUCCINO', 'price': 7.50, 'category': 'Coffee'},
    {'name': 'MOCHA', 'price': 8.50, 'category': 'Coffee'},
    {'name': 'COCONUT LATTE', 'price': 8.50, 'category': 'Coffee'},
    {'name': 'HAZELNUT LATTE', 'price': 8.50, 'category': 'Coffee'},
    {'name': 'FRENCH VANILLA LATTE', 'price': 8.50, 'category': 'Coffee'},
    {'name': 'SALTED CARAMEL LATTE', 'price': 8.50, 'category': 'Coffee'},
    {'name': 'NON COFFEE', 'price': 0.00, 'category': 'Coffee'},  # Sub-header for Non-Coffee drinks
    {'name': 'CHOCOLATE', 'price': 7.00, 'category': 'Coffee'},
    {'name': 'MATCHA LATTE', 'price': 7.80, 'category': 'Coffee'},
    {'name': 'MILO', 'price': 5.00, 'category': 'Coffee'},  # Likely a mistake, categorized under Coffee
    {'name': 'TEH TARIK', 'price': 5.00, 'category': 'Coffee'},
]


ITEMS = []
ITEMS.extend(bakery_food)
ITEMS.extend(deen_food)
ITEMS.extend(htc_food)


CART_FILE = 'cart.txt'

def read_cart():
    cart = {}
    if os.path.exists(CART_FILE):
        with open(CART_FILE, 'r') as file:
            for line in file:
                parts = line.strip().split(', ')
                if len(parts) >= 3:
                    try:
                        item_name = parts[0]
                        item_price = parts[1]
                        item_quantity = int(parts[2].replace(',', ''))  # Remove any extraneous commas
                        item_remarks = ', '.join(parts[3:]) if len(parts) > 3 else ''
                        cart[item_name] = {'price': item_price, 'quantity': item_quantity, 'remarks': item_remarks}
                    except ValueError as e:
                        print(f"Error parsing line: {line}. Error: {e}")
        # with open(CART_FILE, 'r') as file:
        #     for line in file:
        #         parts = line.strip().split(', ')
        #         if len(parts) >= 3:
        #             item_name = parts[0]
        #             item_price = parts[1]
        #             item_quantity = int(parts[2])
        #             item_remarks = ', '.join(parts[3:]) if len(parts) > 3 else ''
        #             cart[item_name] = {'price': item_price, 'quantity': item_quantity, 'remarks': item_remarks}
    return cart

def write_cart(cart):
    with open(CART_FILE, 'w') as file:
        for item_name, details in cart.items():
            file.write(f"{item_name}, {details['price']}, {details['quantity']}, {details['remarks']}\n")

# @app.route('/')
# def menu():
#     cart = read_cart()
#     return render_template('menu.html', items=ITEMS, cart=cart)

@app.route('/', methods=['GET', 'POST'])
def index():
    # store = request.args.get('store')  # Get store from query string
    # if store == 'htc':
    #     items = htc_food
    #     return render_template('htc.html', items=items)
    # elif store == 'deen':
    #     items = deen_food
    #     return render_template('deen.html', items=items)
    # else:
    #     items = bakery_food
    # return render_template('dlight_bakery.html', items=items)
    store = request.args.get('store')  # Get store from query string
    if store == 'htc':
        items = htc_food
    elif store == 'deen':
        items = deen_food
    else:
        items = bakery_food

    selected_item = None
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        selected_item = next((item for item in ITEMS if item['name'] == item_name), None)

    return render_template('dlight_bakery.html', items=items, cart=read_cart(), selected_item=selected_item)


@app.route('/', methods=['GET', 'POST'])
def bakery():
    cart = read_cart()
    selected_item = None
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        selected_item = next((item for item in ITEMS if item['name'] == item_name), None)
        if selected_item and item_name in cart:
            selected_item['quantity'] = cart[item_name]['quantity']
            selected_item['remarks'] = cart[item_name]['remarks']
        else:
            selected_item['quantity'] = 0
            selected_item['remarks'] = ''
    return render_template('dlight_bakery.html', items=ITEMS, cart=cart, selected_item=selected_item)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_name = request.form.get('item_name')
    item_price = request.form.get('item_price')
    cart = read_cart()
    if item_name in cart:
        cart[item_name]['quantity'] += 1
    else:
        cart[item_name] = {'price': item_price, 'quantity': 1, 'remarks': ''}
    write_cart(cart)
    return redirect(url_for('bakery'))

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    item_name = request.form.get('item_name')
    cart = read_cart()
    if item_name in cart:
        if cart[item_name]['quantity'] > 1:
            cart[item_name]['quantity'] -= 1
        else:
            del cart[item_name]
    write_cart(cart)
    return redirect(url_for('bakery'))

@app.route('/update_remarks', methods=['POST'])
def update_remarks():
    item_name = request.form.get('item_name')
    remarks = request.form.get('remarks')
    cart = read_cart()
    if item_name in cart:
        cart[item_name]['remarks'] = remarks
    write_cart(cart)
    return redirect(url_for('bakery'))



# @app.route('/', methods=['GET']) 
# def menu():
#     with open("remarks.txt", "r") as file:
#         remarks = file.read()
#     return render_template('menu.html', remarks=remarks)

@app.route('/home', methods=['GET']) 
def home():
    return render_template('home.html')

@app.route('/deen', methods=['GET']) 
def deen():
    return render_template('deen.html')

@app.route('/htc', methods=['GET']) 
def htc():
    return render_template('htc.html')

# @app.route('/bakery', methods=['GET']) 
# def bakery():
#     return render_template('dlight_bakery.html')

# @app.route('/add_to_cart', methods=['POST', 'GET']) 
# def add_to_cart():
#     if request.method == 'POST':
        

#         # remarks = request.form['remarks']
#         # testvalue = "x"
#         # print(remarks)
#         # sql = "INSERT INTO customer.user_remarks (remarks, username) VALUES (%s, %s)"
    
#         # cursor.execute(sql, (remarks, testvalue))
#         # db.commit()
        
#         with open("remarks.txt", "a") as file:
#             file.write(remarks + "\n")
#         print(remarks)

#     return render_template("menu.html", remarks=remarks, testvalue=testvalue)

# @app.route('/')  # Assuming you want to display remarks on the root route
# def display_remarks():
#   # Connect to database (省略 - omitted for brevity)
#   cursor = db.cursor()
#   cursor.execute("SELECT remarks FROM user_remarks")
#   remarks_data = cursor.fetchall()  # Fetch all remarks as a list of tuples
#   cursor.close()  # Close the cursor
#   return render_template('menu.html', remarks=remarks_data)



app.run(debug=True)