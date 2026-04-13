import pdfplumber
import re

skills_list = [
    "python", "java", "machine learning", "ai",
    "data science", "sql", "c++", "deep learning"
]

def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.lower()


def extract_email(text):
    pattern = r'\b[\w\.-]+@[\w\.-]+\.\w+\b'
    matches = re.findall(pattern, text)
    return matches[0] if matches else "Not Found"


def extract_phone(text):
    pattern = r'\+?\d[\d\s\-]{8,15}'
    matches = re.findall(pattern, text)
    return matches[0] if matches else "Not Found"


def extract_skills(text):
    found = []
    for skill in skills_list:
        if skill in text:
            found.append(skill.capitalize())
    return found


def extract_name(text):
    lines = text.split("\n")
    if lines:
        return lines[0].title()
    return "Not Found"