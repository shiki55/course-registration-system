# from typing import List, Dict, Tuple, Set
# from datetime import datetime

# from .enrollable import Enrollable

# class ScheduleConflict:
#     '''Finds all scheduling conflicts and is a component of ScheduleConflictHandler'''





#     def get_all_conflicts(self, target_enrollment: Enrollable, all_registered: List[Enrollable]) -> Set[Enrollable]:
#         '''returns a set of lab/course section from all_registered that result in a scheduling conflict with
#            desired_course_or_lab. Empty set returned if no conflict'''
#         conflicts = set()
#         for datetime_start_new, datetime_end_new, _  in self.__convert_to_datetime(enrollable=target_enrollment):
#             for datetime_start_curr, datetime_end_curr, curr_id  in self.__convert_to_datetime(records=all_registered):
#                 is_conflict = max(datetime_start_new, datetime_start_curr) < min(datetime_end_new, datetime_end_curr)
#                 if is_conflict:
#                     conflicts.add(curr_id)
#         return conflicts
