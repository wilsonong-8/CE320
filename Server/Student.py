class Student:
    # Student class initializer for Student Clients
    def __init__(self, student_id, seat_no, course_no, addr, conn):
        self.student_id = student_id
        self.seat_no = seat_no
        self.course_no = course_no
        self.addr = addr
        self.conn = conn

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "seat_no": self.seat_no,
            "course_no": self.course_no,
            "addr": self.addr,
        }