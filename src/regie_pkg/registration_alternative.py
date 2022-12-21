"""This module contains a class to find and display alternative course or lab sections."""
from typing import List
from .enrollable import Enrollable
from .mysql_db import MySQLDB
from .text_formatting import bold, underline, insert_newline

class RegistrationAlternative:
    """This class finds alternative registration options and displays them."""

    __db = MySQLDB()
    __days_of_week_order = {
                'mon': 1,
                'tues': 2,
                'wed': 3,
                'thurs': 4,
                'fri': 5,
                'sat': 6,
                'sun': 7,
                }
    def find_alternatives(self, id):
        """Find alternative course section/lab registration options."""
        alternatives: List[Enrollable] # alternative course sections or labs
        if self.__db.is_course_section(id):
            course_section = self.__db.get_course_section(id)
            alternatives = [ course_section
                for course_section in self.__db.get_all_course_sections(course_id=course_section.course_id)
                if course_section.id != id
                ]
        else:
            lab = self.__db.get_lab(id)
            alternatives = [ lab
                for lab in self.__db.get_all_labs(course_id=lab.course_id)
                if lab.id != id
                ]

        if not alternatives:
            print("No alternative course sections or labs available.\n")
            return

        alternatives.sort(key=self.__compare) # sort alternatives
        self.__display_alternatives(alternatives)
        return

    def __compare(self, enrollable: Enrollable):
        """
        Custom sorting function for sorting the list of alternatives
        based on the day of the week.
        """
        # start_day_of_week is the first day of the week that this course section/lab is offered
        start_day_of_week = enrollable.days_of_week.split(',')[0].strip().lower()
        day_of_week_num = self.__days_of_week_order[start_day_of_week]
        return day_of_week_num

    def __display_alternatives(self, alternatives):
        """Displaying the alternative options."""

        print(bold(underline("Alternative Course Section/Lab Offerings:")))
        for enrollable in alternatives:
            print(f"\tID: {enrollable.id}")
            print(f"\tDays of Week: {enrollable.days_of_week}")
            print(f"\tStart Time: {enrollable.start_time}")
            print(f"\tEnd Time: {enrollable.end_time}")
            print(f"\tLocation: {enrollable.location}")
            print(f"\tTotal Enrollment: {enrollable.curr_reg}/{enrollable.max_reg}")
            insert_newline()