import csv
import os


class Host:
    def __init__(self):
        self.request_list = []
        self.student_list = []
        self.lecturer_list = []
        self.course_dict = {}

        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(self.current_directory, 'courses.csv')
        self.load_courses_from_csv(file_path)

    # Loads course.csv from Server and adds them into course_dict dictionary
    def load_courses_from_csv(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                course_code = row[0]
                course_name = row[1]
                topics = row[2:]
                self.course_dict[course_code + ': ' + course_name] = topics

    # Defines the save path as Server Folder and appends the chat_log list into a txt file
    def save_chat_log(self, chat_log):
        file_path = os.path.join(self.current_directory, "Request and Chat Record.txt")

        with open(file_path, 'a') as file:  # 'a' mode for appending
            # Header for request details
            file.write(' '.join(chat_log) + '\n')

    # Add the provided Request instance to the request_list
    def add_request(self, request):
        self.request_list.append(request)

