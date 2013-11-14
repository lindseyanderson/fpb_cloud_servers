from flask import render_template, flash, redirect, request
from app import app
from forms import LoginForm
import pyrax
import pyrax.exceptions as exc

@app.route('/', methods = ['POST', 'GET'])
@app.route('/login', methods = ['POST', 'GET'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    return redirect('/auth')
  return render_template('login.html',
    title = 'Sign In',
    form = form)

@app.route('/auth', methods = ['POST'])
def auth():
  username = str(request.form['username'])
  apikey   = str(request.form['apikey'])  

  try: 
    pyrax.settings.set('identity_type', 'rackspace')
    pyrax.set_credentials(username, apikey)
  except exc.AuthenticationFailed:
    return redirect('/login')

  cloudservers_ord = pyrax.connect_to_cloudservers(region="ORD")
  cloudservers_dfw = pyrax.connect_to_cloudservers(region="DFW")
  cloudservers_iad = pyrax.connect_to_cloudservers(region="IAD")

  cloudservers = cloudservers_ord.list() + cloudservers_dfw.list() + cloudservers_iad.list()
  return render_template('cloud_servers.html',
    title = 'Cloud Servers',
    username = username,
    servers = cloudservers)
