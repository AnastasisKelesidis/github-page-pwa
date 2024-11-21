import matplotlib.pyplot as plt
from influxdb_client import InfluxDBClient

# Define connection details for read-only access
influxdb_url = "http://150.140.186.118:8086"
bucket = "Temp1084039"
org = "students"
readonly_token = "udCIpwvfntsslWHiqxLQ4s6Xu-gPHM2FbjUBlZClqRxxcwXon4--ApTv23qsCa8USx1vy0ovCJ-SeeGV2O6wZA=="
measurement = "sensor_data"

# Create InfluxDB client
client = InfluxDBClient(url=influxdb_url, token=readonly_token, org=org)
query_api = client.query_api()

def fetch_sensor_data():
    # Define the Flux query to fetch all temperature data from the measurement
    flux_query = f'''
    from(bucket: "{bucket}")
    |> range(start: -30d)  // adjust time range as needed
    |> filter(fn: (r) => r["_measurement"] == "{measurement}")
    |> filter(fn: (r) => r["_field"] == "value")
    |> filter(fn: (r) => r["sensor"] == "temperature")
    |> keep(columns: ["_time", "_value"])
    '''
    
    result = query_api.query(flux_query)
    times = []
    values = []

    # Parse the result
    for table in result:
        for record in table.records:
            times.append(record.get_time())
            values.append(record.get_value())

    return times, values

def plot_sensor_data():
    times, values = fetch_sensor_data()

    # Plotting the data
    plt.figure(figsize=(10, 5))
    plt.plot(times, values, label='Temperature (°C)', marker='o')
    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.title("Temperature Sensor Data")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_sensor_data()
