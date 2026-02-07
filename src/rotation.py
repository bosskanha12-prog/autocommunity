from datetime import datetime

def rotate(items):
    index = datetime.utcnow().timetuple().tm_yday % len(items)
    return items[index]
