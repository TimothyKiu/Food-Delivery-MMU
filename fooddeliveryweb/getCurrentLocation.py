from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('getCurrentLocationHTML.html')

@app.route('/current_location', methods=['POST'])
def current_location():
    data = request.get_json()
    latitude = data['latitude']
    longitude = data['longitude']
    # Process location data as needed
    print("rider location: Latitude {}, Longitude {}".format(latitude, longitude))
    return "rider location: Latitude {}, Longitude {}".format(latitude, longitude)

if __name__ == '__main__':
    app.run(debug=True)
