from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# Simulating the pending order status, you can replace this with your actual logic
pending_order = False

@app.route('/')
def index():
    global pending_order
    if pending_order:
        return redirect(url_for('page1'))
    else:
        return redirect(url_for('page2'))

@app.route('/page1')
def page1():
    return render_template('page1.html')

@app.route('/page2')
def page2():
    return render_template('page2.html')

if __name__ == '__main__':
    app.run(debug=True)
