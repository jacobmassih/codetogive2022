import folium
from create_coordinates import get_lat_and_long

places = {"id 0001":{"Argentina":{"idea":"where does Horacio Pagani live?", "comments":{"bob":"idk"}}, "creation":{"author": "jorge", "date": "novembre 5th 2022", "tags": ["life"], "likes":1}},
          "id 0002":{"Malé": {"idea":"vacation", "comments": {"jeff": "nice place"}}, "creation":{"author": "ben", "date": "novembre 6th 2022", "tags": ["life"], "likes":85}},
          "id 0003":{"Montreal, QC": {"idea":"congestion sur la ligne bleue", "comments": {"steven":"rien de nouveau"}}, "creation":{"author": "adam", "date": "novembre 7th 2022", "tags": ["transport", "commute", "life"], "likes":4}},
          "id 0004":{"Tokyo, Japan": {"idea":"what are jdm cars", "comments": {"Han": "life"}}, "creation":{"author": "jamal", "date": "novembre 5th 2022", "tags": ["life", "jdm", "environment", "happiness"], "likes":900000}},
          "id 0005":{"france": {"idea":"baguette", "comments": {"François": "un très bon repas"}}, "creation":{"author": "arthur", "date": "novembre 3rd 2022","tags": ["food", "happiness"], "likes":76}},
          "id 0006":{"deutschland": {"idea":"what is the best beer", "comments": {"chad": "they're all good"}},  "creation":{"author": "josh", "date": "novembre 2nd 2022", "tags": ["happiness", "life"], "likes":60}},
          "id 0007":{"ICELAND": {"idea":"how cold does it get", "comments":{"josh": "very"}},  "creation":{"author": "sergei", "date": "novembre 11th 2022", "tags": ["weather", "environment"], "likes":5}},
          "id 0008":{"Ohio": {"idea":"how many potatoes are collected per day", "comments":{"franck": "lots"}},  "creation":{"author": "vlad", "date": "novembre 5th 2022", "tags": ["food", "environment", "economy", "business"], "likes":89}},
          "id 0009":{"Montreal, QC": {"idea": "congestion sur la ligne orange", "comments": {"steven2": "rien de nouveau"}},  "creation":{"author": "jorge", "date": "novembre 8th 2022", "tags": ["transport"],"likes":86}}
          }

def creat_map(places):
    map = folium.Map(location=[20, 10],
                     zoom_start=2)

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
        <script>
            readInputsForComments()
            </script>
        <p>Comments:</p>
        <ul>
            <comment>{places[id][place]["comments"]}</comment>
        </ul>
        <p>Enter a comment</p>
        <input type="text" id="comment" name="user comment"><br><br>
        <input type="submit" onclick="readInputsForComments" value="Post comment">
        <script></script>
        """
        file = f"idea{id}.html"

        with open(file, "w") as f:
            f.write(idea_html)

        # Generates the content read in the popup bubbles when a location is clicked
        # Todo: fix the link, it's not working

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
            <script></script>
            </p>
            <a href={file}>Click here to read more about the idea</a>
                  
        """
        iframe = folium.IFrame(html=html_on_map, width=300, height=300)
        popup = folium.Popup(iframe, max_width=1650)
        loc = list(get_lat_and_long(place))
        folium.Marker(location=loc, popup=popup, tooltip=place).add_to(map)

    map.save("map.html")
    print("ready")
