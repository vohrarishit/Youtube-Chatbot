# 🎥 YouTube Chatbot using LangChain

A chatbot that allows users to ask questions about any YouTube video. The application extracts the video transcript, stores it in a vector database, and uses an LLM to answer user queries based on the video content.

## 🚀 Features

* Extract transcript from YouTube videos
* Convert transcript into vector embeddings
* Store embeddings in a vector database
* Ask questions about video content
* Context-aware responses using Retrieval-Augmented Generation (RAG)
* Simple and interactive user interface

## 🛠️ Tech Stack

* Python
* LangChain
* YouTube Transcript API
* ChromaDB
* Hugging Face Embeddings
* Streamlit
* Groq/OpenAI LLM

## 📂 Project Structure

```text
Youtube-Chatbot/
│
├── app.py
├── yt_transcript.py
├── vector_store.py
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/vohrarishit/Youtube-Chatbot.git
cd Youtube-Chatbot
```

### Create virtual environment

```bash
python -m venv venv
```

### Activate virtual environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## 🔑 Environment Variables

Create a `.env` file in the project root and add:

```env
GROQ_API_KEY=your_api_key
```

## ▶️ Run the Application

```bash
streamlit run app.py
```

## 📌 How It Works

1. User provides a YouTube video URL.
2. Transcript is extracted using the YouTube Transcript API.
3. Transcript is split into chunks.
4. Embeddings are generated and stored in ChromaDB.
5. User asks questions.
6. Relevant transcript chunks are retrieved.
7. LLM generates answers using the retrieved context.

## 💡 Example Questions

* What is the video about?
* Summarize the main points.
* What are the key concepts discussed?
* Explain a specific topic mentioned in the video.

## 📈 Future Improvements

* Support multiple videos
* Chat history memory
* PDF export of responses
* Advanced filtering and search
* Deploy on Streamlit Cloud/Vercel

## 👨‍💻 Author

**Rishit Vohra**

GitHub: https://github.com/vohrarishit

```
```
