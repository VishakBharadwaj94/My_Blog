from flask import Flask, render_template,url_for,redirect
 

app = Flask(__name__)

posts = [
	{
	'author':'Vishak Bharadwaj',
	'title':'My first blogpost',
	'date_posted':'5th September 2018',
	'content':'Fist content'	
	
	}
,
	{
	'author':'Roger Ebert',
	'title'	:'',
	'date_posted':'6th September 2018',
	'content':'second content'	
	
	}
]

@app.route('/')
@app.route('/home')

#	using two decorators redirects both URLs to the same fucntion

def home():

	return render_template('home.html',posts=posts) 

#  you can use ''' and write html code inside''' for eg return ''' <!DOCTYPE html>

#	</html>'''

@app.route('/about')

def about():

	return render_template('about.html',title="About Me")


if __name__=='__main__':
	app.run(debug=True)

