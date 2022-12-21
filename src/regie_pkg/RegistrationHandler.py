from abc import ABC, abstractmethod
from .RegistrationApproval import RegistrationApproval, IStudentOverload, IApprovalRequired
from .RegistrationAlternative import RegistrationAlternative
from .enrollable import Enrollable
from .mysql_db import MySQLDB
from .text_formatting import insert_newline, bold

class RegistrationHandler(ABC):
    '''Chain of Responsibility'''
    next_handler_obj = None
    _db = MySQLDB() # protected
    
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
        all_reg_sec_result: Enrollable = self._db.get_all_registered_course_sections(student_id=student_id)
        all_reg_lab_result: Enrollable = self._db.get_all_registered_labs(student_id=student_id) 
        for enrollable in all_reg_sec_result + all_reg_lab_result:
            if enrollable.id == course_id:
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
        course_section = self._db.get_course_section(course_section_id=course_id)
        lab = self._db.get_lab(lab_id=course_id)
        enrollable: Enrollable = course_section  if course_section is not None else lab
        if enrollable.curr_reg >= enrollable.max_reg:
            print("Courses section or lab is full. Cannot add.") 
            print("Pulling up alternative registration options...")
            print("")
            self.registration_alternative.find_alternatives(id=enrollable.id)
            return 
        return super().process_request(student_id, course_id) 

class StudentRestrictionsHandler(RegistrationHandler):
    '''handler for request to register for a course section/lab by a student with account restrictions'''
    def process_request(self, student_id, course_id):
        student = self._db.get_student(student_id=student_id)
        if student.restrictions is not None:
            print(f"Cannot add course because you have the following restriction(s): {student.restrictions}")
            return
        return super().process_request(student_id, course_id) 


class StudentOverloadHandler(RegistrationHandler):
    '''handler for request to register for a course section/lab that requires overloading approval'''
    registration_approval: IStudentOverload = RegistrationApproval() # helper for executing actions when overload approval is needed
    def process_request(self, student_id, course_id):
        student = self._db.get_student(student_id=student_id)
        all_reg_sec_result = self._db.get_all_registered_course_sections(student_id=student_id)
        if (student.status == 'full-time' and len(all_reg_sec_result) >= 3) or \
           (student.status == 'part-time' and len(all_reg_sec_result) >= 2):
            self.registration_approval.StudentOverloadHandler(student_id=student_id)
            return  
        else:
            return super().process_request(student_id, course_id)
        

class PrerequisiteNotMetHandler(RegistrationHandler):
    '''handler for request to register for a course section/lab for which the student does not have the prerequisites met'''
    def process_request(self, student_id, course_id):
        courses_taken = {course.id for course in self._db.get_completed_courses(student_id=student_id)}
        required_prereqs = {course.id for course in self._db.get_all_prereqs(id=student_id)}
        if len(courses_taken.intersection(required_prereqs)) < len(required_prereqs):
           insert_newline()
           print("Cannot add because you have not taken the prerequisites.")
           print("The following course(s) must be taken and completed before registering for the requested course:")
           for need_to_take_course_id in required_prereqs-courses_taken:
               course = self._db.get_course(course_id=need_to_take_course_id)
               print(bold("\tCourse Name: ") + f"{course.name}")
           return
        return super().process_request(student_id, course_id)

class ApprovalRequiredHandler(RegistrationHandler):
    '''handler for request to register for a course section that requires instructor approval'''
    registration_approval: IApprovalRequired = RegistrationApproval()
    def process_request(self, student_id, course_id):
        '''approval may be required when registering for a course section (approval not required for labs)'''

        if not self._db.is_course_section(course_id): # registration is not for a course section so approval not required
            return super().process_request(student_id, course_id)
        course_section = self._db.get_course_section(course_section_id=course_id)
        course = self._db.get_course(course_id=course_section.course_id)
        if course.approval_req:
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
        course_sections: Enrollable = self._db.get_all_registered_course_sections(student_id=student_id)
        labs: Enrollable = self._db.get_all_registered_labs(student_id=student_id)
        for enrollable in course_sections + labs:
            if enrollable.id == course_id:
                print(f"Cannot add because you are already registered for a course section or lab with id {enrollable.id}")
                return
        return super().process_request(student_id, course_id)


class ScheduleConflictHandler(RegistrationHandler):
    '''handler for request to register for a course section/lab which leads to schedule conflict'''
    def process_request(self, student_id, course_id):
        target_enrollment = self._db.get_course_section(course_section_id=course_id) if self._db.is_course_section(id=course_id) \
                                     else self._db.get_lab(lab_id=course_id)
        # all course sections and labs the student is enrolled in
        all_registered = self._db.get_all_registered_course_sections(student_id=student_id) + \
                         self._db.get_all_registered_labs(student_id=student_id)
        
        all_conflicts = []
        for enrollable in all_registered:
            if target_enrollment.schedule_conflict_with(enrollable):
                all_conflicts.append(enrollable)

        if all_conflicts:
            print("Cannot register due to scheduling conflicts with the following courses:")
            insert_newline()
            for enrollable in all_conflicts:
                print(bold("\tCourse Name: ") + enrollable.name)
                print(bold("\tType: ") + enrollable.course_type)
                insert_newline()
            return
        return super().process_request(student_id, course_id)
        