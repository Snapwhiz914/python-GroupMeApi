import gmbot
import gmuser
import time
import requests

TOKEN = "KnQL5l3v3qK9myt8okjr9fRnQEVj7Sp4c586HTm4"
GROUP_ID = "86024117" #86024117: test group, 85769602: class of 2025

def get_group_members():
    res = requests.get(f"https://api.groupme.com/v3/groups/{GROUP_ID}?token={TOKEN}")
    print(res.json())
    return res.json()["response"]["members"]

#loci: [
#          [
#           Start loc in string
#           length of name mention
#           ]
#        ]

atter_bot = gmbot.GroupMeBot(TOKEN, create=True, name="Atter", group_id=GROUP_ID)

message = ""
message_dict = {
    'bot_id': atter_bot.bot_id,
    'text': "",
    'attachments': [
        {
            "loci": [
                
            ],
            "type": "mentions",
            "user_ids": [

            ]
        }
    ]
}
for member in get_group_members():
    id = member["user_id"] #string
    name = member["nickname"] #string

    message_dict["attachments"][0]["user_ids"].append(id)

    message = message + "@" + name + " "
    start_loc = message.index("@" + name)
    loci_length = len("@" + name)

    message_dict["attachments"][0]["loci"].append([start_loc, loci_length])

message_dict["text"] = message
atter_bot.send_message(message_dict["text"], attachments=message_dict["attachments"])
atter_bot.destroy()