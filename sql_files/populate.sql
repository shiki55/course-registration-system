

INSERT INTO student (student_id, name, status, division, department, email, major, restriction) VALUES (1, 'Volodymyr Zelenskyy', 'full-time', 'Division of Physical Sciences', 'Department of Physics', 'zelenskyy@uchicago.edu', 'Physics', null);
INSERT INTO student (student_id, name, status, division, department, email, major, restriction) VALUES (2, 'Floyd Mayweather', 'full-time', 'Division of Humanities', 'Department of English Language and Literature', 'mayweather@uchicago.edu', 'English', 'tuition not paid');
INSERT INTO student (student_id, name, status, division, department, email, major, restriction) VALUES (3, 'Ketanji Jackson', 'full-time', 'Division of Physical Sciences', 'Department of Physics', 'jackson@uchicago.edu', 'Physics', null);

INSERT INTO faculty (faculty_id, name, status, email, title) VALUES (1, 'Jamie Boyer', 'full-time', 'boyer@uchicago.edu', 'Professor');
INSERT INTO faculty (faculty_id, name, status, email, title) VALUES (2, 'Sarah Johnson', 'full-time', 'johnson@uchicago.edu', 'Professor');
INSERT INTO faculty (faculty_id, name, status, email, title) VALUES (3, 'Katie Smith', 'part-time', 'ksmith@uchicago.edu', 'Teaching Assistant');

INSERT INTO course (course_id, name, approval_req, faculty_id, course_desc, subject, division) VALUES (11111111, 'Introduction to Discrete Math', 0, 1, 'We will be learning about the fundamentals of discrete math needed for computer science.', 'Math', 'Division of Physical Sciences');
INSERT INTO course (course_id, name, approval_req, faculty_id, course_desc, subject, division) VALUES (22222222, 'English Grammar and Syntax', 0, 2, 'This course is about grammar and syntax and will invlove a lot of writing.', 'English', 'Department of English Language and Literature');
INSERT INTO course (course_id, name, approval_req, faculty_id, course_desc, subject, division) VALUES (33333333, 'Introduction to Computer Systems', 0, 1, 'All about computers and how they work.', 'Computer Science', 'Division of Physical Sciences');
INSERT INTO course (course_id, name, approval_req, faculty_id, course_desc, subject, division) VALUES (44444444, 'Databases', 0, 1, 'This course will teach you everything you need to know about databases.', 'Computer Science', 'Division of Physical Sciences');
INSERT INTO course (course_id, name, approval_req, faculty_id, course_desc, subject, division) VALUES (14444444, 'Distributed Systems', 1, 1, 'This course focuses on the theory and practice of distributed systems.', 'Computer Science', 'Division of Physical Sciences');
INSERT INTO course (course_id, name, approval_req, faculty_id, course_desc, subject, division) VALUES (24444444, 'Cloud Computing', 0, 1, 'This course provides an introduction to cloud computing with specific consideration for development of highly scalable (or so-called “web-scale”) web applications that leverage cloud infrastructure and platform services (IaaS and PaaS).', 'Computer Science', 'Division of Physical Sciences');
INSERT INTO course (course_id, name, approval_req, faculty_id, course_desc, subject, division) VALUES (34444444, 'Algorithms', 0, 2, 'This course will teach you everything you need to know about algorithms.', 'Computer Science', 'Division of Physical Sciences');
INSERT INTO course (course_id, name, approval_req, faculty_id, course_desc, subject, division) VALUES (54444444, 'Functional Programming', 0, 2, 'This course will teach you everything you need to know about functional programming.', 'Computer Science', 'Division of Physical Sciences');
INSERT INTO course (course_id, name, approval_req, faculty_id, course_desc, subject, division) VALUES (54444445, 'C++ for Advanced Programmers', 0, 1, 'This course is meant for student with prior experience with C++', 'Computer Science', 'Division of Physical Sciences');

