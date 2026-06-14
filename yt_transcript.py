import os
from requests import Session
from youtube_transcript_api import YouTubeTranscriptApi

def parse_cookies_string(session, cookies_str):
    try:
        cookies_str = cookies_str.strip()
        if not cookies_str:
            return False
        
        # 1. Try JSON format
        if cookies_str.startswith('['):
            try:
                import json
                cookies_list = json.loads(cookies_str)
                loaded_count = 0
                for cookie in cookies_list:
                    name = cookie.get('name') or cookie.get('key')
                    value = cookie.get('value')
                    domain = cookie.get('domain')
                    path = cookie.get('path', '/')
                    if name and value:
                        session.cookies.set(name, value, domain=domain, path=path)
                        loaded_count += 1
                if loaded_count > 0:
                    print(f"Successfully loaded {loaded_count} JSON cookies.")
                    return True
            except Exception as json_err:
                print(f"Failed to load JSON cookies: {json_err}. Falling back to text parser.")

        # 2. Try Netscape format (tab or space separated)
        loaded_count = 0
        for line in cookies_str.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            parts = line.split('\t')
            if len(parts) < 7:
                parts = line.split()
                
            if len(parts) >= 7:
                domain = parts[0]
                path = parts[2]
                name = parts[5]
                value = parts[6]
                session.cookies.set(name, value, domain=domain, path=path)
                loaded_count += 1
                
        if loaded_count > 0:
            print(f"Successfully loaded {loaded_count} Netscape cookies.")
            return True
        return False
    except Exception as e:
        print(f"Error parsing cookies string: {e}")
        return False

def get_transcript(video_id):
    try:
        session = Session()
        cookies_loaded = False
        
        # 1. Try to load cookies from environment variable (secure, for deployment)
        youtube_cookies_env = os.environ.get("YOUTUBE_COOKIES")
        if youtube_cookies_env:
            cookies_loaded = parse_cookies_string(session, youtube_cookies_env)
        
        # 2. Try to load cookies from local cookie files (for local dev)
        if not cookies_loaded:
            for filepath in ['cookies.txt', 'cookies.json']:
                if os.path.exists(filepath):
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                        if parse_cookies_string(session, content):
                            cookies_loaded = True
                            break
                    except Exception as file_err:
                        print(f"Failed to read cookie file {filepath}: {file_err}")
        
        api = YouTubeTranscriptApi(http_client=session)
        transcript = api.fetch(video_id)

        text = " ".join(
            chunk.text for chunk in transcript
        )

        return text

    except Exception as e:
        print(f"Transcript Error: {e}")
        return ""