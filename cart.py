from flask import Flask, request, render_template, redirect

app = Flask(__name__)

@app.route('/', methods=['GET'])  # Specify methods for each route
def menu():
    return render_template('menu.html')


@app.route('/add_to_cart', methods=['POST'])  # Specify methods for each route
def addtocart():
    remarks = request.form.get('remarks')

    # Append remarks to text file (assuming write permissions)
    with open("remarks.txt", "a") as file:
        file.write(remarks + "\n")

    return "successful"

# ... (other routes)

if __name__ == '__main__':
    app.run('0.0.0.0' , debug=True)