INSERT INTO course (course_id, name, approval_req, faculty_id, course_desc, subject, division) VALUES (12345670, 'iOS Application Development', 0, 1, 'Fun times with ios dev', 'Computer Science', 'Division of Physical Sciences');
INSERT INTO course (course_id, name, approval_req, faculty_id, course_desc, subject, division) VALUES (13345670, 'Applied Data Analysis', 1, 1, 'How to become a Palantirian', 'Computer Science', 'Division of Physical Sciences');
INSERT INTO course (course_id, name, approval_req, faculty_id, course_desc, subject, division) VALUES (13445670, 'Parallel Programming', 0, 1, 'All things parallel', 'Computer Science', 'Division of Physical Sciences');
INSERT INTO course (course_id, name, approval_req, faculty_id, course_desc, subject, division) VALUES (34444449, 'Machine Learning', 0, 1, 'How to build our successors', 'Computer Science', 'Division of Physical Sciences');
INSERT INTO course (course_id, name, approval_req, faculty_id, course_desc, subject, division) VALUES (54444414, 'Introduction to Scientific Computing', 0, 1, 'How to compute...scientifically :)', 'Computer Science', 'Division of Physical Sciences');
INSERT INTO course (course_id, name, approval_req, faculty_id, course_desc, subject, division) VALUES (59444445, 'OO Architecture: Patterns, Technologies, Implementations', 0, 1, 'Introduction to design and architectural patterns', 'Computer Science', 'Division of Physical Sciences');


INSERT INTO lab (lab_id, max_reg, curr_reg, days_of_week, start_time, end_time, location, year, quarter, course_id) VALUES (99999999, 20, 14, 'Tues', '5:00 PM', '6:00 PM', 'Ryerson Laboratory, Room 217', 2022, 'winter', 11111111);

INSERT INTO course_section (course_section_id, max_reg, curr_reg, days_of_week, start_time, end_time, location, year, quarter, course_id) VALUES (11111112, 60, 50, 'Mon, Wed, Fri', '9:00 AM', '10:30 AM', 'John Crerar Library, Room 320', 2022, 'winter', 11111111);
INSERT INTO course_section (course_section_id, max_reg, curr_reg, days_of_week, start_time, end_time, location, year, quarter, course_id) VALUES (11111113, 60, 20, 'Mon, Wed, Fri', '11:00 AM', '12:00 PM', 'John Crerar Library, Room 320', 2022, 'winter', 11111111);
INSERT INTO course_section (course_section_id, max_reg, curr_reg, days_of_week, start_time, end_time, location, year, quarter, course_id) VALUES (21111112, 60, 60, 'Mon, Thurs', '12:15 PM', '2:00 PM', 'John Crerar Library, Room 320', 2022, 'winter', 11111111);
INSERT INTO course_section (course_section_id, max_reg, curr_reg, days_of_week, start_time, end_time, location, year, quarter, course_id) VALUES (11111114, 40, 10, 'Tues, Wed', '2:10 PM', '3:30 PM', 'John Crerar Library, Room 110', 2022, 'winter', 22222222);
INSERT INTO course_section (course_section_id, max_reg, curr_reg, days_of_week, start_time, end_time, location, year, quarter, course_id) VALUES (11111115, 40, 25, 'Mon, Wed', '3:45 PM', '4:45 PM', 'John Crerar Library, Room 321', 2022, 'winter', 33333333);
INSERT INTO course_section (course_section_id, max_reg, curr_reg, days_of_week, start_time, end_time, location, year, quarter, course_id) VALUES (11111116, 30, 23, 'Mon, Fri', '5:15 PM', '6:30 PM', 'John Crerar Library, Room 112', 2022, 'winter', 44444444);

INSERT INTO course_section (course_section_id, max_reg, curr_reg, days_of_week, start_time, end_time, location, year, quarter, course_id) VALUES (11111117, 30, 25, 'Mon, Tues', '6:45 PM', '7:45 PM', 'John Crerar Library, Room 111', 2022, 'winter', 14444444);
INSERT INTO course_section (course_section_id, max_reg, curr_reg, days_of_week, start_time, end_time, location, year, quarter, course_id) VALUES (11111118, 30, 21, 'Wed, Fri', '8:00 PM', '9:30 PM', 'John Crerar Library, Room 112', 2022, 'winter', 24444444);
INSERT INTO course_section (course_section_id, max_reg, curr_reg, days_of_week, start_time, end_time, location, year, quarter, course_id) VALUES (11111119, 30, 21, 'Wed, Fri', '5:00 PM', '7:30 PM', 'John Crerar Library, Room 303', 2022, 'winter', 34444444);
INSERT INTO course_section (course_section_id, max_reg, curr_reg, days_of_week, start_time, end_time, location, year, quarter, course_id) VALUES (11111121, 30, 21, 'Wed, Thurs', '8:00 PM', '9:30 PM', 'John Crerar Library, Room 403', 2022, 'winter', 54444444);
INSERT INTO course_section (course_section_id, max_reg, curr_reg, days_of_week, start_time, end_time, location, year, quarter, course_id) VALUES (11111129, 30, 21, 'Mon, Wed, Thurs', '11:00 AM', '6:30 PM', 'John Crerar Library, Room 401', 2022, 'winter', 54444445);


