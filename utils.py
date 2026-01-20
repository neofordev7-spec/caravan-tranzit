import datetime, random

def normalize_car(text):
    return text.replace(" ", "").upper()

def generate_app_id():
    now = datetime.datetime.now().strftime("%Y%m%d%H%M")
    rand = random.randint(1000, 9999)
    return f"D{now}{rand}"