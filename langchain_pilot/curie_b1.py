from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, AIMessage, HumanMessage
from langchain_google_firestore import FirestoreChatMessageHistory
from google.cloud import firestore
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
import os

#init
load_dotenv()
model = ChatGoogleGenerativeAI(model = "gemini-1.5-flash")

PROJECT_ID = "langchain-pilot-ff684"
SESSION_ID = "user_session_chain1"
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

####Summerizer
summer_message = [
    ("system", "You are a helpful assistant that is very good at understanding the context and summarizing the given episode of the podcast channel 'Business of AI in Healthcare'"),
    ("human", "I need a summary of a podcast. {conditions} Here's the transcript of the podcast: {transcript}."),
]
summer_template = ChatPromptTemplate.from_messages(summer_message)
# summer_prompt = summer_template.invoke({"conditions":"We need it in bullet points.", "transcript":"Macbook pro features"})
# print(summer_prompt)

chain = summer_template | model | StrOutputParser()

# Get the current directory and file path
current_dir = os.path.dirname(os.path.abspath(__file__))
episode_path = os.path.join(current_dir, "Episode_11.md")

# Read the transcript file
with open(episode_path, 'r') as file:
    transcripts = file.read()

#Invoke the chain with conditions
result = chain.invoke({"conditions":"We need it in a single line.", "transcript":transcripts})

print(result)


