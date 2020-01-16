from PIL import Image
import cv2
import pytesseract
import requests
import shutil
import os
from io import BytesIO
#import urllib.request


response = []
url = 'https://img.gadgethacks.com/img/37/33/63696445509613/0/format-whatsapp-messages-with-italic-bold-strikethrough-monospaced-text.w1456.jpg'

#resp = request.get(url, stream=True)
#with open('ingggg.jpg', 'wb') as out_file:
#    shutil.copyfileobj(resp.raw, out_file)
    

response = requests.get(url)
image =  Image.open(BytesIO(response.content))
#image = Image.open(urllib.request.urlopen(url))
text = pytesseract.image_to_string(image)
print(text)


