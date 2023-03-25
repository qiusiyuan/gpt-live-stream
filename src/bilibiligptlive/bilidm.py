import requests
import time
roomid = ""
# URL for Bilibili API
url = f"https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory?roomid={roomid}"

last_history = set()


def get_dm_history():
    response = requests.get(url)
    data = response.json()

    if data["code"] == 0:
        messages = data["data"]["room"]
        user_messages = [f"{message['nickname']}: {message['text']}" for message in messages]
        return new_messages(user_messages)
    return []
    
            

def new_messages(user_messages):
    global last_history
    new_messages = [user_message for user_message in user_messages if user_message not in last_history]
    last_history = set(user_messages)
    return new_messages
    

    
if __name__=="__main__":
    print(get_dm_history())
    time.sleep(5)
    print(get_dm_history())
    time.sleep(5)
    print(get_dm_history())
    print(last_history)
