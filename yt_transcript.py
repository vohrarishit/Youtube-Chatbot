import os
import tempfile
from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id, custom_cookies=None):
    temp_cookie_file = None
    try:
        # 1. Determine if we have a cookies string or local cookies file
        cookies_content = None
        if custom_cookies:
            cookies_content = custom_cookies
        else:
            youtube_cookies_env = os.environ.get("YOUTUBE_COOKIES")
            if youtube_cookies_env:
                cookies_content = youtube_cookies_env
            else:
                for filepath in ['cookies.txt', 'cookies.json']:
                    if os.path.exists(filepath):
                        try:
                            with open(filepath, 'r', encoding='utf-8') as f:
                                cookies_content = f.read()
                            break
                        except Exception:
                            pass
        
        # 2. Write cookies to a temporary file if we have cookies content
        if cookies_content:
            fd, temp_path = tempfile.mkstemp(suffix='.txt')
            try:
                with os.fdopen(fd, 'w', encoding='utf-8') as f:
                    f.write(cookies_content)
                temp_cookie_file = temp_path
            except Exception as e:
                print(f"Failed to create temporary cookies file: {e}")
        
        # 3. Call youtube-transcript-api using session loading (v1.2.4+)
        from requests import Session
        session = Session()
        
        if temp_cookie_file and cookies_content:
            cookies_loaded = False
            # Try parsing as JSON first
            if cookies_content.strip().startswith('['):
                try:
                    import json
                    cookies_list = json.loads(cookies_content)
                    for cookie in cookies_list:
                        name = cookie.get('name') or cookie.get('key')
                        value = cookie.get('value')
                        domain = cookie.get('domain')
                        path = cookie.get('path', '/')
                        if name and value:
                            session.cookies.set(name, value, domain=domain, path=path)
                    cookies_loaded = True
                except Exception:
                    pass
            
            # Fallback to MozillaCookieJar Netscape loader
            if not cookies_loaded:
                try:
                    import http.cookiejar
                    cj = http.cookiejar.MozillaCookieJar(temp_cookie_file)
                    cj.load(ignore_discard=True, ignore_expires=True)
                    session.cookies = cj
                except Exception as cookie_err:
                    print(f"Failed to load Netscape cookies: {cookie_err}")
        
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