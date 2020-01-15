from flask import Flask, jsonify, request, render_template, redirect
from datetime import datetime
from data import *

app = Flask(__name__)


@app.route("/user", methods=['POST'])
def getData():
	docName = request.form['docname']
	email = request.form['email']

	if request.files:
		image = request.files['dropfile']

		response = getImgDetails(docName, email, image)

	else:
		response = "Please add a file"


	result = {"response":response}


	return jsonify(result)


@app.route('/')
def index():
	return render_template('index.html')



if __name__ == '__main__':
	app.run(host="localhost", port=4000, debug=True)

