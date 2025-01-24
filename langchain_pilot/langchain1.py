from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from google.cloud import firestore
from langchain_google_firestore import FirestoreChatMessageHistory

#Load environment Variables from .env
load_dotenv()

#Create a ChatOpenAI model
#model = ChatOpenAI(model = "gpt-4o")

#Create a Google Gemini model
model = ChatGoogleGenerativeAI(model='gemini-1.5-flash')
'''
#1
#Invoke the model with a message
result = model.invoke("Hi")
print(result)
print(result.content)

'''

'''
#2
#Basic conversation

messages = [
    SystemMessage(content="Convert my sentences into Shakesperian English"),
    HumanMessage(content="How are you today?"),
    AIMessage(content="How art thou this day?"),
    HumanMessage(content="Great now say that in Hindi"),
    #AIMessage(content="Aap kaise ho?"),
    #HumanMessage(content="Summarize our conversation for me please")
]
result = model.invoke(messages)
print(result.content)

'''

'''
# 3
# Conversation with Chat History
chat_history = [] #list to store messages

system_message=SystemMessage(content="You are a helpful AI assistant. You try your best to keep your response as short as possible while covering the required amount of information.")
chat_history.append(system_message)

#Chat loop
while True:
    query = input("You: ")
    if query.lower() == "exit":
        break
    chat_history.append(HumanMessage(content=query))
    result = model.invoke(chat_history)
    print(f"AI: {result.content}")
    chat_history.append(AIMessage(content=result.content))

print("-------Message History--------")
print(chat_history)

'''

#4
#Save chat history on firestore

PROJECT_ID = "langchain-pilot-ff684"
SESSION_ID = "user_session_new"
COLLECTION_NAME = "chat_history"

print("Init Firestore chat message history....")

client = firestore.Client(project=PROJECT_ID)

chat_history = FirestoreChatMessageHistory(
    session_id = SESSION_ID,
    collection=COLLECTION_NAME,
    client = client,
)

print("Chat History session initialized")
print("Current Chat History: ", chat_history.messages)

while True:
    human_input = input("User: ")
    if human_input.lower() == "exit":
        break

    chat_history.add_user_message(human_input)

    ai_response = model.invoke(chat_history.messages)
    chat_history.add_ai_message(ai_response.content)

    print(f"AI Message: {ai_response.content}")
    