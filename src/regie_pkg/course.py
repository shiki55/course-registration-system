
class Course:
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


# class ActiveCourse(Course):
#     def __init__(self, 
#                 _id,
#                 name,
#                 approval_req,
#                 faculty_id,
#                 desc,
#                 subject,
#                 division,
#                 reg_status,       
#         ):
#         super().__init__(
#                 _id,
#                 name,
#                 approval_req,
#                 faculty_id,
#                 desc,
#                 subject,
#                 division,
#         )
#         self.reg_status = reg_status