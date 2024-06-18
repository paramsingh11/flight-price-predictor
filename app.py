import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# Replace 'YOUR_RAPIDAPI_KEY' with your actual RapidAPI key
RAPIDAPI_KEY = 'efc4bc7378msha129e8a1e7b01f0p1a7ce3jsnc3f0e9c11c01'

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/predict_flight_price', methods=['POST'])
def predict_flight_price():
    data = request.get_json()
    origin_sky_id = data['origin_sky_id']
    destination_sky_id = data['destination_sky_id']
    origin_entity_id = data['origin_entity_id']
    destination_entity_id = data['destination_entity_id']
    cabin_class = data.get('cabin_class', 'economy')
    adults = data.get('adults', 1)
    sort_by = data.get('sort_by', 'best')
    currency = data.get('currency', 'USD')
    market = data.get('market', 'en-US')
    country_code = data.get('country_code', 'US')

    url = "https://sky-scrapper.p.rapidapi.com/api/v2/flights/searchFlightsComplete"
    params = {
        'originSkyId': origin_sky_id,
        'destinationSkyId': destination_sky_id,
        'originEntityId': origin_entity_id,
        'destinationEntityId': destination_entity_id,
        'cabinClass': cabin_class,
        'adults': adults,
        'sortBy': sort_by,
        'currency': currency,
        'market': market,
        'countryCode': country_code
    }
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': 'sky-scrapper.p.rapidapi.com'
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return jsonify({'error': 'Could not fetch flight data'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)




