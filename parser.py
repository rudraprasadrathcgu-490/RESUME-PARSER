import pdfplumber
import re

skills_list = [
    "python", "java", "machine learning", "ai",
    "data science", "sql", "c++", "deep learning"
]

def extract_text(file):
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception as e:
        print("PDF Error:", e)
        return ""

    return text.lower()


def extract_email(text):
    try:
        pattern = r'\b[\w\.-]+@[\w\.-]+\.\w+\b'
        matches = re.findall(pattern, text)
        return matches[0] if matches else "Not Found"
    except:
        return "Not Found"


def extract_phone(text):
    try:
        pattern = r'\+?\d[\d\s\-]{8,15}'
        matches = re.findall(pattern, text)
        return matches[0] if matches else "Not Found"
    except:
        return "Not Found"


def extract_skills(text):
    found = []
    try:
        for skill in skills_list:
            if skill in text:
                found.append(skill.capitalize())
    except:
        pass
    return found


def extract_name(text):
    try:
        lines = text.split("\n")
        if lines:
            return lines[0].title()
    except:
        pass
    return "Not Found"
