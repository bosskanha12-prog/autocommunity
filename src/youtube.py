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


def upload_community_post(text, image_path=None):
    """
    Publish a text community/bulletin-style post.

    Note: the Data API activities.insert endpoint used here does not support
    uploading an image for community posts. `image_path` is accepted to keep
    the caller interface stable and for future implementation.
    """
    youtube = get_youtube_client()

    if image_path:
        print(
            "⚠️ image_path was provided but YouTube Data API does not support "
            "attaching an image via activities.insert; posting text only."
        )

    request = youtube.activities().insert(
        part="snippet,contentDetails",
        body={
            "snippet": {"description": text},
            "contentDetails": {"bulletin": {}},
        },
    )

    return request.execute()
