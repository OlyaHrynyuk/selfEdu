import json
from validators import validate_title, validate_content
from lesson import Lesson


class Task:
    """Клас для керування завданнями в системі онлайн-курсів"""
    def __init__(self, lesson_id, description, max_score, deadline=None):
        self.lesson_id = lesson_id
        self.description = description
        self.max_score = max_score
        self.deadline = deadline

    def to_dict(self):
        """Конвертація об'єкта завдання в словник для серіалізації"""
        return {
            "lesson_id": self.lesson_id,
            "description": self.description,
            "max_score": self.max_score,
            "deadline": self.deadline
        }

    @staticmethod
    def from_dict(task_dict):
        """Метод для створення об'єкту завдання з словника"""
        return Task(
            task_dict["lesson_id"],
            task_dict["description"],
            task_dict["max_score"],
            task_dict.get("deadline")
        )

    @staticmethod
    def load_tasks():
        """Завантаження всіх завдань з файлу json"""
        try:
            with open("tasks.json", "r", encoding="utf-8") as file:
                tasks_data = json.load(file)
                tasks = []
                for task_dict in tasks_data:
                    tasks.append(Task.from_dict(task_dict))
                return tasks
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def save_tasks(tasks):
        """Збереження списку завдань у json файл"""
        tasks_data = [task.to_dict() for task in tasks]
        with open("tasks.json", "w", encoding="utf-8") as file:
            json.dump(tasks_data, file, ensure_ascii=False, indent=2)

    @staticmethod
    def add_to_course():
        """Додавання нового завдання до курсу"""
        from course import Course

        print("\nДодавання завдання до курсу")

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

        # Збираємо дані для створення завдання
        title = input("Введіть назву завдання: ")
        summary = input("Введіть короткий опис завдання: ")
        description = input("Введіть повний опис завдання: ")

        try:
            max_score = int(input("Введіть максимальний бал за завдання: "))
            if max_score <= 0:
                print("Максимальний бал повинен бути більше нуля")
                return
        except ValueError:
            print("Максимальний бал повинен бути числом")
            return

        deadline = input("Введіть дедлайн (необов'язково, формат YYYY-MM-DD): ")

        # Валідація введених даних
        if not validate_title(title):
            print("Назва завдання не може бути порожньою")
            return

        if not validate_content(description):
            print("Опис завдання не може бути порожнім")
            return

        # Створюємо новий урок
        lesson_type = "task"
        new_lesson = Lesson.create_lesson(title, summary, lesson_type)

        if not new_lesson:
            return

        # Створюємо нове завдання
        tasks = Task.load_tasks()
        new_task = Task(new_lesson.lesson_id, description, max_score, deadline if deadline else None)
        tasks.append(new_task)
        Task.save_tasks(tasks)

        # Додаємо завдання до курсу
        if course.add_lesson(new_lesson.lesson_id):
            print(f"Завдання '{title}' успішно додано до курсу '{course.title}'")
        else:
            print("Помилка при додаванні завдання до курсу")

    @staticmethod
    def submit_solution():
        """Метод для подання рішення завдання студентом"""
        from student import Student

        print("\nПодання рішення завдання")

        # Отримуємо ID студента
        student_id_input = input("Введіть ID студента: ")
        try:
            student_id = int(student_id_input)
        except ValueError:
            print("ID студента має бути числом")
            return

        # Перевіряємо існування студента
        student = Student.find_by_id(student_id)
        if not student:
            print("Студента з таким ID не знайдено")
            return

        if not student.enrolled_courses:
            print("Ви не записані на жодний курс")
            return

        # Виводимо курси, на які записаний студент
        from course import Course

        enrolled_courses = []
        for course_id in student.enrolled_courses:
            course = Course.find_by_id(int(course_id))
            if course:
                enrolled_courses.append(course)

        if not enrolled_courses:
            print("Помилка: не знайдено курсів, на які записаний студент")
            return

        print("\nВаші курси:")
        for idx, course in enumerate(enrolled_courses, 1):
            print(f"{idx}. {course.title}")

        try:
            course_idx = int(input("\nВиберіть номер курсу: ")) - 1
            if course_idx < 0 or course_idx >= len(enrolled_courses):
                print("Невірний вибір курсу")
                return
        except ValueError:
            print("Введіть числове значення")
            return

        selected_course = enrolled_courses[course_idx]

        # Виводимо список завдань з цього курсу
        tasks_in_course = []
        lessons = Lesson.load_lessons()
        all_tasks = Task.load_tasks()

        for lesson_id in selected_course.lessons:
            for lesson in lessons:
                if str(lesson.lesson_id) == lesson_id and lesson.type == "task":
                    for task in all_tasks:
                        if task.lesson_id == lesson.lesson_id:
                            tasks_in_course.append((lesson, task))

        if not tasks_in_course:
            print("У цьому курсі немає завдань")
            return

        print("\nЗавдання у курсі:")
        for idx, (lesson, task) in enumerate(tasks_in_course, 1):
            completed = str(lesson.lesson_id) in student.progress.get(str(selected_course.course_id), {}).get(
                "completed_lessons", [])
            status = "✓ Виконано" if completed else "◯ Не виконано"
            print(f"{idx}. {lesson.title} - {status}")

        try:
            task_idx = int(input("\nВиберіть номер завдання для виконання: ")) - 1
            if task_idx < 0 or task_idx >= len(tasks_in_course):
                print("Невірний вибір завдання")
                return
        except ValueError:
            print("Введіть числове значення")
            return

        selected_lesson, selected_task = tasks_in_course[task_idx]

        print(f"\nЗавдання: {selected_lesson.title}")
        print(f"Опис: {selected_task.description}")
        print(f"Максимальний бал: {selected_task.max_score}")

        solution = input("\nВведіть ваше рішення: ")

        if not solution.strip():
            print("Рішення не може бути порожнім")
            return

        # Оновлюємо прогрес студента
        if student.update_progress(selected_course.course_id, selected_lesson.lesson_id):
            print("Рішення успішно подано!")
        else:
            print("Помилка при поданні рішення")