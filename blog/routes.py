import os
import os.path
from flask import render_template, url_for, redirect, request, session, flash, logging
from blog import app
from blog.model import check_user,user_signup,search_user_by_username,change_password,change_uname,add_post_db,all_posts,find_post,delete,check_pic,pic_status
from passlib.hash import sha256_crypt
from blog.forms import RegistrationForm
from blog.nocache import nocache
from PIL import Image 
import datetime



@app.after_request
def add_header(response):
    
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route("/")
@app.route("/home")
@nocache
def home():

	posts=all_posts()
	return render_template('home.html',posts=posts)


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact")

def contact():

	return render_template("contact.html")


#follow the below format in wtforms, 1st create a class for every form needed


@app.route("/register",methods=['GET','POST'])

def register():

	form = RegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		user_info={}

		user_info["name"] = form.name.data
		user_info["username"] = form.username.data
		user_info["email"] = form.email.data
		user_info["password"] = sha256_crypt.encrypt(str(form.password.data))

		if check_user(user_info["username"]) is None:

			results=user_signup(user_info)
			if(results[0] is True):
				session['username'] = user_info['username']
				session['user_id'] = str(results[1])
				session['name'] = user_info['name']
				app.logger.info("SIGNUP SUCCESSFUL")
				flash('signup Sucessful!','success')
			return redirect(url_for('home'))
		
		else:	

			flash('the username already exists. Please enter another username','danger')
			return(redirect(url_for('register')))
	else:

		return render_template("register.html",form=form)



@app.route("/login", methods=['GET','POST'])

def login():
	
	#wtforms not needed here

	if request.method == 'POST':

		inbound_username = request.form['username']
		existing_user = search_user_by_username(inbound_username)
		if (existing_user is None):
			app.logger.info("NO USER")
			error="Username or Password is incorrect!"
			return render_template('login.html',error=error)

		elif(sha256_crypt.verify(request.form['password'],existing_user['password'])):
			app.logger.info("PASSWORD MATCHED,LOGGING IN")
		
			session['user_id'] = str(existing_user['_id'])
			session['username']=existing_user['username']
			session['name']=existing_user['name']
			session['email']=existing_user['email']
		
			flash('Login Sucessful!','success')

			if session.get('prev_page') and session.get('user_id'):
				session['next_page'] = session['prev_page']
				session.pop('prev_page')
				return redirect(url_for(session['next_page']))
			
			else:

				return redirect(url_for('home'))



		else: 
			app.logger.info("WRONG PASSWORD")
			error="Username or Password is incorrect!"
			return render_template('login.html',error=error)

	

	if ("user_id" in session.keys()):
		
		
		return render_template('home.html')

	
	return render_template('login.html')


@app.route('/logout',methods=['GET','POST'])
def logout():

	session.clear()
	flash('You have logged out','success')
	return redirect(url_for('home'))

@app.route('/account', methods=['GET'])
def account():

	if session.get('next_page')=='account' or session.get('user_id'):

		default = False
		name = session['username']+'.jpg'
		pic_path=os.path.join(app.root_path,'static/profile_pics',name)

		if os.path.isfile(pic_path):
			session['pic']=True
			pass 	

		else:
			default = True
			name = 'default.jpg'
			pic_path=os.path.join(app.root_path,'static/profile_pics',name)
		


		if session.get('user_id'):

			session.pop('next_page',None)
			return render_template('account.html',title='Account',default=default)

		else:
			
			return render_template('account.html',title='Account',default=default)





	else:
		session['prev_page']='account'
		error="You have to login to access this page"
		return render_template('login.html',error=error)

@app.route('/change_username',methods=['GET','POST'])

def change_username():

	if request.method=='POST':

		present_name = session['username']
		new_uname = request.form['username']

		if search_user_by_username(new_uname) is not None:

			flash('username exists, enter some other username','danger')
			return(redirect(url_for('account')))

		else:

			change_uname(new_uname,session['user_id'])
			flash('your username has been changed has been changed','success')
			return redirect(url_for('home'))

	else:

		return(redirect(url_for('account')))


			
@app.route('/change_password',methods=['GET','POST'])

def change_pass():

	if request.method=='POST':

		p1 = request.form['npassword']
		p2 = request.form['rnpassword']

		existing_user = search_user_by_username(session['username'])
		temp = (sha256_crypt.verify(request.form['password'],existing_user['password']))

		if sha256_crypt.verify(request.form['password'],existing_user['password']):

			if p1==p2:
				p3=sha256_crypt.encrypt(str(p1))
				change_password(p3,session['user_id'])
				flash('password has been changed','success')
				return redirect(url_for('home'))

			else:

				error="New password entries don't match"
				return render_template('account.html',error=error)
				
		else:

				error="Wrong password entered by user"
				return render_template('account.html',error=error)

	else:

		return(redirect(url_for('account')))	


@app.route('/uploadimage', methods=['GET','POST'])

def uploadimage():


	try:
		pic = request.files['image']
	except NameError:
		pic = None
	except KeyError:
		pic = None

	if pic is None:

		flash('No picture uploaded','danger')
		return redirect(url_for('account'))
	else:
		
		name = session['username'] + '.jpg'
		pic_path=os.path.join(app.root_path,'static/profile_pics',name)
		pic.save(pic_path)
		pic_status('yes',session['username'])
		return redirect(url_for('account'))

@app.route("/remove_pic",methods=['GET','POST'])

def remove():

	if request.method=='GET':

		return(redirect(url_for('account')))

	else:
		name = session['username'] + '.jpg'
		pic_path=os.path.join(app.root_path,'static/profile_pics',name)
		os.remove(pic_path)
		session.pop('pic',None)
		pic_status('no',session['username'])
		return(redirect(url_for('account')))
 
@app.route('/post/new', methods=['GET','POST'])

def new_post():

	if request.method=='GET':

		return render_template('create_post.html',title='New Post')

	else:
		post_info={}
		post_info['title'] = request.form['title']
		post_info['body'] = request.form['body']	
		post_info['name'] = session['username']
		post_info['date'] = datetime.datetime.now()
		post_info['dp'] = check_pic(session['username'])
		add_post_db(post_info)	
		flash('your post has been created!','success')
		return redirect(url_for('home'))


@app.route('/post',methods=['POST'])

def post():
	
	post_id = request.form['id']
	post = find_post(post_id)
	session['post_id']=str(post['_id'])
	return render_template('post.html',post=post)


@app.route('/delete', methods=['POST'])

def delete_post():

	post_id = request.form['id']
	name =  request.form['name']
	if name ==session['username']:

		post_id = session['post_id']
		post = delete(post_id)
		del session['post_id']
		flash('your post has been deleted','success')
		return redirect(url_for('home'))

	else:

		flash('you cannot delete this post,redirecting to homepage!','danger')
		return(redirect(url_for('home')))

@app.route("/posts",methods=['POST'])

def user_posts():

	name = request.form['search']
	import pdb;pdb.set_trace()
	posts= find_posts_by_title(name)
	return render_template('home.html',posts=posts)






