"""
This module contains classes for representing and viewing schedules.

The Schedule class is an abstract base class that defines the interface for a schedule.

The StudentSchedule class is a concrete implementation of the Schedule class that
represents a student's schedule, including their registered course sections and labs.
"""

from abc import ABC, abstractmethod
from typing import Dict
import re
from datetime import datetime

from .enrollable import Enrollable
from .mysql_db import MySQLDB
from .text_formatting import bold, underline, insert_newline

class Schedule(ABC):
    """
    Abstract base class representing a schedule.
    """
    db = MySQLDB()

    @abstractmethod
    def view_week(self):
        """
        Abstract method for viewing the schedule for a given week.
        """

class StudentSchedule(Schedule):
    """
    A class representing a student's schedule (registered course sections and labs).
    """
    def __init__(self, student_id):
        self.course_sections = self.db.get_all_registered_course_sections(student_id=student_id)
        self.labs = self.db.get_all_registered_labs(student_id=student_id)

    def view_week(self):
        """
        Prints a week view of the student's schedule,
        including the days of the week, start times, end times,
        locations, and types of each course and lab.
        """
        week_schedule = self.__prepare_week_view()

        print(bold(underline("Week View of Course Schedule")))
        for day_of_week, enrollables in week_schedule.items():
            print(day_of_week + ":")
            if not enrollables:
                print(f"\tNothing scheduled for {day_of_week}")
                insert_newline()
            for enrollable in enrollables:
                print(f"\tcourse: {enrollable.name}")
                print(f"\t{enrollable.display_class_name} id: {enrollable.id}")
                print(f"\tstart time: {enrollable.start_time}")
                print(f"\tend time: {enrollable.end_time}")
                print(f"\tlocation: {enrollable.location}")
                print(f"\ttype: {enrollable.course_type}")
                insert_newline()

    def __prepare_week_view(self) -> Dict[str, Enrollable]:
        """
        Helper function for preparing a week view of the student's schedule.

        Returns:
            Dict[str, Enrollable]: A dictionary mapping days of the
            week to lists of enrollables (courses and labs)
            scheduled on that day.
        """
        week_schedule = {
                        'Mon': [],
                        'Tues': [],
                        'Wed': [],
                        'Thurs': [],
                        'Fri': [],
                        'Sat': [],
                        'Sun': [],
                        }
        for enrollable in self.course_sections + self.labs:
            for day_of_week in re.split(r',\s*', enrollable.days_of_week):
                week_schedule[day_of_week].append(enrollable)

        for lst in week_schedule.values():
            # sort within each day of the week by start time
            lst.sort(key=lambda enrollable: datetime.strptime(enrollable.start_time, "%I:%M %p"))

        return week_schedule
