from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id):

    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=['en']
        )

        text = " ".join(
            item["text"] for item in transcript
        )

        return text

    except Exception as e:
        print(f"Transcript Error: {e}")
        return None