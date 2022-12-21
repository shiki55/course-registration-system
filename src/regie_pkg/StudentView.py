import re
from datetime import datetime
from abc import ABC, abstractmethod
from .mysql_db import MySQLDB 
from .text_formatting import underline, bold, insert_newline
from .transcript import Transcript
from .course_schedule import StudentSchedule

'''All student views where each view can be thought of as a particular "strategy"'''

class StudentView(ABC):
    _db = MySQLDB()
    @abstractmethod
    def view(self, student_id):
        pass

class ViewRegisteredCourses(StudentView):
    def view(self, student_id):

        all_registered = self._db.get_all_registered_course_sections(student_id=student_id) + \
                         self._db.get_all_registered_labs(student_id=student_id) 

        if not len(all_registered):
            print(bold(underline("You are not registered for any course sections or labs.")))
            insert_newline()
            return 

        print(bold(underline("Registered course sections and labs:")))
        for enrollable in all_registered:
            course = self._db.get_course(course_id=enrollable.course_id)
            print(bold(f"\t{course.name}: ") + bold(f"registered {enrollable.display_class_name} id {enrollable.id}"))
        insert_newline()
        return 

class ViewRestrictions(StudentView):
    def view(self, student_id):
        student = self._db.get_student(student_id=student_id)
        print(bold("Student Restrictions: ") + f"{student.restrictions}")
        insert_newline()
        return

class ViewTranscript(StudentView):
    def view(self, student_id):
        Transcript(student_id).view()
        return 

class ViewSchedule(StudentView):
    def view(self, student_id):
        '''A week view of the student's schedule'''
        StudentSchedule(student_id).view_week()
        return 