from .DB import DB
from .RegistrationHandler import (
                                NotRegisteredHandler, 
                                DropCourseHandler,
                                AlreadyRegisteredHandler,
                                CourseDoesNotExistHandler,
                                ClosedCourseHandler,
                                StudentRestrictionsHandler,
                                StudentOverloadHandler,
                                PrerequisiteNotMetHandler,
                                ApprovalRequiredHandler,
                                AddCourseHandler,
                                ScheduleConflictHandler,
                                )


class CourseRegistration:
    '''facade design pattern: interface for all course registration actions'''
    def __init__(self):
        self._drop_course_chain = self.__create_chain(NotRegisteredHandler(), DropCourseHandler())
        self._add_course_chain = self.__create_chain(
                                                    CourseDoesNotExistHandler(),
                                                    AlreadyRegisteredHandler(),
                                                    ClosedCourseHandler(),
                                                    StudentRestrictionsHandler(),
                                                    StudentOverloadHandler(),
                                                    PrerequisiteNotMetHandler(),
                                                    ApprovalRequiredHandler(),
                                                    ScheduleConflictHandler(),
                                                    AddCourseHandler(),
                                                )
        self.__db = DB()
    
    def add_course(self, student_id, course_id):
        '''
        chain of responsibility design pattern

        1. check if course exists
        2. check if student is already registered
        3. check if course is closed/full
        4. check student account restrictions
        5. check if student is overloading
        6. check if student has met prerequisites
        7. check if course requires instructor approval
        8. check if registering for course results in schedule conflict
        9. update database w/ student registration

        NOTE: course_id is either course_section_id (id of course section) or lab_id (id of lab)
        '''
        
        self._add_course_chain.process_request(student_id=student_id, course_id=course_id)
        return 
    
    def drop_course(self, student_id, course_id):
        '''
        chain of responsibility design pattern
        
        1. check if student is registered for the course
        2. drop course
        '''

        self._drop_course_chain.process_request(student_id=student_id, course_id=course_id)
        return 


    def drop_all(self, student_id):
        '''drop all course section/lab registrations'''

        all_reg_course_sec = self.__db.get_all_registered_course_sections(student_id=student_id)
        all_reg_lab = self.__db.get_all_registered_labs(student_id=student_id)
        for record in all_reg_course_sec + all_reg_lab:
            id_to_drop = record['course_section_id'] if record.get('course_section_id') is not None else record['lab_id']
            self.__db.unregister_course(student_id=student_id, course_id=id_to_drop)
        print("Dropped all courses")
        return 
    
    @staticmethod
    def __create_chain(*args):
        '''building the chain of handlers where the first handler
           passed in becomes the first handler of the request in the chain
           and the last handler passed in becomes the last handler in the chain'''
           
        first_handler = args[0]
        prev_handler = first_handler
        for handler in args[1:]:
            prev_handler.set_next(handler)
            prev_handler = handler
        return first_handler