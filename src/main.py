import shutil
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
from time import sleep

def login() -> Student:
    auth = UserAuthenticator()
    person_factory = REGIEPersonFactory()
    while True:
        try:
            student_id_input = int(input("Enter student id: "))
        except ValueError:
            print("student id must be an integer. Please try again.")
            print("")
            continue
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
        print("")
        try: 
            user_choice = int(input("Enter choice by number: "))
            print("")
        except ValueError:
            print("Entered choice must be an integer. Please try again.")
            print("")
            continue
        if user_choice == 1:
            student.view(view_trans)
        elif user_choice == 2:
            student.view(view_restrictions)
        elif user_choice == 3:
            student.view(view_sched)
        elif user_choice == 4:
            course_id = int(input("Enter the eight digit course section/lab id: "))
            course_reg.add_course(student_id=student.id, course_id=course_id)
        elif user_choice == 5:
            course_id = int(input("Enter the eight digit course section/lab id: "))
            course_reg.drop_course(student_id=student.id, course_id=course_id)
        elif user_choice == 6:
            course_reg.drop_all(student_id=student.id)
        elif user_choice == 7:
            student._change_password()
        else:
            print("Invalid choice, try again.")
        print("")
        input("\033[1mHit Enter to go back to Menu options\033[0m")
        print("")



if __name__ == '__main__':
    main()
