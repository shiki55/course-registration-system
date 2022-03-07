from .DB import DB

class RegistrationAlternative:
    '''class which finds alternative registration options and displays them'''

    __db = DB()
    __days_of_week_order = {
                'mon': 1,
                'tues': 2,
                'wed': 3,
                'thurs': 4,
                'fri': 5,
                'sat': 6,
                'sun': 7,
                }
    def find_alternatives(self, id):
        '''finds alternative course section/lab registration options'''
        
        if self.__db.is_course_section(id):
            course_info = self.__db.get_course_info_from_section_id(id)
            query_result = self.__db.get_all_course_sections(course_id=course_info['course_id'])
            id_name = 'course_section_id'
        else:
            course_info = self.__db.get_course_info_from_lab_id(id)
            query_result = self.__db.get_all_labs(course_id=course_info['course_id'])
            id_name = 'lab_id'

        alternatives = [] # alternative course sections or labs
        for record in query_result: 
            if record[id_name] != id: # only including alternative course sections or labs
                alternatives.append(record)
        if not alternatives:
            print("No alternative course sections or labs available.")
            print("")
            return 
        
        alternatives.sort(key=self.__compare) # sort alternatives
        self.__display_alternatives(alternatives)
        return

    def __compare(self, record):
            '''custom sorting function for sorting the list of alternatives
               based on the day of the week'''

            start_day_of_week = record['days_of_week'].split(',')[0].strip().lower() # first day of the week that this course section/lab is offered
            day_of_week_num = self.__days_of_week_order[start_day_of_week]
            return day_of_week_num

    def __display_alternatives(self, alternatives):
        '''displaying the alternative options'''

        print("\033[4m\033[1mAlternative Course Section/Lab Offerings:\033[0m")
        for record in alternatives:
            print(f"\tID: {record.get('course_section_id', record.get('lab_id'))}")
            print(f"\tDays of Week: {record['days_of_week']}")
            print(f"\tStart Time: {record['start_time']}")
            print(f"\tEnd Time: {record['end_time']}")
            print(f"\tLocation: {record['location']}")
            print(f"\tTotal Enrollment: {record['curr_reg']}/{record['max_reg']}")
            print("")
    