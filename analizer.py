import csv
from exception import *


class AnalizerMarks:
    available_mode = ("student", "teacher", "worst_teacher", "best_student",
                      "easiest_course", "best_students_on_course")

    def __init__(self):
        self.filename = None

    def infinite_pooling(self) -> None:
        self.filename = self.get_file_name()
        while True:
            method, arg = self.get_requirement_function()
            if arg:
                try:
                    result = method(arg)
                    if isinstance(result, dict):
                        for key, value in result.items():
                            print(f"{key}: {value}")
                    else:
                        print(result)
                except NameDoesNotExist:
                    print("Entered name does not exist, repeat your request.")
            else:
                result = method()
                if isinstance(result, dict):
                    for key, value in result.items():
                        print(f"{key}: {value}")
                else:
                    print(result)

    def get_requirement_function(self):
        while True:
            command = input("Enter mode and parameter "
                            "(if requires): ")
            if command.split()[0] in self.available_mode:
                if len(command.split()) == 1:
                    mode = command
                    if mode == "worst_teacher":
                        return self.worst_teacher, None
                    elif mode == "best_student":
                        return self.best_student, None
                    elif mode == "easiest_course":
                        return self.easiest_course, None
                    elif mode == "best_students_on_course":
                        return self.best_students_on_course, None
                elif len(command.split()) == 2:
                    mode, name = command.split()
                    if mode == "student":
                        return self.student, name
                    elif mode == "teacher":
                        return self.teacher, name
            else:
                print("Enter an available mode from the list:")
                for mode_id, mode_name in enumerate(self.available_mode):
                    print(f"{mode_id}. {mode_name};")

    def get_file_name(self):
        while True:
            fname = input("Enter file name: ")
            try:
                if fname.split(sep=".")[-1] == "csv":
                    with open(fname, newline="\n"):
                        pass
                    return fname
                else:
                    print("Enter file name with extension csv")
            except FileNotFoundError:
                print("File was not found in current directory")

    def student(self, student_name):
        with open(self.filename, newline="\n") as r_file:
            f_reader = csv.reader(r_file, delimiter=";")
            subjects = {}
            for row in f_reader:
                if row[1] == student_name:
                    if row[2] not in subjects:
                        subjects[row[2]] = [int(row[4])]
                    else:
                        subjects[row[2]].append(int(row[4]))
            if len(subjects.keys()) == 0:
                raise NameDoesNotExist
            result = {"name": student_name,
                      "subjects": {}}

            for subject, value in subjects.items():
                result["subjects"][subject] = sum(value) / len(value)
            return result

    def teacher(self, teacher_name):
        with open(self.filename, newline="\n") as r_file:
            f_reader = csv.reader(r_file, delimiter=";")

            subjects = {}
            for row in f_reader:
                if row[3] == teacher_name:
                    if row[2] not in subjects:
                        subjects[row[2]] = [int(row[4])]
                    else:
                        subjects[row[2]].append(int(row[4]))
            if len(subjects.keys()) == 0:
                raise NameDoesNotExist
            result = {"name": teacher_name,
                      "subjects": {}}

            for subject, value in subjects.items():
                result["subjects"][subject] = sum(value) / len(value)
            return result

    def worst_teacher(self):
        with open(self.filename, newline="\n") as r_file:
            f_reader = csv.reader(r_file, delimiter=";")

            teachers_names = []
            teachers_average_marks = []
            for row in f_reader:
                if row[3] not in teachers_names:
                    teachers_names.append(row[3])

            for teacher_name in teachers_names:
                teachers_average_marks.append(self.teacher(teacher_name))

            worst_teacher_name = ""
            worst_subject_name = ""
            worst_teacher_average_mark = 5
            for teacher in teachers_average_marks:
                for subject_name, subject_mark in teacher["subjects"].items():
                    if subject_mark < worst_teacher_average_mark:
                        worst_teacher_name = teacher["name"]
                        worst_subject_name = subject_name
                        worst_teacher_average_mark = subject_mark

            result = f"Teacher name: {worst_teacher_name}\n" \
                     f"Worst subject: {worst_subject_name}"
            return result

    def best_student(self):
        with open(self.filename, newline="\n") as r_file:
            f_reader = csv.reader(r_file, delimiter=";")

            students = {}

            for row in f_reader:
                if row[1] not in students:
                    students[row[1]] = [int(row[4])]
                else:
                    students[row[1]].append(int(row[4]))

            students_average_marks = {}
            for student_name, student_marks_list in students.items():
                students_average_marks[student_name] = \
                    sum(student_marks_list) / len(student_marks_list)

            best_student_name = ""
            best_average = 0
            for student_name, average_marks in students_average_marks.items():
                if average_marks > best_average:
                    best_student_name = student_name
                    best_average = average_marks

            result = f"Student name: {best_student_name}\n" \
                     f"Average mark: {best_average}"
            return result

    def easiest_course(self):
        with open(self.filename, newline="\n") as r_file:
            f_reader = csv.reader(r_file, delimiter=";")

            courses = {}

            for row in f_reader:
                if row[2] not in courses:
                    courses[row[2]] = [int(row[4])]
                else:
                    courses[row[2]].append(int(row[4]))

            courses_average_marks = {}
            for course_name, course_marks_list in courses.items():
                courses_average_marks[course_name] = \
                    sum(course_marks_list) / len(course_marks_list)

            best_course_name = ""
            best_average = 0
            for course_name, average_marks in courses_average_marks.items():
                if average_marks > best_average:
                    best_course_name = course_name
                    best_average = average_marks

            result = f"Easiest course: {best_course_name}\n" \
                     f"Average mark: {best_average}"
            return result

    def best_students_on_course(self):
        with open(self.filename, newline="\n") as r_file:
            f_reader = csv.reader(r_file, delimiter=";")

            courses = {}
            for row in f_reader:
                if row[2] not in courses:
                    courses.update(
                        {row[2]:
                            {row[1]: [int(row[4])]
                             }
                         })
                elif row[1] not in courses[row[2]]:
                    courses[row[2]][row[1]] = [int(row[4])]
                else:
                    courses[row[2]][row[1]].append(int(row[4]))

            for course_name, students in courses.items():
                for student_name, marks in students.items():
                    courses[course_name][student_name] = sum(marks)/len(marks)

            best_students_on_course_average = {}
            for course_name, students in courses.items():
                best_student_name = ""
                best_courses_name = ""
                best_student_average = 0
                for student_name, average_mark in students.items():
                    if average_mark > best_student_average:
                        best_student_name = student_name
                        best_courses_name = course_name
                        best_student_average = average_mark
                best_students_on_course_average.update(
                    {
                        best_courses_name:
                            {
                                best_student_name:
                                    {
                                        best_student_average
                                    }
                            }
                    }
                )
            result = ""
            for course_name, student in best_students_on_course_average.items():
                for student_name, average_mark in student.items():
                    result += f"Course name: {course_name};" \
                              f" Best student: {student_name};" \
                              f" Average mark: {average_mark}\n"
            return result
