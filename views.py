

import botutils
import crypto_db
import user_db
from credentials import credentials
from pymessenger.bot import Bot


# import credential keys
app_token = credentials['ACCESS_TOKEN']

bot = botutils.Messenger_wrapper(app_token)
bot1 = Bot(app_token)

def intro_message(entity_dict):
    user_id = entity_dict['user_id']
    user_db.add_user_to_db(user_id)
    bot.send_text_message(user_id,"Hey, I'm Serge🤠! I'll tell you when cryptocurrency prices spike💸📈 up and when it comes down📉.")
    bot.send_text_message(user_id,"I'll get you the 5 highest percentage rises out of the Top 20 Coins everyday so you can invest wisely🙆‍♂")
    crypto_reply = (["Top coins last 24hr","@show_top_coins","text"],["Nothing","@nothing","text"])
    bot.quick_reply(user_id,"What would you like to do?",crypto_reply)

def show_top_coins(entity_dict):
    user_id = entity_dict['user_id']
    top_coin_percent = 30
    top_cryptos = crypto_db.get_percentage('24hr_percent',top_coin_percent)
    top_cryptos = top_cryptos[0:5] # only top 5 crpyts
    for crp in top_cryptos:
        #print(crp,"lol")
        #bot.send_text_message(user_id,"yo")
        crp_str = "{1} ${2} ({0}%)📈".format(crp[0],crp[1],crp[2],crp[3])
        crp_btn_text = [{
                "title":"Get it here💰",
                "type":"web_url",
                "url":crp[3],
            },]
        if len(top_cryptos) < 3:
            bot.send_text_message(user_id,"hm... looks like the market isn't doing too well right now. I'm only showing you coins that have made over a 30% gain. This could change in an hour or so, so make sure to check back 😄")
        bot1.send_button_message(user_id,crp_str,crp_btn_text)

def show_top_coins_last_hour(entity_dict):
    user_id = entity_dict['user_id']
    top_coin_percent = 5
    top_cryptos = crypto_db.get_percentage('1hr_percent',top_coin_percent)
    print(top_cryptos)
    count = 0
    crp_str = ""
    for crp in top_cryptos:
        #print(crp,"lol")
        #bot.send_text_message(user_id,"yo")
        crp_str += "{1} ${2} ({0}%). ".format(crp[0],crp[1],crp[2])
    bot.send_text_message(user_id,crp_str + "📈")


def nothing(entity_dict):
    user_id = entity_dict['user_id']
    bot.send_text_message(user_id,"No worries! I'm always here :)")
