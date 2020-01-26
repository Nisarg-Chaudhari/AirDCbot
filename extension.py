import requests
import json
import argparse

auth_user = ("user", "User@123")

header = {"Content-Type": "application/json"}

class Hub:
    def __init__(self, api_url, hub_url):
        self.api_url = api_url
        self.hub_url = hub_url
        self.auth_token = None
        self.auth_header = {"Authorization": self.auth_token,
                            'Content-Type': 'application/json'}
        self.hub_id = None

    def create_session(self):
        path = '/sessions/authorize'
        data = {"username" : "user",
                "password" : "User@123"}
        res = requests.post(self.api_url + path ,data=data)
        self.auth_token = json.loads(res.text)['auth_token']
        return self.auth_token

    def get_hub_id(self):
        path = '/hubs/find_by_url'
        data = {"hub_url": self.hub_url}
        res = requests.post(self.api_url + path, data=data)
        self.hub_id = json.loads(res.text)['id']

    def send_chat(self,message):
        path ='/hubs/chat_message'
        data ={"text":message,
                "huburls":[self.hub_url]}
        res = requests.post(self.api_url + path,data=data)

    def recv_chat(self,max_count):
        path = f'/hubs/{self.hub_id}/messages/{max_count}'
        res = requests.get(self.api_url + path ,headers=self.auth_header)
        res_json = json.loads(res.text)
        print(json.dumps(res_json,indent=2))

def start(api_url, hub_url):
    hub = Hub(api_url,hub_url)
    print("auth-",hub.auth_token)
    hub.create_session()
    print("auth-",hub.auth_token)
    print("id-",hub.hub_id)
    hub.get_hub_id()
    print("id-",hub.hub_id)

parser = argparse.ArgumentParser()
parser.add_argument("--hub_url",help="Hub URL")
parser.add_argument("--api_url",help="API URL")

if __name__ == "__main__":
    args = parser.parse_args()
    start(args.api_url, args.hub_url)
