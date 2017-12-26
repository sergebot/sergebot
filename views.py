

import botutils
import crypto_db
import user_db
from credentials import credentials
from pymessenger.bot import Bot
from  crypto_name_list import crypto_names
from crp_img import crp_img_list


# import credential keys
app_token = credentials['ACCESS_TOKEN']

bot = botutils.Messenger_wrapper(app_token)
bot1 = Bot(app_token)

def intro_message(entity_dict):
    user_id = entity_dict['user_id']
    bot.send_text_message(user_id,"Hey, I'm Serge👽! I'll tell you when cryptocurrency prices sky rockets🚀 and when it hits the ground🌎.")
    bot.send_text_message(user_id,"I'll get you the 5 highest percentage rises out of the Top 5 Coins everyday so you can invest wisely🙌")
    crypto_reply = (["Top coins last 24hr","@show_top_coins","text"],["Nothing","@nothing","text"])
    bot.quick_reply(user_id,"What would you like to do?",crypto_reply)


# img : http://micro.sme.gov.tw/upload/105article/1050406_02.jpg
def show_top_coins(entity_dict):
    user_id = entity_dict['user_id']
    top_coin_percent = 30
    top_cryptos = crypto_db.get_percentage('24hr_percent',top_coin_percent)
    top_cryptos = top_cryptos[0:5] # only top 5 crpyts
    element_data_list = []
    # To dynamically generate the list of cards we loop through the top_cryptos list
    # and extract the required data and put all of it in the required format so
    # that the generic_template function can build cards from it
    for crp in top_cryptos:
        try:
            crp_name = crypto_names[crp[1]] # use the crp symbol to get the name from the dict
            crp_str = "{4}({1}) ${2} ({0}%)📈".format(crp[0],crp[1],crp[2],crp[3],crp_name)
            try:
                cryp_img = crp_img_list[crp[1]]
            except:
                cryp_img = "http://micro.sme.gov.tw/upload/105article/1050406_02.jpg"
            # this  is the required format. It's added to the list
            element_data_list.append({
                                "data":[ crp_str,cryp_img,"",crp[3] ],
                                "button":["web_url",crp[3],"Get it here!"]
                                })
        except:
            pass
    # then the list is added to a dict
    generic_elements = {"element_data":element_data_list}

    # show this message only if the top_cryptos list has less than 3 items
    if len(top_cryptos) < 3:
        bot.send_text_message(user_id,"hm... looks like the market isn't doing too well right now. I'm only showing you coins that have made over a 30% gain. This could change in an hour or so, so make sure to check back 😄")
    bot.generic_template(user_id,generic_elements)
    if not user_db.does_user_exists(user_id):
        ask_free_subscription(entity_dict)

def nothing(entity_dict):
    user_id = entity_dict['user_id']
    bot.send_text_message(user_id,"No worries! I'm always here :)")

def show_premium(entity_dict):
    user_id = entity_dict['user_id']
    premium_cards = [
        {
            "data":[ "Get Premium now!","https://dov5cor25da49.cloudfront.net/products/6586/470x600design_01.jpg","","http://sergebot.com/" ],
            "button":["web_url","http://sergebot.com/","Get it here!"]
        },
        {
            "data":[ "What's my secret code?","http://images.all-free-download.com/images/graphiclarge/blue_3d_geometric_abstract_background_6815669.jpg","secret code makes your transaction more secure","http://sergebot.com/" ],
            "button":["postback","@show_secret_code","Get it here!"]
        },
    ]

    generic_elements = {"element_data":premium_cards}
    bot.generic_template(user_id,generic_elements)

def show_secret_code(entity_dict):
    user_id = entity_dict['user_id']
    bot.send_text_message(user_id,"redridinghood")
    bot.send_text_message(user_id,"The above text is your secret code. You'll be asked for it during the checkout.")


def ask_free_subscription(entity_dict):
    user_id = entity_dict['user_id']
    bot.quick_reply(user_id,"Would you like to get notified when \
    cryptocurrencies prices sky rockets?",(["sub me now!","@subscribe","text"],\
    ["Not now","@nothing","text"]))

def subscribe(entity_dict):
    user_id = entity_dict['user_id']
    user_db.add_user_to_db(user_id)
    bot.send_text_message(user_id,"Awesome! You'll be notified everyday 🔥")

def unsubscribe(entity_dict):
    user_id = entity_dict['user_id']
    user_db.unsubscribe_user(user_id)
    bot.send_text_message(user_id,"You've been unsubscribed!")
