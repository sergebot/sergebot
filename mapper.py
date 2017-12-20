

class MapFunction(object):
    """ class that maps functions to key words. Here key words are the payload
         keys set in the request/payload builder
    """
    def __init__( self, entity_dict,trigger_dict):
        self.user_payload = entity_dict['user_payload']
        self.trigger_dict = trigger_dict

    def key_lookup_and_call(self,entity_dict):
        """ Looks for the user_payload key in the flow_payload
              Then checks if the user_payload is equal,  if true calls
              the function which is mapped to the user_payload

              trigger_dict format :

              { 'payload': function_reference,....}
        """
        self.entity_dict = entity_dict
        # looping through the tag names in the dict
        # then checking if the current key is equal
        # if true launch the function
        for dict_key in self.trigger_dict.keys():
            if dict_key == self.user_payload:
                # fb sends 2 requests. How i came to know about this is due to the different
                # user_ids in the json body. Not sure why they do it, but the first response from
                # fb seems to be fine, but the second response is a bit different.
                # It only has a user_id key-vlue pair, probably it's for some kind of security verification.
                # so here we check if the dict has more than 1 entity, this means it's the first response
                # and does't launch any function
                # works as expected, needs some tuning though
                if len(self.entity_dict) > 1:
                    #print("launching trigger function")
                    self.trigger_dict[dict_key](self.entity_dict)
                else:
                    pass
