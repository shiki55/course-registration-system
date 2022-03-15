from abc import ABC, abstractmethod
from .RegistrationApproval import RegistrationApproval, IStudentOverload, IApprovalRequired
from .RegistrationAlternative import RegistrationAlternative
from .ScheduleConflict import ScheduleConflict
from .DB import DB

class RegistrationHandler(ABC):
    '''Chain of Responsibility'''
    next_handler_obj = None
    _db = DB() # protected
    
    def set_next(self, handler_obj):
        self.next_handler_obj = handler_obj
        return handler_obj
    
    @abstractmethod
    def process_request(self, student_id, course_id): 
        if self.next_handler_obj:
            return self.next_handler_obj.process_request(student_id, course_id)
        return None

class NotRegisteredHandler(RegistrationHandler):
    '''handler for a request to drop a course the student is not registered for'''
    def process_request(self, student_id, course_id):
        all_reg_sec_result = self._db.get_all_registered_course_sections(student_id=student_id)
        all_reg_lab_result = self._db.get_all_registered_labs(student_id=student_id) 
        for record in all_reg_sec_result + all_reg_lab_result:
            course_section_or_lab_id = record['course_section_id'] if record.get('course_section_id') is not None else record['lab_id']
            if course_section_or_lab_id == course_id:
                return super().process_request(student_id, course_id)
    
        print(f"Cannot drop because you are not registered for a course section or lab with id {course_id}.")
        return 


class DropCourseHandler(RegistrationHandler):
    '''handler which updates the database with course section/lab drop'''
    def process_request(self, student_id, course_id):
        self._db.unregister_course(student_id=student_id, course_id=course_id)
        print("Course drop successful")  
        return


class CourseDoesNotExistHandler(RegistrationHandler):
    '''handler for request to register for a course section/lab which does not exist'''
    def process_request(self, student_id, course_id):                
        if not (self._db.is_lab(id=course_id) or self._db.is_course_section(id=course_id)):
            print(f"Cannot add because {course_id} is not an id for a course section or lab.")
            return
        return super().process_request(student_id, course_id)

class ClosedCourseHandler(RegistrationHandler):
    registration_alternative = RegistrationAlternative()
    '''handler for request to register for a course section/lab which is closed'''
    def process_request(self, student_id, course_id):
        course_sec_result = self._db.get_course_section_info(course_section_id=course_id)
        lab_result = self._db.get_lab_info(lab_id=course_id)
        record = course_sec_result if course_sec_result is not None else lab_result
        if record['curr_reg'] >= record['max_reg']:
            print("Courses section or lab is full. Cannot add.") # TODO: show alternatives (implement this when you have more data)
            print("Pulling up alternative registration options...")
            print("")
            self.registration_alternative.find_alternatives(id=record.get('course_section_id', record.get('lab_id')))
            return 
        return super().process_request(student_id, course_id) 

class StudentRestrictionsHandler(RegistrationHandler):
    '''handler for request to register for a course section/lab by a student with account restrictions'''
    def process_request(self, student_id, course_id):
        student_result = self._db.get_student_profile(student_id=student_id)
        student_restriction = student_result['restriction']
        if student_restriction is not None:
            print(f"Cannot add course because you have the following restriction(s): {student_restriction}")
            return
        return super().process_request(student_id, course_id) 


class StudentOverloadHandler(RegistrationHandler):
    '''handler for request to register for a course section/lab that requires overloading approval'''
    registration_approval: IStudentOverload = RegistrationApproval() # helper for executing actions when overload approval is needed
    def process_request(self, student_id, course_id):
        student_result = self._db.get_student_profile(student_id=student_id)
        student_status = student_result['status']
        all_reg_sec_result = self._db.get_all_registered_course_sections(student_id=student_id)
        if (student_status == 'full-time' and len(all_reg_sec_result) >= 3) or \
           (student_status == 'part-time' and len(all_reg_sec_result) >= 2):
            self.registration_approval.StudentOverloadHandler(student_id=student_id)
            return  
        else:
            return super().process_request(student_id, course_id)
        

