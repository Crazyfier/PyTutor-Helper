import re
import os
import datetime

clear = lambda: os.system("cls")

# You are able to edit this to your liking or add on additional option
class_option = {
    "1" : {"Time" : "10am-12pm", "Teacher" : "Miss Olivia"},
    "2" : {"Time" : "2pm-4pm", "Teacher" : "Miss Lucia"},
    "3" : {"Time" : "4pm-6pm", "Teacher" : "Miss Olivia"}
}

# Where all list and dictionaries are

day = {"1" : "monday", "2" : "tuesday", "3" : "wednesday", "4" : "thursday", "5" : "friday", "6" : "saturday", "7" : "sunday"}

month = {"1" : "january", "2" : "february", "3" : "march", "4" : "april", "5" : "may", "6" : "june", "7" : "july", "8" : "august", "9" : "september", "10" : "october", "11" : "november", "12" : "december"}

student_data = {
    1: {"Name": "Edison", "Age": 21, "Contact Info": "0138300886"},
    2: {"Name": "Ayato", "Age": 18, "Contact Info": "0138300886"},
    3: {"Name": "Yoimiya", "Age": 18, "Contact Info": "0138300886"},
    4: {"Name": "Shinobu", "Age": 19, "Contact Info": "0138300886"},
    5: {"Name": "Kojuro", "Age": 20, "Contact Info": "0138300886"},
    6: {"Name": "Muzan", "Age": 18, "Contact Info": "0138300886"},
    7: {"Name": "Tanjiro", "Age": 17, "Contact Info": "0138300886"},
    8: {"Name": "Sengoku", "Age": 18, "Contact Info": "0138300886"},
    9: {"Name": "Narute", "Age": 17, "Contact Info": "0138300886"},
    10: {"Name": "Sasuke", "Age": 18, "Contact Info": "0138300886"}
}

student_schedule = {
    1 : {"Name" : "Edison", "Month": "april", "Day": "wednesday", "Time": "10am-12pm", "Teacher" : "Miss Olivia"},
    2 : {"Name": "Ayato", "Month": "april", "Day": "wednesday", "Time": "10am-12pm", "Teacher" : "Miss Olivia"},
    3 : {"Name": "Yoimiya", "Month": "april", "Day": "wednesday", "Time": "10am-12pm", "Teacher" : "Miss Olivia"},
    4 : {"Name": "Shinobu", "Month": "april", "Day": "wednesday", "Time": "10am-12pm", "Teacher" : "Miss Olivia"},
    5 : {"Name": "Kojuro", "Month": "april", "Day": "wednesday", "Time": "10am-12pm", "Teacher" : "Miss Olivia"},
    6 : {"Name": "Muzan", "Month": "april", "Day": "wednesday", "Time": "10am-12pm", "Teacher" : "Miss Olivia"},
    7 : {"Name": "Tanjiro", "Month": "april", "Day": "wednesday", "Time": "10am-12pm", "Teacher" : "Miss Olivia"},
    8 : {"Name": "Sengoku", "Month": "april", "Day": "wednesday", "Time": "10am-12pm", "Teacher" : "Miss Olivia"},
    9 : {"Name": "Narute", "Month": "april", "Day": "wednesday", "Time": "10am-12pm", "Teacher" : "Miss Olivia"},
    10 : {"Name": "Sasuke", "Month": "april", "Day": "wednesday", "Time": "10am-12pm", "Teacher" : "Miss Olivia"}
}

# This section is where the all the modules are

def add_student(student_name, student_age, student_contact, session_month, session_day, class_num):
    student_data_number = len(student_data) + 1

    student_data[student_data_number] = {}

    student_data[student_data_number]["Name"] = student_name
    student_data[student_data_number]["Age"] = student_age
    student_data[student_data_number]["Phone Number"] = student_contact

    
    student_schedule[student_data_number] = {}

    student_schedule[student_data_number]["Name"] = student_name
    student_schedule[student_data_number]["Month"] = session_month
    student_schedule[student_data_number]["Day"] = session_day
    student_schedule[student_data_number]["Time"] = class_option[class_num]["Time"]
    student_schedule[student_data_number]["Teacher"] = class_option[class_num]["Teacher"]

def phone_val(number):
    if len(number) == 10:
        return number[0] == "0" and number.isnumeric()
    else:
        return False

def input_val(input, IfWord, IfNum):
    while input[0] == " ":
        input = input.replace(" ", "", 1)
            
    while input.count("  ") > 0:
        input = input.replace("  ", " ")

    tempvar = input.replace(" ", "")
    return (tempvar.isalpha() == IfWord or tempvar.isspace() or tempvar.isnumeric() == IfNum)\
        , input



# This is the start of the program
print("""

What would you like to do?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(1) Register Student  | Register a new student
(2) Student List      | View/edit student list
(3) Student Fee       | 
(4) Remove Student
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")

decision = str(input("Enter your option [1/2/3/4]: "))

while (input_val(decision, True, False)[0]) or decision not in ["1","2","3","4"]:
    decision = str(input("Invalid option, try again [1/2/3/4]: "))

if decision == "1":

    # Entering Name
    student_name = str(input("Name: "))
    while (input_val(student_name, False, True)[0]):
        print("Invalid input try again.")
        student_name = str(input("Name: "))

    student_name = input_val(student_name, False, True)[1]


    # Entering Age
    student_age = str(input("Age: ")).replace(" ","")
    while (input_val(student_age, True, False)[0]) or int(input_val(student_age, False, True)[1]) > 100:
        print("Invalid input try again.")
        student_age = str(input("Age: ")).replace(" ","")

    student_age = int(input_val(student_age, False, True)[1])


    # Entering Contact
    student_contact = str(input("Phone Number: ")).replace(" ","")
    while (input_val(student_contact, True, False)[0]) or phone_val(student_contact) == False:
        print("Invalid input try again.")
        student_contact = str(input("Phone Number: ")).replace(" ","")
    

    # Entering Month
    response_month = input("Enter the number of month: ")
    while (input_val(response_month, True, False)[0]) or response_month not in month:
        print("Invalid input try again.")
        response_month = str(input("Enter the number of month: ")).replace(" ","")


    # Entering Day
    response_day = input("Enter day of the week: ")


    # Entering Time
    session_time = input("Enter Number: ")

    add_student(student_name, student_age, student_contact, month[response_month], day[response_day], session_time)

    clear()
    print(student_data,"\n")
    print(student_schedule)