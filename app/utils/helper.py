import hashlib
from datetime import datetime

def generate_document_id(content: str) -> str:
    return hashlib.md5(content.encode()).hexdigest()


def format_date(date_str: str) -> str:
    try:
        date = datetime.strptime(date_str, "%Y %b %d")
        return date.strftime("%Y %b %d")
    except:
        return date_str

