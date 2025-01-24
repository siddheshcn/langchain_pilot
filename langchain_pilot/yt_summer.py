from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.document_loaders import YoutubeLoader

#initialize environment variables
load_dotenv()

def yt_summer(yt_url: str, yt_conditions: str) -> str:
    """
    Summarizes a YouTube video transcript based on a given condition.

    Args:
        youtube_url (str): The URL of the YouTube video.
        condition (str): The summarization condition (e.g., "We need it in a single line.").

    Returns:
        str: The summary of the YouTube video.
    """
    try:
        #load the LLM model
        llm = ChatGoogleGenerativeAI(model = "gemini-1.5-flash")
        
        #load YT transcripts from API
        loader = YoutubeLoader.from_youtube_url(yt_url, add_video_info=False)
        result = loader.load()

        #extract transcripts from the loaded result
        yt_transcript = result[0].page_content

        #Define summarization prompt
        yt_summer_message = [
            ("system", "You are amazingly helpful assistant that is very good at understanding the context and summarizing the given transcripts of a youtube video"),
            ("human", "I need a summary of a the video.{yt_conditions} Here's the transcript of the youtube video: {yt_transcript}."),
        ]
        yt_summer_template = ChatPromptTemplate.from_messages(yt_summer_message)
        yt_chain = yt_summer_template | llm | StrOutputParser()
        #Invoke the chain with conditions
        yt_summary = yt_chain.invoke({"yt_conditions" : yt_conditions, "yt_transcript":yt_transcript})
        return yt_summary
    except Exception as e:
        return f"An error occurred: {e}"

#Example Usage
youtube_url = "https://www.youtube.com/watch?v=7YcH3yIuPb0"
condition = "Keep it concise."

youtube_summary = yt_summer(youtube_url,condition)

print(youtube_summary)
