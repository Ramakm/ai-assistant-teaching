from urllib.parse import urlencode

import requests
import json
from pydub import AudioSegment


api_key = "G0gaXSL56dHKQoHi1WWkldnb"
secret_key = "RGoQe3ZwD0xhGDtgHWxhBHgYBFdU0trB"

def get_access_token():
    """
    Use API Key and Secret Key to get access_token. Replace the example API Key and Secret Key below.
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
        "tex":text,
        "lan":"en",  # Change language to English
        "ctp":"1",
        "cuid":"toch",
        "aue":"6",
        "per":per,
        "tok":access_token
    }

    payload = urlencode(parameter)

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.content



def sovits_get_audio_from_text(text):
    url = "http://127.0.0.1:9880/?text=" + text + "&text_language=zh"

    payload = json.dumps(
        {
        "refer_wav_path": "zhou.wav",
        "prompt_text": "I just saw someone say, waiting for me to start the broadcast will drop Xiaozhen",
        "prompt_language": "zh",
        "text": text,
        "text_language": "zh"
    }
    )

    response = requests.request("POST", url, data=payload)
    return response.content


def main():
    """
    Replace the API name in the example below when creating the service.
    """
    tok = get_access_token()
    url = "https://tsn.baidu.com/text2audio"

    headers = {
        'Content-Type': 'audio/wav;'
    }

    parameter = {
        "tex":"Hello, I heard your request, please wait while Xiaohui thinks about it",
        "lan":"en",  # Change language to English
        "ctp":"1",
        "cuid":"toch",
        "aue":"6",
        "tok":get_access_token()
    }

    payload = urlencode(parameter)

    response = requests.request("POST", url, headers=headers, data=payload)

    with open("out.wav", 'wb') as f:
        f.write(response.content)

if __name__ == '__main__':
    response_audio = get_audio_from_text(
        "You're welcome! I'm glad I could help you. If you have any other questions or need assistance, feel free to let me know anytime.", get_access_token())

    with open("out.wav", 'wb') as f:
        f.write(response_audio)
