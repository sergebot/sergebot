
# This module contains fb_response_handler class to parse the json object sent by FB


class fb_response_handler(object):
    ''' This class handles the fb response object
    '''
    def __init__(self):
        # this dict will be filled with all the necessery data and returned
        # set defaults so it doesnt throw an error
        self.entity_collection = {
            "user_payload":"@default",
        }

    def get_entities_in_dict(self,data):

        ''' This is the ugly part of the bot. This parses the json
            response sent by FB and puts them into a dict.
        '''
        self.data = data
        for event in self.data['entry']:
            if event.get('messaging'):
                messaging = event['messaging']
                for x in messaging:
                    if x.get('message'):
                        self.entity_collection['user_id'] = x['sender']['id']

                        if x['message'].get('text'):
                            self.entity_collection['user_msg'] = x['message']['text']
                            print("got the text!")

                        if x['message'].get('quick_reply'):
                            self.entity_collection['user_payload'] = x['message']['quick_reply']['payload']

                        if x['message'].get('attachments'):
                            if x['message']['attachments'][0].get('payload'):
                                if x['message']['attachments'][0]['payload'].get('coordinates'):
                                    self.entity_collection['location'] = x['message']['attachments'][0]['payload']['coordinates']

                    if x.get('postback'):  # for postback getstarted button
                        self.entity_collection['user_id'] = x['sender']['id']
                        if x['postback'].get('referral'):
                            if x['postback']['referral'].get('ref'):
                                self.entity_collection['user_payload'] = x['postback']['referral']['ref']
                        if x['postback'].get('payload'):
                            self.entity_collection['user_payload'] = x['postback']['payload']
        return self.entity_collection
