from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .forms import UploadForm
import folium
from folium.plugins import MarkerCluster
import requests


places = {"id0001": {"Argentina": {"idea": "where does Horacio Pagani live?", "comments": {"bob": "idk"}}, "creation": {"author": "jorge", "date": "novembre 5th 2022", "tags": ["life"], "likes": 1}},
          "id0002": {"Malé": {"idea": "vacation", "comments": {"jeff": "nice place"}}, "creation": {"author": "ben", "date": "novembre 6th 2022", "tags": ["life"], "likes": 85}},
          "id0003": {"Montreal, QC": {"idea": "congestion sur la ligne bleue", "comments": {"steven": "rien de nouveau"}}, "creation": {"author": "adam", "date": "novembre 7th 2022", "tags": ["transport", "commute", "life"], "likes": 4}},
          "id0004": {"Tokyo, Japan": {"idea": "what are jdm cars", "comments": {"Han": "life"}}, "creation": {"author": "jamal", "date": "novembre 5th 2022", "tags": ["life", "jdm", "environment", "happiness"], "likes": 900000}},
          "id0005": {"france": {"idea": "baguette", "comments": {"François": "un très bon repas"}}, "creation": {"author": "arthur", "date": "novembre 3rd 2022", "tags": ["food", "happiness"], "likes": 76}},
          "id0006": {"deutschland": {"idea": "what is the best beer", "comments": {"chad": "they're all good"}},  "creation": {"author": "josh", "date": "novembre 2nd 2022", "tags": ["happiness", "life"], "likes": 60}},
          "id0007": {"ICELAND": {"idea": "how cold does it get", "comments": {"josh": "very"}},  "creation": {"author": "sergei", "date": "novembre 11th 2022", "tags": ["weather", "environment"], "likes": 5}},
          "id0008": {"Ohio": {"idea": "how many potatoes are collected per day", "comments": {"franck": "lots"}},  "creation": {"author": "vlad", "date": "novembre 5th 2022", "tags": ["food", "environment", "economy", "business"], "likes": 89}},
          "id0009": {"Laval, QC": {"idea": "congestion sur la ligne orange", "comments": {"steven2": "rien de nouveau"}},  "creation": {"author": "jorge", "date": "novembre 8th 2022", "tags": ["transport"], "likes": 86}},
          }


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


def create_map(places):
    map = folium.Map(location=[20, 10], zoom_start=2, min_zoom=2)
    home_map = "map.html"
    marker_cluster = MarkerCluster(name="clustered ideas").add_to(map)
    for id in places.keys():

        place = list(places[id].keys())[0]
        idea = places[id][place]["idea"]
    # Generates the "idea" html file when a location is clicked
        idea_html = f"""
        <!DOCTYPE html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
        <title>{idea}</title>
        <p>Author: {places[id]["creation"]["author"]}</p>
        <p>Date of creation: {places[id]["creation"]["date"]}</p>
        <p>Tags: {places[id]["creation"]["tags"]}</p>
        <p>likes: {places[id]["creation"]["likes"]}</p>
        <input type="button" onclick="readInputsForComments" value="Like">
        <p></p>
        <p>Comments:</p>
        <ul>
            <comment>{places[id][place]["comments"]}</comment>
        </ul>
        <p>Enter a comment</p>
        <input type="text" id="comment" name="user comment"><br><br>
        <input type="submit" onclick="readInputsForComments" value="Post comment">
        <center><a href={home_map}>Click here to go back to the map</a></center>

        """

        file = f"idea_{id}.html"

        # with open(file, "w") as f:
        #     f.write(idea_html)

        # Generates the content read in the popup bubbles when a location is clicked
        # Link is now working

        html_on_map = f"""
            <h1> {idea}</h1>
            <p> Last comment posted:</p>
            <ul>
                <comment>{str(list(places[id][place]["comments"].keys())[-1])+" posted: "+ str(list(places[id][place]["comments"].values())[-1])}</comment>
            </ul>
            </p>
            <p>Enter a comment</p>
            <input type="text" id="comment" name="user comment", placeholder="reply to {str(list(places[id][place]["comments"].keys())[-1])}"><br><br>
            <input type="submit" onclick="readInputsForComments" value="Post comment">
            </p>
            <center><a href={file}>Click here to read more about the idea</a></center>

        """

        popup = folium.Popup(folium.Html(
            html_on_map, script=True, width=300, height=350), max_width=300, max_height=350)
        loc = list(get_lat_and_long(place))
        folium.Marker(location=loc, popup=popup,
                      tooltip=place).add_to(marker_cluster)

    folium.LayerControl().add_to(map)

    return map._repr_html_()


def index(request):
    context = {'map': create_map(places), 'form': UploadForm}
    if (request.method == 'POST'):
        form = UploadForm(request.POST)
        if form.is_valid():
            form.save()

    return render(request, 'map/index.html', context)
