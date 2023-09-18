from flask import Flask
from flask_cors import CORS

import asf_search
from datetime import datetime, timedelta
from PIL import Image
import requests
import tensorflow as tf

import io
''' Worst backend written in my life'''

app = Flask(__name__)
CORS(app) 
# model = tf.keras.models.load_model('model_path')

def get_landslide_images(latitude, longitude):
    """Extracts images of landslides from the ASF SearchAPI using the
    given latitude and longitude.

    Args:
        latitude: The latitude of the landslide.
        longitude: The longitude of the landslide.

    Returns:
        A list of URLs to images of the landslide.
    """

    # Search for SAR data over the given latitude and longitude.
    centroid = f'POINT({latitude} {longitude})'
    end = datetime.now()
    start = end - timedelta(days = 10)
    results = asf_search.geo_search(platform = [asf_search.PLATFORM.SENTINEL1], intersectsWith = centroid, start = start, end = end)

    # Extract the URLs to the images.
    image_urls = []
    for result in results:
        img = result.geojson().get("properties").get("browse")
        if img:image_urls += img

    return image_urls

# @app.route("/")
def getImages(latitude = 47.2160, longitude = 9.8160):
    # Extract images for each landslide.
    image_urls = get_landslide_images(latitude, longitude)

    # Save the images to disk.
    for i, image_url in enumerate(image_urls):
        try:
            image_response = requests.get(image_url)
        
            with open(f"./static/{latitude}_{longitude}_{i}.jpg", "wb") as f:f.write(image)

        except:
            pass
    return len(image_urls)

@app.route("/api/submit", methods=['POST'])
def predict():
    # data = request.get_json()
    # latitude = float(data['latitude'])
    # longitude = float(data['longitude'])


    latitude = 45.234
    longitude = 9.234

    # n = getImages(latitude, longitude)
    # average prediction script goes here:

    # result = model.predict()
    result = 71.32
    return {"result": result}

if __name__ == '__main__':
    app.run(debug = True) 