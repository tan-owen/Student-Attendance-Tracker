from tkinter import *
##### CLASS DEFINITION $$$$$
class User: # format in file: john123,1234,John,Doe
    def __init__(self, user_ID, password, first_name, last_name):
        self.user_ID = user_ID
        self.__password = password
        self.first_name = first_name
        self.last_name = last_name
        
    def set_password(self):
        self.__password
    def get_password(self):
        return self.__password
class Student(User): 
    def __init__(self, user_ID, password, first_name, last_name):
        super().__init__(user_ID, password, first_name, last_name)
        self.attendance_records = []

    def add_attendance_records(self, record):
        self.attendance_records.append(record)
class Attendance_Logs: # format in file: CS1000,john123,1200,29112025,1
    def __init__(self, subject_ID, user_ID,time_registered, date_registered, status):
        self.subject_ID = subject_ID
        self.user_ID = user_ID
        self.time_registered = time_registered # HHMM format
        self.date_registered = date_registered # DDMMYYYY format
        self.status = status
class Subject:
    def __init__(self, subject_ID, name, number_class):
        self.subject_ID = subject_ID
        self.name = name
        self.number_class = number_class

##### FILE HANDLING #####
def load_student_from_file(filepath):
    data_list = []
    try:
        with open(filepath) as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                student_list = line.split(",")
                if len(student_list) < 4:
                    continue
                try:
                    data_list.append(
                        Student(student_list[0], student_list[1], student_list[2], student_list[3])
                    )
                except Exception:
                    continue
    except Exception:
        return []
    return data_list
def load_attendance_from_file(filepath):
    data_list = []
    try:
        with open(filepath) as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                attendance_list = line.split(",")
                if len(attendance_list) < 5:
                    continue
                try:
                    data_list.append(
                        Attendance_Logs(
                            attendance_list[0],
                            attendance_list[1],
                            attendance_list[2],
                            attendance_list[3],
                            attendance_list[4]
                        )
                    )
                except Exception:
                    continue
    except Exception:
        return []
    return data_list
def append_attendance_to_student(student_list, attendance_list):
    try:
        for logs_index in range(0, len(attendance_list)):
            for user_index in range(0, len(student_list)):
                try:
                    if student_list[user_index].user_ID == attendance_list[logs_index].user_ID:
                        student_list[user_index].add_attendance_records(attendance_list[logs_index])
                except Exception:
                    continue
    except Exception:
        pass
def load_subject_from_file(filepath):
    subject_dict = {}
    try:
        with open(filepath) as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                subject_list = line.split(",")
                if len(subject_list) < 3:
                    continue
                try:
                    subject_dict.update({
                        subject_list[0]: Subject(subject_list[0], subject_list[1], subject_list[2])
                    })
                except Exception:
                    continue
    except Exception:
        return {}
    return subject_dict

##### DEBUGGING FUNCTIONS #####
def print_student_list(student_list):
    for item in student_list:
        print(item.user_ID, item.get_password(), item.first_name, item.last_name,end="")
def print_attendace_list(student_list, array_index):
    
    print(f"Attendance for {student_list[array_index].first_name} {student_list[array_index].last_name}")
    for logs in student_list[array_index].attendance_records:
        print(f"Subject: {logs.subject_ID}")
        print(f"User_ID: {logs.user_ID}")
        print(f"Time: {logs.time_registered}")
        print(f"Date: {logs.date_registered}")
        print(f"Status: {"Present" if logs.status == 1 else "Absent"}\n")
def print_subjects_info(subject_dict):
    for key in subject_dict:
        print(f"Subject ID: {subject_dict[key].subject_ID}")
        print(f"Subject Name: {subject_dict[key].name}")
        print(f"Number of Classes: {subject_dict[key].number_class}")
def print_attendance_by_subject(subject_dict, student_index):
    for subject in subject_dict:
        print(f"Attendance for {subject_dict[subject].name}: ", end="")
        class_attended = 0
        for logs in student_list[student_index].attendance_records: #[x] for student at index "x"
            if logs.subject_ID == subject_dict[subject].subject_ID:
                class_attended += int(logs.status)
        print(f"{class_attended}/{subject_dict[subject].number_class}")

    
##### GUI #####
class App:
    def __init__(self,student_list):
        self.student_list = student_list
        self.window = Tk()
        self.window.title("Login")
        self.window.minsize(800,450)
        self.page_select_screen()
        





        self.window.mainloop()
        
    def page_select_screen(self):
        self.page_selection_frame = Frame(self.window)
        self.page_selection_frame.pack(fill='both',expand=True, pady=10,padx=10)
        self.login_page_button = Button(self.page_selection_frame, text="Login Page", command=self.login_screen)
        self.login_page_button.pack()

    def login_screen(self):
        # Deletes previous page
        self.page_selection_frame.pack_forget()

        # Creates login page frame
        # self.login_page_frame = Frame(self.window)
        # self.login_page_frame.config(bg="red")
        # self.login_page_frame.pack(fill='both',expand=True, pady=10,padx=10)

        # Top Label
        Label(self.window, text="Student Attendance Tracker").pack()

        self.login_page_frame = Frame(self.window,padx="20",pady="10")
        self.login_page_frame.configure(bg="red")
        self.login_page_frame.pack(fill="both",expand=True)

        # Username Entry UI
        username_label = Label(self.login_page_frame, text="Username ")
        username_label.grid(row=0, column=0,pady="5")
        
        self.username_entry = Entry(self.login_page_frame)
        self.username_entry.grid(row=0,column=1)

        # Password Entry UI
        password_label = Label(self.login_page_frame, text="Password ")
        password_label.grid(row=1, column=0,pady="5")

        self.password_entry = Entry(self.login_page_frame)
        self.password_entry.grid(row=1,column=1)

        # Login Button
        login_button = Button(self.login_page_frame, text="Login", command=self.user_validation)
        login_button.grid(row=2,column=0, columnspan=2, sticky="ew")

    def attendance_page(self):
        self.login_page_frame.pack_forget()

    # Functions
    def user_validation(self):
        input_user = self.username_entry.get()
        input_pass = self.password_entry.get()
        
        for user in self.student_list:
            if input_user == user.user_ID:
                if input_pass == user.get_password():
                    print("Login Successful")
                    self.attendance_page()
                else:
                    print("Incorrect Password")
                continue
            else:
                print("User not found")
                continue
      
   
        
if __name__ == "__main__":
    # Loading data from file
    student_list = load_student_from_file("res/student.txt")
    attendance_list = load_attendance_from_file("res/attendance.txt")
    subject_dict = load_subject_from_file("res/subject.txt")
    append_attendance_to_student(student_list,attendance_list)

    # Debug
    # print_attendace_list(student_list, 0)
    # print_subjects_info(subject_dict)
    # print_attendance_by_subject(subject_dict,1)
    print(student_list[1].user_ID)






    


            

    App(student_list=student_list)
