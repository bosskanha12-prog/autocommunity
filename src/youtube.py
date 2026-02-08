import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = [
    "https://www.googleapis.com/auth/youtube.force-ssl"
]


def get_youtube_client():
    creds = Credentials(
        token=None,  # always refresh in GitHub Actions
        refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["YOUTUBE_CLIENT_ID"],
        client_secret=os.environ["YOUTUBE_CLIENT_SECRET"],
        scopes=SCOPES,
    )

    creds.refresh(Request())

    return build("youtube", "v3", credentials=creds)


def upload_community_post(text, image_path):
    youtube = get_youtube_client()

    media = MediaFileUpload(
        image_path,
        mimetype="image/png",
        resumable=False
    )

    request = youtube.activities().insert(
        part="snippet,contentDetails",
        body={
            "snippet": {
                "description": text
            },
            "contentDetails": {
                "bulletin": {}
            }
        },
        media_body=media
    )

    response = request.execute()
    return response
