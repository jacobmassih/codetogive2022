import requests

API_TOKEN = "AIzaSyBkmSyt4ooNWKph1sJ-xq4Z2NpzspFnZNY"

def get_lat_and_long(address):
    params = {
        "key": API_TOKEN,
        "address": address
    }

    url = "https://maps.googleapis.com/maps/api/geocode/json?"
    response = requests.get(url, params=params).json()

    if response["status"] == "OK":
        location = response["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]

print(get_lat_and_long("Montreal, QC"))
