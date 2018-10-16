from flask import Flask, render_template, url_for, redirect, request, session, flash, logging
from models.model import check_user,user_signup,search_user_by_username
from passlib.hash import sha256_crypt
from forms import RegistrationForm


app = Flask(__name__)
app.config['SECRET_KEY']='Hello'


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


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

		session["username"]=user_info["name"]

		if check_user(user_info["username"]) is None:

			results=user_signup(user_info)
			if(results[0] is True):

				session['user_id'] = str(results[1])
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
		
			flash('Login Sucessful!','success')
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
   # remove the username from the session if it is there
   #session.pop('user_id', None)
	if session:
		session.clear()
		flash('You have logged out','success')
		return redirect(url_for('home'))

	else:
		flash('You have not logged in yet','success')
		return redirect(url_for('home'))	


if __name__ == '__main__':
    app.run(debug=True)
