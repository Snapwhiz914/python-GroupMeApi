import requests

class GroupMeBot:
    def __init__(self, token, create, bot_id="", pfp_url="", name="", group_id=0):
        self.token = token
        if create == True:
            self.create(name, pfp_url, group_id)
        else:
            self.bot_id = bot_id
    
    def send_message(self, message_content, attachments=[]):
        if len(attachments) == 0:
            res = requests.post("https://api.groupme.com/v3/bots/post", json={
                "bot_id": self.bot_id,
                "text": message_content,
            })
        else:
            res = requests.post("https://api.groupme.com/v3/bots/post", json={
                "bot_id": self.bot_id,
                "text": message_content,
                'attachments': attachments
            })
    
    def create(self, name, pfp_url, gid):
        res = requests.post(f"https://api.groupme.com/v3/bots?token={self.token}", json={
            "bot": {
                "name": name,
                "group_id": str(gid),
                "avatar_url": pfp_url
            }
        })
        print(res.json())
        self.bot_id = res.json()["response"]["bot"]["bot_id"]
    
    def destroy(self):
        res = requests.post(f"https://api.groupme.com/v3/bots/destroy?token={self.token}", json={
            "bot_id": self.bot_id,
        })
