from os import path
from exception import *


class AnalizerMarks:
    available_commands = {
        "student": "Format: 'student [student name]'. The average grade in "
                   "each subject",
        "teacher": "Format: 'student [student name]'. The "
                   "average grade given by the teacher",
        "worst_teacher": "the name of the teacher and the subject in which "
                         "the average score of all students is the lowest",
        "best_student": "the last name of the student who has "
                        "the highest average scores in all "
                        "subjects is displayed",
        "easiest_course": "the name of the course in which all students have "
                          "the highest scores",
        "best_students_on_course": "displays the best student in each course",
    }

    def __init__(self):
        self.filename = self.get_file_name()
        self.filedata = []
        self.fill_data(self.filename)

    def infinite_pooling(self) -> None:
        while True:
            try:
                user_command = self.get_command()
                method, parameter = self.user_method_filter(user_command)
                if parameter:
                    try:
                        result = method(parameter)
                        self.print_result(result)
                    except NameDoesNotExist:
                        print(
                            "Entered name does not exist,"
                            " repeat your request.")
                else:
                    result = method()
                    self.print_result(result)
            except CommandDoesNotExists:
                print("\nEntered command does not exists. See the manual:")
                self.help()
            except WrongMethodParameters:
                print("\nEntered parameters do not fit the function. "
                      "See the manual")
                self.help()

    def get_file_name(self):
        while True:
            fname = input("Enter file name: ")
            if path.exists(fname) and fname.endswith(".csv"):
                return fname

    def fill_data(self, fname):
        with open(fname, mode="r", newline="\n") as file:
            for row in file:
                self.filedata.append(row.split(sep=";"))

    def get_command(self):
        command = input("Enter mode and parameter "
                        "(if requires): ")
        if command.split()[0] in self.available_commands.keys():
            return command
        else:
            raise CommandDoesNotExists

    def user_method_filter(self, command):
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
            raise WrongMethodParameters

    def help(self):
        for command, description in self.available_commands.items():
            print(f"\t{command} - {description}", end="\n")

    def print_result(self, data: dict, amount_value_tabulation=0):
        for key, value in data.items():
            print("{tab}{key}:".format(
                tab="\t" * amount_value_tabulation,
                key=key,
            ))
            if isinstance(value, (dict, list)):
                self.print_result(value, amount_value_tabulation + 1)
            else:
                print("{tab}{value}".format(
                    tab="\t" * (amount_value_tabulation + 1),
                    value=value,
                ))

    def student(self, student_name: str):
        subjects = self.get_distinct_values(name=student_name,
                                            id_column_name=1)

        result = {
            "Name": student_name,
            "Subjects": {},
        }

        for subject, mark in subjects.items():
            result["Subjects"][subject] = sum(mark) / len(mark)

        return result

    def teacher(self, teacher_name):
        subjects = self.get_distinct_values(name=teacher_name,
                                            id_column_name=3)

        result = {
            "Name": teacher_name,
            "Subjects": {},
        }

        for subject, mark in subjects.items():
            result["Subjects"][subject] = round(sum(mark) / len(mark), 2)

        return result

    def get_distinct_values(self, id_column_name, name=""):
        subjects = {}
        for row in self.filedata:
            if row[id_column_name] == name:
                if row[2] not in subjects:
                    subjects[row[2]] = [int(row[4])]
                else:
                    subjects[row[2]].append(int(row[4]))

        if len(subjects.keys()) == 0:
            raise NameDoesNotExist

        return subjects

    def worst_teacher(self):
        teachers_names = []
        teachers_average_marks = []

        for row in self.filedata:
            if row[3] not in teachers_names:
                teachers_names.append(row[3])

        for teacher_name in teachers_names:
            teachers_average_marks.append(self.teacher(teacher_name))

        worst_teacher_name = ""
        worst_subject_name = ""
        worst_teacher_average_mark = 5
        for teacher in teachers_average_marks:
            for subject_name, subject_mark in teacher["Subjects"].items():
                if subject_mark < worst_teacher_average_mark:
                    worst_teacher_name = teacher["Name"]
                    worst_subject_name = subject_name
                    worst_teacher_average_mark = subject_mark

        result = {
            "Teacher name": worst_teacher_name,
            "Worst subject": worst_subject_name,
        }
        return result

    def best_student(self):
        students = {}

        for row in self.filedata:
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

        result = {
            "Student name": best_student_name,
            "All subjects average marks": best_average,
        }
        return result

    def easiest_course(self):
        courses = {}

        for row in self.filedata:
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

        result = {
            "Easiest course name": best_course_name,
            "Subject average marks": best_average,
        }
        return result

    def best_students_on_course(self):
        courses = {}

        for row in self.filedata:
            if row[2] not in courses:
                courses.update(
                    {row[2]:
                        {
                            row[1]: [int(row[4])]
                        }
                    })
            elif row[1] not in courses[row[2]]:
                courses[row[2]][row[1]] = [int(row[4])]
            else:
                courses[row[2]][row[1]].append(int(row[4]))

        for course_name, students in courses.items():
            for student_name, marks in students.items():
                courses[course_name][student_name] = sum(marks) / len(marks)

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
            best_students_on_course_average.update({best_courses_name: {
                best_student_name: best_student_average}})

        result = {"Courses": {}}
        for course_name, student in \
                best_students_on_course_average.items():
            for student_name, average_mark in student.items():
                result["Courses"].update({
                    course_name: {"Best student": student_name,
                                  "Average mark": average_mark}
                })

        return result
