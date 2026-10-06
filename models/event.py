class Event:
    def __init__(self, event_id, event_name, date, venue, max_participants):
        self.event_id = event_id
        self.event_name = event_name
        self.date = date
        self.venue = venue
        self.max_participants = max_participants

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "event_name": self.event_name,
            "date": self.date,
            "venue": self.venue,
            "max_participants": self.max_participants
        }

    def display(self):
        print("-" * 70)
        print(f"Event ID          : {self.event_id}")
        print(f"Event Name        : {self.event_name}")
        print(f"Date              : {self.date}")
        print(f"Venue             : {self.venue}")
        print(f"Maximum Participants: {self.max_participants}")