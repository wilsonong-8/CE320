from datetime import datetime
from enum import Enum, auto
import json


class Priority(Enum):
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()


class Status(Enum):
    WAITING = auto()
    WORKING = auto()
    COMPLETE = auto()


class Request:
    def __init__(self, topic, priority, description, student):
        self.topic = topic
        self.priority = self.get_priority_from_string(priority)  # Convert string to Priority enum
        self.description = description
        self.time = self.get_current_time()
        self.status = Status.WAITING
        self.student = student

    class RequestEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Request):
                # Convert the Request object to a dictionary representation
                return {
                    "topic": obj.topic,
                    "priority": obj.priority.name,
                    "description": obj.description,
                    "time": obj.time,
                    "status": obj.status.name,
                    "student": {
                        "student_id": obj.student.student_id,
                        "seat_no": obj.student.seat_no,
                        "course_no": obj.student.course_no,
                        "addr": obj.student.addr,
                    }
                }
            # For any other object types, use the default serialization
            return super().default(obj)

    def get_priority_from_string(self, priority_str):
        # Mapping between priority names and Priority enum values
        priority_mapping = {
            "Super Urgent": Priority.HIGH,
            "I have a question": Priority.MEDIUM,
            "I need some information": Priority.LOW,
        }
        return priority_mapping.get(priority_str, Priority.LOW)  # Default to LOW if priority_str is not found

    def get_current_time(self):
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")  # Format as "xx:xx am/pm"
        return time_str
