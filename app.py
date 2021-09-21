from flask import Flask,render_template,request,redirect,url_for
import os
import shutil
from werkzeug.utils import secure_filename
import pyrebase

import random,string



ALLOWED_EXTENSIONS = {'zip'}



def specific_string(length):  
     
    letters = string.ascii_lowercase # define the lower case string  
     # define the condition for random.choice() method  
    result = ''.join((random.choice(letters)) for x in range(length))  
    print(" Random generated string with repetition: ", result)  
    return result


url = "http://192.168.1.36:5000"
firebaseConfig = {
  "apiKey": "AIzaSyDS3vS4p7a8BOluV6aKKGAeXa1KNahNl9c",
  "authDomain": "d-shop-9ae79.firebaseapp.com",
  "projectId": "d-shop-9ae79",
  "storageBucket": "d-shop-9ae79.appspot.com",
  "messagingSenderId": "53986995265",
  "appId": "1:53986995265:web:f48441dcbca0b3e2026ac0",
  "measurementId": "G-978KCFWE4T",
  "databaseURL":"https://d-shop-9ae79-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "./static/models"


@app.route('/')
def index():
	products = db.child("Items").get().val()
	return render_template("homeShop.html",products=products,db=db)

@app.route('/view/<modelName>')
def view(modelName):
	return render_template("index.html",modelName=modelName)

@app.route('/index.js')
def jsMain():

	return url_for('static',filename="index.js")


@app.route('/models/<modelFolder>')
def openModel(modelFolder):
	return url_for('static',filename=f"models/{modelFolder}/scene.gltf")

@app.route('/admin',methods=['POST','GET'])
def admin():
	if request.method == "POST":
		title = request.form['title']
		price = request.form['price']
		modelFolder = request.files['modelFile']
		desc = request.form['description']

		if modelFolder:
			try:
				os.system(f'rm static/models/{title}.zip')
			except:
				pass
			modelFolder.save(os.path.join(app.config['UPLOAD_FOLDER'], title+'.zip'))
			shutil.unpack_archive('./static/models/'+title+'.zip', f'./static/models/{title}')
			os.system(f'rm /static/models/{title}.zip')

			data = {
				'title':title,
				'price':price,
				'modelFolder':title,
				'desc':desc
			}
			db.child("Items").child(title).set(data)

		return redirect('/admin')
	return render_template("admin.html")

@app.route('/product/<title>')
def product(title):
	price = db.child("Items").child(title).child("price").get().val()
	desc = db.child("Items").child(title).child("desc").get().val()
	return render_template("buy.html",title=title,price=price)

@app.route('/buy/<product>',methods=['POST','GET'])
def buy(product):
	if request.method == "POST":
		FullName = request.form['FullName']
		Addr = request.form['Addr']
		City = request.form['City']
		PostalCode = request.form['PostalCode']
		email= request.form['email']
		phoneNumber= request.form['phoneNumber']
		cargo= request.form['cargo']

		#Randomized Key
		the_random_one=specific_string(37)


		data = {'FullName':FullName,'Addr':Addr,'City':City,'PostalCode':PostalCode,'email':email,'phoneNumber':phoneNumber,'Transparent':cargo,'boughtItem':product}
		db.child("Orders").child(the_random_one).set(data)
		
	return render_template("payment.html",title=product,price=db.child("Items").child(product).child("price").get().val())


@app.route('/buyHistory/<token>')
def buyHistoey(token):
	data = db.child("Orders").child(token).get().val()
	return str(data)

app.run(debug=True,host="0.0.0.0")