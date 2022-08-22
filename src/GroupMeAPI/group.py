import requests
import uuid

BASE_URL = "https://api.groupme.com/v3/"

class Group():
    def __init__(self, token, id=0, from_response_obj=False):
        self.token = token
        if not from_response_obj:
            self.id = id
        else:
            for key, val in from_response_obj.items():
                setattr(self, key, val)
    
    def _verify_success(self, response):
        if response.status_code > 204:
            raise Exception("Status code error: " + response.url + " returned code " + response.status_code + "with meta: " + response.json()["meta"])
    
    def add_members(self, members_to_add):
        res = requests.post(f"{BASE_URL}groups/{self.id}/members/add", headers={"X-Access-Token": self.token}, json={
            "members": members_to_add
        })
        self._verify_success(res)
        return res.json()["response"]["results_id"]
    
    def get_member_add_results(self, results_id):
        res = requests.get(f"{BASE_URL}groups/{self.id}/members/results/{results_id}", headers={"X-Access-Token": self.token})
        if res.status_code == 503 or res.status_code == 404: return False
        self._verify_success(res)
        return res.json()["response"]["members"]
    
    def remove_member(self, membership_id):
        res = requests.post(f"{BASE_URL}groups/{self.id}/members/{membership_id}/remove", headers={"X-Access-Token": self.token})
        self._verify_success(res)
        return True
    
    def update_my_nickname(self, new_nickname):
        res = requests.post(f"{BASE_URL}groups/{self.id}/memberships/update", headers={"X-Access-Token": self.token}, json={
            "membership": {
                "nickname": new_nickname
            }
        })
        self._verify_success(res)
        return True
    
    def get_messages(self, before_id=0, since_id=0, after_id=0, limit=20):
        req_obj = {}
        if before_id != 0: req_obj["before_id"] = before_id
        if after_id != 0: req_obj["after_id"] = after_id
        if since_id != 0: req_obj["since_id"] = since_id
        req_obj["limit"] = limit
        res = requests.get(f"{BASE_URL}groups/{self.id}/messages", headers={"X-Access-Token": self.token}, json=req_obj)
        self._verify_success(res)
        return res.json["response"]["messages"]
    
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

    def send_message(self, text, attachments=[]):
        res = requests.post(f"{BASE_URL}groups/{self.id}/messages", headers={"X-Access-Token": self.token}, json={
            "message": {
                "source_guid": str(uuid.uuid4()),
                "text": text,
                "attachments": attachments
            }
        })
        self._verify_success(res)
        return res.json["response"]["message"]
    
    def get_liked_messages(self, time_period):
        res = requests.get(f"{BASE_URL}groups/{self.id}/likes?period={time_period}", headers={"X-Access-Token": self.token})
        self._verify_success(res)
        return res.json["response"]["messages"]
    
    def get_my_liked_messages(self):
        res = requests.get(f"{BASE_URL}groups/{self.id}/likes/mine", headers={"X-Access-Token": self.token})
        self._verify_success(res)
        return res.json["response"]["messages"]
    
    def get_my_messages_others_have_liked(self):
        res = requests.get(f"{BASE_URL}groups/{self.id}/likes/for_me", headers={"X-Access-Token": self.token})
        self._verify_success(res)
        return res.json["response"]["messages"]