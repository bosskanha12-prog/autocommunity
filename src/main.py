import yaml
from rotation import rotate
from image_ai import generate_image
from poll_builder import build_image_poll

with open("config/rotation.yaml") as f:
    rotation = yaml.safe_load(f)

with open("config/image_polls.yaml") as f:
    polls = yaml.safe_load(f)["polls"]

topic = rotate(rotation["topics"])
style = rotate(rotation["styles"])
poll = rotate(polls)

image_prompt = f"{topic}, {style}"
generate_image(image_prompt)

post_text = build_image_poll(poll["question"], poll["options"])

print("READY TO UPLOAD:")
print(post_text)
