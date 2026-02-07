def build_image_poll(question, options):
    post = f"🖼️ IMAGE POLL\n\n🗳️ {question}\n\n"
    post += "\n".join(options)
    post += "\n\n👇 Comment A / B / C / D"
    return post
