from .mysql_db import MySQLDB 
from .Student import Student
from .course import CompletedCourse
from .text_formatting import bold, underline, insert_newline

class Transcript:
    __db = MySQLDB()
    def __init__(self, student_id):
        self.student: Student = self.__db.get_student(student_id)
        self.completed_courses: CompletedCourse = self.__db.get_completed_courses(student_id)

    def view(self):
        if not self.completed_courses:
            print(bold(underline("No academic history to show")))
            insert_newline()

        # sorting based on year (descending) and quarter
        completed_courses_sorted = sorted(self.completed_courses,key=self.__compare, reverse=True) 

        print(bold(underline(f"Academic Transcript of {self.student.name}:")))
        print(f"Status: {self.student.status}")
        print(f"Major: {self.student.major}")
        print(f"Student ID: {self.student.id}")
        insert_newline()
        for idx, course in enumerate(completed_courses_sorted):
            if idx > 0 and (completed_courses_sorted[idx-1].year != course.year or 
                            completed_courses_sorted[idx-1].quarter != course.quarter): # create separation for new year or quarter
                print("---------------------")
            print(f"course: {course.name}, grade: {course.grade}, year: {course.year}, quarter: {course.quarter}")
        insert_newline()

    def __compare(self, course: CompletedCourse):
        '''custom sorting function for sorting the list of courses taken
           by the student in order of year, quarter descending'''
        quarter_order = {
        "winter": 1,
        "spring": 2,
        "summer": 3,
        "autumn": 4,
        }
        return (course.year, quarter_order[course.quarter])

