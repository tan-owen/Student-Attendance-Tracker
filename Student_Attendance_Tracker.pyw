from tkinter import *
from tkinter import messagebox # Added for safer error handling if needed, though stuck to labels as per style
import os

##### CLASS DEFINITION #####
class User: 
    # Base class for a basic user information
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
    # Inherits from User and adds list to store attendance records
    def __init__(self, user_ID, password, first_name, last_name):
        super().__init__(user_ID, password, first_name, last_name)
        self.attendance_records = []

    def add_attendance_records(self, record):
        self.attendance_records.append(record)

class Teacher(User):
    # Inherits from User, represents the admin/teacher user
    def __init__(self, user_ID, password, first_name, last_name):
        super().__init__(user_ID, password, first_name, last_name)

class Attendance_Logs: 
    # Stores details for a single attendance entry
    def __init__(self, subject_ID, user_ID,time_registered, date_registered, status):
        self.subject_ID = subject_ID
        self.user_ID = user_ID
        self.time_registered = time_registered # HHMM format
        self.date_registered = date_registered # DDMMYYYY format
        self.status = status

class Subject:
    # Stores subject info
    def __init__(self, subject_ID, name, number_class):
        self.subject_ID = subject_ID
        self.name = name
        self.number_class = number_class

##### FILE HANDLING #####
def load_student_from_file(filepath):
    # Reads student.txt and creates Student objects
    data_list = []
    try:
        with open(filepath) as file:
            for line in file:
                line = line.strip()
                if not line: continue
                student_list = line.split(",")
                if len(student_list) < 4: continue
                try:
                    data_list.append(Student(student_list[0], student_list[1], student_list[2], student_list[3]))
                except Exception: continue
    except Exception: return []
    return data_list

def load_teacher_from_file(filepath):
    # Reads teacher.txt and creates Teacher objects
    data_list = []
    try:
        with open(filepath) as file:
            for line in file:
                line = line.strip()
                if not line: continue
                teacher_list = line.split(",")
                if len(teacher_list) < 4: continue
                try:
                    data_list.append(Teacher(teacher_list[0], teacher_list[1], teacher_list[2], teacher_list[3]))
                except Exception: continue
    except Exception: return []
    return data_list

def load_attendance_from_file(filepath):
    # Reads attendance.txt and creates Attendance_Logs objects
    data_list = []
    try:
        with open(filepath) as file:
            for line in file:
                line = line.strip()
                if not line: continue
                attendance_list = line.split(",")
                if len(attendance_list) < 5: continue
                try:
                    data_list.append(Attendance_Logs(attendance_list[0], attendance_list[1], attendance_list[2], attendance_list[3], attendance_list[4]))
                except Exception: continue
    except Exception: return []
    return data_list

def append_attendance_to_student(student_list, attendance_list):
    # Add loaded attendance logs to its corresponding Student object in the array
    try:
        for logs_index in range(0, len(attendance_list)):
            for user_index in range(0, len(student_list)):
                try:
                    if student_list[user_index].user_ID == attendance_list[logs_index].user_ID:
                        student_list[user_index].add_attendance_records(attendance_list[logs_index])
                except Exception: continue
    except Exception: pass

def load_subject_from_file(filepath):
    # Reads subject.txt and creates a dictionary of Subjects
    subject_dict = {}
    try:
        with open(filepath) as file:
            for line in file:
                line = line.strip()
                if not line: continue
                subject_list = line.split(",")
                if len(subject_list) < 3: continue
                try:
                    subject_dict.update({subject_list[0]: Subject(subject_list[0], subject_list[1], subject_list[2])})
                except Exception: continue
    except Exception: return {}
    return subject_dict

