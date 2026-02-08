import os
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def get_youtube_client():
    creds = Credentials(
        token=None,
        refresh_token=os.getenv("YOUTUBE_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("YOUTUBE_CLIENT_ID"),
        client_secret=os.getenv("YOUTUBE_CLIENT_SECRET"),
        scopes=SCOPES,
    )

    request = google.auth.transport.requests.Request()
    creds.refresh(request)

    return build("youtube", "v3", credentials=creds)


def upload_community_post(text, image_path):
    youtube = get_youtube_client()

    # Step 1: upload image
    media = MediaFileUpload(image_path, mimetype="image/png")

    image_response = youtube.thumbnails().set(
        videoId="communityPost",
        media_body=media
    ).execute()

    # Step 2: create community post
    request = youtube.activities().insert(
        part="snippet,contentDetails",
        body={
            "snippet": {
                "description": text
            },
            "contentDetails": {
                "bulletin": {
                    "resourceId": {
                        "kind": "youtube#image"
                    }
                }
            }
        }
    )

    response = request.execute()
    return response
