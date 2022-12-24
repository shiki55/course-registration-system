DROP TABLE IF EXISTS course_prerequisites;
DROP TABLE IF EXISTS registered_student_section;
DROP TABLE IF EXISTS registered_student_lab;
DROP TABLE IF EXISTS student_course_grade;
DROP TABLE IF EXISTS faculty_lab_section;
DROP TABLE IF EXISTS faculty_course_section;
DROP TABLE IF EXISTS course_section;
DROP TABLE IF EXISTS lab;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS faculty;
DROP TABLE IF EXISTS student;

CREATE TABLE student (
    student_id int,
    name varchar(100),
    status varchar(100),
    division varchar(100),
    department varchar(100),
    email varchar(100),
    major varchar(100),
    restriction varchar(100),
    PRIMARY KEY (student_id)
);

CREATE TABLE faculty (
    faculty_id int,
    name varchar(100),
    status varchar(100),
    email varchar(100),
    title varchar(50),
    PRIMARY KEY (faculty_id)
);

CREATE TABLE course (
    course_id int(8),
    name varchar(100),
    approval_req boolean,
    faculty_id int,
    course_desc varchar(500),
    subject varchar(100),
    division varchar(100),
    PRIMARY KEY (course_id)
);

CREATE TABLE lab (
    lab_id int(8),
    max_reg int,
    curr_reg int,
    days_of_week varchar(50),
    start_time varchar(50),
    end_time varchar(50),
    location varchar(50),
    year int,
    quarter varchar(20),
    course_id int(8),
    PRIMARY KEY (lab_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE course_section (
    course_section_id int(8),
    max_reg int,
    curr_reg int,
    days_of_week varchar(50),
    start_time varchar(50),
    end_time varchar(50),
    location varchar(50),
    year int,
    quarter varchar(20),
    course_id int(8),
    PRIMARY KEY (course_section_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE faculty_course_section (
    faculty_id  int,
    course_section_id int(8),
    PRIMARY KEY (faculty_id, course_section_id),
    FOREIGN KEY (course_section_id) REFERENCES course_section(course_section_id),
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
);

CREATE TABLE faculty_lab_section (
    faculty_id  int,
    lab_id int(8),
    PRIMARY KEY (faculty_id, lab_id),
    FOREIGN KEY (lab_id) REFERENCES lab(lab_id),
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
);

CREATE TABLE student_course_grade (
    student_course_grade_id int,
    grade ENUM('A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'D', 'F'),
    year int,
    quarter varchar(20),
    student_id int,
    course_id int(8),
    PRIMARY KEY (student_course_grade_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE registered_student_lab (
    lab_id int(8),
    student_id int,
    PRIMARY KEY (lab_id, student_id),
    FOREIGN KEY (lab_id) REFERENCES lab(lab_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id)
);

CREATE TABLE registered_student_section (
    course_section_id int(8),
    student_id int,
    reg_status ENUM('registered', 'awaiting approval'),
    PRIMARY KEY (course_section_id, student_id),
    FOREIGN KEY (course_section_id) REFERENCES course_section(course_section_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id)
);

CREATE TABLE course_prerequisites (
    course_id int(8),
    course_id_prereq int(8),
    PRIMARY KEY (course_id, course_id_prereq),
    FOREIGN KEY (course_id) REFERENCES course(course_id),
    FOREIGN KEY (course_id_prereq) REFERENCES course(course_id)
);










