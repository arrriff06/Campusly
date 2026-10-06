class Registration:
    def __init__(self, registration_id, student_id, event_id):
        self.registration_id = registration_id
        self.student_id = student_id
        self.event_id = event_id

    def to_dict(self):
        return {
            "registration_id": self.registration_id,
            "student_id": self.student_id,
            "event_id": self.event_id
        }