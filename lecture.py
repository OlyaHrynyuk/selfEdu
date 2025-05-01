import json
from validators import validate_title, validate_content
from lesson import Lesson


class Lecture:
    """Клас для керування лекціями в системі онлайн-курсів"""

    def __init__(self, lesson_id, content, duration, video_url=None):
        """Ініціалізація нової лекції з базовими атрибутами"""
        self.lesson_id = lesson_id
        self.content = content
        self.duration = duration
        self.video_url = video_url

    def to_dict(self):
        """Конвертація об'єкта лекції в словник для серіалізації"""
        return {
            "lesson_id": self.lesson_id,
            "content": self.content,
            "duration": self.duration,
            "video_url": self.video_url
        }

    @staticmethod
    def from_dict(lecture_dict):
        """Фабричний метод для створення об'єкту лекції з словника"""
        return Lecture(
            lecture_dict["lesson_id"],
            lecture_dict["content"],
            lecture_dict["duration"],
            lecture_dict.get("video_url")
        )

    @staticmethod
    def load_lectures():
        """Завантаження всіх лекцій з файлу json"""
        try:
            with open("lectures.json", "r", encoding="utf-8") as file:
                lectures_data = json.load(file)
                lectures = []
                for lecture_dict in lectures_data:
                    lectures.append(Lecture.from_dict(lecture_dict))
                return lectures
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def save_lectures(lectures):
        """Збереження списку лекцій у json файл"""
        lectures_data = [lecture.to_dict() for lecture in lectures]
        with open("lectures.json", "w", encoding="utf-8") as file:
            json.dump(lectures_data, file, ensure_ascii=False, indent=2)

    @staticmethod
    def add_to_course():
        """Додавання нової лекції до курсу"""
        from course import Course

        print("\nДодавання лекції до курсу")

        # Перевіряємо наявність курсів
        courses = Course.load_courses()
        if not courses:
            print("Немає доступних курсів. Спочатку створіть курс.")
            return

        # Виводимо список доступних курсів
        print("\nДоступні курси:")
        for idx, course in enumerate(courses, 1):
            print(f"{idx}. {course.title} (ID: {course.course_id})")

        # Обираємо курс
        try:
            course_idx = int(input("\nВиберіть номер курсу: ")) - 1
            if course_idx < 0 or course_idx >= len(courses):
                print("Невірний вибір курсу")
                return
        except ValueError:
            print("Введіть числове значення")
            return

        course = courses[course_idx]

        # Збираємо дані для створення лекції
        title = input("Введіть назву лекції: ")
        description = input("Введіть короткий опис лекції: ")
        content = input("Введіть вміст лекції: ")

        try:
            duration = int(input("Введіть тривалість лекції (хвилин): "))
            if duration <= 0:
                print("Тривалість повинна бути більше нуля")
                return
        except ValueError:
            print("Тривалість повинна бути числом")
            return

        video_url = input("Введіть URL відео (необов'язково): ")

        # Валідація введених даних
        if not validate_title(title):
            print("Назва лекції не може бути порожньою")
            return

        if not validate_content(content):
            print("Вміст лекції не може бути порожнім")
            return

        # Створюємо новий урок
        lesson_type = "lecture"
        new_lesson = Lesson.create_lesson(title, description, lesson_type)

        if not new_lesson:
            return

        # Створюємо нову лекцію
        lectures = Lecture.load_lectures()
        new_lecture = Lecture(new_lesson.lesson_id, content, duration, video_url if video_url else None)
        lectures.append(new_lecture)
        Lecture.save_lectures(lectures)

        # Додаємо лекцію до курсу
        if course.add_lesson(new_lesson.lesson_id):
            print(f"Лекція '{title}' успішно додана до курсу '{course.title}'")
        else:
            print("Помилка при додаванні лекції до курсу")