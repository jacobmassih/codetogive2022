from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from map.models import Topic
from .forms import UploadForm
import folium
from folium.plugins import MarkerCluster
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


def create_map(topics):
    map = folium.Map(location=[20, 10], zoom_start=2, min_zoom=2)
    home_map = "map.html"
    marker_cluster = MarkerCluster(name="clustered ideas").add_to(map)
    for topic in topics:

        print(topic)
        city = topic.city
        topicTitle = topic.title
    # Generates the "idea" html file when a location is clicked
        idea_html = f"""
        <!DOCTYPE html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
        <title>{topicTitle}</title>
        <p>Author: {topic.author}</p>
        <p>Date of creation: {topic.date}</p>
        <p>Tags: {topic.label}</p>
        <p>likes: {topic.likes}</p>
        <input type="button" onclick="readInputsForComments" value="Like">
        <p></p>
        <p>Comments:</p>
        <ul>
            <comment></comment>
        </ul>
        <p>Enter a comment</p>
        <input type="text" id="comment" name="user comment"><br><br>
        <input type="submit" onclick="readInputsForComments" value="Post comment">
        <center><a href={home_map}>Click here to go back to the map</a></center>

        """

        file = f"idea_{topic}.html"

        # with open(file, "w") as f:
        #     f.write(idea_html)

        # Generates the content read in the popup bubbles when a location is clicked
        # Link is now working

        html_on_map = f"""
            <h1> {topicTitle}</h1>
            <p> Last comment posted:</p>
            <ul>
                <comment></comment>
            </ul>
            </p>
            <p>Enter a comment</p>
            <input type="text" id="comment" name="user comment", placeholder="reply to"><br><br>
            <input type="submit" onclick="readInputsForComments" value="Post comment">
            </p>
            <center><a href={file}>Click here to read more about the idea</a></center>

        """

        popup = folium.Popup(folium.Html(
            html_on_map, script=True, width=300, height=350), max_width=300, max_height=350)
        loc = list(get_lat_and_long(city))
        folium.Marker(location=loc, popup=popup,
                      tooltip=city).add_to(marker_cluster)

    folium.LayerControl().add_to(map)

    return map._repr_html_()


def index(request):
    topics = Topic.objects.all()

    context = {'map': create_map(topics), 'form': UploadForm}
    if (request.method == 'POST'):
        form = UploadForm(request.POST)
        if form.is_valid():
            form.save()

    return render(request, 'map/index.html', context)
