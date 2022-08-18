import requests
import uuid

BASE_URL = "https://api.groupme.com/v3/"

class DirectMessage():
    def __init__(self, token, from_response_obj):
        self.token = token
        for key, val in from_response_obj.items():
            setattr(self, key, val)
    
    def _verify_success(self, response):
        if response.status_code > 204:
            raise Exception("Status code error: " + response.url + " returned code " + response.status_code + "with meta: " + response.json()["meta"])
    
    def get_messages(self, use_this_user_id=True, *args):
        res = requests.get(f"{BASE_URL}direct_messages?other_user_id={self.other_user.id if use_this_user_id == True else use_this_user_id}&before_id={args[0]}&since_id={args[1]}", headers={"X-Access-Token": self.token})
        self._verify_success(res)
        return res.json()["response"]
    
    def attachment_obj_creator(type="image", *args):
        if type == "image":
            return {
                "type": type,
                "url": args[0]
            }
        if type == "location":
            return {
                "type": type,
                "name": args[0],
                "lat": args[1],
                "lng": args[2]
            }
        if type == "emoji":
            return {
                "type": type,
                "placeholder": args[0],
                "charmap": args[1]
            }
        if type == "mentions":
            return {
                "type": "mentions",
                "loci": args[0],
                "user_ids": args[1]
            }
        raise Exception("Bad type, must be one of: image, location, emoji, mentions")
    
    def send_message(self, text, attachments=[], use_this_user_id=True):
        res = requests.post(f"{BASE_URL}direct_messages", headers={"X-Access-Token": self.token}, json={
            "source_guid": str(uuid.uuid4()),
            "recipient_id": self.other_user.id if use_this_user_id == True else use_this_user_id,
            "text": text,
            "attachments": attachments
        })
        self._verify_success(res)
        return res.json["response"]["message"]