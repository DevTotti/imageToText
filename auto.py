from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from flask_cors import CORS
from flask_bcrypt import Bcrypt 
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token)
import cloudinary
import cloudinary.uploader as cloudUpload
import cloudinary.api as cloudAPI

app = Flask(__name__)



#app.config['MONGO_DBNAME'] = 'mongotask'
try:
	app.config["MONGO_URI"] = "mongodb://devtotti:jankulovski@newclustera-shard-00-00-c85ej.mongodb.net:27017,newclustera-shard-00-01-c85ej.mongodb.net:27017,newclustera-shard-00-02-c85ej.mongodb.net:27017/test?ssl=true&replicaSet=NewClusterA-shard-0&authSource=admin&retryWrites=true&w=majority"
	app.config["JWT_SECRET_KEY"] = 'secret'

	mongo = PyMongo(app)
	bcyrypt = Bcrypt(app)
	jwt = JWTManager(app)
	CORS(app)
	
	cloudinary.config(
	cloud_name = "neptunetech",
	api_key = "522122983864784",
	api_secret = "2nWtDIvF5U7FT5ZoX8J6iR4K6bg"
	)

	print("Connected successfully!")

except Exception as error:
	print("Error here: "+str(error))



@app.route("/")
def index():
	return """
		<form method="POST" action="/create" enctype="multipart/form-data">
			<input type="text" name="username">
			<input type="text" name="email">
			<input type="file" name="profile_image">
			<input type="text" name="description">
			<input type="text" name="password">
			<input type="submit">
		</form>
	"""


@app.route("/create", methods=['POST'])
def create():
	upload = mongo.db.users
	if request.files:
		try:
			profile_image = request.files['profile_image']

			save_file = cloudUpload.upload(
				profile_image.filename,
				folder = "FlaskProjects"
				)

			created = datetime.utcnow()
			user_name =  request.form['username']
			email = request.form['email']
			password = request.form['password']
			desc = request.form['description']
			passw = bcyrypt.generate_password_hash(password)
			file_name = profile_image.filename
			file_url = save_file['url']
			file_public_id = save_file['public_id']
		
			try:
				uploads = upload.insert_one({'username': user_name,'email': email,'password': passw,'created': created, 'profile_name':file_name, 'description': desc, 'file_url': file_url, 'file_id':file_public_id})
				result = ('file '+ str(file_name)+ ' successfully uploaded')

			except Exception as error:
				result = 'Error heree: '+str(error)


		except Exception as error:
			result = error

	else:
		result = "Error uploading"



	return str(result)


if __name__ == '__main__':
	app.run(host="localhost", port=5014, debug=True)

