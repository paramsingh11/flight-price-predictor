from flask import Flask, request, jsonify
import joblib
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Load the model
model = joblib.load('flight_price_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    date = data['date']
    day_of_week = datetime.strptime(date, '%Y-%m-%d').weekday()
    days_until_flight = (datetime.strptime(date, '%Y-%m-%d') - datetime.now()).days
    input_data = pd.DataFrame({
        'day_of_week': [day_of_week],
        'days_until_flight': [days_until_flight]
    })
    predicted_price = model.predict(input_data)[0]
    return jsonify({'predicted_price': predicted_price})

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Flight Price Predictor</title>
    </head>
    <body>
        <h1>Flight Price Predictor</h1>
        <form id="predict-form">
            <label for="origin">Origin:</label>
            <input type="text" id="origin" name="origin"><br><br>
            <label for="destination">Destination:</label>
            <input type="text" id="destination" name="destination"><br><br>
            <label for="date">Date:</label>
            <input type="date" id="date" name="date"><br><br>
            <input type="submit" value="Predict">
        </form>
        <h2 id="result"></h2>
        <script>
            document.getElementById('predict-form').addEventListener('submit', function(event) {
                event.preventDefault();
                var origin = document.getElementById('origin').value;
                var destination = document.getElementById('destination').value;
                var date = document.getElementById('date').value;

                fetch('/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ origin: origin, destination: destination, date: date }),
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('result').innerText = `Predicted price: $${data.predicted_price}`;
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
            });
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
