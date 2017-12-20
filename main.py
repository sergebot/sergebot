from flask import Flask,jsonify
from flask import request,render_template
from credentials import credentials
from mapper import MapFunction
import response_handler
import views
import botutils
import utility



# import credential keys
app_token = credentials['ACCESS_TOKEN']
verify_token = credentials['VERIFY_TOKEN']

app = Flask(__name__)

bot = botutils.Messenger_wrapper(app_token)
v = botutils.get_started_btn()
print(v)
botutils.Persistant_menu()


@app.route('/')
def index_page():
    return "OK"

@app.route('/hook',methods=['GET'])
def verify_webhook():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == verify_token:
            return request.args.get("hub.challenge")
        return "OK",200


@app.route('/hook',methods=['POST'])
def handle_incomming_responses():
    if request.method == 'POST':
        response_data = request.get_json()
        # send in the json data into a function and let it send a dict with all the vital stuff ;)
        # pass the response recieved from fb into fb_response_handler class and instantiate it
        # Use the object to access the function which returns the dict with entities
        hResp = response_handler.fb_response_handler()
        # fb dict contains all the required entities for the bot function
        # To get user id : fb_dict['user_id']
        entity_dict = hResp.get_entities_in_dict(response_data)
        #print("parsed dict :",entity_dict)
        #print("launching response handler...")
        handle_message_responses(entity_dict)
        return "OK",200



def handle_message_responses(entity_dict):
    print("showing current entities:",entity_dict)
    # no need for any checking or try-except statements since there's a default
    # payload entity is set to `@default` if anything goes wrong, it launches the default function.
    user_payload = entity_dict['user_payload']

    # add the place_name to the db
    # to make things a bit faster, keep the global var as it is or add some kind of cache mech
    # then only request the location from the db if the place_name var is None due to
    # local var scope or cache expiration

    trigger_tags = {
                    "@get_started": views.intro_message,
                    "@show_top_coins":views.show_top_coins,
                    "@last_hour_coins":views.show_top_coins_last_hour,
                    "@nothing":views.nothing,

    }

    # send in the trigger tag-functions dict and entity_dict to map to the right function
    # and launch it
    mapper = MapFunction(entity_dict, trigger_tags)
    # calls the matched function from the dict
    # sending in the entity_dict so that all the required variables during an event will
    # be avaiable for use (using the dict locally)
    mapper.key_lookup_and_call(entity_dict)



if __name__ == '__main__':
    app.run(debug=True,port=9999,threaded=True)