class PrerequisiteNotMetHandler(RegistrationHandler):
    '''handler for request to register for a course section/lab for which the student does not have the prerequisites met'''
    def process_request(self, student_id, course_id):
        courses_taken_result = self._db.get_all_completed_courses(student_id=student_id)
        courses_taken_set = {record['course_id'] for record in courses_taken_result}
        required_prereqs_result = self._db.get_all_prereqs(course_id)
        required_prereqs_set = set(required_prereqs_result)
        if len(required_prereqs_set) > 0 and \
           len(courses_taken_set.intersection(required_prereqs_set)) < len(required_prereqs_set):
           print("")
           print("Cannot add because you have not taken the prerequisites.")
           print("The following course(s) must be taken and completed before registering for the requested course:")
           for need_to_take_course_id in required_prereqs_set-courses_taken_set:
               course_info = self._db.get_course_info(course_id=need_to_take_course_id)
               print(f"\033[1m\tCourse Name:\033[0m {course_info['name']}")
           return 
        return super().process_request(student_id, course_id)

class ApprovalRequiredHandler(RegistrationHandler):
    '''handler for request to register for a course section that requires instructor approval'''
    registration_approval: IApprovalRequired = RegistrationApproval()
    def process_request(self, student_id, course_id):
        '''approval may be required when registering for a course section (approval not required for labs)'''

        if not self._db.is_course_section(course_id): # registration is not for a course section so approval not required
            return super().process_request(student_id, course_id)
        course_sec_result = self._db.get_course_section_info(course_section_id=course_id)
        base_course_id = course_sec_result['course_id']
        course_result = self._db.get_course_info(course_id=base_course_id)
        if course_result['approval_req']:
            self.registration_approval.ApprovalRequiredHandler(student_id, course_id)
            return

        return super().process_request(student_id, course_id)


class AddCourseHandler(RegistrationHandler):
    '''handler which updates the database with course registration for a student'''
    def process_request(self, student_id, course_id):
        self._db.register_course(student_id=student_id, course_id=course_id)
        if self._db.is_course_section(course_id):
            print("Successfully registered for the requested course section.")
        else:
            print("Successfully registered for the requested lab.")

        return super().process_request(student_id, course_id)

class AlreadyRegisteredHandler(RegistrationHandler):
    '''handler for request to register for a course section/lab for which the student is already registered for'''
    def process_request(self, student_id, course_id):
        reg_student_sec_result = self._db.get_all_registered_course_sections(student_id=student_id)
        reg_student_lab_result = self._db.get_all_registered_labs(student_id=student_id)
        for record in reg_student_sec_result + reg_student_lab_result:
            course_section_or_lab_id = record['course_section_id'] if record.get('course_section_id') is not None else record['lab_id']
            if course_section_or_lab_id == course_id:
                print(f"Cannot add because you are already registered for a course section or lab with id {course_section_or_lab_id}")
                return
        return super().process_request(student_id, course_id)


class ScheduleConflictHandler(RegistrationHandler):
    '''handler for request to register for a course section/lab which leads to schedule conflict'''
    schedule_conflict = ScheduleConflict()
    def process_request(self, student_id, course_id):
        course_section_or_lab_info = self._db.get_course_section_info(course_section_id=course_id) if self._db.is_course_section(id=course_id) \
                                     else self._db.get_lab_info(lab_id=course_id)
        all_registered_records = []
        for record in self._db.get_all_registered_course_sections(student_id=student_id) + self._db.get_all_registered_labs(student_id=student_id):
            course_section_or_lab_id = record['course_section_id'] if record.get('course_section_id') is not None else record['lab_id']
            if self._db.is_course_section(id=course_section_or_lab_id):
                all_registered_records.append(self._db.get_course_section_info(course_section_id=course_section_or_lab_id))
            else:
                all_registered_records.append(self._db.get_lab_info(lab_id=course_section_or_lab_id))

        all_conflicts = self.schedule_conflict.get_all_conflicts(
                                                                desired_course_or_lab=course_section_or_lab_info,
                                                                all_registered=all_registered_records
                                                                )
        if all_conflicts:
            print("Cannot register due to scheduling conflicts with the following courses:")
            print("")
            for conflicting_id in all_conflicts:
                if self._db.is_course_section(id=conflicting_id):
                    course_type = 'lecture'
                    course_name = self._db.get_course_name_from_section_id(course_section_id=conflicting_id)
                else:
                    course_type = 'lab'
                    course_name = self._db.get_course_name_from_lab_id(lab_id=conflicting_id)
                print(f"\033[1m\tCourse Name:\033[0m {course_name}")
                print(f"\033[1m\tType:\033[0m {course_type}")
                print("")
            return
        return super().process_request(student_id, course_id)
        