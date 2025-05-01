import re

def validate_email(email):
    """Перевіряє коректність формату електронної пошти"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_name(name):
    """Перевіряє, що ім'я не порожнє і складається з літер"""
    if not name:
        return False
    return all(c.isalpha() or c.isspace() for c in name)

def validate_title(title):
    """Перевіряє, що назва не порожня"""
    return bool(title and len(title.strip()) > 0)

def validate_content(content):
    """Перевіряє, що вміст не порожній"""
    return bool(content and len(content.strip()) > 0)

def validate_lesson_type(lesson_type):
    """Перевіряє, що тип уроку вказаний вірно"""
    return lesson_type in ["lecture", "task"]