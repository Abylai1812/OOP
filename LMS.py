import json
import os
from datetime import datetime

class Teacher:
    def __init__(self, name: str, subject: str):
        self.name = name
        self.subject = subject

    def to_dict(self):
        return {
            "name": self.name,
            "subject": self.subject
        }

    def __str__(self):
        return f'Учитель {self.name} (Язык программирования: {self.subject})'

class Course:
    def __init__(self, name: str, teacher: Teacher):
        self.name = name
        self.teacher = teacher
        self.students = []

    def to_dict(self):
        return {
            "name": self.name,
            "teacher_name": self.teacher.name,
            "student_names": [student.name for student in self.students]
        }

    def __str__(self):
        return f'Курс: {self.name}, Учитель: {self.teacher.name}'

class Student:
    def __init__(self, name: str):
        self.name = name
        self.join_date = datetime.now()
        self.grades = {}

    def add_grade(self, course, grade):  
        self.grades[course] = grade

    def add_grades(self, grades):
        self.grades.update(grades)
    
    def get_grades(self):
        return self.grades

    def calculate_year_grade(self):
        if not self.grades:
            return 0
        return sum(self.grades.values()) / len(self.grades)

    def to_dict(self):
        return {
            "name": self.name,
            "join_date": self.join_date.strftime("%Y-%m-%d %H:%M:%S")
        }

    def __str__(self):
        return f'Студент: {self.name}'

class LMS:
    def __init__(self):
        self.teachers = []
        self.courses = []
        self.students = []

    def add_teacher(self, name: str, subject: str):
        teacher = Teacher(name, subject)
        self.teachers.append(teacher)
        print(f"Учитель {teacher.name} добавлен. Номер учителя: {len(self.teachers)}")

    def add_course(self, name: str, teacher: Teacher):
        course = Course(name, teacher)
        self.courses.append(course)
        print(f"Курс {course.name} добавлен. Номер курса: {len(self.courses)}")

    def add_student(self, name: str):
        student = Student(name)
        self.students.append(student)
        print(f"Студент {student.name} добавлен. Номер студента: {len(self.students)}")

    def enroll_student_in_course(self, student, course):
        course.students.append(student)
        print(f"{student.name} был добавлен в курс {course.name}")

    def get_grades_input(self) -> dict:
        grades = {}
        while True:
            grade_input = input("Введите оценки или q для выхода: ")
            if grade_input.lower() == 'q':
                break
            grade = int(grade_input)
            grades[lms.courses[course_index]] = grade
        return grades
    
    def add_grades_for_student(self, student, grades):
        for course, grade in grades.items():
            student.add_grade(course, grade)
        print(f"Оценки {grades} были добавлены для {student.name}")

    def display_information(self):
        print("Учителя:")
        for i, teacher in enumerate(self.teachers, start=1):
            print(f"{i}. {teacher}")

        print("\nКурсы:")
        for i, course in enumerate(self.courses, start=1):
            print(f"{i}. {course}")
            print("Студенты записанные:")
            for student in course.students:
                print(f"  - {student.name}")

        print("\nСтуденты:")
        for i, student in enumerate(self.students, start=1):
            print(f"{i}. {student}")
            my_grades = student.get_grades()
            for course, grade in my_grades.items():
                print(f"  - {course.name}: {grade}")

    def save_to_file(self, filename: str = "data.json"):
        data = {
            "teachers": [teacher.to_dict() for teacher in self.teachers],
            "courses": [course.to_dict() for course in self.courses],
            "students": [student.to_dict() for student in self.students]
        }

        with open(filename, 'w') as file:
            json.dump(data, file)

    def load_from_file(self, filename: str = "data.json"):
        with open(filename, 'r') as file:
            data = json.load(file)

        self.teachers = [Teacher(**teacher) for teacher in data["teachers"]]
        self.courses = [Course(course["name"], Teacher(course["teacher_name"], "")) for course in data["courses"]]
        self.students = [Student(name=student_data["name"]) for student_data in data["students"]]


    def choose_file(self) -> str:
        self.list_files()
        filename = input("Введите названия файла: ")
        return filename

    def list_files(self):
        print("Досупные файлы:")
        for i, file in enumerate(os.listdir(".")):
            if file.endswith(".json"):
                print(f"{i + 1}. {file}")


    def delete_file(self, filename: str):
        try:
            os.remove(filename)
            print(f"Файл {filename} успешно удален.")
        except FileNotFoundError:
            print(f"Файл {filename} не найден.")
        except Exception as e:
            print(f"Ошибка: {e}")

    def save_grades_to_file(self, filename: str = "grades.json"):
        grades_data = {}

        for student in self.students:
            student_grades = {}
            for course, grade in student.get_grades().items():
                course_name = course.name
                student_grades[course_name] = grade

            grades_data[student.name] = {
                "grades": student_grades,
                "average_grade": student.calculate_year_grade()
            }

        with open(filename, 'w') as file:
            json.dump(grades_data, file)
            
    def save_students_to_file(self, filename: str = "students.json"):
        students_data = []

        for student in self.students:
            students_data.append(student.to_dict())

        with open(filename, 'w') as file:
            json.dump(students_data, file)
            
            
