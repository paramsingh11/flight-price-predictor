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

if __name__ == '__main__':
    app.run(debug=True)

