import os
import json
from student import Student
from course import Course
from lecture import Lecture
from task import Task

def initialize_files():
    """Перевірка чи є відповідні файли і створює їх при відсутності"""
    files = ["students.json", "courses.json", "lessons.json", "lectures.json", "tasks.json"]

    for file in files:
        if not os.path.exists(file):
            with open(file, "w", encoding="utf-8") as f:
                json.dump([], f)


def main():
    initialize_files()

    while True:
        print("\nМеню системи онлайн-курсів")
        print("1. Зареєструвати студента")
        print("2. Створити курс")
        print("3. Додати лекцію до курсу")
        print("4. Додати завдання до курсу")
        print("5. Записати студента на курс")
        print("6. Показати прогрес студента")
        print("7. Редагувати курс")
        print("8. Переглянути доступні курси")
        print("9. Переглянути інформацію про курс")
        print("10. Вирішити завдання")
        print("0. Вихід")

        choice = input("Оберіть опцію: ")

        if choice == "1":
            Student.register_student()
        elif choice == "2":
            Course.create_course()
        elif choice == "3":
            Lecture.add_to_course()
        elif choice == "4":
            Task.add_to_course()
        elif choice == "5":
            Course.enroll_student()
        elif choice == "6":
            Student.show_progress()
        elif choice == "7":
            Course.edit_course()
        elif choice == "8":
            Course.list_all_courses()
        elif choice == "9":
            Course.show_course_details()
        elif choice == "10":
            Task.submit_solution()
        elif choice == "0":
            print("Програму завершено!")
            break
        else:
            print("Невірна опція. Спробуйте ще раз.")


if __name__ == "__main__":
    main()