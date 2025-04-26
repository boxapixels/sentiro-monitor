
import pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision


# InfluxDB configuration
INFLUXDB_URL = "http://192.168.100.58:8086"  
INFLUXDB_TOKEN = "zVSag-BZOU9M6aLw_EUgO0Nzih2F46OkZVeP-KNW0zAQrpIXfwtYE52hR3u78VEXo3uO0QiAJsb48jjWRkK28g=="
INFLUXDB_ORG = "sentiro"                
INFLUXDB_BUCKET = "sentiro"          

influxdb_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)

def fetch_data():
    query = f'''
    from(bucket: "{INFLUXDB_BUCKET}")
    |> range(start: -30d)
    |> filter(fn: (r) => r["_measurement"] == "sensor_data")
    '''
    result = influxdb_client.query_api().query(query)

    data_records = []
    if result:
        for table in result:
            for record in table.records:
                record_dict = record.values.copy()
                record_dict['time'] = record_dict.pop('_time')
                data_records.append(record_dict)
        return pd.DataFrame(data_records)
    else:
        print("No data found for the specified query.")
        return None
    


def main():

    combined_df = fetch_data()

    if combined_df is not None:
        print(combined_df.head())

if __name__ == "__main__":
    main()