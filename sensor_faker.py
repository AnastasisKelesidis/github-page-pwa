import time
import random
from influxdb_client import InfluxDBClient, Point, WritePrecision

# Define connection details
influxdb_url = "http://150.140.186.118:8086"
bucket = "Temp1084039"
org = "students"
token = "kl9GBnLGG53jBKvIxmmV6g6BgLpnyJ2UbTWoJ5AHXkMzQUrTU_Jqguuf7NUU2kBVFqjv_lgQeKsQdcm04doygA=="
measurement = "sensor_data"

# Create InfluxDB client
client = InfluxDBClient(url=influxdb_url, token=token, org=org)
write_api = client.write_api()  # No need to pass WritePrecision here

def generate_sensor_data():
    while True:
        # Generate random temperature value
        temperature = round(random.uniform(20.0, 30.0), 2)

        # Create a data point
        point = Point(measurement).tag("sensor", "temperature").field("value", temperature).time(time.time_ns(), WritePrecision.NS)

        # Write the point to the database
        write_api.write(bucket=bucket, org=org, record=point)
        print(f"Written temperature data: {temperature}°C")

        # Sleep for 2 seconds before generating the next point
        time.sleep(2)

if __name__ == "__main__":
    generate_sensor_data()