from flask import Flask, request, redirect, make_response, Response

import redis
import uuid

# initialize redis connection
session = redis.Redis(host='127.0.0.1', port=6379, db=0)

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == "GET":
		if "guid" in request.cookies:
			login_html = """
<a href="/">click here</a> to access restricted page, you will redirected back to /login if haven't logged in
<br><br>
<form action="" method="post">
   <input type="text" name="username">
   <br>
      <input type="password" name="password">
      <br>
      <button type="submit">login</button>
</form>
			"""
			return Response(login_html, mimetype='text/html')
		else:
			# generate guid, use uuid.uuid4(), set cookie
			# then redirect to login, any user must have guid cookie
			# !IMPORTANT
			response = make_response(redirect('/login'))
			response.set_cookie('guid', value=uuid.uuid4().hex, max_age=604300, path="/", httponly=True)
			return response
	else:
		if "username" in request.form and "password" in request.form:
			username = request.form["username"]
			password = request.form["password"]
			if username == "kuda" and password == "kuda":
				# tugas nya mencatat bahwa GUID login dengan akun berUSERNAME xxx
				guid = request.cookies["guid"]
				user_gid = "gid-{}".format(guid) # user get user gid
				session.set(username, guid, 604800) # username ini sedang dipakai guid ini
				session.set(guid, username, 604800) # guid ini sedang memakai username ini
				session.set(user_gid, username, 604800) # guid (diformat gid-) sedang menggunakan username ini
				return redirect("/", code=302)
		return redirect("/login", code=302)

@app.route('/logout')
def logout():
	if "guid" in request.cookies:
		guid = request.cookies["guid"]
		user_gid = "gid-{}".format(guid) # sama seperti line 38
		session.delete(user_gid) # hapus key user_gid dari redis
		session.delete(guid) # hapus guid dari redis
	return redirect("/login", code=302)

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
			return redirect("/login", code=302)

@app.route("/")
def _index():
	return 'Logged <a href="/logout">Click here to logout</a>'

app.run(port=3001)
