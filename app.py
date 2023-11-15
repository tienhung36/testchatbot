import requests
import os, signal
from flask import Flask, request
import openai
import pickle
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import gradio as gr
messages = [
        SystemMessage(
            content="You are a Q&A bot and you will answer all the questions that the user has. If you dont know the answer, output 'Sorry, I dont know' .")
    ]
app = Flask(__name__)
os.environ["OPENAI_API_KEY"] = "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"

#This is API key for OpenAI
openai.api_key = "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"
# This is page access token that you get from facebook developer console.
PAGE_ACCESS_TOKEN = "EAAET6pq5qH8BO4fYZAQqUi7GgvPy3Y0c5pDLf0EzCBoMKBi21h38CXx5ZASoccQxA8U7dhY4ekfXQs9iwrWTBYKeDomyfb91rPgBx3DyeIo5SAK7kmTpUKpk1bVY9FGrurO4WoEqxXZBtaKcstqeb7AKJ0XubC4bpZCMseHSqFunPnRNZB1Sv2ZACNzDx76e6L"
# This is API key for facebook messenger.
API="https://graph.facebook.com/v16.0/me/messages?access_token="+PAGE_ACCESS_TOKEN
chat = ChatOpenAI(temperature=0)
message_history = []

with open("testbot.pkl", 'rb') as f: 
    faiss_index = pickle.load(f)
def pdf_load(input):
    '''Find the k best matched chunks to the queried test. 
    These will be the context over which our bot will try to answer the question.
    The value of k can be adjusted so as to get the embeddings for the best n chunks.'''
    docs = faiss_index.similarity_search(input, K = 6)

    main_content = input + "\n\n"
    for doc in docs:
        main_content += doc.page_content + "\n\n"
    messages.append(HumanMessage(content=main_content))
    ai_response = chat(messages).content
    # messages.remove(messages)
    # messages.pop()
    return ai_response
@app.route('/', methods=['GET'])
def verify():
    # Verify the webhook subscription with Facebook Messenger
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hungdeptrai":
            return "Verification token missmatch", 403
        return request.args['hub.challenge'], 200
    return "Hello world", 200

@app.route("/", methods=['POST'])
def fbwebhook():
    data = request.get_json()
    try:
        if data['entry'][0]['messaging'][0]['sender']['id']:
            message = data['entry'][0]['messaging'][0]['message']
            sender_id = data['entry'][0]['messaging'][0]['sender']['id']
            text_input=message['text']
            print(text_input)
                     
            chatbot_res = pdf_load(text_input)
            text_input=""
            print("BotChat Response=>",chatbot_res)
            response = {
                'recipient': {'id': sender_id},
                'message': {'text': chatbot_res}
            }
            requests.post(API, json=response)
    except Exception as e:
        print(e)
        pass
    return '200 OK HTTPS.'
  # Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
