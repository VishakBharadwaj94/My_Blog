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