##### GUI #####
class App:
    def __init__(self,student_list, teacher_list, attendance_list,subject_dict,attendance_file_path):
        # Initialize main application data
        self.student_list = student_list
        self.teacher_list = teacher_list
        self.attendance_list = attendance_list
        self.subject_dict = subject_dict
        self.attendance_file_path = attendance_file_path
        
        # State variables for teacher selection
        self.selected_student_for_viewing = None

        # Setup main window
        self.window = Tk()
        self.window.title("Teacher Attendance Portal")
        self.window.minsize(800,600) 
        self.window.configure(bg="#f0f2f5") 
        
        # Load icon if available
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(base_dir, "res", "icon.ico")
            self.window.iconbitmap(icon_path)
        except Exception:
            pass

        # Start at login screen
        self.login_screen()

        self.window.mainloop()
        
    def page_select_screen(self):
        # Clear previous frame
        try: self.login_page_frame.forget() 
        except: pass

        # Setup Menu Frame
        self.page_selection_frame = Frame(self.window, bg="#f0f2f5") 
        self.page_selection_frame.pack(fill='both',expand=True, pady=10,padx=10)
        
        # Configure Grid Weights for Centering
        self.page_selection_frame.grid_columnconfigure(0, weight=1)
        self.page_selection_frame.grid_rowconfigure(0, weight=1)
        self.page_selection_frame.grid_rowconfigure(3, weight=1)

        container = Frame(self.page_selection_frame, bg="#f0f2f5")
        container.pack(expand=True)

        # Retrieve Teacher Name for Welcome Message
        full_name = "Teacher"
        for teacher in self.teacher_list:
            if teacher.user_ID == self.logged_in_user_ID:
                full_name = f"{teacher.first_name} {teacher.last_name}"
                break
        
        # Screen selection button
        Label(container, text=f"Welcome, {full_name}", font=("Helvetica", 20, "bold"), bg="#f0f2f5", fg="#333").pack(pady=(0, 30))

        self.attendance_registration_button = Button(container,text="Mark Student Attendance",command=self.attendance_registration_screen,font=("Arial", 16, "bold"),width=25,height=2,bg="#4CAF50")
        self.attendance_registration_button.pack(pady=20)

        self.check_attendance_button = Button(container,text="View Student Logs",command=self.attendance_screen,font=("Arial", 16, "bold"),width=25,height=2,bg="#2196F3")
        self.check_attendance_button.pack(pady=20)
        
        # Logout Button
        Button(container, text="Logout", command=self.logout, font=("Arial", 12), bg="#ff6666", width=15).pack(pady=20)


    def logout(self):
        # Resets user session and returns to login
        self.page_selection_frame.forget()
        self.logged_in_user_ID = ""
        self.login_screen()

    def login_screen(self):
        # Main background frame
        self.login_page_frame = Frame(self.window, bg="#f0f2f5")
        self.login_page_frame.pack(fill="both", expand=True)

        # Center Card Frame
        login_card = Frame(self.login_page_frame, bg="white", padx=20, pady=20)
        login_card.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        Label(login_card, text="Teacher Login Portal", font=("Helvetica", 16, "bold"), bg="white", fg="#333").pack(pady=(0, 5))

        # Username Entry
        Label(login_card, text="Teacher ID", font=("Arial", 11), bg="white", fg="#555").pack(anchor="w")
        self.username_entry = Entry(login_card, font=("Arial", 12), width=25, bd=1, relief="solid")
        self.username_entry.pack(pady=(5, 15), ipady=5)

        # Password Entry
        Label(login_card, text="Password", font=("Arial", 11), bg="white", fg="#555").pack(anchor="w")
        self.password_entry = Entry(login_card, show="*", font=("Arial", 12), width=25, bd=1, relief="solid")
        self.password_entry.pack(pady=(5, 25), ipady=5)

        # Login Button
        login_button = Button(login_card,text="LOGIN",command=self.user_validation,font=("Arial", 12, "bold"),bg="#007bff",width=20)
        login_button.pack(ipady=5)

        # Error Message
        self.login_message_label = Label(login_card, text="", font=("Arial", 10), bg="white", fg="red")
        self.login_message_label.pack(pady=(15, 0))

        # Footer
        Label(self.login_page_frame, text="Attendance System by Tan Owen & Loong Shi Xian", bg="#f0f2f5", fg="#aaa").place(relx=0.5, rely=0.95, anchor="center")

    def attendance_screen(self):
        # Clears menu and shows subject list
        self.page_selection_frame.forget()
        self.attendance_screen_frame = Frame(self.window)
        self.attendance_screen_frame.configure(bg="#f0f2f5")
        self.attendance_screen_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Navigation
        top_bar = Frame(self.attendance_screen_frame, bg="#f0f2f5")
        top_bar.pack(fill="x", padx=10, pady=5)
        Button(top_bar, text="< Back", command=self.back_from_check).pack(side=LEFT)

        Label(self.attendance_screen_frame, text="View Student Attendance",font=("Helvetica", 24, "bold"),bg="#f0f2f5").pack(pady=5)

        # Student Selection for Viewing
        selection_frame = Frame(self.attendance_screen_frame, bg="#f0f2f5")
        selection_frame.pack(pady=10)
        
        Label(selection_frame, text="Select Student: ", bg="#f0f2f5", font=("Arial", 12)).pack(side=LEFT)
        
        self.view_student_map = {}
        student_options = []
        for student in self.student_list:
            name = f"{student.first_name} {student.last_name} ({student.user_ID})"
            self.view_student_map[name] = student.user_ID
            student_options.append(name)
        
        if not student_options: student_options = ["No Students"]

        self.selected_view_student_var = StringVar(self.window)
        self.selected_view_student_var.set(student_options[0])
        self.selected_student_for_viewing = self.view_student_map.get(student_options[0])

        # Dropdown
        view_dropdown = OptionMenu(selection_frame, self.selected_view_student_var, *student_options, command=self.update_subject_list_view)
        view_dropdown.pack(side=LEFT, padx=10)

        # Container for subject list
        self.subject_list_container = Frame(self.attendance_screen_frame, bg="#f0f2f5")
        self.subject_list_container.pack(fill="both", expand=True)

        # Initial Load
        self.refresh_subject_list()

    def update_subject_list_view(self, value):
        # Callback when dropdown changes
        self.selected_student_for_viewing = self.view_student_map.get(value)
        self.refresh_subject_list()

    def refresh_subject_list(self):
        # Clear existing widgets in container
        for widget in self.subject_list_container.winfo_children():
            widget.destroy()

        if not self.selected_student_for_viewing: return

        # Populate list of subjects the SELECTED student has attended
        subject_list = self.get_subject(self.selected_student_for_viewing) 
        
        if not subject_list:
             Label(self.subject_list_container, text="No attendance records found for this student.", bg="#f0f2f5", fg="gray").pack(pady=20)

        for subject_id in subject_list:
            self.add_subject(subject_id, self.selected_student_for_viewing) 

    def view_subject_details(self, subject_id, student_id):
        # Shows detailed logs for a specific subject AND specific student
        self.attendance_screen_frame.forget()

        self.detail_frame = Frame(self.window)
        self.detail_frame.pack(fill="both", expand=True, padx=20, pady=20)

        Button(self.detail_frame, text="< Back", command=self.back_from_details).pack(anchor="w", pady=5)

        sub_name = self.subject_dict[subject_id].name
        
        # Find student name for header
        st_name = "Student"
        for st in self.student_list:
            if st.user_ID == student_id:
                st_name = f"{st.first_name} {st.last_name}"
                break

        Label(self.detail_frame, text=f"Logs for: {sub_name}", font=("Arial", 18, "bold")).pack(pady=(15,5))
        Label(self.detail_frame, text=f"Student: {st_name}", font=("Arial", 12)).pack(pady=(0,15))

        # Attendance Log Container
        log_container = Frame(self.detail_frame)
        log_container.pack(fill="both", expand=True)

        current_student = None
        for student in self.student_list:
            if student.user_ID == student_id:
                current_student = student
                break
        
        if current_student:
            # Filter logs for the selected subject
            subject_logs = [log for log in current_student.attendance_records if log.subject_ID == subject_id]

            # Sorting the attendance log by their date (YYYYMMDD) and time registered
            subject_logs.sort(key=lambda x: x.date_registered[4:] + x.date_registered[2:4] + x.date_registered[:2] + x.time_registered) 

            if subject_logs:
                for log in subject_logs:
                    # Formatting Date
                    d = log.date_registered
                    fmt_date = f"{d[:2]}/{d[2:4]}/{d[4:]}"
                    # Formatting Time
                    t = log.time_registered
                    fmt_time = f"{t[:2]}:{t[2:]}"
                    # Determining Status Color
                    is_present = str(log.status) == "1"
                    status_txt = "PRESENT" if is_present else "ABSENT"
                    color = "green" if is_present else "red"
                    
                    display_text = f"{fmt_date}   |   {fmt_time}   |   {status_txt}"
                    
                    Label(log_container, text=display_text, fg=color, font=("Arial", 12)).pack(pady=3)
            else:
                Label(log_container, text="No attendance records found.", fg="gray").pack(pady=20)

    def back_from_details(self):
        # Return to subject list
        self.detail_frame.forget()
        self.attendance_screen_frame.pack(fill="both", expand=True)

    def attendance_registration_screen(self):
        # Clears menu and shows registration form
        self.page_selection_frame.forget()

        self.attendance_registration_frame = Frame(self.window,padx="20",pady="10")
        self.attendance_registration_frame.configure(bg="#f0f2f5")  
        self.attendance_registration_frame.pack(fill="both",expand=True) 
        
        Button(self.attendance_registration_frame, text="< Back", command=self.back_from_reg).pack(anchor="nw", pady=5)

        Label(self.attendance_registration_frame, text="Mark Student Attendance",font=("Helvetica", 24, "bold"),bg="#f0f2f5").pack(pady=10)

        form_frame = Frame(self.attendance_registration_frame, bg="white", padx=20, pady=20)
        form_frame.pack()

        # Dropdown for Students (New Addition)
        Label(form_frame, text="Student:", bg="white").grid(row=0, column=0, sticky="e", pady=5)
        
        self.student_name_map = {}
        student_dropdown_options = []
        for student in self.student_list:
            name = f"{student.first_name} {student.last_name} ({student.user_ID})"
            self.student_name_map[name] = student.user_ID
            student_dropdown_options.append(name)
        
        if not student_dropdown_options: student_dropdown_options = ["No Students"]

        self.selected_target_student_var = StringVar(self.window)
        self.selected_target_student_var.set(student_dropdown_options[0])
        OptionMenu(form_frame, self.selected_target_student_var, *student_dropdown_options).grid(row=0, column=1, sticky="w", pady=5)

        # Dropdown for subjects
        self.subject_name_map = {}
        dropdown_options = []
        for subject_id in self.subject_dict:
            name = self.subject_dict[subject_id].name
            self.subject_name_map[name] = subject_id
            dropdown_options.append(name)
        
        if not dropdown_options: dropdown_options = ["No Subjects"]

        Label(form_frame, text="Subject:", bg="white").grid(row=1, column=0, sticky="e", pady=5)
        self.selected_subject_var = StringVar(self.window)
        self.selected_subject_var.set(dropdown_options[0])
        OptionMenu(form_frame, self.selected_subject_var, *dropdown_options).grid(row=1, column=1, sticky="w", pady=5)

        # DATE Dropdowns
        Label(form_frame, text="Date:", bg="white").grid(row=2, column=0, sticky="e", pady=5)
        
        date_frame = Frame(form_frame, bg="white")
        date_frame.grid(row=2, column=1, sticky="w")

        days = [f"{i:02d}" for i in range(1, 32)]      
        months = [f"{i:02d}" for i in range(1, 13)]    
        years = [str(i) for i in range(2023, 2030)]    

        self.day_var = StringVar(self.window); self.day_var.set("01")
        self.month_var = StringVar(self.window); self.month_var.set("01")
        self.year_var = StringVar(self.window); self.year_var.set("2025")

        OptionMenu(date_frame, self.day_var, *days).pack(side=LEFT)
        Label(date_frame, text="/", bg="white").pack(side=LEFT)
        OptionMenu(date_frame, self.month_var, *months).pack(side=LEFT)
        Label(date_frame, text="/", bg="white").pack(side=LEFT)
        OptionMenu(date_frame, self.year_var, *years).pack(side=LEFT)

        # TIME Dropdowns
        Label(form_frame, text="Time:", bg="white").grid(row=3, column=0, sticky="e", pady=5)
        
        time_frame = Frame(form_frame, bg="white")
        time_frame.grid(row=3, column=1, sticky="w")

        hours = [f"{i:02d}" for i in range(0, 24)]      
        minutes = [f"{i:02d}" for i in range(0, 60)]   

        self.hour_var = StringVar(self.window); self.hour_var.set("12")
        self.minute_var = StringVar(self.window); self.minute_var.set("00")

        OptionMenu(time_frame, self.hour_var, *hours).pack(side=LEFT)
        Label(time_frame, text=":", bg="white").pack(side=LEFT)
        OptionMenu(time_frame, self.minute_var, *minutes).pack(side=LEFT)

        # STATUS Radio Buttons
        Label(form_frame, text="Status:", bg="white").grid(row=4, column=0, sticky="e", pady=5)
        
        status_frame = Frame(form_frame, bg="white")
        status_frame.grid(row=4, column=1, sticky="w")

        self.status_var = StringVar(value="1") # Default is 1
        
        Radiobutton(status_frame, text="Present", variable=self.status_var, value="1", bg="white").pack(side=LEFT, padx=5)
        Radiobutton(status_frame, text="Absent", variable=self.status_var, value="0", bg="white").pack(side=LEFT, padx=5)

        Button(form_frame, text="Mark Attendance", command=self.save_attendance_data, bg="green", fg="white").grid(row=5, column=0, columnspan=2, pady=15, sticky="ew")
        
        self.status_label = Label(self.attendance_registration_frame, text="", bg="#f0f2f5", fg="white")
        self.status_label.pack(pady=10)

    def back_from_reg(self):
        # Return to menu
        self.attendance_registration_frame.forget()
        self.page_select_screen()

    def back_from_check(self):
        # Return to menu
        self.attendance_screen_frame.forget()
        self.page_select_screen()

    def save_attendance_data(self):
        # Get target student
        target_student_name = self.selected_target_student_var.get()
        if target_student_name not in self.student_name_map:
            self.status_label.config(text="Error: Invalid Student", fg="red")
            return
        
        target_user_ID = self.student_name_map[target_student_name]

        subject_name = self.selected_subject_var.get()
        date_in = self.day_var.get() + self.month_var.get() + self.year_var.get()
        time_in = self.hour_var.get() + self.minute_var.get()
        
        if subject_name not in self.subject_name_map:
            self.status_label.config(text="Error: Invalid Subject", fg="red")
            return

        subject_id = self.subject_name_map[subject_name]
        status_val = self.status_var.get() 

        #Check for duplicate logs
        for student in self.student_list:
            if student.user_ID == target_user_ID:
                for record in student.attendance_records:
                    if (record.subject_ID == subject_id and 
                        record.date_registered == date_in and 
                        record.time_registered == time_in):
                        
                        self.status_label.config(text="Error: Log already exists.", fg="red")
                        return
                break


        # Validation (checks to see if the max amount of classes has been reached already)
        try:
            max_classes = int(self.subject_dict[subject_id].number_class)
        except:
            max_classes = 100 

        current_log_count = 0
        for student in self.student_list:
            if student.user_ID == target_user_ID:
                for record in student.attendance_records:
                    if record.subject_ID == subject_id:
                        current_log_count += 1
                break
        
        if current_log_count >= max_classes:
            self.status_label.config(text=f"Limit Reached: {max_classes} max classes.", fg="red")
            return

        # Write to file and update runtime
        try:
            line_to_write = f"{subject_id},{target_user_ID},{time_in},{date_in},{status_val}\n"
            with open(self.attendance_file_path, "a") as file: 
                file.write(line_to_write)
            new_log = Attendance_Logs(subject_id, target_user_ID, time_in, date_in, status_val)
            self.attendance_list.append(new_log)
            
            for student in self.student_list:
                if student.user_ID == target_user_ID:
                    student.add_attendance_records(new_log)

            self.status_label.config(text="Success! Saved.", fg="lightgreen")

        except Exception as e:
            self.status_label.config(text="Error saving file.", fg="red")
            print(e)

    def user_validation(self):
        # Validate credentials against loaded TEACHER list
        input_user = self.username_entry.get()
        input_pass = self.password_entry.get()
        self.logged_in_user_ID = ""
        found_user = False
        
        for user in self.teacher_list:
            if input_user == user.user_ID:
                found_user = True
                if input_pass == user.get_password():
                    print("Login Successful")
                    self.logged_in_user_ID = user.user_ID
                    self.page_select_screen()
                    return # Exit if successful
                else: 
                    self.login_message_label.config(text="Incorrect Password")
                    return
        
        if not found_user:
            self.login_message_label.config(text="Teacher ID not found")
    
    def get_subject(self, student_id):
        #Returns list of unique subjects attended by the SELECTED student
        student_subject_list = []
        for logs in self.attendance_list:
            if (logs.subject_ID not in student_subject_list) and (logs.user_ID == student_id):
                student_subject_list.append(logs.subject_ID)
            else: continue
        return student_subject_list

    def add_subject(self, subject_id, student_id):
        # Creates a clickable list item with progress bar for a subject
        subject_frame = Frame(self.subject_list_container)
        subject_frame.pack(fill="x", padx=10, pady=5) 
        
        # Temp function to stop it from immediately executing
        on_click = lambda event: self.view_subject_details(subject_id, student_id)

        subject_frame.bind("<Button-1>", on_click)
        subject_frame.configure(cursor="hand2")

        subject_name = self.subject_dict[subject_id].name
        lbl = Label(subject_frame, text=f"Subject: {subject_name}")
        lbl.pack(anchor="w")
        lbl.bind("<Button-1>", on_click)
        
        # Attendance Progress Bar
        attendance_bar = Canvas(subject_frame, height=20, bg="lightgray", highlightthickness=0)
        attendance_bar.pack(fill="x", padx=0, pady=0)
        attendance_bar.bind("<Button-1>", on_click)
        attendance_bar.configure(cursor="hand2")

        self.window.update_idletasks() 
        canvas_width = attendance_bar.winfo_width()
        
        # Calculate Progress
        class_attended = 0
        for student in self.student_list:
            if student.user_ID == student_id:
                for logs in student.attendance_records:
                    if logs.subject_ID == subject_id:
                        class_attended += int(logs.status)
            else: continue
                
        total_classes = int(self.subject_dict[subject_id].number_class)
        progress_ratio = class_attended / total_classes if total_classes > 0 else 0
        
        # Draw Attedance Bar using progress
        attendance_bar.create_line(0, 10, canvas_width, 10, fill="#CBCBCB", width=20)
        attendance_bar.create_line(0, 10, progress_ratio * canvas_width, 10, fill="green", width=20)
        
        class_attended_percentage = f"{class_attended:02d}/{total_classes:02d}  Class Attended   |   {str(round(progress_ratio * 100,2))}%"
        attendance_bar.create_text(90,9,text=class_attended_percentage)

if __name__ == "__main__":
    # Get absolute path
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    res_dir = os.path.join(BASE_DIR, "res")
    student_path = os.path.join(res_dir, "student.txt")
    teacher_path = os.path.join(res_dir, "teacher.txt") # New file
    attendance_path = os.path.join(res_dir, "attendance.txt")
    subject_path = os.path.join(res_dir, "subject.txt")

    try:

        student_list = load_student_from_file(student_path)
        teacher_list = load_teacher_from_file(teacher_path)
        attendance_list = load_attendance_from_file(attendance_path)
        subject_dict = load_subject_from_file(subject_path)
        
        append_attendance_to_student(student_list, attendance_list)
    
        App(student_list, teacher_list, attendance_list, subject_dict, attendance_path)
        
    except FileNotFoundError:
        print(f"Error: Could not find files in {res_dir}. Please ensure the 'res' folder and txt files exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")