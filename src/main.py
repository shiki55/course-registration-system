import shutil
from time import sleep
from regie_pkg.UserAuthenticator import UserAuthenticator
from regie_pkg.REGIEPersonFactory import REGIEPersonFactory
from regie_pkg.Student import Student
from regie_pkg.StudentView import (
                                    ViewRegisteredCourses, 
                                    ViewRestrictions, 
                                    ViewTranscript, 
                                    ViewSchedule,
                                    )
from regie_pkg.CourseRegistration import CourseRegistration
from regie_pkg.InputValidator import (
                                        StudentIDInputValidator,
                                        MenuChoiceInputValidator,
                                        ValidationExecutor,
                                        CouseIDInputValidator,
                                     )


def login() -> Student:
    auth = UserAuthenticator()
    person_factory = REGIEPersonFactory()
    validation_executor = ValidationExecutor(input_validator=StudentIDInputValidator())
    while True:
        student_id_input = input("Enter student id: ")
        err_msg, valid_input = validation_executor.validate(input_val=student_id_input)
        if not valid_input:
            print(err_msg)
            print("")
            continue
        student_id_input = int(student_id_input)
        password_input = input("Enter password: ")
        account_type = 'student'
        if auth.authenticate(id=student_id_input, password=password_input, account_type=account_type):
            print("Login credentials authenticated.")
            print("")
            return person_factory.get_person(id=student_id_input, account_type=account_type)
        else: 
            print("Wrong student id or password. Try again.")
            print("")


def main():
    view_reg_courses = ViewRegisteredCourses()
    view_restrictions = ViewRestrictions()
    view_trans = ViewTranscript()
    view_sched = ViewSchedule()
    course_reg = CourseRegistration()
    course_id_input_validator = CouseIDInputValidator()
    menu_choice_input_validator = MenuChoiceInputValidator()
    validation_executor = ValidationExecutor()
    while True:
        student: Student = login()
        print("\033[1mWelcome to your REGIE account!\033[0m".center(shutil.get_terminal_size().columns))
        while True:
            student.view(view_reg_courses)
            print('---------------------------')
            print("\033[1mMenu options:\033[0m")
            print("\t1. View My Academic Transcript")
            print("\t2. View My Account Restrictions")
            print("\t3. View My Course Schedule")
            print("\t4. Add Course Section/Lab")
            print("\t5. Remove Course Section/Lab")
            print("\t6. Remove All Course Section/Lab")
            print("\t7. Change Password")
            print("\t8. Log Out")
            print("")
            user_choice = input("Enter choice by number: ")
            validation_executor.set_validator(input_validator=menu_choice_input_validator)
            err_msg, valid_input = validation_executor.validate(input_val=user_choice)
            if not valid_input:
                print(err_msg)
                print("")
                input("\033[1mHit Enter to go back to Menu options\033[0m")
                continue
            print("")
            user_choice = int(user_choice)
            if user_choice == 1:
                student.view(view_trans)
            elif user_choice == 2:
                student.view(view_restrictions)
            elif user_choice == 3:
                student.view(view_sched)
            elif user_choice == 4:
                course_id = input("Enter the eight digit course section/lab id: ")
                validation_executor.set_validator(input_validator=course_id_input_validator)
                err_msg, valid_input = validation_executor.validate(input_val=course_id)
                if not valid_input:
                    print(err_msg)
                    print("")
                    input("\033[1mHit Enter to go back to Menu options\033[0m")
                    continue
                course_reg.add_course(student_id=student.id, course_id=int(course_id))
            elif user_choice == 5:
                course_id = input("Enter the eight digit course section/lab id: ")
                validation_executor.set_validator(input_validator=course_id_input_validator)
                err_msg, valid_input = validation_executor.validate(input_val=course_id)
                if not valid_input:
                    print(err_msg)
                    print("")
                    input("\033[1mHit Enter to go back to Menu options\033[0m")
                    continue
                course_reg.drop_course(student_id=student.id, course_id=int(course_id))
            elif user_choice == 6:
                course_reg.drop_all(student_id=student.id)
            elif user_choice == 7:
                student.change_password()
            elif user_choice == 8:
                print("Logging off")
                for _ in range(3):
                    print("")
                    sleep(0.75)
                break
        
            print("")
            input("\033[1mHit Enter to go back to Menu options\033[0m")
            print("")



if __name__ == '__main__':
    main()
