from flask import Flask, request, redirect, Response

import redis
import uuid

# initialize redis connection
session = redis.Redis(host='127.0.0.1', port=6379, db=0)

app = Flask(__name__)

EXCLUDE_AUTH = ["login", "assets"]
@app.before_request # before any request middleware
def global_middleware():
	parent_path = request.path.split("/")[1]
	if parent_path not in EXCLUDE_AUTH:
		is_logged = False
		# apakah visitor telah memiliki guid
		if "guid" in request.cookies:
			# jika telah memiliki
			guid = request.cookies["guid"]
			# ambil username berdasar guid
			username = session.get(guid)
			if username is not None: # jika username DITEMUKAN
				logged_guid = session.get(username) # coba ambil info guid yang digunakan berdasar username
				if logged_guid is not None: # jika guid yang dicari DITEMUKAN maka login valid
					is_logged = True
		if is_logged == False:
			# http://localhost:3001/ will redirect to http://localhost:3001/login
			# if wasn't logged
			return redirect("http://localhost:3001/", code=302)

@app.route("/")
def _index():
	return 'SUKSES LOGIN !'

app.run(port=3002)
