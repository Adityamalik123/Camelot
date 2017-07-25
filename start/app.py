from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, User
from flask import session as login_session
import random, string
from werkzeug.security import generate_password_hash, check_password_hash
import os, sys
from message import regText

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

engine = create_engine('mysql+pymysql://sql12186731:Nww4rvFEwW@sql12.freemysqlhosting.net:3306/sql12186731')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def get_current_user():
	user_result = None
	if 'id' in login_session:
		id = login_session['id']
		user_result=session.query(User).filter_by(id=id).one()
	return user_result



@app.route('/')
def index():
	return 'welcome'


@app.route('/register', methods=['POST', 'GET'])
def register():
	user = get_current_user()
	if request.method == 'POST':
		existing_user=session.query(User).filter_by(email=request.form['email']).first()
		if existing_user:
			return 'already exists email'

		otp=regText(request.form['mobile'])
		hashed_password=generate_password_hash(request.form['password'], method='sha256')
		newUser=User(name=request.form['name'], password=hashed_password, email
			=request.form['email'], mobile=request.form['mobile'], admin=0, company=request.form['company-select'])
		session.add(newUser)
		session.commit()

		id=session.query(User.id).filter_by(email=request.form['email']).one()
		login_session['id']=id
		return redirect(url_for('index'))

	return '''<form method="POST" action="/register"><input type="text" name="name" placeholder="Name"><br/><input type="password" name="password" placeholder="Password">/
	<br/><input type="text" name="mobile" placeholder="Contact No."><br/><input type="text" name="email" placeholder="Email ID">/
	<br/><input type="text" name="company-select" placeholder="Company"><button type="submit" value="Submit"></button></form>'''


	

@app.route('/login', methods=['GET', 'POST'])
def login():
	user=get_current_user()
	if request.method=='POST':
		email=request.form['email']
		password=request.form['password']
		user_result=session.query(User).filter_by(email=email).first()
		if user_result:
			if check_password_hash(user_result.password, password):
				login_session['id']=user_result.id
				if user_result.admin==1:
					return redirect(url_for(admin))
				return redirect(url_for('index'))
			else:
				return 'wrong password'
		else:
			return 'no user'
	return '''<form method="POST" action="/login"><input type="text" name="email" placeholder="Email ID"><br/><input type="password" name="password" placeholder="Password">/
	<button type="submit" value="Submit"></button></form>'''

#@app.route('/Slotbooking')


@app.route('/logout')
def logout():
	login_session.pop('id', None)
	return redirect(url_for('index'))

#@app.route('/testimonials')
#return render_template('testimonials.html')

#@app.route('/admin')
#return render_template('admin.html')

#@app.route('/CompanyControl')
#def 
#@app.route('/set_testimonials')

#@app.route('/promote/<int:user_id>')

#@app.route('/users')

if __name__ == '__main__':
	app.run(host="0.0.0.0" , port= 5000, debug=True)