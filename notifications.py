

import botutils
import crypto_db
import user_db
from pymessenger.bot import Bot
from credentials import credentials
from apscheduler.schedulers.blocking import BlockingScheduler

ACCESS_TOKEN = credentials['ACCESS_TOKEN']

bot = botutils.Messenger_wrapper(ACCESS_TOKEN)
sched = BlockingScheduler()

def show_top_coins(user_id):
    top_coin_percent = 30
    top_cryptos = crypto_db.get_percentage('24hr_percent',top_coin_percent)
    print(top_cryptos)
    count = 0
    #crp_str = ""
    for crp in top_cryptos:
        #print(crp,"lol")
        #bot.send_text_message(user_id,"yo")
        crp_str = "{1} ${2} ({0}%). ".format(crp[0],crp[1],crp[2],crp[3])
        bot.send_text_message(user_id,crp_str + "📈")


class push_notification():
    ''' This class contains methods that send notifications
    '''
    @classmethod
    def send_push_notifications(self,msg="hey"):
        users = db.get_users_who_subscribed_for(subscription_type)
        if len(users) is 0:
            return "No subscribers found!"
        for user_id in users:
            show_top_coins(user_id)
            print("message sent!")

@sched.scheduled_job('cron', day_of_week="mon-sun",hour=9,minute=15)
def daily_notifications():
    push_notification.send_push_notifications()

def start_schedueler():
    print("scheduler started!")
    sched.start()

if __name__ == "__main__":
    start_schedueler()
