from typing import List, Dict, Tuple, Set
from datetime import datetime


class ScheduleConflict:
    '''Finds all scheduling conflicts and is a component of ScheduleConflictHandler'''

    # Weekday as locale’s full name (%A)
    __day_of_week_dict = {
            'Sun': 'Sunday',
            'Mon': 'Monday',
            'Tues': 'Tuesday',
            'Wed': 'Wednesday',
            'Thurs':'Thursday',
            'Fri': 'Friday',
            'Sat': 'Saturday'
    }

    # strftime ignores weekday when only specifying the day of the week and time so adding %U and %Y 
    __dummy_date: str = datetime.strftime(datetime.today(), '%U %Y') # %U: week number of the year, %Y: year

    def get_all_conflicts(self, desired_course_or_lab: Dict, all_registered: List[Dict]) -> Set[int]:
        '''returns a set of lab/course section ids from all_registered that result in a scheduling conflict with
           desired_course_or_lab. Empty set returned if no conflict'''
        conflicts = set()
        for datetime_start_new, datetime_end_new, _  in self.__convert_to_datetime(records=[desired_course_or_lab]):
            for datetime_start_curr, datetime_end_curr, curr_id  in self.__convert_to_datetime(records=all_registered):
                is_conflict = max(datetime_start_new, datetime_start_curr) < min(datetime_end_new, datetime_end_curr)
                if is_conflict:
                    conflicts.add(curr_id)
        return conflicts

    def __convert_to_datetime(self, records: List[Dict]) -> List[Tuple]:
        '''returns a list of tuples where each tuple has three elements 
           (datetime object, datetime object, int) -> (start time, end time, lab/course section id)'''
        start_end_id_tups = []
        for record in records:
            days_of_week = [day_of_week.strip() for day_of_week in record['days_of_week'].split(',')]
            start_time = record['start_time']
            end_time = record['end_time']
            course_section_or_lab_id = record['course_section_id'] if record.get('course_section_id') is not None else record['lab_id']
            for day_of_week in days_of_week:
                start_datetime = datetime.strptime(
                                        f"{self.__day_of_week_dict[day_of_week]} {start_time} {self.__dummy_date}", 
                                        "%A %I:%M %p %U %Y"
                                        )
                end_datetime = datetime.strptime(
                        f"{self.__day_of_week_dict[day_of_week]} {end_time} {self.__dummy_date}", 
                        "%A %I:%M %p %U %Y"
                        )
                start_end_id_tups.append((start_datetime, end_datetime, course_section_or_lab_id))
        return start_end_id_tups
                