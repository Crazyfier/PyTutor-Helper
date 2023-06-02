from mymodule import *

# Used for displaying the registraition title
def registration_title():
    clear()
    print("")
    print("{:^60}".format(f"-------- Registration --------"))
    print("{:^60}".format(f"[  #back to return  ]\n"))



# PROMPT USER TO INPUT THEIR NAME  
def input_student_name():
    global student_name
    registration_title()
    student_name = str(input("Name : "))
    while input_val(student_name, False, True)[0]:
        registration_title()

        if student_name == command_to_return:
            return "n"
        elif student_name == command_to_quit:
            end_screen()
        elif student_name.isspace() or student_name == "":
            print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
        else:
            print("{:^60}".format("[  Special characters or numbers detected, try again.  ]\n"))
            
        student_name = str(input("Name : "))

    student_name = str(input_val(student_name, False, True)[1]).lower()

# PROMPT USER TO INPUT THEIR AGE
def input_student_age():
    global student_age
    registration_title()
    print(f"Name : {student_name.capitalize()}")
    student_age = str(input("Age  : ")).replace(" ","")
    while input_val(student_age, True, False)[0] or int(input_val(student_age, False, True)[1]) > 50:
        registration_title()
        print(f"Name : {student_name.capitalize()}\n")

        if student_age == command_to_return:
            return "n"
        elif student_age == command_to_quit:
            end_screen()
        elif student_age.isspace() or student_age == "":
            print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
        elif input_val(student_age, True, False)[0]:
            print("{:^60}".format("[  Special characters or alphbets detected, try again.  ]\n"))
        elif int(input_val(student_age, False, True)[1]) > 50:
            print("{:^60}".format("[  Exceed age limit 50 years old, try again.  ]\n"))
            
        student_age = str(input("Age  : ")).replace(" ","")

    student_age = int(input_val(student_age, False, True)[1])

# PROMPT USER TO INPUT THEIR MOBILE NUMBER
def input_student_contact():
    global student_contact

    registration_title()
    print(f"Name         : {student_name.capitalize()}")
    print(f"Age          : {student_age}")
    student_contact = str(input("Phone Number : ")).replace(" ","")
    while input_val(student_contact, True, False)[0] or phone_val(student_contact) == False:
        registration_title()
        print(f"Name         : {student_name.capitalize()}")
        print(f"Age          : {student_age}\n")

        if student_contact == command_to_return:
            return "n"
        elif student_contact == command_to_quit:
            end_screen()
        elif student_contact.isspace() or student_contact == "":
            print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
        elif input_val(student_contact, True, False)[0]:
            print("{:^60}".format("[  Special characters or alphbets detected, try again.  ]\n"))
        elif phone_val(student_contact) == False:
            print("{:^60}".format("[  Input must be 10-digit and begin with 0.  ]"))
            print("{:^60}".format("[   eg. 0XX XXX XXXX   ]\n"))
        
        student_contact = str(input("Phone Number : ")).replace(" ","")

# PROMPT USER OF THE MONTH THEY WISH TO ATTEND
def input_student_month():
    global student_month

    registration_title()
    print(f"Name         : {student_name.capitalize()}")
    print(f"Age          : {student_age}")
    print(f"Phone Number : {student_contact}")

    print(textwrap.dedent("""
    ~~~~~~~~~~~~~~~~~~~~~~ Select a month ~~~~~~~~~~~~~~~~~~~~~~
      (1) January    (5) April   (7) July        (10) October
      (2) February   (6) May     (8) August      (11) November
      (3) March      (7) June    (9) September   (12) December
    """))

    student_month = str(input("Enter number of the month : ")).replace(" ","")

    # Validation for user input
    while input_val(student_month, True, False)[0] or int(input_val(student_month, True, False)[1]) not in month:
        registration_title()
        print(f"Name         : {student_name.capitalize()}")
        print(f"Age          : {student_age}")
        print(f"Phone Number : {student_contact}")

        print(textwrap.dedent("""
        ~~~~~~~~~~~~~~~~~~~~~~ Select a month ~~~~~~~~~~~~~~~~~~~~~~
          (1) January    (4) April   (7) July        (10) October
          (2) February   (5) May     (8) August      (11) November
          (3) March      (6) June    (9) September   (12) December
        """))

        if student_month == command_to_return:
            return "n"
        elif student_month == command_to_quit:
            end_screen()
        elif student_month.isspace() or student_month == "":
            print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
        elif input_val(student_month, True, False)[0]:
            print("{:^60}".format("[  Special characters or alphbets detected, try again.  ]\n"))
        else:
            print("{:^60}".format("[  Enter numbers between 1 and 12, try again.  ]\n"))
        
        student_month = str(input("Enter number of the month : ")).replace(" ","")
        
    student_month = int(input_val(student_month, True, False)[1])

