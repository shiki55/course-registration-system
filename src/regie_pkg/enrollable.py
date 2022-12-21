from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Tuple
import re


class Enrollable(ABC):
    """Abstract class inherited by classes 
       which are able to be enrolled in (e.g. Lab, CourseSection)
    """

    def __init__(self, 
                course_id, 
                max_reg, 
                curr_reg, 
                days_of_week,
                start_time, 
                end_time, 
                _id, 
                location, 
                year, 
                quarter,
                name):
                self.course_id = course_id
                self.max_reg = max_reg
                self.curr_reg = curr_reg
                self.days_of_week = days_of_week
                self.start_time = start_time
                self.end_time = end_time
                self.id = _id
                self.location = location
                self.year = year
                self.quarter = quarter
                self.name = name 

    def is_full(self):
        if self.curr_reg >= self.max_reg:
            return True
      
    @property
    def sessions(self) -> List[Tuple[datetime, datetime]]:
        '''
        Returns a list of sessions represented as a tuple for each enrollable object.
        A session refers to a single meeting of the course on a particular day at a specific time.
        For example, if a course section meets Mon & Fri from 6PM-8PM then it has two sessions. 
        (datetime object, datetime object) -> (start time, end time)
        '''
        # Weekday as locale’s full name (%A)
        day_of_week_dict = {
               'Sun': 'Sunday',
               'Mon': 'Monday',
               'Tues': 'Tuesday',
               'Wed': 'Wednesday',
               'Thurs':'Thursday',
               'Fri': 'Friday',
               'Sat': 'Saturday'
            }
        # strftime ignores weekday when only specifying the day of the week and time so adding %U and %Y 
        dummy_date: str = datetime.strftime(datetime.today(), '%U %Y') # %U: week number of the year, %Y: year
        all_sessions = []
        for day_of_week in [day_of_week.strip() for day_of_week in self.days_of_week.split(',')]:
           start_datetime = datetime.strptime(
                                 f"{day_of_week_dict[day_of_week]} {self.start_time} {dummy_date}", 
                                 "%A %I:%M %p %U %Y"
                                 )
           end_datetime = datetime.strptime(
               f"{day_of_week_dict[day_of_week]} {self.end_time} {dummy_date}", 
               "%A %I:%M %p %U %Y"
               )
           all_sessions.append((start_datetime, end_datetime))

        return all_sessions
      
    def schedule_conflict_with(self, enrollable: Enrollable) -> bool:
        """
        Checks if there is a scheduling conflict (does any of the meeting times overlap?)
        """
        for datetime_start_self, datetime_end_self in self.sessions:
            for datetime_start, datetime_end in enrollable.sessions:
                is_conflict = max(datetime_start_self, datetime_start) < min(datetime_end_self, datetime_end)
                if is_conflict:
                    return True
        return False

    @property
    def display_class_name(self):
        """
        return a lowercased string of the class name where each word is 
        separated by a space (e.g.'course section')
        """
        return " ".join([word.lower() for word in re.findall(r'[A-Z][a-z0-9]*', self.__class__.__name__)])



class Lab(Enrollable):
    def __init__(self, 
                course_id, 
                max_reg, 
                curr_reg, 
                days_of_week,
                start_time, 
                end_time, 
                _id, 
                location, 
                year, 
                quarter,
                name,
                course_type="lab",
                ):
                self.course_type = course_type
                super().__init__(
                        course_id, 
                        max_reg, 
                        curr_reg, 
                        days_of_week,
                        start_time, 
                        end_time, 
                        _id, 
                        location, 
                        year, 
                        quarter,
                        name)

class CourseSection(Enrollable):
    def __init__(self, 
                course_id, 
                max_reg, 
                curr_reg, 
                days_of_week,
                start_time, 
                end_time, 
                _id, 
                location, 
                year, 
                quarter,
                name,
                course_type="lecture",
                ):
                self.course_type = course_type
                super().__init__(
                    course_id, 
                    max_reg, 
                    curr_reg, 
                    days_of_week,
                    start_time, 
                    end_time, 
                    _id, 
                    location, 
                    year, 
                    quarter,
                    name
                )