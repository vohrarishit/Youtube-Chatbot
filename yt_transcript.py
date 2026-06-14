from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id):

    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    text = " ".join(
        item["text"] for item in transcript
    )

    return text