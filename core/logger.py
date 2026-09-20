import os
from datetime import datetime

class SystemLogger:
    def __init__(self, log_file="cta_system.log"):
        self.log_file = log_file

    def log(self, level: str, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level.upper()}] {message}\n"
        print(log_entry.strip())
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception:
            pass

    def info(self, msg):
        self.log("INFO", msg)

    def error(self, msg):
        self.log("ERROR", msg)

    def warning(self, msg):
        self.log("WARNING", msg)