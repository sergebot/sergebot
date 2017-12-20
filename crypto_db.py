
from pymongo import MongoClient
from operator import itemgetter



user_name = "crypto_list"
password_db = "sergebot"
connect_url = "mongodb://{0}:{1}@ds159856.mlab.com:59856/current_crypo".format(user_name,password_db)

client = MongoClient(connect_url)
db = client.current_crypo

def add_crypto(crypt_sym,p1hr,p24hr,p7d,cryp_price,link):
    crp_x = db.crypto_list.update({'crp_symbol':crypt_sym},
            {
                "$set":{
                    "1hr_percent":float(p1hr[0:-1]), # convert the str to float and remove %
                    "24hr_percent":float(p24hr[0:-1]),
                    "7d_percent":float(p7d[0:-1]),
                    "cur_cryp_price":float(cryp_price[1:]),
                    "link":link,
                }
            },upsert=True)
    if crp_x.get('ok') and crp_x['ok'] == 1.0:
        print("{} added to db...".format(crypt_sym))
    else:
        print("failed to add to db:{}".format(crypt_sym))

def get_all_cryptos():
    if db.crypto_list.count() == 0:
        return 'empty'
    crp_x = db.crypto_list.find({})
    return [cyx for cyx in crp_x]

def get_percentage(key,rise):
    top_cryptos_list = []
    crp_x = db.crypto_list.find({key:{'$gt':rise}})
    sort_crp_x = sort_using_key(crp_x,key)
    for x in sort_crp_x:
        print((x[key],x['crp_symbol'],x['cur_cryp_price']))
        top_cryptos_list.append((x[key],x['crp_symbol'],x['cur_cryp_price'],x['link']))
    return top_cryptos_list

def remove_cryptos(key):
    if key == 'remove-all':
        crp_x = db.crypto_list.remove({})
        if crp_x.get('ok') and crp_x['ok'] == 1.0:
            print('Cleaned up the DB...')
    else:
        crp_x = db.crypto_list.remove({'crp_symbol':key})
        if crp_x.get('ok') and crp_x['ok'] == 1.0:
            print('removed ',key)


def sort_using_key(xdict,sort_using_key):
    if not xdict:
        return None
    return sorted(xdict, key=itemgetter(sort_using_key),reverse=True)


if __name__ == "__main__":
    #add_crypto("BTC",3.44,6.22,48.33,19588)
    #add_crypto("ETH",3.44,6.22,48.33,19588)
    #print(get_all_cryptos())
    get_percentage('24hr_percent',30)
    #remove_cryptos('remove-all')