# PROMPT USER OF THE DAY THEY WISH TO ATTEND
def input_student_day():
    global student_day 
    valid_day = []
    for row in day:
        cursor = conn.execute(f"SELECT class_no, start, end, teacher from {day[row]}_class")
        if len(list(cursor)) != 0:
            valid_day.append(row)
    
    registration_title()
    print(f"Name         : {student_name.capitalize()}")
    print(f"Age          : {student_age}")
    print(f"Phone Number : {student_contact}")
    print(f"Month        : {month[student_month].capitalize()}")

    print("\n~~~~~~~~~~~~~~~~~~~~~~~ Select a Day ~~~~~~~~~~~~~~~~~~~~~~~")
    line_length = 0
    for row in valid_day:
        day_with_number = f" ({row}) {day[row].capitalize()}"
        day_length = len(day_with_number)

        if line_length + day_length > 85:
            print()
            line_length = 0

        padding = ' ' * (13 - day_length)
        print(f"{day_with_number}{padding}", end=' ')
        line_length += day_length + 10

    student_day = str(input("\n\nEnter number of the day : ")).replace(" ","")
    while input_val(student_day, True, False)[0] or int(input_val(student_day, True, False)[1]) not in valid_day:
        registration_title()
        print(f"Name         : {student_name.capitalize()}")
        print(f"Age          : {student_age}")
        print(f"Phone Number : {student_contact}")
        print(f"Month        : {month[student_month].capitalize()}")

        print("\n~~~~~~~~~~~~~~~~~~~~~~~ Select a Day ~~~~~~~~~~~~~~~~~~~~~~~")
        line_length = 0
        for row in valid_day:
            day_with_number = f" ({row}) {day[row].capitalize()}"
            day_length = len(day_with_number)

            if line_length + day_length > 85:
                print()
                line_length = 0

            padding = ' ' * (13 - day_length)
            print(f"{day_with_number}{padding}", end=' ')
            line_length += day_length + 10
        print("\n")
        if student_day == command_to_return:
            return "n"
        elif student_day == command_to_quit:
            end_screen()
        elif student_day.isspace() or student_day == "":
            print("{:^60}".format("[  Come on you didn't even type, try again.  ]"))
        elif input_val(student_day, True, False)[0]:
            print("{:^60}".format("[  Special characters or alphbets detected, try again.  ]"))
        elif int(input_val(student_day, True, False)[1]) not in valid_day:
            print("{:^60}".format("[  No classes on selected day, try again.  ]"))

        student_day = str(input("\nEnter number of the day : ")).replace(" ","")
        
    student_day = int(input_val(student_day, True, False)[1])

