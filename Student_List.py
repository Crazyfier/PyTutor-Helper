from mymodule import *

def oh_look_students():
    clear()
    
    cursor = conn.execute("SELECT rowid, name, age, contact, month, day, time, teacher from student_data")
    print ("\x1B[4m{:<3}|{:^30} |{:^5}|{:^11} |{:^10} |{:^13} |{:^15} |{:^42}| \x1B[0m".format("ID", "Name", "Age", "Contact", "Month", "Day", "Time", "Teacher"))

    id = {}
    for row in cursor:
        id[row[0]] = row[1], row[2], row[3], row[4], row[5], row[6], row[7]
        print ("{:<3}| {:<30}| {:<3} | {:<11}| {:<10}| {:<13}| {:<15}| {:<41}|".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

    print(textwrap.dedent("""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    (1) Edit Student Info
    (2) Remove Student

    [0] Back
    """))

    decision = str(input("Enter your option [0/1/2]: ")).replace(" ","")
    while (input_val(decision, True, False)[0]) or int(input_val(decision, True, False)[1]) not in [0, 1, 2]:
        if decision == command_to_quit:
            return "n"
        decision = str(input("Invalid option, try again [0/1/2]: ")).replace(" ","")
    
    decision = int(input_val(decision, True, False)[1])

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    if len(id) == 0:
        input("List is empty. Press any key to return.")
        return "n"
    
    elif decision == 0:
        return "n"
    
    else:
        student_number = str(input("Enter student number: ")).replace(" ","")
        while (input_val(student_number, True, False)[0]) or int(input_val(student_number, True, False)[1]) not in id:
            if student_number == command_to_quit:
                return "y"
            student_number = str(input("Invalid student number, try again: ")).replace(" ","")

        student_number = int(input_val(student_number, True, False)[1])

    if decision == 1:

        print(textwrap.dedent("""
        (1) Name       (5) Day
        (2) Age        (6) Time
        (3) Contact    (7) Teacher
        (4) Month      
        """))
        target = str(input("Enter the number of the category one wish to change: ")).replace(" ","")
        
        category = {1 : "name", 2 : "age", 3 : "contact", 4 : "month", 5 : "day", 6 : "time", 7 : "teacher"}
        while (input_val(target, True, False)[0]) or int(input_val(target, True, False)[1]) not in category:
            if target == command_to_quit:
                return "y"
            target = str(input("Invalid option, its up there: "))

        target = category[int(input_val(target, True, False)[1])]

        if target == "name":

            correction = str(input("Enter change: "))
            while (input_val(correction, False, True)[0]):
                if correction == command_to_quit:
                    return "y"
                correction = str(input("Input contains invalid characters, try again: "))

            name = str(input_val(correction, False, True)[1])

            update_student(student_number, target, name)

        elif target == "age":

            correction = str(input("Age: ")).replace(" ","")
            while (input_val(correction, True, False)[0]) or int(input_val(correction, False, True)[1]) > 50:
                if correction == command_to_quit:
                    return "y"
                correction = str(input("Input only accepts numbers: ")).replace(" ","")

            age = int(correction)

            update_student(student_number, target, age)

        elif target == "contact":

            contact = str(input("Phone Number: ")).replace(" ","")
            while (input_val(contact, True, False)[0]) or phone_val(contact) == False:
                if contact == command_to_quit:
                    return "y"
                contact = str(input("Input 10-digit mobile number: ")).replace(" ","")


            update_student(student_number, target, contact)

        elif target == "month":

            correction = str(input("Enter the number of month [1 - 12]: ")).replace(" ","")
            while (input_val(correction, True, False)[0]) or int(input_val(correction, True, False)[1]) not in month:
                if correction == command_to_quit:
                    return "y"
                correction = str(input("Enter a number from 1 - 12 : ")).replace(" ","")

            correction = int(input_val(correction, True, False)[1])

            update_student(student_number, target, month[correction].title())

        elif target == "day":

            correction = str(input("Enter day of the week [1 - 7]: ")).replace(" ","")
            while (input_val(correction, True, False)[0]) or int(input_val(correction, True, False)[1]) not in day:
                if correction == command_to_quit:
                    return "y"
                correction = str(input("Enter a number from 1 - 7 : ")).replace(" ","")

            correction = int(input_val(correction, True, False)[1])

            update_student(student_number, target, day[correction].title())


        elif target == "time":

            # Getting a specific data from the data base that is the students schedule day
            cursor = conn.cursor()
            cursor.execute(f"SELECT * from student_data where rowid = {student_number}")
            record = cursor.fetchone()

            cursor = conn.execute(f"SELECT class_no, time, teacher from {record[4].lower()}_class")
            print ("\x1B[4m  {:<1} |{:^15} |{:^19} \x1B[0m".format("", "Time", "Teacher"))


            #Classifying time and teacher into a dictionary to store in mymodule
            class_data = {}
            for row in cursor:
                class_data[row[0]] = row[1], row[2]
                print ("({:<1}) |{:^15} |{:^19}".format(row[0], row[1], row[2]))
            print("")


            # Entering Time
            correction = str(input("Enter Number: ")).replace(" ","")
            while (input_val(correction, True, False)[0]) or int(input_val(correction, True, False)[1]) not in class_data:
                print("I want you to think again.")
                correction = str(input("Enter Number: ")).replace(" ","")
            
            correction = int(input_val(correction, True, False)[1])

            update_student(student_number, "teacher", class_data[correction][1])

            update_student(student_number, target, class_data[correction][0])

    elif decision == 2:

        confirmation = str(input("Do you want to remove this student? [y / n]: ")).replace(" ","")
        while (input_val(confirmation, False, True)[0]) or str(input_val(confirmation, False, True)[1]) not in ("y","n"):
            confirmation = str(input("... : ")).replace(" ","")
        
        confirmation = str(input_val(confirmation, False, True)[1])

        if confirmation in (command_to_quit, "n"):
            return "y"
        else:      
            delete_student(student_number)
            return "y"