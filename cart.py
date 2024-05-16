from flask import Flask, request, render_template,redirect

app = Flask(__name__)

@app.route('/', methods=['GET']) 
def menu():
    with open("remarks.txt", "r") as file:
        remarks = file.read()
    return render_template('menu.html', remarks=remarks)

@app.route('/', methods=['GET']) 
def home():
    return render_template('home.html')


@app.route('/add_to_cart', methods=['POST']) 
def add_to_cart():
    remarks = request.form.get('remarks')

    with open("remarks.txt", "a") as file:
        file.write(remarks + "\n")

    # return render_template('menu.html', remarks=remarks)
    return "successful"


if __name__ == '__main__':
    app.run('0.0.0.0' , debug=True)
