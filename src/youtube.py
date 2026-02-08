import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
]


def get_youtube_client():
    creds = Credentials(
        token=None,
        refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["YOUTUBE_CLIENT_ID"],
        client_secret=os.environ["YOUTUBE_CLIENT_SECRET"],
        scopes=SCOPES,
    )

    creds.refresh(Request())
    return build("youtube", "v3", credentials=creds)


def upload_community_post(text):
    youtube = get_youtube_client()

    request = youtube.activities().insert(
        part="snippet,contentDetails",
        body={
            "snippet": {
                "description": text
            },
            "contentDetails": {
                "bulletin": {}
            }
        }
    )

    return request.execute()
