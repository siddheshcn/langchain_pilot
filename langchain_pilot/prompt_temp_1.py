'''Prompt Template

##Generate a summary for Youtube Video.

Youtube Summarizer
- Check if the message contains youtube link
    - Yes? Fetch transcripts for the video
        - No Transcripts? SORRY
    - Return Transcripts
- Generate a summary for the youtube video based on the transcript: {}



##Tell me what does the speaker mean by templates in this video:

- 1 line summary of the video (fetch transcript and summarize)
- Understand the HumanMessage: If it is just a video link or a question with it?
    - Here's the transcript of the video {}. Based on this, respond to the user query.
        - If no query, simply summarize.
    - Keep transcript in context for an hour. So the user could have a back and forth with it



'''




from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
############## Basic test
# template = "Tell me {count} jokes about {topic}"
# my_prompt_template = ChatPromptTemplate.from_template(template)

# print("--------Prompt Template-------")
# prompt = my_prompt_template.invoke({"topic": "cats", "count":"3"})
# print(prompt)


############# Level 2 Test
my_message = [
    ("system", "You are a comedian who tells jokes about {topic}."),
    ("human", "Tell me {count} jokes.")
]
my_prompt_template = ChatPromptTemplate.from_messages(my_message)
prompt = my_prompt_template.invoke({"topic":"cats","count":3})
print(prompt)
