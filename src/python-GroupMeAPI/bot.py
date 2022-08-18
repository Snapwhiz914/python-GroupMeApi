import requests

BASE_URL = "https://api.groupme.com/v3/"

class Bot:
    def __init__(self, token, bot_id=0, from_response_obj=False):
        self.token = token
        if not from_response_obj:
            self.bot_id = bot_id
        else:
            for key, val in from_response_obj.items():
                setattr(self, key, val)
    
    def _verify_success(self, response):
        if response.status_code > 204:
            raise Exception("Status code error: " + response.url + " returned code " + response.status_code + "with meta: " + response.json()["meta"])
    
    def send_message(self, text, picture_url=""):
        res = requests.post(f"{BASE_URL}bots/post", headers={"X-Access-Token": self.token}, json={
            "bot_id": self.bot_id,
            "text": text,
            "picture_url": picture_url
        })
        self._verify_success(res)
        return res.json["response"]["message"]
