import re
from datetime import datetime
from abc import ABC, abstractmethod
from .DB import DB 

'''All student views where each view can be thought of as a particular "strategy"'''

class StudentView(ABC):
    _db = DB()
    @abstractmethod
    def view(self, student_id):
        pass

class ViewRegisteredCourses(StudentView):
    def view(self, student_id):

        all_reg_course_sections = self._db.get_all_registered_course_sections(student_id=student_id)
        all_reg_labs = self._db.get_all_registered_labs(student_id=student_id) 

        if not (len(all_reg_course_sections) or len(all_reg_labs)):
            print("\033[4m" + "\033[1m" + "You are not registered for any course sections or labs." + "\033[0m")
            print("")
            return 

        print("\033[4m" + "\033[1m" + "Registered course sections and labs:" + "\033[0m")
        for record in all_reg_course_sections:
            course_section_id = record['course_section_id']
            course_info = self._db.get_course_info_from_section_id(course_section_id=course_section_id)
            print(f"\033[1m\t{course_info['name']}\033[0m:  registered course section id {course_section_id}")
        for record in all_reg_labs:
            lab_id = record['lab_id']
            course_info = self._db.get_course_info_from_lab_id(lab_id=lab_id)
            print(f"\033[1m\t{course_info['name']}\033[0m:  registered lab id {lab_id}")
        print("")
        return 

class ViewRestrictions(StudentView):
    def view(self, student_id):
        student = self._db.get_student(student_id=student_id)
        print(f"\033[1mStudent Restrictions:\033[0m {student.restrictions}")
        print("")
        return student.restrictions

class ViewTranscript(StudentView):
    __quarter_order = {
        "winter": 1,
        "spring": 2,
        "summer": 3,
        "autumn": 4,
    }

    def view(self, student_id):
        completed_courses_result = self._db.get_all_completed_courses(student_id=student_id)
        if not len(completed_courses_result):
            print("\033[4m\033[1mNo academic history to show\033[0m")
            print("")

        for record in completed_courses_result:
            course_info = self._db.get_course_info(course_id=record['course_id'])
            record['course_name'] = course_info['name'] # course name
        
        completed_courses_result.sort(key=self.__compare, reverse=True) # sorting based on year (descending) and quarter
        student = self._db.get_student(student_id=student_id)
        self.__ViewTranscript_display(completed_courses_result, student=student)        


    def __compare(self, elem):
        '''custom sorting function for sorting the list of courses taken
           by the student in order of year, quarter descending'''
        year = elem['year']
        quarter = elem['quarter']
        quarter_num = self.__quarter_order[quarter]
        return (year, quarter_num)

    @staticmethod
    def __ViewTranscript_display(res, student):
        print(f"\033[4m\033[1mAcademic Transcript of {student.name}:\033[0m")
        print(f"Status: {student.status}")
        print(f"Major: {student.major}")
        print(f"Student ID: {student.id}")
        print("")
        for idx, r in enumerate(res):
            if idx > 0 and (res[idx-1]['year'] != r['year'] or res[idx-1]['quarter'] != r['quarter']): # create separation for new year or quarter
                print("---------------------")
            print(f"course: {r['course_name']}, grade: {r['grade']}, year: {r['year']}, quarter: {r['quarter']}")
        print("")

class ViewSchedule(StudentView):

    def view(self, student_id):
        '''Schedule view of courses for which the student is registered for'''

        all_reg_course_sections = self._db.get_all_registered_course_sections(student_id=student_id)
        all_reg_labs = self._db.get_all_registered_labs(student_id=student_id)
        all_reg_course_sections = [ self._db.get_course_section_info(course_section_id=record['course_section_id']) \
                                    for record in all_reg_course_sections]
        all_reg_labs = [ self._db.get_lab_info(lab_id=record['lab_id']) for record in all_reg_labs]

        schedule_dict = self.__ViewSchedule_prepare(all_reg_course_sections, all_reg_labs)
        self.__ViewSchedule_display(schedule_dict)


    def __ViewSchedule_prepare(self, reg_sec_query_result, reg_lab_query_result):
        days_of_week_dict = {
                        'Mon': [],
                        'Tues': [],
                        'Wed': [],
                        'Thurs': [],
                        'Fri': [],
                        'Sat': [],
                        'Sun': [],
                        }
        for record in reg_sec_query_result:
            record['type'] = 'lecture'
            record['name'] = self._db.get_course_name_from_section_id(course_section_id=record['course_section_id'])
            record['id'] = record.pop('course_section_id')
        for record in reg_lab_query_result:
            record['type'] = 'lab'
            record['name'] = self._db.get_course_name_from_lab_id(lab_id=record['lab_id']) # course name
            record['id'] = record.pop('lab_id')
        for record in reg_sec_query_result + reg_lab_query_result:
            for day_of_week in re.split(r',\s*', record['days_of_week']):
                days_of_week_dict[day_of_week].append(record)
    
        for lst in days_of_week_dict.values():
            lst.sort(key=lambda record: datetime.strptime(record['start_time'], "%I:%M %p")) # sort within each day by start time

        return days_of_week_dict

    @staticmethod
    def __ViewSchedule_display(days_of_week_dict):
        print("\033[4m\033[1mWeek View of Course Schedule\033[0m")
        for day_of_week, courses in days_of_week_dict.items():
            print(day_of_week + ":")
            if not courses:
                print(f"\tNothing scheduled for {day_of_week}")
                print("")
            for course in courses:
                print(f"\tcourse: {course['name']}")
                print(f"\t{course['type']} id: {course['id']}")
                print(f"\tstart time: {course['start_time']}")
                print(f"\tend time: {course['end_time']}")
                print(f"\tlocation: {course['location']}")
                print(f"\ttype: {course['type']}")
                print("")
