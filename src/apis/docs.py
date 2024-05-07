import requests

requests.baseUrl('http://127.0.0.1:8000')

def helloWorldBack ():
    demo = requests.get('/')
    return demo

