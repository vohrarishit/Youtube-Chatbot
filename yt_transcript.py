import os
import tempfile
import http.cookiejar
from requests import Session
from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id):
    temp_cookie_file = None
    try:
        session = Session()
        
        # 1. Try to load cookies from environment variable (secure, for deployment)
        youtube_cookies_env = os.environ.get("YOUTUBE_COOKIES")
        
        if youtube_cookies_env:
            # Write cookies to a temporary file to load via MozillaCookieJar
            fd, temp_path = tempfile.mkstemp()
            try:
                with os.fdopen(fd, 'w', encoding='utf-8') as f:
                    f.write(youtube_cookies_env)
                cj = http.cookiejar.MozillaCookieJar(temp_path)
                cj.load(ignore_discard=True, ignore_expires=True)
                session.cookies = cj
                print("Successfully loaded cookies from YOUTUBE_COOKIES environment variable.")
            except Exception as env_cookie_err:
                print(f"Failed to load cookies from YOUTUBE_COOKIES env var: {env_cookie_err}")
            finally:
                temp_cookie_file = temp_path
        
        # 2. Try to load cookies from a local cookies.txt file (for local development)
        elif os.path.exists('cookies.txt'):
            cj = http.cookiejar.MozillaCookieJar('cookies.txt')
            try:
                cj.load(ignore_discard=True, ignore_expires=True)
                session.cookies = cj
                print("Successfully loaded cookies from local cookies.txt.")
            except Exception as file_cookie_err:
                print(f"Failed to load cookies from cookies.txt file: {file_cookie_err}")
        
        api = YouTubeTranscriptApi(http_client=session)
        transcript = api.fetch(video_id)

        text = " ".join(
            chunk.text for chunk in transcript
        )

        # Clean up temporary cookie file
        if temp_cookie_file and os.path.exists(temp_cookie_file):
            try:
                os.remove(temp_cookie_file)
            except Exception:
                pass

        return text

    except Exception as e:
        # Clean up temporary cookie file in case of exception
        if temp_cookie_file and os.path.exists(temp_cookie_file):
            try:
                os.remove(temp_cookie_file)
            except Exception:
                pass
        print(f"Transcript Error: {e}")
        return ""