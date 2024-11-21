import time
import random
import json
from influxdb_client import InfluxDBClient, Point, WritePrecision
import paho.mqtt.client as mqtt

# Define connection details for InfluxDB
influxdb_url = "http://150.140.186.118:8086"
bucket = "Temp1084039"
org = "students"
token = "kl9GBnLGG53jBKvIxmmV6g6BgLpnyJ2UbTWoJ5AHXkMzQUrTU_Jqguuf7NUU2kBVFqjv_lgQeKsQdcm04doygA=="
measurement = "sensor_data"

# Create InfluxDB client
client = InfluxDBClient(url=influxdb_url, token=token, org=org)
write_api = client.write_api()  # No need to pass WritePrecision here

# MQTT broker details
broker = '150.140.186.118'
port = 1883
client_id = 'rand_id' + str(random.random())
topic = 'json/Environmental/dutch-sensor-systems-ranos-db-2:1'

def process_func(message):
    """Process the incoming message and extract temperature data."""
    try:
        # Load the JSON message
        data = json.loads(message)
        
        # Extract temperature from measurements
        measurements = data.get('object', {}).get('measurements', [])
        if measurements:
            # Assuming we are interested in the first measurement's LAeq as the temperature value
            temperature = measurements[0].get('LAeq')  # Modify if you need a different value
            if temperature is not None:
                return round(float(temperature), 2)
    except json.JSONDecodeError:
        print("Received message is not valid JSON.")
    except (IndexError, ValueError):
        print("Error extracting temperature from measurements.")
    
    return None

def on_message(client, userdata, message):
    """Callback function for processing received messages."""
    print(f"Message received: {message.payload.decode()}")
    temperature = process_func(message.payload.decode())
    if temperature is not None:
        # Create a data point
        point = Point(measurement).tag("sensor", "temperature").field("value", temperature).time(time.time_ns(), WritePrecision.NS)
        
        # Write the point to the database
        write_api.write(bucket=bucket, org=org, record=point)
        print(f"Written temperature data: {temperature}°C")

def main():
    # Create an MQTT client instance
    mqtt_client = mqtt.Client(client_id=client_id)

    # Set the on_message callback function
    mqtt_client.on_message = on_message

    # Connect to the MQTT broker
    mqtt_client.connect(broker, port)

    # Subscribe to the specified topic
    mqtt_client.subscribe(topic)

    # Start the MQTT client loop
    mqtt_client.loop_forever()

if __name__ == "__main__":
    main()
