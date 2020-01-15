import PIL
from PIL import Image
import cv2
import pytesseract
import requests
import os
#from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
#from flask_cors import CORS
#from flask_bcrypt import Bcrypt 
#from flask_jwt_extended import JWTManager
#from flask_jwt_extended import (create_access_token)
import cloudinary
import cloudinary.uploader as cloudUpload
import cloudinary.api as cloudAPI


try:
	#app.config["MONGO_URI"] = "mongodb://devtotti:jankulovski@newclustera-shard-00-00-c85ej.mongodb.net:27017,newclustera-shard-00-01-c85ej.mongodb.net:27017,newclustera-shard-00-02-c85ej.mongodb.net:27017/test?ssl=true&replicaSet=NewClusterA-shard-0&authSource=admin&retryWrites=true&w=majority"
	#app.config["JWT_SECRET_KEY"] = 'secret'
	client = MongoClient("mongodb://devtotti:jankulovski@newclustera-shard-00-00-c85ej.mongodb.net:27017,newclustera-shard-00-01-c85ej.mongodb.net:27017,newclustera-shard-00-02-c85ej.mongodb.net:27017/HealthApp?ssl=true&replicaSet=NewClusterA-shard-0&authSource=admin&retryWrites=true&w=majority")
	db = client.imageToText

	#mongo = PyMongo(app)
	#bcyrypt = Bcrypt(app)
	#jwt = JWTManager(app)
	#CORS(app)
	
	cloudinary.config(
	cloud_name = "neptunetech",
	api_key = "522122983864784",
	api_secret = "2nWtDIvF5U7FT5ZoX8J6iR4K6bg"
	)

	print("Connected successfully!")

except Exception as error:
	print("Error here: "+str(error))





def getImgDetails(docName, email, image):

	profile_image = image
	user_email = email
	document_name = docName

	image_url, image_public_id = getImgUrl(profile_image)

	imageText = getImgText(image_url)

	store = saveData(user_email, document_name, imageText, image_url, image_public_id)

	if store == 'success':
		print("File upload successful")

	elif store == 'failure':
		print("File upload failed")



	return imageText




def saveData(user_email, *args):
	email = user_email
	docName = args[0]
	text = args[1]
	url = args[2]
	public_id = args[3]
	upload = db.download

	created = datetime.now()

	try:
		uploads = upload.insert_one({
			"email":email,
			"document":docName,
			"text":text,
			"image_url":url,
			"image_public_id":public_id,
			"created_at":created
			})

		result = "success"

	except Exception as error:
		result = "failure"


	return result






def getImgText(image_url):
	url = image_url

	response = requests.get(url)
	image =  Image.open(BytesIO(response.content))
	#image = Image.open(urllib.request.urlopen(url))
	text = pytesseract.image_to_string(image)

	return text





def getImgUrl(profile_image):
	image =  profile_image

	save_file = cloudUpload.upload(
				profile_image.filename,
				folder = "imageToText"
				)
	image_url = save_file['url']
	image_public_id = save_file['public_id']

	return (image_url, image_public_id)
