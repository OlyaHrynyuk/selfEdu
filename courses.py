import json
from validators import validate_title, validate_content


class Course:
    """Клас представлення курсів"""
    __COURSE_ID = 1

    def __init__(self, title, description, author, lessons=None, enrolled_students=None):
        self.course_id = Course.__COURSE_ID
        self.title = title
        self.description = description
        self.author = author
        self.lessons = lessons if lessons else []
        self.enrolled_students = enrolled_students if enrolled_students else []
        Course.course_index()

    @classmethod
    def course_index(cls):
        """Лічильник індексів, робить їх унікальними"""
        cls.__COURSE_ID += 1

    def to_dict(self):
        """Перетворення об'єкта в словник"""
        return {
            "course_id": self.course_id,
            "title": self.title,
            "description": self.description,
            "author": self.author,
            "lessons": self.lessons,
            "enrolled_students": self.enrolled_students
        }

    @staticmethod
    def from_dict(course_dict):
        """Створює новий об'єкт з словника"""
        course = Course(
            course_dict["title"],
            course_dict["description"],
            course_dict["author"],
            course_dict.get("lessons", []),
            course_dict.get("enrolled_students", [])
        )
        course.course_id = course_dict["course_id"]
        return course

    @staticmethod
    def load_courses():
        """Підтягує всі курси з словника"""
        try:
            with open("courses.json", "r", encoding="utf-8") as file:
                courses_data = json.load(file)
                courses = []
                for course_dict in courses_data:
                    course = Course.from_dict(course_dict)
                    courses.append(course)
                return courses
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def save_courses(courses):
        """Зберігає курси у словник"""
        courses_data = []
        for course in courses:
            courses_data.append(course.to_dict())

        with open("courses.json", "w", encoding="utf-8") as file:
            json.dump(courses_data, file, ensure_ascii=False, indent=2)

    @staticmethod
    def create_course():
        """Створення нового курсу"""
        print("\nСтворення нового курсу")
        title = input("Введіть назву курсу: ")
        description = input("Введіть опис курсу: ")
        author = input("Введіть ім'я автора курсу: ")

        if not validate_title(title):
            print("Назва курсу не може бути порожньою")
            return

        if not validate_content(description):
            print("Опис курсу не може бути порожнім")
            return

        if not validate_title(author):
            print("Ім'я автора не може бути порожнім")
            return

        courses = Course.load_courses()
        new_course = Course(title, description, author)
        courses.append(new_course)
        Course.save_courses(courses)
        print(f"Курс '{title}' з ID {new_course.course_id} успішно створено!")

    @staticmethod
    def find_by_id(course_id):
        """Пошук курсу за ID"""
        courses = Course.load_courses()
        for course in courses:
            if course.course_id == course_id:
                return course
        return None

    def add_lesson(self, lesson_id):
        """Додавання уроку до курсу"""
        if str(lesson_id) not in self.lessons:
            self.lessons.append(str(lesson_id))

            courses = Course.load_courses()
            for i, course in enumerate(courses):
                if course.course_id == self.course_id:
                    courses[i] = self
                    Course.save_courses(courses)
                    return True
        return False

    def add_student(self, student_id):
        """Додавання студента до курсу"""
        if str(student_id) not in self.enrolled_students:
            self.enrolled_students.append(str(student_id))

            courses = Course.load_courses()
            for i, course in enumerate(courses):
                if course.course_id == self.course_id:
                    courses[i] = self
                    Course.save_courses(courses)
                    return True
        return False

    @staticmethod
    def enroll_student():
        """Зареєструвати студента на курс"""
        from student import Student

        print("\nЗапис студента на курс")

        students = Student.load_students()
        if not students:
            print("Немає зареєстрованих студентів. Спочатку зареєструйте студента.")
            return

        courses = Course.load_courses()
        if not courses:
            print("Немає доступних курсів. Спочатку створіть курс.")
            return

        print("\nДоступні студенти:")
        for i, student in enumerate(students, 1):
            print(f"{i}. {student.first_name} {student.last_name} (ID: {student.student_id})")

        try:
            student_index = int(input("\nВиберіть номер студента: ")) - 1
            if student_index < 0 or student_index >= len(students):
                print("Невірний вибір студента")
                return
        except ValueError:
            print("Введіть числове значення")
            return

        student = students[student_index]

        print("\nДоступні курси:")
        for i, course in enumerate(courses, 1):
            print(f"{i}. {course.title} (ID: {course.course_id})")

        try:
            course_index = int(input("\nВиберіть номер курсу: ")) - 1
            if course_index < 0 or course_index >= len(courses):
                print("Невірний вибір курсу")
                return
        except ValueError:
            print("Введіть числове значення")
            return

        course = courses[course_index]

        if str(student.student_id) in course.enrolled_students:
            print(f"Студент вже записаний на курс '{course.title}'")
            return

        if course.add_student(student.student_id) and student.enroll_in_course(course.course_id):
            print(f"Студент {student.first_name} {student.last_name} успішно записаний на курс '{course.title}'")
        else:
            print("Помилка при записі на курс")

    @staticmethod
    def edit_course():
        """Редагування існуючого курсу"""
        print("\nРедагування курсу")

        courses = Course.load_courses()
        if not courses:
            print("Немає доступних курсів для редагування")
            return

        print("\nДоступні курси:")
        for i, course in enumerate(courses, 1):
            print(f"{i}. {course.title} (ID: {course.course_id})")

        try:
            course_index = int(input("\nВиберіть номер курсу для редагування: ")) - 1
            if course_index < 0 or course_index >= len(courses):
                print("Невірний вибір курсу")
                return
        except ValueError:
            print("Введіть числове значення")
            return

        course = courses[course_index]

        print("\nЩо ви хочете редагувати?")
        print("1. Назву курсу")
        print("2. Опис курсу")
        print("3. Автора курсу")

        try:
            edit_choice = int(input("\nВаш вибір: "))
            if edit_choice < 1 or edit_choice > 3:
                print("Невірний вибір опції")
                return
        except ValueError:
            print("Введіть числове значення")
            return

        if edit_choice == 1:
            new_title = input("Введіть нову назву курсу: ")
            if not validate_title(new_title):
                print("Назва курсу не може бути порожньою")
                return
            course.title = new_title
            print("Назву курсу успішно оновлено")

        elif edit_choice == 2:
            new_description = input("Введіть новий опис курсу: ")
            if not validate_content(new_description):
                print("Опис курсу не може бути порожнім")
                return
            course.description = new_description
            print("Опис курсу успішно оновлено")

        elif edit_choice == 3:
            new_author = input("Введіть нового автора курсу: ")
            if not validate_title(new_author):
                print("Ім'я автора не може бути порожнім")
                return
            course.author = new_author
            print("Автора курсу успішно оновлено")

        for i, c in enumerate(courses):
            if c.course_id == course.course_id:
                courses[i] = course
                Course.save_courses(courses)
                break

    @staticmethod
    def list_all_courses():
        """Виведення списку всіх доступних курсів"""
        courses = Course.load_courses()

        if not courses:
            print("\nНемає доступних курсів")
            return

        print("\nДоступні курси:")
        for i, course in enumerate(courses, 1):
            student_count = len(course.enrolled_students)
            lesson_count = len(course.lessons)
            print(f"{i}. {course.title} (ID: {course.course_id})")
            print(f"   Автор: {course.author}")
            print(f"   Кількість уроків: {lesson_count}")
            print(f"   Кількість студентів: {student_count}")
            print("-" * 30)

    @staticmethod
    def show_course_details():
        """Показати детальну інформацію про курс"""
        from lesson import Lesson
        from lecture import Lecture
        from task import Task

        print("\nІнформація про курс")
        course_id_input = input("Введіть ID курсу: ")

        try:
            course_id = int(course_id_input)
        except ValueError:
            print("ID курсу повинен бути числом")
            return

        course = Course.find_by_id(course_id)
        if not course:
            print("Курс з таким ID не знайдено")
            return

        print(f"\nНазва курсу: {course.title}")
        print(f"Опис: {course.description}")
        print(f"Автор: {course.author}")

        student_count = len(course.enrolled_students)
        print(f"Кількість зареєстрованих студентів: {student_count}")

        if not course.lessons:
            print("\nУ цьому курсі ще немає уроків")
            return

        print("\nСписок уроків:")

        lessons = Lesson.load_lessons()
        lectures = Lecture.load_lectures()
        tasks = Task.load_tasks()

        for i, lesson_id in enumerate(course.lessons, 1):
            lesson = None
            for l in lessons:
                if str(l.lesson_id) == lesson_id:
                    lesson = l
                    break

            if not lesson:
                continue

            print(f"{i}. {lesson.title} (ID: {lesson.lesson_id})")

            if lesson.type == "lecture":
                for lecture in lectures:
                    if lecture.lesson_id == int(lesson_id):
                        print(f"   Тип: Лекція")
                        print(f"   Тривалість: {lecture.duration} хв")
                        break

            elif lesson.type == "task":
                for task in tasks:
                    if task.lesson_id == int(lesson_id):
                        print(f"   Тип: Завдання")
                        print(f"   Максимальний бал: {task.max_score}")
                        break

            print("-" * 30)
