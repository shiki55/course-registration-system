


from abc import ABC, abstractmethod
from typing import Dict
import re
from datetime import datetime

from .enrollable import Enrollable
from .mysql_db import MySQLDB
from .text_formatting import bold, underline, insert_newline



db = MySQLDB()

class Schedule(ABC):
    @abstractmethod
    def view_week(self):
        pass


class StudentSchedule(ABC):
    def __init__(self, student_id):
        self.course_sections = db.get_all_registered_course_sections(student_id=student_id)
        self.labs = db.get_all_registered_labs(student_id=student_id)
    

    def view_week(self):
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