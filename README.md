---
title: YouTube Chatbot
emoji: 🎥
colorFrom: indigo
colorTo: pink
sdk: streamlit
sdk_version: 1.35.0
app_file: app.py
pinned: false
---

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

## 🚀 Deployment Guide

This application can be deployed using several methods:

### 1. Streamlit Community Cloud (Recommended & Easiest)
1. Push the code to your GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and click **"New app"**.
3. Select your repository, branch (`main`), and set the main file path to `app.py`.
4. Click **"Advanced settings"** and add `GROQ_API_KEY = "your_actual_key"` under **"Secrets"**.
5. Click **"Deploy"**.

### 2. Hugging Face Spaces
Since the frontmatter is already added in the `README.md`, you can deploy directly:
1. Go to [Hugging Face Spaces](https://huggingface.co/new-space).
2. Choose **Streamlit** as the SDK.
3. Under Space Settings, add `GROQ_API_KEY` to **Variables and Secrets**.
4. Push your repository files to the Space.

### 3. Docker Deployment
A `Dockerfile` is provided for deploying on container services (e.g. Render, Railway, AWS, GCP).
1. Build the Docker image:
   ```bash
   docker build -t yt_chatbot .
   ```
2. Run the Docker container locally:
   ```bash
   docker run -p 8501:8501 --env-file .env yt_chatbot
   ```
3. When deploying to production container platforms, expose port `8501` and define the `GROQ_API_KEY` environment variable.

## 👨‍💻 Author

**Rishit Vohra**

GitHub: https://github.com/vohrarishit
