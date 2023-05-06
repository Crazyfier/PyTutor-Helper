import mymodule
import sqlite3

def registration():

    student_name = str(input("Name: "))
    while (mymodule.input_val(student_name, False, True)[0]):
        if student_name == "#cancel":
            return "n"
        print("Invalid input try again.")
        student_name = str(input("Name: "))

    student_name = str(mymodule.input_val(student_name, False, True)[1])


    # Entering Age
    student_age = str(input("Age: ")).replace(" ","")
    while (mymodule.input_val(student_age, True, False)[0]) or int(mymodule.input_val(student_age, False, True)[1]) > 50:
        if student_age == "#cancel":
            return "n"
        print("Invalid input. Exceed age limit.")
        student_age = str(input("Age: ")).replace(" ","")

    student_age = int(mymodule.input_val(student_age, False, True)[1])


    # Entering Contact
    student_contact = str(input("Phone Number: ")).replace(" ","")
    while (mymodule.input_val(student_contact, True, False)[0]) or mymodule.phone_val(student_contact) == False:
        if student_contact == "#cancel":
            return "n"
        print("Input 10-digit mobile number.")
        student_contact = str(input("Phone Number: ")).replace(" ","")


    # Entering Month
    student_month = str(input("Enter the number of month [1 - 12]: ")).replace(" ","")
    while (mymodule.input_val(student_month, True, False)[0]) or int(mymodule.input_val(student_month, True, False)[1]) not in mymodule.month:
        if student_month == "#cancel":
            return "n"
        print("Enter a number from 1 - 12.")
        student_month = str(input("Enter the number of month [1 -12]: ")).replace(" ","")

    student_month = int(mymodule.input_val(student_month, True, False)[1])

    # Entering Day
    student_day = str(input("Enter day of the week [1 - 7]: ")).replace(" ","")
    while (mymodule.input_val(student_day, True, False)[0]) or int(mymodule.input_val(student_day, True, False)[1]) not in mymodule.day:
        if student_day == "#cancel":
            return "n"
        print("Enter a number from 1 - 7.")
        student_day = str(input("Enter day of the week [1 - 7]: ")).replace(" ","")

    student_day = int(mymodule.input_val(student_day, True, False)[1])

    mymodule.clear()

    #Display Time Option
    conn = sqlite3.connect('Class_Schedule.db')
    cursor = conn.execute(f"SELECT class_no, time, teacher from {mymodule.day[student_day]}_class")
    print ("\x1B[4m  {:<1} |{:^15} |{:^19} \x1B[0m".format("", "Time", "Teacher"))

    #Classifying time and teacher into a dictionary to store in mymodule
    class_data = {}
    for row in cursor:
        class_data[row[0]] = row[1], row[2]
        print ("({:<1}) |{:^15} |{:^19}".format(row[0], row[1], row[2]))
    print("")

    # Entering Time
    student_time = str(input("Enter Number: ")).replace(" ","")
    while (mymodule.input_val(student_time, True, False)[0]) or int(mymodule.input_val(student_time, True, False)[1]) not in class_data:
        if student_time == "#cancel":
            return "n"
        print("I want you to think again.")
        student_time = str(input("Enter Number: ")).replace(" ","")
    
    student_time = int(mymodule.input_val(student_time, True, False)[1])

    # Calculating student fee based on the month and amount of week in the month
    # The fee is calculated by the week
    student_fee = 0

    mymodule.add_student(student_name, student_age, student_contact, (mymodule.month[student_month]).title(), (mymodule.day[student_day]).title(), class_data[student_time][1], class_data[student_time][2], student_fee)
    
    mymodule.clear()

    proceed = str(input("Would you like to add another student? [ y / n ]: ")).replace(" ","")
    while (mymodule.input_val(proceed, False, True)[0]) or str(mymodule.input_val(proceed, False, True)[1]) not in ["y", "n"]:
        print("Invaid input.")
        proceed = str(input("Would you like to add another student? [ y / n ]: ")).replace(" ","")

    return str(mymodule.input_val(proceed, False, True)[1])