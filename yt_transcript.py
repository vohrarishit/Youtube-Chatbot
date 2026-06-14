from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id):
    try:
        api = YouTubeTranscriptApi()

        transcript = api.fetch(video_id)

        text = " ".join(
            chunk.text for chunk in transcript
        )

        return text

    except Exception as e:
        print(f"Transcript Error: {e}")
        return ""