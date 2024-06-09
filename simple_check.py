import pymongo


mongo_client = pymongo.MongoClient("mongodb://localhost:27020/")

test_db = mongo_client["testDatabase"]
users = test_db['users']

users_ids = {user['_id'] for user in users.find()}
print(f'There are {len(users_ids)} unique users')
