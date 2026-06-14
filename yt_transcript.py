from youtube_transcript_api import YouTubeTranscriptApi


def get_transcript(video_id):

    api = YouTubeTranscriptApi()

    transcript = api.fetch(video_id)

    text = " ".join(
        chunk.text for chunk in transcript
    )

    return text