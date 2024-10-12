import time
import board
import adafruit_dht
import firebase_admin
from firebase_admin import credentials, db

# Firebase credentials and initialization
cred = credentials.Certificate("path/to/your-firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-project-id.firebaseio.com/'
})

# Define the DHT11 sensor and its GPIO pin
dht_device = adafruit_dht.DHT11(board.D4)  # Adjust GPIO pin accordingly

# Reference to the Firebase Realtime Database
ref = db.reference('weather')

while True:
    try:
        # Reading temperature and humidity
        temperature = dht_device.temperature
        humidity = dht_device.humidity

        if humidity is not None and temperature is not None:
            data = {'temperature': temperature, 'humidity': humidity}
            ref.push(data)
            print(f'Temp: {temperature:.1f}°C  Humidity: {humidity:.1f}%')
        else:
            print('Failed to retrieve data from sensor')
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    time.sleep(10)  # Delay in seconds before the next reading
