from flask import Flask, request
from flask_cors import CORS

import asf_search
from datetime import datetime, timedelta
from PIL import Image
import requests
import tensorflow as tf

import io
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np

app = Flask(__name__)
CORS(app) 

model = tf.saved_model.load('/Users/abhinavrawal/Desktop/SIH/backend/model')

# @app.route("/")
def get_landslide_images(latitude, longitude):
    # Search for SAR data over the given latitude and longitude.
    centroid = f'POINT({latitude} {longitude})'
    end = datetime.now()
    start = end - timedelta(days = 10)
    results = asf_search.geo_search(platform = [asf_search.PLATFORM.SENTINEL1], intersectsWith = centroid, start = start, end = end)

    image_urls = []
    for result in results:
        img = result.geojson().get("properties").get("browse")
        if img:image_urls += img

    return image_urls

def getImages(latitude = 47.2160, longitude = 9.8160):
    # Extract images for each landslide.
    image_urls = get_landslide_images(latitude, longitude)

    # Save the images to disk.
    paths = []
    for i, image_url in enumerate(image_urls):
        try:
            image_response = requests.get(image_url)
            with open(f"./static/{latitude}_{longitude}_{i}.jpg", "wb") as f:f.write(image_response.content)

            paths.append(f"./static/{latitude}_{longitude}_{i}.jpg")

        except:
            pass
    return paths

def getResult(images):
    result = 0

    if (len(images) == 0):
        return 0
    
    for path in images:
        image = load_img(path, target_size = (256, 256, 3))
        image = img_to_array(image)
        image = np.expand_dims(image, axis = 0)

        y = model.signatures['serving_default'](tf.constant(image))['dense_1']
        print(y, "hi")
        prediction = y.numpy()[0][0]
        result += prediction
    
    return result / len(images)

@app.route("/api/submit", methods=['POST'])
def predict():
    data = request.get_json()
    latitude = float(data['latitude'])
    longitude = float(data['longitude'])

    images = getImages(latitude, longitude)
    result = round(100 * getResult(images), 2)

    return {"result": result}

if __name__ == '__main__':
    app.run(debug = True) 