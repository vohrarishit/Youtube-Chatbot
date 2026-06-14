import streamlit as st
from urllib.parse import urlparse, parse_qs
from yt_transcript import get_transcript
from vector_store import create_vector_store
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA

load_dotenv()

# App styling
st.set_page_config(
    page_title="YouTube Chatbot",
    page_icon="🎥",
    layout="centered"
)

# Inject custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* Main Container styling */
.stApp {
    background: radial-gradient(circle at top left, #1e1b4b, #09090b 70%) !important;
    color: #f4f4f5 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Custom card container for UI elements */
.glass-card {
    background: rgba(255, 255, 255, 0.02) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 16px !important;
    padding: 24px !important;
    margin-bottom: 24px !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4) !important;
}

/* Styling headers */
h1, h2, h3 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    color: #ffffff !important;
}

/* Customize streamlit default input elements */
div[data-baseweb="input"] {
    background-color: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    transition: all 0.3s ease !important;
}

div[data-baseweb="input"]:focus-within {
    border-color: #a78bfa !important;
    box-shadow: 0 0 10px rgba(167, 139, 250, 0.4) !important;
}

/* Input text color */
input {
    color: #ffffff !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #d946ef 0%, #8b5cf6 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3) !important;
    width: 100% !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(139, 92, 246, 0.5) !important;
    background: linear-gradient(135deg, #e879f9 0%, #a78bfa 100%) !important;
    color: white !important;
}

.stButton > button:active {
    transform: translateY(1px) !important;
}

/* Success & Error alerts styling */
div[data-testid="stNotification"] {
    background-color: rgba(16, 185, 129, 0.08) !important;
    border: 1px solid rgba(16, 185, 129, 0.2) !important;
    border-radius: 10px !important;
}

div[data-testid="stNotification"] [data-testid="stMarkdownContainer"] {
    color: #34d399 !important;
}

div[data-testid="stException"], div[role="alert"] {
    background-color: rgba(239, 68, 68, 0.08) !important;
    border: 1px solid rgba(239, 68, 68, 0.2) !important;
    border-radius: 10px !important;
}

div[role="alert"] [data-testid="stMarkdownContainer"] {
    color: #f87171 !important;
}

/* Custom Answer Card */
.answer-card {
    background: rgba(139, 92, 246, 0.04) !important;
    border-left: 4px solid #8b5cf6 !important;
    border-radius: 0 12px 12px 0 !important;
    padding: 20px !important;
    margin-top: 20px !important;
    border-top: 1px solid rgba(139, 92, 246, 0.1) !important;
    border-right: 1px solid rgba(139, 92, 246, 0.1) !important;
    border-bottom: 1px solid rgba(139, 92, 246, 0.1) !important;
}
</style>
""", unsafe_allow_html=True)


def get_video_id(url):
    if not url:
        return None
    parsed = urlparse(url)
    if parsed.hostname == "youtu.be":
        return parsed.path[1:]
    if parsed.hostname in ("youtube.com", "www.youtube.com"):
        if parsed.path.startswith("/shorts/"):
            return parsed.path.split("/")[2]
        if parsed.path.startswith("/embed/"):
            return parsed.path.split("/")[2]
        if parsed.path.startswith("/v/"):
            return parsed.path.split("/")[2]
        # Query parameters
        return parse_qs(parsed.query).get("v", [None])[0]
    return None


# Styled Header
st.markdown("""
<div style="text-align: center; margin-top: 1rem; margin-bottom: 2rem;">
    <h1 style="background: linear-gradient(135deg, #a78bfa 0%, #ec4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.8rem; font-weight: 800; letter-spacing: -0.5px;">🎥 YouTube Chatbot</h1>
    <p style="color: #94a3b8; font-size: 1.1rem; font-weight: 400; margin-top: 0.5rem;">
        Extract transcripts, embed content, and chat with any YouTube video in real-time.
    </p>
</div>
""", unsafe_allow_html=True)

# Step 1: Video Input Section
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("<h3 style='margin-top:0; font-size: 1.25rem;'>1. Connect YouTube Video</h3>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔍 Fetch Automatically", "✍️ Paste Transcript Manually"])

with tab1:
    st.markdown("<div style='margin-bottom: 8px; font-weight: 500;'>Enter YouTube URL</div>", unsafe_allow_html=True)
    youtube_url = st.text_input(
        "Enter YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
        label_visibility="collapsed",
        key="auto_url"
    )
    
    with st.expander("⚙️ Advanced: Configure YouTube Cookies (Bypass cloud IP blocks)"):
        st.markdown("""
        <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 8px;">
            YouTube blocks requests from cloud provider servers. To bypass this, export cookies from your logged-in YouTube account using a browser extension like <i>Get cookies.txt LOCALLY</i> (Netscape or JSON format) and paste them here.
        </div>
        """, unsafe_allow_html=True)
        cookies_input = st.text_area(
            "Paste JSON or Netscape cookies here:",
            placeholder='[{"name": "...", "value": "..."}, ...]\nor\n# Netscape HTTP Cookie File...',
            height=100,
            label_visibility="collapsed"
        )
        
    if st.button("Process Video", key="btn_process_auto"):
        video_id = get_video_id(youtube_url)
        
        if not video_id:
            st.error("Invalid YouTube URL. Please make sure it is a valid link.")
        else:
            with st.spinner("Fetching transcript and building vector embeddings..."):
                custom_cookies = cookies_input.strip() if cookies_input.strip() else None
                transcript = get_transcript(video_id, custom_cookies=custom_cookies)
                if not transcript:
                    st.error("Could not retrieve transcript automatically. YouTube is blocking this server's IP address. Please use the 'Paste Transcript Manually' tab above to paste the transcript.")
                else:
                    vector_db = create_vector_store(transcript)
                    st.session_state.vector_db = vector_db
                    st.session_state.current_video_id = video_id
                    st.session_state.current_video_url = youtube_url
                    st.success("Video processed successfully! You can now ask questions below.")

with tab2:
    st.markdown("<div style='margin-bottom: 8px; font-weight: 500;'>YouTube URL (Optional reference)</div>", unsafe_allow_html=True)
    youtube_url_manual = st.text_input(
        "YouTube URL (Optional reference)",
        placeholder="https://www.youtube.com/watch?v=...",
        label_visibility="collapsed",
        key="manual_url"
    )
    
    st.markdown("<div style='margin-top: 12px; margin-bottom: 8px; font-weight: 500;'>Paste Transcript Text</div>", unsafe_allow_html=True)
    pasted_transcript = st.text_area(
        "Paste transcript",
        placeholder="Copy the transcript text from YouTube's sidebar, captions, or a transcript generator tool and paste it here...",
        height=200,
        label_visibility="collapsed",
        key="pasted_text"
    )
    
    if st.button("Process Pasted Transcript", key="btn_process_manual"):
        if not pasted_transcript.strip():
            st.error("Please paste the transcript text first.")
        else:
            video_id = get_video_id(youtube_url_manual) if youtube_url_manual else "manual_input"
            with st.spinner("Processing transcript and building vector embeddings..."):
                vector_db = create_vector_store(pasted_transcript)
                st.session_state.vector_db = vector_db
                st.session_state.current_video_id = video_id
                st.session_state.current_video_url = youtube_url_manual if youtube_url_manual else "Pasted Transcript"
                st.success("Transcript processed successfully! You can now ask questions below.")
st.markdown('</div>', unsafe_allow_html=True)

# Step 2: Chat / QA Section
if "vector_db" in st.session_state:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # Active video info
    current_url = st.session_state.get("current_video_url", "")
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 20px; padding: 10px 14px; background: rgba(255, 255, 255, 0.03); border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.05);">
        <span style="font-size: 14px; color: #a78bfa; font-weight: 600;">Active Video:</span>
        <a href="{current_url}" target="_blank" style="color: #e2e8f0; font-size: 14px; text-decoration: none; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 400px; hover: underline;">{current_url}</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='margin-top:0; font-size: 1.25rem;'>2. Ask Questions</h3>", unsafe_allow_html=True)
    
    question = st.text_input(
        "Ask a question",
        placeholder="What is this video about? Summarize key points...",
        label_visibility="collapsed"
    )
    
    if question:
        with st.spinner("Analyzing transcript and generating answer..."):
            llm = ChatGroq(
                model="llama-3.3-70b-versatile"
            )
            
            retriever = st.session_state.vector_db.as_retriever()
            
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                retriever=retriever
            )
            
            try:
                answer = qa_chain.run(question)
                st.markdown('<div class="answer-card">', unsafe_allow_html=True)
                st.markdown("<h4 style='margin-top:0; color: #a78bfa; font-size: 1.1rem;'>Answer</h4>", unsafe_allow_html=True)
                st.markdown(f"<div style='color: #e2e8f0; line-height: 1.6;'>{answer}</div>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error generating answer: {e}")
                
    st.markdown('</div>', unsafe_allow_html=True)
