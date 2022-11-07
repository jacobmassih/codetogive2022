from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .models import Comment, Topic
from .forms import CommentForm, UploadForm
import folium
from folium.plugins import MarkerCluster
import requests
from django.http import HttpResponseRedirect
from django.templatetags.static import static


from django.shortcuts import redirect


API_TOKEN = "AIzaSyDvKefewp_aeI01GAXoKM7o2t_2yJT8Eok"


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

    cluster_function_js = """
        function(cluster) {
        var childCount = cluster.getChildCount(); 
        var c = ' marker-cluster-';

        if (childCount <= 3) {
            c += 'small';
        } else if (childCount < 5 && childCount > 3) {
            c += 'medium';
        } else {
            c += 'large'
        }
        return new L.DivIcon({ html: '<div><span>' + childCount + '</span></div>', className: 'marker-cluster' + c, iconSize: new L.Point(40, 40) });
        }
        """

    marker_cluster = MarkerCluster(
        name="Topics", icon_create_function=cluster_function_js).add_to(map)

    for topic in topics:

        date = str(topic.date).split('.')[0]
        # Generates the content read in the popup bubbles when a location is clicked
        popupContent = """
        <style>
            .comments {
                border: none;
                padding: 5px;
                font: 14px/16px sans-serif;
                width: 100%;
                height: 200px;
                overflow: scroll;
                }

                /* Scrollbar styles */
                ::-webkit-scrollbar {
                width: 12px;
                height: 12px;
            }
            .name{
                color:blue;
            }
            .paragraph-text{
                text-align: justify;
                text-justify: inter-word;
            }
            .label{
                background-color: green;
                color:white;
            }
            .like{
                width:30px;
            }
            .main-flex{
                display: flex;
                align-items: center;
                justify-content: space-between;
            }

            </style>""" + f"""
            <h2>{topic.title}</h2>
            <p class="label">{topic.label} </p>
            <p class="paragraph-text">{topic.description} </p>
            
            <div class="main-flex">
                    <div class="main-flex">
                        <img class="like" src="{static('like.png') }">
                        <p>{topic.likes} </p>
                    </div>
                    <small><i>by <span class="name">{topic.author} </span> on {date} </i> </small>
            </div>

            <h4>Comments</h4>
            <div class="comments">
        """

        comments = Comment.objects.filter(topic_id=topic.id).values()
        for comment in comments:
            popupContent += f"""
            <hr>
            <p> {comment['author']}: {comment['comment']} [Status :  {comment['status']}] <p>
            """
        popupContent += "</div>"

        popupContent += f"""
        <input type="text" placeholder="Enter your comment">
        <input type="submit">
        """

        popup = folium.Popup(folium.Html(
            popupContent, script=True, width=350), max_width=350, max_height=500)

        coords = list(get_lat_and_long(topic.city))

        folium.Marker(location=coords, popup=popup,
                      tooltip=topic.city).add_to(marker_cluster)

    folium.LayerControl().add_to(map)

    return map._repr_html_()


def index(request):
    topics = Topic.objects.all()

    context = {'map': create_map(
        topics), 'form': UploadForm}

    if (request.method == 'POST'):
        form = UploadForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/map/')

    return render(request, 'map/index.html', context)
