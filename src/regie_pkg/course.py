"""
This module contains classes for representing courses and completed courses.

The Course class represents a course, including its ID, name, approval requirements,
instructor/faculty id, course description, subject area, and division.

The CompletedCourse class represents a course that has been completed
by a student, including the student's id, grade, year, and quarter in which
the course was completed.
"""

class Course:
    """A class representing a course."""

    def __init__(self,
                _id,
                name,
                approval_req,
                faculty_id,
                desc,
                subject,
                division,
        ):
        self.id=_id
        self.name=name
        self.approval_req=approval_req
        self.faculty_id=faculty_id
        self.desc=desc
        self.subject=subject
        self.division=division


class CompletedCourse(Course):
    """A class representing a course that has been completed by a student."""

    def __init__(self,
                _id,
                name,
                approval_req,
                faculty_id,
                desc,
                subject,
                division,
                student_id,
                grade,
                year,
                quarter,
        ):
        super().__init__(
                _id,
                name,
                approval_req,
                faculty_id,
                desc,
                subject,
                division,
        )
        self.student_id = student_id
        self.grade = grade
        self.year = year
        self.quarter = quarter
