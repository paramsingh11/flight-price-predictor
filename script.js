const form = document.getElementById('flight-search-form');
const flightResults = document.getElementById('flight-results');

form.addEventListener('submit', async function(event) {
    event.preventDefault();

    const origin = form.elements['origin'].value;
    const destination = form.elements['destination'].value;
    const departureDate = form.elements['departure-date'].value;
    const adults = form.elements['adults'].value;
    const children = form.elements['children'].value;
    const teens = form.elements['teens'].value;
    const infants = form.elements['infants'].value;

    const flights = await searchFlights(origin, destination, departureDate, adults, children, teens, infants);

    displayFlights(flights);
});

async function searchFlights(origin, destination, departureDate, adults, children, teens, infants) {
    const url = 'https://ryanair2.p.rapidapi.com/api/v1/searchFlights';

    const querystring = {
        origin,
        destination,
        outboundDate: departureDate,
        adults,
        teens,
        children,
        infants
    };

    const headers = {
        'x-rapidapi-key': 'efc4bc7378msha129e8a1e7b01f0p1a7ce3jsnc3f0e9c11c01',
        'x-rapidapi-host': 'ryanair2.p.rapidapi.com'
    };

    try {
        const response = await fetch(`${url}?${new URLSearchParams(querystring)}`, { headers });
        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching flight data:', error);
        alert('An error occurred while fetching flight data. Please try again later.');
        return [];
    }
}

function displayFlights(flights) {
    flightResults.innerHTML = '';

    if (flights.length === 0) {
        flightResults.innerHTML = '<p>No flights found.</p>';
        return;
    }

    const flightsHtml = flights.map(flight => `
        <div class="flight-item">
            <h3>${flight.flightNumber}</h3>
            <p>Departure: ${flight.departureAirport} (${flight.departureTime})</p>
            <p>Arrival: ${flight.arrivalAirport} (${flight.arrivalTime})</p>
            <p>Price: ${flight.price}</p>
        </div>
    `).join('');

    flightResults.innerHTML = flightsHtml;
}
