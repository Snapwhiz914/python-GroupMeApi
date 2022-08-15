import uuid
import requests
from groups import Group

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
        res.url
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
'''
    def set_group_id(self, id):
        self.group_id = id
    
    def send_message(self, message_content):
        if self.group_id == 0:
            return
        res = requests.post(f"https://api.groupme.com/v3/groups/{self.group_id}/messages?token={self.token}", json={
            "message": {
                "source_guid": str(uuid.uuid4()),
                "text": message_content
            }
        })
'''    

