import json
from validators import validate_email, validate_name


class Student:
    __STUDENT_ID = 1

    def __init__(self, first_name, last_name, email, phone=None, enrolled_courses=None, progress=None):
        self.student_id = Student.__STUDENT_ID
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.enrolled_courses = enrolled_courses if enrolled_courses else []
        self.progress = progress if progress else {}
        Student.increment_student_id()

    @classmethod
    def increment_student_id(cls):
        """Лічильник індексів, робить їх унікальними"""
        cls.__STUDENT_ID += 1

    def to_dict(self):
        """Перетворення об'єкта в словник"""
        return {
            "student_id": self.student_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "enrolled_courses": self.enrolled_courses,
            "progress": self.progress
        }

    @staticmethod
    def from_dict(student_dict):
        """Створює новий об'єкт з словника"""
        student = Student(
            student_dict["first_name"],
            student_dict["last_name"],
            student_dict["email"],
            student_dict.get("phone"),
            student_dict.get("enrolled_courses", []),
            student_dict.get("progress", {})
        )
        student.student_id = student_dict["student_id"]
        return student

    @staticmethod
    def load_students():
        """Підтягує всіх студентів з словника"""
        try:
            with open("students.json", "r", encoding="utf-8") as file:
                students_data = json.load(file)
                students = []
                for student_dict in students_data:
                    student = Student.from_dict(student_dict)
                    students.append(student)
                return students
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def save_students(students):
        """Зберігає студентів у словник"""
        students_data = []
        for student in students:
            students_data.append(student.to_dict())

        with open("students.json", "w", encoding="utf-8") as file:
            json.dump(students_data, file, ensure_ascii=False, indent=2)

    @staticmethod
    def register_student():
        """Реєстрація студента"""
        print("\nРеєстрація студента")
        first_name = input("Введіть ім'я студента: ")
        last_name = input("Введіть прізвище студента: ")
        email = input("Введіть електронну пошту: ")
        phone = input("Введіть номер телефону (необов'язково): ")

        if not validate_name(first_name) or not validate_name(last_name):
            print("Ім'я та прізвище повинні містити тільки літери і не бути порожніми")
            return

        if not validate_email(email):
            print("Некоректний формат електронної пошти")
            return

        students = Student.load_students()
        for student in students:
            if student.email == email:
                print("Студент з такою електронною поштою вже існує")
                return

        phone = phone if phone else None
        new_student = Student(first_name, last_name, email, phone)
        students.append(new_student)
        Student.save_students(students)
        print(f"Студент {first_name} {last_name} з ID {new_student.student_id} успішно зареєстрований!")

    @staticmethod
    def find_by_id(student_id):
        """Пошук студента за ID"""
        students = Student.load_students()
        for student in students:
            if student.student_id == student_id:
                return student
        return None

    def enroll_in_course(self, course_id):
        """Запис студента на курс"""
        if str(course_id) not in self.enrolled_courses:
            self.enrolled_courses.append(str(course_id))
            self.progress[str(course_id)] = {"completed_lessons": [], "overall_progress": 0}

            students = Student.load_students()
            for i, student in enumerate(students):
                if student.student_id == self.student_id:
                    students[i] = self
                    Student.save_students(students)
                    return True
        return False

    def update_progress(self, course_id, lesson_id):
        """Оновлює прогрес студента після завершення уроку"""
        course_id_str = str(course_id)
        lesson_id_str = str(lesson_id)

        if course_id_str in self.progress:
            if lesson_id_str not in self.progress[course_id_str]["completed_lessons"]:
                self.progress[course_id_str]["completed_lessons"].append(lesson_id_str)

                # Оновлюємо загальний прогрес курсу
                from course import Course
                course = Course.find_by_id(int(course_id))
                if course:
                    total_lessons = len(course.lessons)
                    completed_lessons = len(self.progress[course_id_str]["completed_lessons"])

                    if total_lessons > 0:
                        progress_percentage = round((completed_lessons / total_lessons) * 100)
                        self.progress[course_id_str]["overall_progress"] = progress_percentage

                students = Student.load_students()
                for i, student in enumerate(students):
                    if student.student_id == self.student_id:
                        students[i] = self
                        Student.save_students(students)
                        return True
        return False

    @staticmethod
    def show_progress():
        """Відображення прогресу студента за всіма курсами"""
        print("\nПерегляд прогресу студента")
        student_id_input = input("Введіть ID студента: ")

        try:
            student_id = int(student_id_input)
        except ValueError:
            print("ID студента повинен бути числом")
            return

        student = Student.find_by_id(student_id)
        if not student:
            print("Студента з таким ID не знайдено")
            return

        print(f"\nПрогрес студента: {student.first_name} {student.last_name}")

        if not student.enrolled_courses:
            print("Студент не записаний на жодний курс")
            return

        from course import Course

        for course_id in student.enrolled_courses:
            course = Course.find_by_id(int(course_id))
            if course:
                progress_info = student.progress.get(course_id, {"overall_progress": 0})
                print(f"Курс: {course.title}")
                print(f"Прогрес: {progress_info['overall_progress']}%")

                completed_lessons = progress_info.get("completed_lessons", [])
                print(f"Завершено уроків: {len(completed_lessons)} з {len(course.lessons)}")
                print("-" * 30)