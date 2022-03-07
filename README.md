# REGIE Course Registration System
Using Python Version 3.9.10, pymongo version 4.0.1, mysql-connector-python 8.0.28



# A CLI app mock-up of a course registration system
**Project Scope**: My project focused on implementing student usecases to handle the following actions:
1. course/lab registration (add course, drop course, drop all course)
    - a series of seven validations are performed before the database is updated with the requested course registration. This includes checking if the student has met the prerequisite requirements, ensuring the course enrollment is not full, and more. Each validation step has it's own implementation for what occurs when it is not met. For example, if the course enrollment is already at full capacity, the user will be presented with alternative sections of the same course/lab. Details can be found in the "CourseRegistration.py" file under the regie_pkg directory. 
2. student views (currently registered courses, course schedule, transcript, and account restrictions)
    
3. change password 

### Setting up the database (MySQL and MongoDB)
- The MySQL connection configration has the following settings:
>host="localhost",\
 user="root",\
 passwd="123abc$$$",\
>database="REGIE_db"

\*  Please change the passwd constant to match whatever password is used for your MySQL instance by going to "MySQLConnect.py" and "build_mysql_db.py". Other parameters may need to be changed depending on your local MySQL set up. 
- cd into the "src" directory and run the python script "build_mysql_db.py". This will create the MySQL database REGIE_db and populate it with pre-existing data which can be found in the file "populate.sql". 
- cd into the src directory and run the python script "build_mongo_db.py". This will create the mongodb database password_db and populate it with pre-existing data which can be found in the script "build_mongo_db.py" itself. Mongodb is used to store account passwords.

### Dropping all databases (MySQL and MongoDB)
- cd into the src directory and run "drop_all_db.py"

### How to start the program
- cd into the src directory and run "main.py". This is the entry point of the program. 


### How to use the app
- login using the student id and password of any of the student account below:
    - "Volodymyr Zelenskyy" (recommended because it has most data populated)
        - student id: 1
        - password: pass123
    - "Floyd Mayweather" (has student account restriction for "tuition not paid" so cannot register)
        - student id: 2
        - password: pass123
    - "Ketanji Jackson" 
        - student id: 3
        - password: pass123

- Some sample course sections and labs for manual testing
    - "Introduction to Discrete Math"
        - section id: 11111113
        - section id: 21111112 (full enrollment, cannot register)
        - lab id: 99999999

    - "English Grammar and Syntax"
        - section id: 11111114

    - "Databases" (has prerequisite requirement to complete 'Introduction to Computer Systems')
        - section id: 11111116
        \*login as "Ketanji Jackson" to test the prerequisite check

    - "Distributed Systems" (has instructor approval required)
        - section id: 11111117


### Design Patterns Used
- **Chain of Responsibility:** 
    - The validation handlers for the course registration actions (add and drop course) are implemented using this design pattern. This allows validations to be easily added or removed. It also allows the sender (CourseRegistration class) of the request to add/drop course without knowing which specific handler will handle the request. (see "CourseRegistration.py", "RegistrationHandler.py")
- **Facade Design Pattern:** 
    - The CourseRegistration class encapsulates the complexities of chaining together the various handler classes necessary to perform registration actions and provides simple interfaces that clients can use to execute the desired course registation operation. (see "CourseRegistration.py") 
- **Strategy Design Pattern:** 
    - The NotificationService class which is responsible for sending notifcations/messages to various individuals is implemented using the strategy design pattern. The NotificationService has a reference to an object which implements the NotificationStrategy interface which allows new notification strategies (ie text message, etc) to be easily added without changing NotificationService itself. (see "NotificationService.py", "Email.py") 
    - All student views (account restrictions, transcripts, etc) are implemented using the strategy design pattern. The Student class's view method takes in an object that implements the StudentView interface and displays different views depending on the object (or view strategy) that was passed in as an argument. This implementation ensures that new views can be added very easily without requiring any modifications to the Student class. (see "StudentView.py", "Student.py")
- **Factory Design Pattern:** 
    - The REGIEPersonFactory is a factory which encapsulates the creation and initialization of all objects which subclass from REGIEPersonFactory. If this project is extended to include Faculty and Admin usecases, the REGIEPersonFactory can easily be extended to accomodate the creation of those classes as well. (see "REGIEPersonFactory.py")




### S.O.L.I.D. Principles
- **Single Responsibility:**
    - Each of the classes I've written are responsible for one job, and it's job (for the most part) can be understood by the class name. 
- **Open/Closed:**
    - A clear example of this in my code is how I implemented the student views. Student views can be extended without modifying the Student class itself. Also, the notification service is implemented to allow for different ways to send notifications (for example text messages) without modifying the NotificationService class. 
- **Liskov Substitution Principle:**
    - I relied heavily on using abstract classes and interfaces in order to ensure that subclasses are forced to respect the "contract" of methods set by the abstract parent class or interface. This ensures subclasses inheriting from the same abstract parent class or implementing the same interface to be interchangeable with each other because there is a guarantee regarding what methods are defined for each subclass based on the abstract parent class or interface that they inherit from or implement. 
    - Also, none of my concrete classes have methods which have an empty implementation just to satisfy some interface or abstract class.
    - The most basic definition of this principle which is "objects of a superclass shall be replaceable with objects of its subclasses without breaking the application" does not really apply to my design because none of the classes inherit from concrete classes. This was a deliberate design decision to favor composition over inheritance. 
- **Interface Segregation Principle:**
    - The add course validation handlers ApprovalRequiredHandler and StudentOverloadHandler require different implementations for when approval is required (because the approval procedures for when a student is trying to overload their course registration is different from when trying to register for an "approval required" course). To handle this I defined a RegistrationApproval class which implements interfaces which are tailored to ApprovalRequiredHandler and StudentOverloadHandler, individually. This ensures that only the methods needed by each client are exposed (can't really implement this in Python, but I used type hints to make it clear what I'm trying to convey). 
    - If Python was a statically-typed language I would have designed my classes to follow this principle more closely. Just as an example, in a statically-typed language I would've defined interfaces for client classes using methods of the DB class. 
- **Dependency Inversion Principle:** 
    - This principle which is based on the idea that the dependency of high-level modules/classes on low-level modules/classes should be inverted follows naturally from the open/closed principles and implementation of the strategy design pattern. In both cases, the high-level class is dependent on an abstraction instead of a concrete class, and the low-level class is dependent on the same abstraction. 