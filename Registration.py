
from mymodule import *

def hey_new_people():

    clear()

    print("~~~~~Registration~~~~~\n")

    student_name = str(input("Name: "))
    while (input_val(student_name, False, True)[0]):
        if student_name == command_to_quit:
            return "n"
        print("Invalid input try again.")
        student_name = str(input("Name: "))

    student_name = str(input_val(student_name, False, True)[1]).capitalize()


    # Entering Age
    student_age = str(input("Age: ")).replace(" ","")
    while (input_val(student_age, True, False)[0]) or int(input_val(student_age, False, True)[1]) > 50:
        if student_age == command_to_quit:
            return "n"
        print("Invalid input. Exceed age limit.")
        student_age = str(input("Age: ")).replace(" ","")

    student_age = int(input_val(student_age, False, True)[1])


    # Entering Contact
    student_contact = str(input("Phone Number: ")).replace(" ","")
    while (input_val(student_contact, True, False)[0]) or phone_val(student_contact) == False:
        if student_contact == command_to_quit:
            return "n"
        print("Input 10-digit mobile number.")
        student_contact = str(input("Phone Number: ")).replace(" ","")


    # Entering Month
    student_month = str(input("Enter the number of month [1 - 12]: ")).replace(" ","")
    while (input_val(student_month, True, False)[0]) or int(input_val(student_month, True, False)[1]) not in month:
        if student_month == command_to_quit:
            return "n"
        print("Enter a number from 1 - 12.")
        student_month = str(input("Enter the number of month [1 -12]: ")).replace(" ","")

    student_month = int(input_val(student_month, True, False)[1])

    # Entering Day
    student_day = str(input("Enter day of the week [1 - 7]: ")).replace(" ","")
    while (input_val(student_day, True, False)[0]) or int(input_val(student_day, True, False)[1]) not in day:
        if student_day == command_to_quit:
            return "n"
        print("Enter a number from 1 - 7.")
        student_day = str(input("Enter day of the week [1 - 7]: ")).replace(" ","")

    student_day = int(input_val(student_day, True, False)[1])

    clear()

    #Display Time Option
    cursor = conn.execute(f"SELECT class_no, time, teacher from {day[student_day]}_class")
    print ("\x1B[4m  {:<1} |{:^15} |{:^19} \x1B[0m".format("", "Time", "Teacher"))

    #Classifying time and teacher into a dictionary to store in mymodule
    class_data = {}
    teacher = {}
    for row in cursor:
        class_data[row[0]] = row[1], row[2]
        teacher[row[0]] = row[2]
        print ("({:<1}) |{:^15} |{:^19}".format(row[0], row[1], row[2]))

    # Entering Time
    student_time = str(input("\nEnter Number: ")).replace(" ","")
    while (input_val(student_time, True, False)[0]) or int(input_val(student_time, True, False)[1]) not in class_data:
        if student_time == command_to_quit:
            return "n"
        print("I want you to think again.")
        student_time = str(input("Enter Number: ")).replace(" ","")
    
    student_time = int(input_val(student_time, True, False)[1])

    # Calculating student fee based on the month and amount of week in the month
    # The fee is calculated by the week
    student_fee = 0

    add_student(student_name, student_age, student_contact, (month[student_month]).title(), (day[student_day]).title(), class_data[student_time][0], teacher[student_time], student_fee)
    
    clear()

    proceed = str(input("Would you like to add another student? [ y / n ]: ")).replace(" ","")
    while (input_val(proceed, False, True)[0]) or str(input_val(proceed, False, True)[1]) not in ["y", "n"]:
        print("Invaid input.")
        proceed = str(input("Would you like to add another student? [ y / n ]: ")).replace(" ","")

    return str(input_val(proceed, False, True)[1])