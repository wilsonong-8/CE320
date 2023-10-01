from datetime import datetime
from enum import Enum, auto
import json


# Define the Priority enumeration class
class Priority(Enum):
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()
    WORKING = auto()
    COMPLETE = auto()


# Define the Request class
class Request:
    def __init__(self, topic, priority, description, student):
        # Initialize instance variables based on provided arguments
        self.topic = topic
        self.priority = self.get_priority_from_string(priority)  # Convert string to Priority enum
        self.description = description
        self.time = self.get_current_time()
        self.conversation = []
        self.student = student

    # Define a JSON encoder for the Request class
    class RequestEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Request):
                # Convert the Request object to a dictionary representation
                return {
                    "topic": obj.topic,
                    "priority": obj.priority.name,
                    "description": obj.description,
                    "time": obj.time,
                    "conversation": obj.conversation,
                    "student": obj.student[0],  # Access the first (and only) element of the list, which is a dictionary
                }
            # For any other object types, use the default serialization
            return super().default(obj)

    # Convert priority string to Priority enum using a mapping
    def get_priority_from_string(self, priority_str):
        priority_mapping = {
            "Super Urgent": Priority.HIGH,
            "I have a question": Priority.MEDIUM,
            "I need some information": Priority.LOW,
            "WORKING": Priority.WORKING,
            "COMPLETE": Priority.COMPLETE
        }
        return priority_mapping.get(priority_str, Priority.LOW)  # Default to LOW if priority_str is not found

    # Get the current time formatted as "xx:xx am/pm"
    def get_current_time(self):
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        return time_str

    # Static method to convert priority string to Priority enum using a mapping
    @staticmethod
    def static_get_priority_from_string(priority_str):
        priority_mapping = {
            "Super Urgent": Priority.HIGH,
            "I have a question": Priority.MEDIUM,
            "I need some information": Priority.LOW,
            "working": Priority.WORKING,
            "complete": Priority.COMPLETE
        }
        return priority_mapping.get(priority_str, Priority.LOW)  # Default to LOW if priority_str is not found
