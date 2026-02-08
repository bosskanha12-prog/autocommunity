import yaml
import os
from rotation import rotate
from image_ai import generate_image
from poll_builder import build_image_poll
from youtube import upload_community_post


ASSET_PATH = "assets/generated/today.png"


def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def main():
    # Load configs
    rotation_cfg = load_yaml("config/rotation.yaml")
    polls_cfg = load_yaml("config/image_polls.yaml")["polls"]

    # Rotate content
    topic = rotate(rotation_cfg["topics"])
    style = rotate(rotation_cfg["styles"])
    poll = rotate(polls_cfg)

    # Build image prompt
    image_prompt = f"{topic}, {style}, high quality, engaging, social media"

    # Generate image
    os.makedirs("assets/generated", exist_ok=True)
    generate_image(image_prompt, ASSET_PATH)

    # Build poll text
    post_text = build_image_poll(
        poll["question"],
        poll["options"]
    )

    print("📢 Posting to YouTube Community...")
    print(post_text)

    # Upload to YouTube
    upload_community_post(
        text=post_text,
        image_path=ASSET_PATH
    )

    print("✅ Successfully posted image poll!")


if __name__ == "__main__":
    main()
