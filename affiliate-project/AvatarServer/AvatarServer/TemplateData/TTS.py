from urllib.parse import urlencode
import requests
import json
from pydub import AudioSegment

api_key = "G0gaXSL56dHKQoHi1WWkldnb"
secret_key = "RGoQe3ZwD0xhGDtgHWxhBHgYBFdU0trB"

def get_access_token():
    """
    Use API Key and Secret Key to get access token. Replace the example application API Key and Secret Key below.
    """
    url = ("http://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&"
           "client_id=" + api_key + "&client_secret=" + secret_key)

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")

def get_audio_from_text(text, access_token, per=111):
    url = "https://tsn.baidu.com/text2audio"

    headers = {
        'Content-Type': 'audio/wav;'
    }

    parameter = {
        "tex": text,
        "lan": "en",  # Changed language to English
        "ctp": "1",
        "cuid": "toch",
        "per": per,
        "tok": access_token
    }

    payload = urlencode(parameter)

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.content

def main():
    """
    Replace the API name below with the one used when creating the service.
    """
    tok = get_access_token()
    url = "https://tsn.baidu.com/text2audio"

    headers = {
        'Content-Type': 'audio/wav;'
    }

    parameter = {
        "tex": "Hello, I am your assistant",  # Changed text to English
        "lan": "en",  # Changed language to English
        "ctp": "1",
        "cuid": "toch",
        "per": "5",
        "tok": get_access_token()
    }

    payload = urlencode(parameter)

    response = requests.request("POST", url, headers=headers, data=payload)

    with open("out.wav", 'wb') as f:
        f.write(response.content)

if __name__ == '__main__':
    main()
