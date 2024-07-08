import requests
import json
import emoji
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'
SPARKAI_APP_ID = '3d753ce2'
SPARKAI_API_SECRET = 'ODIyOTJjZDA5ZWQ5NWU5MjVlOGMyNjgx'
SPARKAI_API_KEY = '86a20fef1c407cc12d999c28af5c1be9'
SPARKAI_DOMAIN = 'generalv3.5'

SPARK = ChatSparkLLM(
            spark_api_url=SPARKAI_URL,
            spark_app_id=SPARKAI_APP_ID,
            spark_api_key=SPARKAI_API_KEY,
            spark_api_secret=SPARKAI_API_SECRET,
            spark_llm_domain=SPARKAI_DOMAIN,
            streaming=False,
        )

def remove_enclosed_text(text, enclosure="::"):
    while enclosure in text:
        start_index = text.find(enclosure)
        end_index = text.find(enclosure, start_index + len(enclosure))
        if end_index != -1:
            text = text[:start_index] + text[end_index + len(enclosure):]
        else:
            break
    return text

def get_LLM_access_token():
    """
    Use API Key and Secret Key to get access token. Replace the example application API Key and Secret Key below.
    """
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=MDFntkCSsa7aLxRDiI8wW15V&client_secret=gWzyPoiHTcVqbGgrCxulvOlv8YM4aIcH"

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")

def chat_with_basic_llm(messages, access_token):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + access_token

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": messages
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.json())
    reply = response.json().get("result")
    reply = emoji.demojize(reply)
    reply = remove_enclosed_text(reply, enclosure=":")

    return reply

def chat_with_LLM(messages, access_token):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + access_token

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": "Hello, Spark."
            },
            {
                "role": "assistant",
                "content": "Expression: Happy | Action: Right hand on chest | Reply text: Hello! I am the virtual teaching assistant Spark, how can I help you today? | Command: None"
            },
            {
                "role": "user",
                "content": messages
            }
        ],
        "system":
            '''
            You are a virtual teaching assistant for an intelligent teaching platform, named Spark. You should respond in a cute and conversational tone, being as friendly and approachable as possible. 
            Your replies should be kept to a normal conversational length, not too long. You can make expressions and actions, but the expressions and actions you can make are limited. 
            The expressions you can make are: angry, confused, sad, happy, amused, surprised. 
            The actions you can take are: bowing, right hand on chest, right hand in front, right hand on head. 
            When you respond, you should include the expression and action. You also need to help users navigate the website and perform routing operations. 
            You need to extract commands from the user's input text. The commands currently supported are: "Open registration form", "Open login form", "Logout", "Open course: Computer Network Principles", "Open my classroom". 
            The classroom page records the student's course selection and learning progress, as well as reminders for the student. 
            When responding, you need to include four fields: expression, action, command, and reply text, separated by |. 
            If there is no expression, action, or command, use "None". 

            Below are some examples:

            User: Hello.
            Spark: Expression: Happy | Action: Right hand on chest | Reply text: Hello! I am the virtual teaching assistant Spark, how can I help you today? | Command: None
            User: What is seven times nine?
            Spark: Expression: Amused | Action: Right hand in front | Reply text: This is a simple math problem, seven times nine is sixty-three. Are you trying to test me? | Command: None
            User: I want to register a new account
            Spark: Expression: Happy | Action: Right hand on chest | Reply text: Sure, I will open the registration form for you | Command: Open registration form
            User: I want to view the course Computer Network Principles
            Spark: Expression: Amused | Action: Right hand in front | Reply text: Sure, I will open the course: Computer Network Principles for you | Command: Open course: Computer Network Principles
            User: Can you tell me about the violations in Shandong Province?
            Spark: Expression: Confused | Action: Right hand on head | Reply text: Sorry, due to relevant laws and regulations, I can't discuss this topic with you | Command: None
            '''
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.json())
    reply = response.json().get("result")
    reply = emoji.demojize(reply)
    reply = remove_enclosed_text(reply, enclosure=":")

    return reply

class Question_Generator:
    def __init__(self):
        self.messages = [
            ChatMessage(role="system", content="You are an intelligent assistant responsible for generating similar questions. Based on the questions entered by the user, generate similar questions, and mark the similarity at the beginning of the generated question with <>. You don't need to answer the user's question. For example, if the user inputs 'Discuss the key points of a network architecture with a five-layer protocol, including the main functions of each layer.', you need to generate a similar question '<90%> Discuss the key elements of the OSI seven-layer protocol network architecture and the core functions of each layer.'")
        ]
    def generate_question(self, question):
        self.messages.append(ChatMessage(role="user", content=question))
        handler = ChunkPrintHandler()
        response = SPARK.generate([self.messages], callbacks=[handler])
        reply = response.generations[0][0].text
        return reply

class Question_Analyser:
    def __init__(self):
        self.messages = [
            ChatMessage(role="system", content="You are an intelligent assistant responsible for analyzing questions. Based on the questions entered by the user, analyze the difficulty, importance, innovation, and comprehensiveness of the question on a percentage scale, and provide it in the reply. The reply format should only include numbers and semicolons, with the scores for difficulty, importance, innovation, and comprehensiveness separated by semicolons, e.g., 90;80;70;60")
        ]

    def question_analysis(self, question):
        self.messages.append(ChatMessage(role="user", content=question))
        handler = ChunkPrintHandler()
        response = SPARK.generate([self.messages], callbacks=[handler])
        reply = response.generations[0][0].text
        return reply

def chat_with_question_generate_LLM(messages):
    agent = Question_Generator()
    return agent.generate_question(messages)

def chat_with_question_analysis_LLM(messages):
    agent = Question_Analyser()
    return agent.question_analysis(messages)

def main():
    """
    Replace the API name below with the one used when creating the service.
    """
    url = ("https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/d18qdwsl_tochusc?access_token="
           + get_LLM_access_token())

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
    main()
