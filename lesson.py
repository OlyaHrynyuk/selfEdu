import json
from validators import validate_title, validate_content, validate_lesson_type

class Lesson:
    __LESSON_ID = 1

    def __init__(self, title, description, type):
        self.lesson_id = Lesson.__LESSON_ID
        self.title = title
        self.description = description
        self.type = type
        Lesson.lesson_index()

    @classmethod
    def lesson_index(cls):
        """Лічильник індексів, робить їх унікальними"""
        cls.__LESSON_ID += 1

    def to_dict(self):
        """Перетворення об'єкта в словник"""
        return {
            "lesson_id": self.lesson_id,
            "title": self.title,
            "description": self.description,
            "type": self.type
        }

    @staticmethod
    def from_dict(lesson_dict):
        """Створює новий об'єкт з словника"""
        lesson = Lesson(
            lesson_dict["title"],
            lesson_dict["description"],
            lesson_dict["type"]
        )
        lesson.lesson_id = lesson_dict["lesson_id"]
        return lesson

    @staticmethod
    def load_lessons():
        """Підтягує всі уроки з словника"""
        try:
            with open("lessons.json", "r", encoding="utf-8") as file:
                lessons_data = json.load(file)
                lessons = []
                for lesson_dict in lessons_data:
                    lesson = Lesson.from_dict(lesson_dict)
                    lessons.append(lesson)
                return lessons
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def save_lessons(lessons):
        """Зберігає уроки у словник"""
        lessons_data = []
        for lesson in lessons:
            lessons_data.append(lesson.to_dict())

        with open("lessons.json", "w", encoding="utf-8") as file:
            json.dump(lessons_data, file, ensure_ascii=False, indent=2)

    @staticmethod
    def create_lesson(title, description, type):
        """Створення нового уроку"""
        if not validate_title(title):
            print("Назва уроку не може бути порожньою")
            return None

        if not validate_content(description):
            print("Опис уроку не може бути порожнім")
            return None

        if not validate_lesson_type(type):
            print("Невірний тип уроку. Допустимі типи: 'lecture', 'task'")
            return None

        lessons = Lesson.load_lessons()
        new_lesson = Lesson(title, description, type)
        lessons.append(new_lesson)
        Lesson.save_lessons(lessons)
        return new_lesson

    @staticmethod
    def find_by_id(lesson_id):
        """Пошук уроку за ID"""
        lessons = Lesson.load_lessons()
        for lesson in lessons:
            if lesson.lesson_id == lesson_id:
                return lesson
        return None