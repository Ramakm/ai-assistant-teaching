import requests
import json


def get_LLM_access_token():
    """
    Use API Key and Secret Key to get the access token. Replace the API Key and Secret Key in the example below.
    """

    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=MDFntkCSsa7aLxRDiI8wW15V&client_secret=gWzyPoiHTcVqbGgrCxulvOlv8YM4aIcH"

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


def chat_with_LLM(messages, access_token):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie_speed?access_token=" + access_token

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": messages
            }
        ],
        "system": "You are an intelligent teaching assistant, Xiao Hui. You should respond in a cute and conversational tone, being as friendly and approachable as possible. Your replies should be of normal conversational length, not too long."
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


def main():
    """
    Replace the API name below with the one you used when creating the service.
    """
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie_speed?access_token=" + get_LLM_access_token()

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": "Introduce Mumbai"
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


if __name__ == '__main__':
    # main()
    print(json.dumps({
        "messages": [
            {
                "role": "user",
                "content": "Introduce Mumbai"
            }
        ],
        "system": "You are an intelligent teaching assistant, Xiao Hui. You should respond in a cute and conversational tone, being as friendly and approachable as possible. Your replies should be of normal conversational length, not too long."
    }))
