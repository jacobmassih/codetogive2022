from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from map.models import Topic
from .forms import UploadForm
import folium
from folium.plugins import MarkerCluster
import requests
from django.http import HttpResponseRedirect

from django.shortcuts import redirect


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
    marker_cluster = MarkerCluster(name="Topics").add_to(map)

    for topic in topics:
        # Generates the content read in the popup bubbles when a location is clicked
        popupContent = f"""
            <h1>{topic.title}</h1>
            <p>{topic.description} </p>
            <p>{topic.author} </p>
            <p>Date of creation: {topic.date}</p>
            <p>Label:{topic.label} </p>
            <p>Likes:{topic.likes} </p>
        """

        popup = folium.Popup(folium.Html(
            popupContent, script=True, width=300, height=350), max_width=300, max_height=350)

        coords = list(get_lat_and_long(topic.city))

        folium.Marker(location=coords, popup=popup,
                      tooltip=topic.city).add_to(marker_cluster)

    folium.LayerControl().add_to(map)

    return map._repr_html_()


def index(request):
    topics = Topic.objects.all()
    context = {'map': create_map(topics), 'form': UploadForm}

    if (request.method == 'POST'):
        form = UploadForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/map/')

    return render(request, 'map/index.html', context)
