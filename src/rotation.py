from datetime import datetime


def rotate(items):
    if not items:
        raise ValueError("rotate() expected a non-empty list")

    index = datetime.utcnow().timetuple().tm_yday % len(items)
    return items[index]
