import asf_search
from datetime import datetime, timedelta
from PIL import Image
import requests
import tensorflow as tf

import io
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
 
model = tf.saved_model.load('/Users/abhinavrawal/Desktop/SIH/backend/model')

latitude = 47.2160
longitude = 9.8160

def get_landslide_images():
    centroid = f'POINT({latitude} {longitude})'
    end = datetime.now()
    start = end - timedelta(days = 10)
    results = asf_search.geo_search(platform = [asf_search.PLATFORM.SENTINEL1], intersectsWith = centroid, start = start, end = end)

    image_urls = []
    for result in results:
        img = result.geojson().get("properties").get("browse")
        if img:image_urls += img

    return image_urls


image_urls = get_landslide_images()
image_response = requests.get(image_urls[0])

with open(f"./static/{latitude}_{longitude}.jpg", "wb") as f:
    f.write(image_response.content)


image = load_img(f"./static/{latitude}_{longitude}.jpg", target_size = (512, 512))
image = img_to_array(image)
image = np.expand_dims(image, axis = 0)
# result = model.predict(image)
print(image)