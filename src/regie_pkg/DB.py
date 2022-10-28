from .Faculty import Faculty
from .MySQLConnect import MySQLConnect
from .Student import Student
from typing import List, Set, Dict


class DB:
    '''This class serves as the interface to communicate with the MySQL database.
       The methods in this class create domain layer objects or updates the database.
    '''

    __my_sql_connect = MySQLConnect()

    def get_student(self, student_id) -> Student: 
        student_result = self.__my_sql_connect.execute_query(
                        f'''SELECT * FROM student WHERE student_id = {student_id};'''
                        )
        return Student(
                name=student_result[0]['name'], 
                status=student_result[0]['status'], 
                department=student_result[0]['department'], 
                division=student_result[0]['division'], 
                email=student_result[0]['email'], 
                id=student_result[0]['student_id'], 
                major=student_result[0]['major'],
                restrictions=student_result[0]['restriction'],
            )

    def get_faculty(self, faculty_id) -> Faculty: 
        faculty_result = self.__my_sql_connect.execute_query(
                        f'''SELECT * FROM faculty WHERE faculty_id = {faculty_id};'''
                        )
        return Faculty(
                name=faculty_result[0]['name'], 
                status=faculty_result[0]['status'],
                email=faculty_result[0]['email'], 
                id=faculty_result[0]['faculty_id'],
                title=faculty_result[0]['title'],
            )

    def get_lab_info(self, lab_id) -> Dict:
        lab_result = self.__my_sql_connect.execute_query(
                        f'''SELECT * FROM lab WHERE lab_id = {lab_id};'''
                        )
        if lab_result:
            return lab_result[0]
        return None

    def get_course_section_info(self, course_section_id) -> Dict:
        course_section_result = self.__my_sql_connect.execute_query(
                        f'''SELECT * FROM course_section WHERE course_section_id = {course_section_id};'''
                        )
        if course_section_result:
            return course_section_result[0]
        return None

    def get_course_info(self, course_id) -> Dict:
        course_result = self.__my_sql_connect.execute_query(
                        f'''SELECT * FROM course WHERE course_id = {course_id};'''
                        )
        if course_result:
            return course_result[0]
        return None
    
    def get_all_registered_course_sections(self, student_id) -> List[Dict]:
        registered_course_sections_result = self.__my_sql_connect.execute_query(
                        f'''SELECT * FROM registered_student_section WHERE student_id = {student_id} AND reg_status = 'registered'; '''
                        )
        return registered_course_sections_result

    def get_all_pending_registrations(self, student_id) -> List[Dict]:
        pending_registrations_result = self.__my_sql_connect.execute_query(
                        f'''SELECT * FROM registered_student_section WHERE student_id = {student_id} AND reg_status = 'awaiting approval'; '''
                        )
        return pending_registrations_result
    
    def get_all_registered_labs(self, student_id) -> List[Dict]:
        registered_lab_result = self.__my_sql_connect.execute_query(
                        f'''SELECT * FROM registered_student_lab WHERE student_id = {student_id};'''
                        )
        return registered_lab_result
    
    def is_lab(self, id) -> bool:
        lab_result = self.__my_sql_connect.execute_query(
                f'''SELECT * FROM lab WHERE lab_id = {id};'''
                )
        if lab_result:
            return True
        return False

    def is_course_section(self, id) -> bool:
        course_section_result = self.__my_sql_connect.execute_query(
                f'''SELECT * FROM course_section WHERE course_section_id = {id};'''
                )
        if course_section_result:
            return True
        return False

    def unregister_course(self, student_id, course_id) -> None:
        if self.is_course_section(course_id): # unregistering course section
            self.__my_sql_connect.execute_query(
                                    f'''DELETE FROM registered_student_section WHERE student_id = {student_id}
                                    AND course_section_id = {course_id}
                                    ''',
                                    commit=True
                                    )
            self.__my_sql_connect.execute_query(f'''UPDATE course_section SET curr_reg = curr_reg - 1 WHERE course_section_id = {course_id};''', commit=True)
        else: # unregistering lab
            self.__my_sql_connect.execute_query(
                                    f'''DELETE FROM registered_student_lab WHERE student_id = {student_id}
                                    AND lab_id = {course_id}
                                    ''',
                                    commit=True
                                    )
            self.__my_sql_connect.execute_query(f'''UPDATE lab SET curr_reg = curr_reg - 1 WHERE lab_id = {course_id};''', commit=True)

        return 
    
    def register_course(self, student_id, course_id) -> None:
        '''insert and update the database with new course registration'''
        if self.is_course_section(course_id): # course section registration
            self.__my_sql_connect.execute_query(f'''INSERT INTO registered_student_section (course_section_id, student_id, reg_status) VALUES ({course_id}, {student_id}, 'registered');''', commit=True)
            self.__my_sql_connect.execute_query(f'''UPDATE course_section SET curr_reg = curr_reg + 1 WHERE course_section_id = {course_id};''', commit=True)
        else: # lab registration
            self.__my_sql_connect.execute_query(f'''INSERT INTO registered_student_lab (lab_id, student_id) VALUES ({course_id}, {student_id});''', commit=True)
            self.__my_sql_connect.execute_query(f'''UPDATE lab SET curr_reg = curr_reg + 1 WHERE lab_id = {course_id};''', commit=True)

    def get_all_completed_courses(self, student_id) -> List[Dict]:
        completed_courses_result = self.__my_sql_connect.execute_query(
                f'''SELECT * FROM student_course_grade WHERE student_id = {student_id}'''
                )
        return completed_courses_result

    def get_all_prereqs(self, id) -> List[int]:
        '''input argument id can be course_id, course_section_id, lab_id
           return a list of course_id pre-reqs'''
        if self.is_course_section(id):
            res = self.get_course_section_info(id)
            id = res['course_id'] # base course id
        elif self.is_lab(id): # id is lab
            res = self.get_lab_info(id)
            id = res['course_id'] # base course id
        
        required_prereqs = self.__my_sql_connect.execute_query(
                         f'''SELECT course_id_prereq FROM course_prerequisites WHERE course_id = {id}'''
                        )

        return [record['course_id_prereq'] for record in required_prereqs]

    def get_all_instructors_of_course(self, id) -> List[int]:
        if self.is_course_section(id=id):
            faculty_id_res = self.__my_sql_connect.execute_query(
                           f'''SELECT faculty_id FROM faculty_course_section WHERE course_section_id = {id}'''
                        )
        else:
            faculty_id_res = self.__my_sql_connect.execute_query(
                           f'''SELECT faculty_id FROM faculty_lab_section WHERE lab_id = {id}'''
                        )
        return [record['faculty_id'] for record in faculty_id_res]

    def get_course_info_from_section_id(self, course_section_id) -> Dict:
        res = self.__my_sql_connect.execute_query(
                        f'''SELECT c.*
                            FROM course_section cs 
                            INNER JOIN course c ON cs.course_id = c.course_id
                            WHERE cs.course_section_id = {course_section_id}'''
                    )
        if res:
            return res[0]
        return None

    def get_course_info_from_lab_id(self, lab_id) -> Dict:
        res = self.__my_sql_connect.execute_query(
                        f'''SELECT c.*
                            FROM lab l 
                            INNER JOIN course c ON l.course_id = c.course_id
                            WHERE l.lab_id = {lab_id}'''
                    )
        if res:
            return res[0]
        return None
    
    def get_course_name_from_section_id(self, course_section_id) -> str:
        course_info = self.get_course_info_from_section_id(course_section_id=course_section_id)
        return course_info['name']
    
    def get_course_name_from_lab_id(self, lab_id) -> str:
        course_info = self.get_course_info_from_lab_id(lab_id=lab_id)
        return course_info['name']

    def get_all_course_sections(self, course_id) -> list[dict]:
        course_sections_result = self.__my_sql_connect.execute_query(f'''SELECT * FROM course_section WHERE course_id = {course_id};''')
        return course_sections_result

    def get_all_labs(self, course_id) -> list[dict]:
        labs_result = self.__my_sql_connect.execute_query(f'''SELECT * FROM lab WHERE course_id = {course_id};''')
        return labs_result