# SHOW USER THE LIST OF CLASSES BASED ON THE DAY THEY PREVIOUSLY INPUTED
# ALSO PROMPT USER TO INPUT CLASS NUMBER
def input_student_class_no():
    global student_class_no

    registration_title()
    print("{:^60}".format(f"[{day[student_day].title()}]"))
    
    class_no_for_validation = []
    if len(list(conn.execute(f"SELECT class_no, start, end, teacher from {day[student_day]}_class"))) == 0:
        print("")
        print("{:^60}".format("[  List is empty  ]\n"))
        input("Press any key to return.")
        clear()
        print("Please select another day.\n")
        
        return True
    else:
        print("____________________________________________________________")
        print ("\x1B[4m|{:^11}|{:^20}|{:^25}|\x1B[0m".format("Class No.", "Time", "Teacher"))
        
        for row in conn.execute(f"SELECT class_no, start, end, teacher from {day[student_day]}_class ORDER BY class_no ASC"):
            class_no_for_validation.append(row[0])
            time = row[1] + " - " + row[2]
            print ("|{:^11}|{:^20}|{:^25}| ".format(row[0], time, row[3]))

        print(overline * 60)

        print(f"Name         : {student_name.capitalize()}")
        print(f"Age          : {student_age}")
        print(f"Phone Number : {student_contact}")
        print(f"Month        : {month[student_month].capitalize()}")
        print(f"Day          : {day[student_day].capitalize()}")

        student_class_no = str(input("\nEnter class number: ")).replace(" ","")
        while input_val(student_class_no, True, False)[0] or int(input_val(student_class_no, True, False)[1]) not in class_no_for_validation:
            registration_title()

            if student_class_no == command_to_return:
                return "n"
            elif student_class_no == command_to_quit:
                end_screen()
            elif student_class_no.isspace() or student_class_no == "":
                print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
            elif input_val(student_class_no, True, False)[0]:
                print("{:^60}".format("[  Special characters or alphbets detected, try again.  ]\n"))
            else:
                print("{:^60}".format("[  Type the available class number.  ]\n"))
            
            print("{:^60}".format(f"[{day[student_day].title()}]"))
            print("____________________________________________________________")
            print ("\x1B[4m|{:^11}|{:^20}|{:^25}|\x1B[0m".format("Class No.", "Time", "Teacher"))
            
            for row in conn.execute(f"SELECT class_no, start, end, teacher from {day[student_day]}_class ORDER BY class_no ASC"):
                class_no_for_validation.append(row[0])
                time = row[1] + " - " + row[2]
                print ("|{:^11}|{:^20}|{:^25}| ".format(row[0], time, row[3]))

            print(overline * 60)

            print(f"Name         : {student_name.capitalize()}")
            print(f"Age          : {student_age}")
            print(f"Phone Number : {student_contact}")
            print(f"Month        : {month[student_month].capitalize()}")
            print(f"Day          : {day[student_day].capitalize()}")
            
            student_class_no = str(input("\nEnter class number: ")).replace(" ","")

        student_class_no = int(input_val(student_class_no, True, False)[1])

        return False



# Main part of the registration function
def Registration_Page():
    resume_input = "y"
    while resume_input == "y":
        clear()
        count = 0
        for row in day:
            if len(list(conn.execute(f"SELECT class_no from {day[row]}_class"))) != 0:
                count += 1
        if count == 0:
            registration_title()
            input("[ There are no classes available to register the student. ]\n\n           [ Please add a class to proceed. ]\n\n               PRESS ANY KEY TO RETURN")
        if input_student_name() == "n" or input_student_age() == "n" or input_student_contact() == "n" or input_student_month() == "n":
            resume_input = "n"
        else:
            empty = True
            while empty == True:
                if input_student_day() == "n":
                    resume_input = "n"
                    break
                else:
                    value = input_student_class_no()
                    if value == "n":
                        resume_input = "n"
                        break
                    elif type(value) == bool:
                        empty = value
            if resume_input != "n":
                current_fee = conn.execute("SELECT fee FROM internal_data").fetchone()[0]
                current_year = conn.execute("SELECT year FROM internal_data").fetchone()[0]

                count = 0
                for row in range (1, calendar.monthrange(datetime.date.today().year, student_month)[1] + 1):
                    if datetime.date(current_year, student_month, row).isoweekday() == student_day:
                        count += 1

                student_fee = count * current_fee

                cursor = conn.execute("SELECT student_id FROM student_data")
                accumulated_student_id = []
                for row in cursor:
                    accumulated_student_id.append(row[0])
                student_id = random.randint(1,200)
                while student_id in accumulated_student_id:
                    student_id = random.randint(1,200)

                add_student(student_id, student_name.capitalize(), student_age, student_contact, day[student_day], student_class_no, student_fee, student_month)
                
                clear()
                registration_title()
                proceed = str(input("Would you like to add another student? [ y / n ]: ")).replace(" ","")
                while input_val(proceed, False, True)[0] or str(input_val(proceed, False, True)[1]) not in ["y", "n"]:
                    registration_title()
                    if proceed == command_to_return:
                        return 
                    elif student_class_no == command_to_quit:
                        end_screen()
                    elif student_class_no.isspace() or student_class_no == "":
                        print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
                    elif input_val(proceed, False, True)[0]:
                        print("{:^60}".format("[  INVALID INPUT  ]"))
                    
                    proceed = str(input("Would you like to add another student? [ y / n ]: ")).replace(" ","")

                resume_input = str(input_val(proceed, False, True)[1])