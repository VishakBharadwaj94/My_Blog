import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId



client = MongoClient()
db = client['blogs']


def user_signup(user_info):
	#save user info dictionary inside mongo
	results = db['users'].insert_one(user_info)
	filter_query = {'username' :user_info['username']}
	results= db['users'].find_one(filter_query)
	
	return (True,results['_id']) 

def check_user(username):
	
	filter_query = {'username' :username}
	results= db['users'].find(filter_query)

	if(results.count()>0):
		return results.next()

	else:
		return None

def search_user_by_username(username):
	filter_query = {'username' :username}
	results = db['users'].find(filter_query)

	if(results.count()>0):
		return results.next()

	else:
		return None 

def change_password(password,user_id):

	db['users'].update({"_id" : ObjectId(user_id)},{"$set":{"password":password}})

def change_uname(uname,user_id):

	db['users'].update({"_id" : ObjectId(user_id)},{"$set":{"username":uname}})

def add_post_db(post):

	db['posts'].insert_one(post)

	return True

def all_posts():

	#offset = 5
	#limit  = 5

	#f_post = db['posts'].find({}).sort('date',pymongo.DESCENDING)
	#l_post = f_post[offset]['date']

	#results = db['posts'].find({"date":{"lte":l_post}}).sort('date',pymongo.DESCENDING).limit(limit)
	results = db['posts'].find().sort('date',pymongo.DESCENDING)
	return results

def find_post(user_id):

	result = db['posts'].find_one({"_id" : ObjectId(user_id)})
	return result


def delete(user_id):
	db['posts'].remove({"_id" : ObjectId(user_id)})
	return True

def check_pic(name):
	result = db['posts'].find_one({"name" : name })
	if result is None:

		return None
	else:
		
		if result.get('pic')=='yes':
			return 'yes'

		else:

			return 'no'

def pic_status(status,name):

	db['users'].update({"username" : name },{"$set":{"dp":status}})
	db['posts'].update({"name" : name },{"$set":{"dp":status}},multi=True,upsert=False)












