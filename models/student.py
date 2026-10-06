class Student:
    def __init__(self, student_id, name, department, email):
        self.student_id = student_id
        self.name = name
        self.department = department
        self.email = email

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "department": self.department,
            "email": self.email
        }

    def display(self):
        print("-" * 70)
        print(f"Student ID   : {self.student_id}")
        print(f"Name         : {self.name}")
        print(f"Department   : {self.department}")
        print(f"Email        : {self.email}")