lms = LMS()

while True:
    print("\nLMS JustCode Меню:")
    print("1. Добавить учителя")
    print("2. Добавить курс")
    print("3. Добавить студента")
    print("4. Записать студента в курс")
    print("5. Сохранить студента")
    print("6. Добавить оценки для студента")
    print("7. Сохранить оценки для студента")
    print("8. Показать информацию")
    print("9. Сохранить")
    print("10. Загрузка")
    print("11. Показать файлы")
    print("12. Удалить файл")
    print("13. Выйти")

    choice = input("Ваш выбор: ")
    if choice == "1":
        name = input("Имя учителя: ")
        subject = input("Язык программирования: ")
        lms.add_teacher(name, subject)
    elif choice == "2":
        name = input("Название курса: ")
        teacher_index = int(input("Введите номер учителя: ")) - 1

        if 0 <= teacher_index < len(lms.teachers):
            teacher = lms.teachers[teacher_index]
            lms.add_course(name, teacher)
        else:
            print("Неверный номер учителя.")
    elif choice == "3":
        name = input("Имя студента: ")
        lms.add_student(name)
    elif choice == "4":
        student_index = int(input("Номер студента для записи: ")) - 1
        course_index = int(input("Номер курса: ")) - 1

        if 0 <= student_index < len(lms.students) and 0 <= course_index < len(lms.courses):
            student = lms.students[student_index]
            course = lms.courses[course_index]
            lms.enroll_student_in_course(student, course)
        else:
            print("Неверный номер студента или курса.")
    elif choice == "5":
        filename = input("Имя файла для сохранения информации о студентах: ")
        lms.save_students_to_file(filename)
        print(f"Информация о студентах сохранена в файл {filename}")
    elif choice == "6":
        student_index = int(input("Номер студента для оценок: ")) - 1
        course_index = int(input("Номер курса: ")) - 1

        if 0 <= student_index < len(lms.students) and 0 <= course_index < len(lms.courses):
            grades = lms.get_grades_input()
            student = lms.students[student_index]
            lms.add_grades_for_student(student, grades)
        else:
            print("Неверный номер студента или курса.")
    elif choice == "7":
        filename = input("Имя файла для сохранения оценок: ")
        lms.save_grades_to_file(filename)
        print(f"Оценки сохранены в файл {filename}")
    elif choice == "8":
        lms.display_information()
    elif choice == "9":
        filename = input("Имя файла: ")
        lms.save_to_file(filename)
        print(f"Файл {filename} сохранен.")
    elif choice == "10":
        filename = lms.choose_file()
        if os.path.exists(filename):
            lms.load_from_file(filename)
            print(f"Файл {filename} загружен.")
        else:
            print(f"Файл {filename} не существует.")
    elif choice == "11":
        lms.list_files()
    elif choice == "12":
        filename = lms.choose_file()
        lms.delete_file(filename)
    elif choice == "13":
        break
    else:
        print("Ошибка ввода!")