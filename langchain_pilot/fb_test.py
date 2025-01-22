from google.cloud import firestore
from langchain_google_firestore import FirestoreChatMessageHistory
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("FirebaseServiceAccountKey.json")
firebase_admin.initialize_app(cred)

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

print("--success--")