import requests
from group import Group
from dm import DirectMessage
from bot import Bot

BASE_URL = "https://api.groupme.com/v3/"

class User:
    def __init__(self, token):
        self.token = token
        self.group_id = 0
    
    def _verify_success(self, response):
        if response.status_code > 204:
            raise Exception("Status code error: " + response.url + " returned code " + response.status_code + "with meta: " + response.json()["meta"])
    
    def get_groups(self, page=1, per_page=10, omit_memberships=False):
        omit_str = "&omit=memberships" if omit_memberships else ""
        res = requests.get(f"{BASE_URL}groups?page={page}&per_page={per_page}{omit_str}", headers={"X-Access-Token": self.token})
        self._verify_success(res)
        groups = []
        for raw_group in res.json()["response"]:
            groups.append(Group(from_response_obj=raw_group))
        
    def get_former_groups(self):
        res = requests.get(f"{BASE_URL}groups/former", headers={"X-Access-Token": self.token})
        self._verify_success(res)
        groups = []
        for raw_group in res.json()["response"]:
            groups.append(Group(self.token, from_response_obj=raw_group))
    
    def get_group(self, group_id):
        res = requests.get(f"{BASE_URL}group/{group_id}", headers={"X-Access-Token": self.token})
        self._verify_success(res)
        return Group(self.token, from_response_obj=res.json()["response"])
    
    def create_group(self, name, desc="", image_url="", share=False):
        assert name is not ""
        res = requests.post(f"{BASE_URL}group/", headers={"X-Access-Token": self.token}, json={"name": name, "desc": desc, "image_url": image_url, "share": share})
        self._verify_success(res)
        return Group(self.token, from_response_obj=res.json()["response"])
    
    def update_group(self, group_id, name="", desc="", image_url="", office_mode="", share=False):
        res = requests.post(f"{BASE_URL}group/{group_id}/update", headers={"X-Access-Token": self.token}, json={"name": name, "desc": desc, "image_url": image_url, "office_mode": office_mode, "share": share})
        self._verify_success(res)
        return Group(self.token, from_response_obj=res.json()["response"])
    
    def destroy_group(self, group_id):
        res = requests.post(f"{BASE_URL}group/{group_id}/destroy", headers={"X-Access-Token": self.token})
        self._verify_success(res)
        return True
    
    def join_group(self, group_id, share_token):
        res = requests.post(f"{BASE_URL}groups/{group_id}/join/{share_token}", headers={"X-Access-Token": self.token})
        self._verify_success(res)
        return True
    
    def rejoin_former_group(self, group_id):
        res = requests.post(f"{BASE_URL}groups/join", headers={"X-Access-Token": self.token}, json={"group_id": group_id})
        self._verify_success(res)
        return True
    
    def change_owner(self, group_id, new_owner_user_id):
        res = requests.post(f"{BASE_URL}groups/change_owners", headers={"X-Access-Token": self.token}, json={
            "requests": [
                {
                    "group_id": group_id,
                    "owner_id": new_owner_user_id
                }
            ]
        })
        self._verify_success(res)
        return res.json()["response"]["results"][0]["status"]
    
    def get_dms(self, page=1, per_page=10):
        res = requests.post(f"{BASE_URL}chats", headers={"X-Access-Token": self.token})
        self._verify_success(res)
        dms = []
        for raw_dm in res.json()["response"]:
            dms.append(DirectMessage(from_response_obj=raw_dm))
        return dms
    
    def like_message(self, conversation_id, message_id):
        res = requests.post(f"{BASE_URL}messages/{conversation_id}/{message_id}/like", headers={"X-Access-Token": self.token})
        self._verify_success(res)
        return True
    
    def unlike_message(self, conversation_id, message_id):
        res = requests.post(f"{BASE_URL}messages/{conversation_id}/{message_id}/unlike", headers={"X-Access-Token": self.token})
        self._verify_success(res)
        return True
    
    def create_bot(self, name, group_id, avatar_url="", callback_url="", dm_notification=False):
        #idk if this will work, but if you want the bot to recive dms for this user, set group_id to an empty string and set dm_notification to True
        res = requests.post(f"{BASE_URL}bots", headers={"X-Access-Token": self.token}, json={
            "bot": {
                "name": name,
                "group_id": group_id,
                "avatar_url": avatar_url,
                "callback_url": callback_url,
                "dm_notification": dm_notification
            }
        })
        self._verify_success(res)
        return Bot(self.token, from_response_obj=res.json()["response"])

    def get_bots(self):
        res = requests.get(f"{BASE_URL}bots", headers={"X-Access-Token": self.token})
        self._verify_success(res)
        bots = []
        for raw_bot in res.json()["response"]:
            bots.append(Bot(from_response_obj=raw_bot))
        return bots
    
    def delete_bot(self, bot_id):
        res = requests.post(f"{BASE_URL}bots/destroy", headers={"X-Access-Token": self.token}, json={"bot_id": bot_id})
        self._verify_success(res)
        return res.json()["response"]
    
    def get_my_user_info(self):
        res = requests.get(f"{BASE_URL}/users/me", headers={"X-Access-Token": self.token})
        self._verify_success(res)
        return res.json["response"]
    
    def update_my_user_info(self, avatar_url="", name="", email="", zip_code=""):
        req_obj = {}
        if avatar_url != "": req_obj["avatar_url"] = avatar_url
        if name != "": req_obj["name"] = name
        if email != "": req_obj["email"] = email
        if zip_code != "": req_obj["zip_code"] = zip_code
        res = requests.post(f"{BASE_URL}users/update", headers={"X-Access-Token": self.token}, json=req_obj)
        self._verify_success(res)
        return res.json["response"]
    
    def enable_sms_mode(self, duration, registration_id=""):
        res = requests.post(f"{BASE_URL}users/sms_mode", headers={"X-Access-Token": self.token}, json={
            "duration": duration,
            "registration_id": registration_id
        })
        self._verify_success(res)
        return True

    def disable_sms_mode(self):
        res = requests.post(f"{BASE_URL}users/sms_mode/delete", headers={"X-Access-Token": self.token})
        self._verify_success(res)
        return True
    
    def get_blocks(self):
        res = requests.get(f"{BASE_URL}blocks?user={self.get_my_user_info()['id']}", headers={"X-Access-Token": self.token})
        self._verify_success(res)
        return res.json()["response"]
    
    def does_block_exist(self, other_user_id):
        res = requests.get(f"{BASE_URL}blocks/between?user={self.get_my_user_info()['id']}&otherUser={other_user_id}", headers={"X-Access-Token": self.token})
        self._verify_success(res)
        return res.json()["response"]["between"]
    
    def block_user(self, other_user_id):
        res = requests.post(f"{BASE_URL}blocks?user={self.get_my_user_info()['id']}&otherUser={other_user_id}", headers={"X-Access-Token": self.token})
        self._verify_success(res)
        return res.json()["response"]
    
    def unblock_user(self, other_user_id):
        res = requests.post(f"{BASE_URL}blocks/delete?user={self.get_my_user_info()['id']}&otherUser={other_user_id}", headers={"X-Access-Token": self.token})
        self._verify_success(res)
        return True