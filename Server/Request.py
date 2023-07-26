from datetime import datetime
from enum import Enum, auto


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
        self.priority = priority
        self.description = description
        self.time = get_current_time()
        self.status = Status.WAITING
        self.student = student


def get_current_time():
    now = datetime.now()
    time_str = now.strftime("%I:%M %p")  # Format as "xx:xx am/pm"
    return time_str
