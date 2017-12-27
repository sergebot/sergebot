

from wit import Wit
from credentials import credentials
from geotext import GeoText

wit_token = credentials["WIT_AI_TOKEN"]


def get_tags(msg):
    client = Wit(wit_token)
    print("input message:",msg)
    resp = client.message(msg)
    if resp["entities"].get("intent"):
        print("In the NLP handler")
        print(resp["entities"]["intent"][0]["value"])
        confidence = resp["entities"]["intent"][0]["confidence"]
        # if the confidence is low show error_msg
        if confidence > 0.5:
            return resp["entities"]["intent"][0]["value"]
        return "@error_msg"
    # default
    print("input message:",msg)
    return "@error_msg"

def is_location(msg):
    places = GeoText(msg)
    if len(places.cities) > 0:
        # remove this condition once the bot is available to other cities
        city_list = ['london','windsor']
        for city in city_list:
            if places.cities[0].lower() == city:
                print("CITY NAME:",places.cities[0].lower())
                return places.cities[0].lower()
            else:
                return "@other_loc"
    return "none"

def check_is_location(loc):
    loc = loc.title() # converts to camel case
    places = GeoText(loc)
    if len(places.cities) > 0:
        return True
    else:
        return False

#print(check_is_location("san francisco"))
