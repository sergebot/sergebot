
from pymongo import MongoClient

user_name = "crp_users"
password_db = "crp_users"
# mongodb://<dbuser>:<dbpassword>@ds161016.mlab.com:61016/crpx_user_db
connect_url = "mongodb://{0}:{1}@ds161016.mlab.com:61016/crpx_user_db".format(user_name,password_db)

client = MongoClient(connect_url)
db = client.crpx_user_db


def add_user_to_db(user_id):
    user_crp_x = db.crp_users.update({'user_id':user_id},
                {
                    "$set":{
                        "plan":"FREE",
                        "secret_id":None,

                    }
                },upsert=True)
    if user_crp_x.get('ok') and user_crp_x['ok'] == 1.0:
        print("user_added to DB")
    else:
        print("Cant add to db")

def update_user_secretcode(user_id,secret_code):
    user_crp_x = db.crp_users.update({'user_id':user_id},
                {
                    "$set":{
                        "secret_id":secret_code,
                    }
                })
    if user_crp_x.get('ok') and user_crp_x['ok'] == 1.0:
        print("updated secret code for user:",user_id)
    else:
        print("cant add secret code for user:",user_id)

def get_secret_code(user_id):
    user_crp_x = db.crp_users.find({'user_id':user_id})
    if user_crp_x.count() == 0:
        return None
    return [u['secret_id'] for u in user_crp_x]

def get_all_users():
    user_crp_x = db.crp_users.find({})
    return [u['user_id'] for u in user_crp_x ]

def unsubscribe_user(user_id):
    user_crp_x = db.crp_users.remove({'user_id':user_id})
    if user_crp_x.get('ok') and user_crp_x['ok'] == 1.0:
        print('removed ',user_id)

def does_user_exists(user_id):
    # '1763343137041409'
    user_crp_x = db.crp_users.find({'user_id':user_id}).count()
    if user_crp_x:
        return True
    return False


if __name__ == "__main__":
    #add_user_to_db("2355445")
    print(get_secret_code('1763343137041409'))
    #unsubscribe_user("2355445")
    #get_all_users()
