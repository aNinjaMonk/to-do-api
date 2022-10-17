import pymongo

# connect to mongodb atlas db 
client = pymongo.MongoClient("mongodb+srv://root:govind12@todo-api-assessment-dat.8aeftkc.mongodb.net/test")
db = client.todo_db

# data = {
#     "name": "Amol",
#     "age": 21,
#     "city": "Nashik"

# }

# insert data into db
# try:
#     db.users.insert_one(data)
# except Exception as e:
#     print(e)

# update data and delete previous in db
# try:
#     db.users.update_one({"name": "Govind"}, {"$set": {"age": 41}})
# except Exception as e:
#     print(e)

# delete data from db
# try:
#     db.users.delete_one({"name": "Govind"})
# except Exception as e:
#     print(e)

# get data from db
# try:
#     data = db.users.find_one({"name": "Amol"})
#     print(data['name'],data['age'],data['city'],data['_id'])
# except Exception as e:
#     print(e)

#get all data from db
# try:
#     data = db.users.find()
#     for i in data:
#         print(i)
# except Exception as e:
#     print(e)

# delete all data from db
try:
    db.users.delete_many({})
except Exception as e:
    print(e)