INSERT INTO faculty_course_section (faculty_id, course_section_id) VALUES (1, 11111112);
INSERT INTO faculty_course_section (faculty_id, course_section_id) VALUES (1, 11111113);
INSERT INTO faculty_course_section (faculty_id, course_section_id) VALUES (1, 11111114);
INSERT INTO faculty_course_section (faculty_id, course_section_id) VALUES (1, 21111112);
INSERT INTO faculty_course_section (faculty_id, course_section_id) VALUES (1, 11111115);
INSERT INTO faculty_course_section (faculty_id, course_section_id) VALUES (1, 11111116);
INSERT INTO faculty_course_section (faculty_id, course_section_id) VALUES (1, 11111117);
INSERT INTO faculty_course_section (faculty_id, course_section_id) VALUES (1, 11111118);
INSERT INTO faculty_course_section (faculty_id, course_section_id) VALUES (1, 11111129);
INSERT INTO faculty_course_section (faculty_id, course_section_id) VALUES (2, 11111119);
INSERT INTO faculty_course_section (faculty_id, course_section_id) VALUES (2, 11111121);



INSERT INTO faculty_lab_section (faculty_id, lab_id) VALUES (3, 99999999);


INSERT INTO student_course_grade (student_course_grade_id, grade, year, quarter, student_id, course_id) VALUES (1, 'A',  2021, 'autumn',  1,  44444444);
INSERT INTO student_course_grade (student_course_grade_id, grade, year, quarter, student_id, course_id) VALUES (2, 'A-', 2021, 'autumn',  1,  33333333);
INSERT INTO student_course_grade (student_course_grade_id, grade, year, quarter, student_id, course_id) VALUES (3, 'A+', 2021, 'autumn',  2,  44444444);
INSERT INTO student_course_grade (student_course_grade_id, grade, year, quarter, student_id, course_id) VALUES (4, 'B-', 2021, 'autumn',  2,  33333333);
INSERT INTO student_course_grade (student_course_grade_id, grade, year, quarter, student_id, course_id) VALUES (5, 'A',  2021, 'autumn',  1,  14444444);
INSERT INTO student_course_grade (student_course_grade_id, grade, year, quarter, student_id, course_id) VALUES (6, 'A-', 2021, 'spring',  1,  24444444);
INSERT INTO student_course_grade (student_course_grade_id, grade, year, quarter, student_id, course_id) VALUES (7, 'A+', 2021, 'spring',  1,  34444444);
INSERT INTO student_course_grade (student_course_grade_id, grade, year, quarter, student_id, course_id) VALUES (8, 'B+', 2021, 'spring',  1,  54444444);
INSERT INTO student_course_grade (student_course_grade_id, grade, year, quarter, student_id, course_id) VALUES (9, 'B-',  2021, 'winter',  1,  12345670);
INSERT INTO student_course_grade (student_course_grade_id, grade, year, quarter, student_id, course_id) VALUES (10, 'A+', 2021, 'winter',  1,  13345670);
INSERT INTO student_course_grade (student_course_grade_id, grade, year, quarter, student_id, course_id) VALUES (11, 'A-', 2021, 'winter',  1,  13445670);
INSERT INTO student_course_grade (student_course_grade_id, grade, year, quarter, student_id, course_id) VALUES (12, 'A+', 2020, 'autumn',  1,  34444449);
INSERT INTO student_course_grade (student_course_grade_id, grade, year, quarter, student_id, course_id) VALUES (13, 'A+', 2020, 'autumn',  1,  54444414);
INSERT INTO student_course_grade (student_course_grade_id, grade, year, quarter, student_id, course_id) VALUES (14, 'A',  2020, 'autumn',  1,  59444445);


INSERT INTO registered_student_lab (lab_id, student_id) VALUES (99999999, 2);



INSERT INTO registered_student_section (course_section_id, student_id, reg_status) VALUES (11111114, 1, 'registered');
INSERT INTO registered_student_section (course_section_id, student_id, reg_status) VALUES (11111115, 1, 'registered');
INSERT INTO registered_student_section (course_section_id, student_id, reg_status) VALUES (11111114, 2, 'registered');




INSERT INTO course_prerequisites (course_id, course_id_prereq) VALUES (44444444, 33333333);

