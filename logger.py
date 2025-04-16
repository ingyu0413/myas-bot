from datetime import datetime

def log(message: str):
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    with open("log.txt", "a") as f:
        f.write(f"[{current_time}] {message}\n")
    return print(f"[{current_time}] {message}")