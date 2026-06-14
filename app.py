import streamlit as st

from urllib.parse import urlparse, parse_qs

from yt_transcript import get_transcript

from vector_store import create_vector_store

from dotenv import load_dotenv

from langchain_groq import ChatGroq

from langchain.chains import RetrievalQA

load_dotenv()


def get_video_id(url):

    parsed = urlparse(url)

    if parsed.hostname == "youtu.be":
        return parsed.path[1:]

    if parsed.hostname in (
        "youtube.com",
        "www.youtube.com"
    ):
        return parse_qs(
            parsed.query
        ).get("v", [None])[0]

    return None


st.title("YouTube Chatbot")

youtube_url = st.text_input(
    "Enter YouTube URL"
)

if st.button("Process Video"):

    video_id = get_video_id(
        youtube_url
    )

    transcript = get_transcript(
        video_id
    )

    vector_db = create_vector_store(
        transcript
    )

    st.session_state.vector_db = vector_db

    st.success(
        "Video Processed Successfully"
    )

llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)

question = st.text_input(
    "Ask a question"
)

if (
    question
    and "vector_db"
    in st.session_state
):

    retriever = (
        st.session_state.vector_db
        .as_retriever()
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever
    )

    answer = qa_chain.run(
        question
    )

    st.write(answer)

