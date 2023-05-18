from mymodule import *

def display_student_list():
    clear()
    if len(conn.execute("SELECT student_id FROM student_data").fetchall()) == 0:
        print("{:^184}".format("[  Student List  ]"))  
        print("{:^184}".format("[  Yup, it's empty. What to do?  ]"))  
    else:
        print("{:^184}".format("[  Student List  ]"))     
        print ("\x1B[4m{:^183}_\x1B[0m".format(""))
        print ("\x1B[4m|{:<3}|{:^31}|{:^5}|{:^12}|{:^12}|{:^13}|{:^19}|{:^18}| {:^60}|\x1B[0m".format("ID", "Name", "Age", "Contact", "Fee", "Day", "Time", "Teacher", "Month"))
        for row in conn.execute("SELECT student_id, name, day, class_no FROM student_data"):
            for row in conn.execute(f"SELECT student_id, name, age, contact, day, fee, start, end, teacher FROM student_data LEFT OUTER JOIN {row[2]}_class ON student_data.class_no = {row[2]}_class.class_no ORDER BY student_id ASC"):
                student_id = row[0]
                name = row[1]
                age = row[2]
                contact = row[3]
                attend_day = row[4]
                fee = row[5]

                if row[6] == None and row [7] == None:
                    time = "No Time Available"
                    teacher = "No teacher"
                else:
                    time = row[6] + " - " + row[7]
                    teacher = row[8]
                

                attend_month = []
                for row in month:
                    if list(conn.execute(f"SELECT student_id, name FROM {month[row]} where name = '{name}'")) != []:
                        attend_month.append((month[row])[:3].capitalize())
                attend_month = ', '.join(attend_month)

                print ("| {:<2}| {:<30}| {:<3} |{:^12}| {:<11}|{:^13}| {:^17} |{:^18}| {:<60}|".format(student_id, name, age, contact, locale.currency(fee), attend_day.capitalize(), time, teacher, attend_month))

        print(overline*184)




def edit_page():
    def editing_name():
        print("{:^60}".format(f"Currently Editing student : {student}\n"))
        print("{:^60}".format(f"[  Type #back to return  ]\n"))
        print("{:^60}".format("-------- Editing Name --------\n"))
        student_name = str(input("Name : "))
        while input_val(student_name, False, True)[0]:
            display_student_list()

            print("{:^60}".format(f"Currently Editing student : {student}\n"))
            print("{:^60}".format(f"[  Type #back to return  ]\n"))
            print("{:^60}".format("-------- Editing Name --------\n"))

            if student_name == command_to_return:
                return "y"
            elif student_name == command_to_quit:
                end_screen()
            elif student_name.isspace() or student_name == "":
                print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
            else:
                print("{:^60}".format("[  Special characters or numbers detected, try again.  ]\n"))
                
            student_name = str(input("Name : "))

        student_name = str(input_val(student_name, False, True)[1]).lower()

    def editing_age():
        print("{:^60}".format(f"Currently Editing student : {student}\n"))
        print("{:^60}".format("--------- Editing Age --------\n"))
        print("{:^60}".format(f"[  Type #back to return  ]\n"))
        student_age = str(input("Age : ")).replace(" ","")
        while input_val(student_age, True, False)[0] or int(input_val(student_age, False, True)[1]) > 50:
            display_student_list()

            print("{:^60}".format(f"Currently Editing student : {student}\n"))
            print("{:^60}".format("--------- Editing Age --------\n"))
            print("{:^60}".format(f"[  Type #back to return  ]\n"))

            if student_age == command_to_return:
                return "y"
            elif student_age == command_to_quit:
                end_screen()
            elif student_age.isspace() or student_age == "":
                print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
            elif input_val(student_age, True, False)[0]:
                print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]\n"))
            elif int(input_val(student_age, False, True)[1]) > 50:
                print("{:^60}".format("[  Exceed age limit 50 years old, try again.  ]\n"))
                

            student_age = str(input("Age : ")).replace(" ","")

        student_age = int(input_val(student_age, False, True)[1])

    def editing_contact():
        print("{:^60}".format(f"Currently Editing student : {student}\n"))
        print("{:^60}".format("------- Editing Contact ------\n"))
        print("{:^60}".format(f"[  Type #back to return  ]\n"))
        student_contact = str(input("Phone Number : ")).replace(" ","")
        while input_val(student_contact, True, False)[0] or phone_val(student_contact) == False:
            display_student_list()

            print("{:^60}".format(f"Currently Editing student : {student}\n"))
            print("{:^60}".format("------- Editing Contact ------\n"))
            print("{:^60}".format(f"[  Type #back to return  ]\n"))
            if student_contact == command_to_return:
                return "y"
            elif student_contact == command_to_quit:
                end_screen()
            elif student_contact.isspace() or student_contact == "":
                print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
            elif input_val(student_contact, True, False)[0]:
                print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]\n"))
            elif phone_val(student_contact) == False:
                print("{:^60}".format("[  Input must be 10-digit and begin with 0.  ]\n"))
                print("{:^60}".format("[   eg. 0XX XXX XXXX   ]\n"))
            
            student_contact = str(input("Phone Number : ")).replace(" ","")

    def editing_day():
        global student_day
        def display_class_list(target_day):
            global class_no_for_validation

            clear()
            print("{:^60}".format(f"{day[target_day].title()}"))
            print("____________________________________________________________")
            print ("\x1B[4m|{:^11}|{:^20}|{:^25}|\x1B[0m".format("Class No.", "Time", "Teacher"))
            
            class_no_for_validation = []
            for row in conn.execute(f"SELECT class_no, start, end, teacher from {day[target_day]}_class ORDER BY class_no ASC"):
                class_no_for_validation.append(row[0])
                time = row[1] + " - " + row[2]
                print ("|{:^11}|{:^20}|{:^25}| ".format(row[0], time, row[3]))
            print(overline * 60)

        valid_day = []
        print("{:^60}".format(f"Currently Editing student : {student}\n"))
        print("{:^60}".format("--------- Editing Day --------\n"))
        print("{:^60}".format(f"[  Type #back to return  ]"))
        for row in day:
            cursor = conn.execute(f"SELECT class_no, start, end, teacher from {day[row]}_class")
            if len(list(cursor)) != 0:
                valid_day.append(row)

        print("~~~~~~~~~~~~~~~~~~~~~~~ Select a Day ~~~~~~~~~~~~~~~~~~~~~~~")
        for row in valid_day:
            print(f"({row}) {day[row].title()}")

        student_day = str(input("\nEnter number of the day : ")).replace(" ","")
        while input_val(student_day, True, False)[0] or int(input_val(student_day, True, False)[1]) not in valid_day:
            
            display_student_list()

            print("{:^60}".format(f"Currently Editing student : {student}\n"))
            print("{:^60}".format("--------- Editing Day --------\n"))
            print("{:^60}".format(f"[  Type #back to return  ]\n"))
            if student_day == command_to_return:
                return "y"
            elif student_day == command_to_quit:
                end_screen()
            elif student_day.isspace() or student_day == "":
                print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
            elif input_val(student_day, True, False)[0]:
                print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]\n"))
            else:
                if int(input_val(student_day, True, False)[1]) in range(1,8) and int(input_val(student_day, True, False)[1]) not in valid_day:
                    print("{:^60}".format("[  No classes available for selected day, try again.  ]\n"))
                else:
                    print("{:^60}".format("[  Enter numbers between 1 and 7, try again.  ]\n"))

            print("~~~~~~~~~~~~~~~~~~~~~~~ Select a Day ~~~~~~~~~~~~~~~~~~~~~~")
            for row in valid_day:
                print(f"  ({row}) {day[row].title()}")

            student_day = str(input("Enter number of the day : ")).replace(" ","")
            
        student_day = int(input_val(student_day, True, False)[1])

        print("{:^60}".format(f"Currently Editing student : {student}\n"))
        display_class_list(student_day)
        print("{:^60}".format(f"[  Type #back to return  ]"))       
        student_class_no = str(input("\nEnter class number: ")).replace(" ","")
        while input_val(student_class_no, True, False)[0] or int(input_val(student_class_no, True, False)[1]) not in class_no_for_validation:
            print("{:^60}".format(f"Currently Editing student : {student}\n"))
            display_class_list(student_day)
            print("{:^60}".format(f"[  Type #back to return  ]\n"))
            if student_class_no == command_to_return:
                return "y"
            elif student_class_no == command_to_quit:
                end_screen()
            elif student_class_no.isspace() or student_class_no == "":
                print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
            elif input_val(student_class_no, True, False)[0]:
                print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]\n"))
            elif int(input_val(student_class_no, True, False)[1]) not in class_no_for_validation:
                print("{:^60}".format("[  Type the available class number.  ]\n"))
            
            student_class_no = str(input("Enter class number: ")).replace(" ","")

        student_class_no = int(input_val(student_class_no, True, False)[1])

    def editing_time():

        def display_class_list(target_day):
            global class_no_for_validation

            clear()
            print("{:^60}".format(f"{target_day[0].title()}"))
            print("____________________________________________________________")
            print ("\x1B[4m|{:^11}|{:^20}|{:^25}|\x1B[0m".format("Class No.", "Time", "Teacher"))
            
            class_no_for_validation = []
            for row in conn.execute(f"SELECT class_no, start, end, teacher from {target_day[0]}_class ORDER BY class_no ASC"):
                class_no_for_validation.append(row[0])
                time = row[1] + " - " + row[2]
                print ("|{:^11}|{:^20}|{:^25}| ".format(row[0], time, row[3]))

            print(overline * 60)

        edit_day = []
        for row in conn.execute(f"SELECT day from student_data where student_id = {student_number}"):
            edit_day.append(row[0])
        print("{:^60}".format(f"Currently Editing student : {student}\n"))
        if len(list(conn.execute(f"SELECT class_no, start, end, teacher from {edit_day[0]}_class"))) == 0:
            clear()
            print("{:^60}".format(f"[  No class on {edit_day[0].title()}, please change to another day  ]\n"))
            input("{:^60}".format("PRESS ANY KEY TO CONTINUE"))

        else:
            print("{:^60}".format(f"Currently Editing student : {student}\n"))
            display_class_list(edit_day)
            print("{:^60}".format(f"[  Type #back to return  ]"))       
            student_class_no = str(input("\nEnter class number: ")).replace(" ","")
            while input_val(student_class_no, True, False)[0] or int(input_val(student_class_no, True, False)[1]) not in class_no_for_validation:
                print("{:^60}".format(f"Currently Editing student : {student}\n"))
                display_class_list(edit_day)
                print("{:^60}".format(f"[  Type #back to return  ]\n"))
                if student_class_no == command_to_return:
                    return "y"
                elif student_class_no == command_to_quit:
                    end_screen()
                elif student_class_no.isspace() or student_class_no == "":
                    print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
                elif input_val(student_class_no, True, False)[0]:
                    print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]\n"))
                elif int(input_val(student_class_no, True, False)[1]) not in class_no_for_validation:
                    print("{:^60}".format("[  Type the available class number.  ]\n"))
                
                student_class_no = str(input("Enter class number: ")).replace(" ","")

            student_class_no = int(input_val(student_class_no, True, False)[1])

    def editing_month():
        wish_to_continue = "y"
        while wish_to_continue == "y":
            display_student_list()
            print("{:^60}".format(f"Currently Editing student : {student}"))
            print(textwrap.dedent("""
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            (1) Add student to month
            (2) Remove student from month
            
            [0] Back
            """))

            decision = str(input("Enter your option : ")).replace(" ","")
            while input_val(decision, True, False)[0] or int(input_val(decision, True, False)[1]) not in range(0,3):
                display_student_list()
                print("{:^60}".format(f"Currently Editing student : {student}"))
                print(textwrap.dedent("""\
                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                (1) Add student to month
                (2) Remove student from month
                
                [0] Back
                """))
                if decision == command_to_return:
                    return "y"
                elif decision ==  command_to_quit:
                    end_screen() 
                elif decision.isspace() or decision == "":
                    print("{:^60}".format("[  Come on you didn't even type, try again.  ]"))
                elif input_val(decision, True, False)[0]:
                    print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]"))
                elif int(input_val(decision, True, False)[1]) not in range(0,3):
                    print("{:^60}".format("[  Type between 0 - 2, try again.  ]"))

                decision = str(input("\nEnter your option : ")).replace(" ","")
            
            decision = int(input_val(decision, True, False)[1])

            if decision == 1:
                display_student_list()
                print("{:^60}".format(f"Currently Editing student : {student}\n"))
                print("{:^60}".format("------ Adding into month -----"))
                print(textwrap.dedent("""
                ~~~~~~~~~~~~~~~~~~~~~~ Select a month ~~~~~~~~~~~~~~~~~~~~~~
                  (1) January    (5) April   (7) July        (10) October
                  (2) February   (6) May     (8) August      (11) November
                  (3) March      (7) June    (9) September   (12) December
                """))

                student_month = str(input("Enter number of the month : ")).replace(" ","")
                in_month = []
                for row in month:
                    if list(conn.execute(f"SELECT student_id, name FROM {month[row]} where student_id = {student_number}")) != []:
                        in_month.append(row)
            
                while input_val(student_month, True, False)[0] or int(input_val(student_month, True, False)[1]) not in month or int(input_val(student_month, True, False)[1]) in in_month:
                    display_student_list()
                    print("{:^60}".format(f"Currently Editing student : {student}\n"))
                    print("{:^60}".format("------ Adding into month -----"))
                    print(textwrap.dedent("""
                    ~~~~~~~~~~~~~~~~~~~~~~ Select a month ~~~~~~~~~~~~~~~~~~~~~~
                      (1) January    (5) April   (7) July        (10) October
                      (2) February   (6) May     (8) August      (11) November
                      (3) March      (7) June    (9) September   (12) December
                    """))
                    if student_month == command_to_return:
                        return "y"
                    elif student_month == command_to_quit:
                        end_screen()
                    elif student_month.isspace() or student_month == "":
                        print("{:^60}".format("[  Come on you didn't even type, try again.  ]"))
                    elif input_val(student_month, True, False)[0]:
                        print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]\n"))
                    elif int(input_val(student_month, True, False)[1]) in in_month:
                        print("{:^60}".format(f"[  Already added to {month[int(student_month)].title()}, try again.  ]"))
                    elif int(input_val(student_month, True, False)[1]) not in month:
                        print("{:^60}".format("[  Enter numbers between 1 and 12, try again.  ]"))

                    student_month = str(input("\nEnter number of the month : ")).replace(" ","")
                student_month = int(input_val(student_month, True, False)[1])
                
                temp_student_info = []
                day_category = {"monday" : 1, "tuesday" : 2, "wednesday" : 3, "thursday" : 4, "friday" : 5, "saturday" : 6, "sunday" : 7}
                for row in conn.execute(f"SELECT day, fee FROM student_data where student_id = {student_number}"):
                    temp_student_info.append(row[0])
                    temp_student_info.append(row[1])
                
                count = 0
                for row in range (1, calendar.monthrange(datetime.date.today().year, student_month)[1] + 1):
                    if datetime.date(current_year, student_month, row).isoweekday() == day_category[temp_student_info[0]]:
                        count += 1
                
                fee = temp_student_info[1] + (count * current_fee)
                input(fee)
                # name = conn.execute(f"SELECT name from student_data where student_id = {student_number}")
                # conn.execute(f"INSERT INTO {month[student_month]}(student_id, name) VALUES ({student_number}, '{name}')")
                # conn.commit()
            elif decision == 2:
                return "y"

            wish_to_continue = str(input("Would you like to add into another month? [ y / n ]: ")).replace(" ","")
            while (input_val(wish_to_continue, False, True)[0]) or str(input_val(wish_to_continue, False, True)[1]) not in ["y", "n"]:
                if wish_to_continue == command_to_return:
                    return "y"
                elif wish_to_continue == command_to_quit:
                    end_screen()
                elif wish_to_continue.isspace() or wish_to_continue == "":
                    print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
                elif input_val(wish_to_continue, False, True)[0]:
                    print("{:^60}".format("[  Special characters or numbers detected, try again.  ]\n"))
                elif str(input_val(wish_to_continue, False, True)[1]) not in ("y","n"):
                    print("{:^60}".format("[  Type either y or n, try again.  ]\n"))

                wish_to_continue = str(input("Do you want to make another change? [y / n] : ")).replace(" ","")

    def editing_fee():
        print(textwrap.dedent("""\
        
        (1) Pay
        (2) Add additional payment
        """))

        decision = str(input("Enter your option : ")).replace(" ","")
        while input_val(decision, True, False)[0] or int(input_val(decision, True, False)[1]) not in range(0,3):
            display_student_list()

            print(textwrap.dedent("""\
            
            (1) Pay
            (2) Add additional payment
            """))

            if decision == command_to_return:
                return "y"
            elif decision.isspace() or decision == "":
                print("{:^60}".format("[  Come on you didn't even type, try again.  ]"))
            elif input_val(decision, True, False)[0]:
                print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]\n"))
            elif int(input_val(decision, True, False)[1]) not in range(0,3):
                print("{:^60}".format("[  Type either 1 or 2, try again.  ]\n"))

            decision = str(input("Enter your option : ")).replace(" ","")

        
        decision = int(input_val(decision, True, False)[1])

        new_fee = str(input("Enter in new fee (numbers only) : ")).replace(" ","")
        while isfloat(new_fee) == False:
            clear()
            print("{:^60}".format(f"Current fee is {locale.currency(current_fee)} per session.\n"))

            if new_fee == command_to_return:
                return "y"
            elif new_fee.isspace() or new_fee == "":
                print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
            elif isfloat(new_fee):
                print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]\n"))
                
            new_fee = str(input("Enter in new fee (numbers only) : ")).replace(" ","")

        new_fee = float(input_val(new_fee, False, True)[1])

    def change_additional_info():
        display_student_list()
        print("{:^60}".format(f"Currently Editing student : {student}\n"))
        add_another_student = str(input("Do you want to make another change? [y / n] : ")).replace(" ","")
        while input_val(add_another_student, False, True)[0] or str(input_val(add_another_student, False, True)[1]) not in ("y","n"):
            display_student_list()
            print("{:^60}".format(f"Currently Editing student : {student}\n"))

            if add_another_student == command_to_return:
                return "y"
            elif add_another_student == command_to_quit:
                end_screen()
            elif add_another_student.isspace() or add_another_student == "":
                print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
            elif input_val(add_another_student, False, True)[0]:
                print("{:^60}".format("[  Special characters or numbers detected, try again.  ]\n"))
            elif str(input_val(add_another_student, False, True)[1]) not in ("y","n"):
                print("{:^60}".format("[  Type either y or n, try again.  ]\n"))

            add_another_student = str(input("Do you want to make another change? [y / n] : ")).replace(" ","")
        return add_another_student

    student_list_edit_page = "y"
    while student_list_edit_page == "y":
        display_student_list()

        print("{:^60}".format(f"Currently Editing student : {student}\n"))  
        print("{:^60}".format("[  Will only change selected category  ]"))  
        print(textwrap.dedent("""\
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            (1) Name   (3) Contact   (5) Time    (7) Month
            (2) Age    (4) Day       (6) Fee 
        """))
        
        target = str(input("Input category number : ")).replace(" ","")
        
        while input_val(target, True, False)[0] or int(input_val(target, True, False)[1]) not in range(1,8):
            display_student_list()
            print("{:^60}".format(f"Currently Editing student : {student}\n"))  
            print("{:^60}".format("[  Will only change selected category  ]"))  
            print(textwrap.dedent("""\
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                (1) Name   (3) Contact   (5) Time    (7) Month
                (2) Age    (4) Day       (6) Fee 
            """))
            if target == command_to_return:
                return "y"
            elif target == command_to_quit:
                end_screen()
            elif target.isspace() or target == "":
                print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
            elif input_val(target, True, False)[0]:
                print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]\n"))
            elif int(input_val(target, True, False)[1]) not in range(1,8):
                print("{:^60}".format("[  Invalid Option, try again.  ]\n"))

            target = str(input("Input category number : ")).replace(" ","")

        target = int(input_val(target, True, False)[1])
        
        display_student_list()

        if target == 1:
            student_list_edit_page = editing_name() or change_additional_info()

        elif target == 2:
            student_list_edit_page = editing_age() or change_additional_info()

        elif target == 3:
            student_list_edit_page = editing_contact() or change_additional_info()

        elif target == 4:
            student_list_edit_page = editing_day() or change_additional_info()

        elif target == 5:
            student_list_edit_page = editing_time() or change_additional_info()

        elif target == 6:
            student_list_edit_page = editing_fee() or change_additional_info()

        elif target == 7:
            student_list_edit_page = editing_month() or change_additional_info()
        
    return "y"











def oh_look_students():
    global student_number, student
    # MAIN PROGROM FOR STUDENT LIST
    student_list_main_page = "y"
    while student_list_main_page == "y":
        if len(conn.execute("SELECT student_id FROM student_data").fetchall()) == 0:
            clear()
            print("----------------------- Student List ----------------------\n")

            input("      ¯\_(ツ)_/¯   Student list is empty   ¯\_(ツ)_/¯  \n\n                  PRESS ANY KEY TO RETURN")
            return "n"
        display_student_list()

        print(textwrap.dedent("""   
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        (1) Edit Student Info
        (2) Remove Student
        
        [0] Back
        """))

        decision = str(input("Enter your option : ")).replace(" ","")
        while input_val(decision, True, False)[0] or int(input_val(decision, True, False)[1]) not in range(0,3):
            display_student_list()
            if decision == command_to_return:
                break
            elif decision ==  command_to_quit:
                end_screen() 
            elif decision.isspace() or decision == "":
                print("{:^60}".format("[  Come on you didn't even type, try again.  ]"))
            elif input_val(decision, True, False)[0]:
                print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]"))
            elif int(input_val(decision, True, False)[1]) not in range(0,3):
                print("{:^60}".format("[  Type between 0 - 2, try again.  ]"))

            print(textwrap.dedent("""\
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            (1) Edit Student Info
            (2) Remove Student
            
            [0] Back
            """))
            decision = str(input("Enter your option : ")).replace(" ","")
        
        if decision == 0 or decision == command_to_return:
            student_list_main_page = "n"

        else:

            # PROMPT USER TO INPUT THE STUDENT NUMBER THEY WISH TO EDIT / REMOVE

            decision = int(input_val(decision, True, False)[1])

            display_student_list()

            print("{:^60}".format("------- Student Number -------\n"))
            student_number = str(input("Enter student number: ")).replace(" ","")

            exisitng_student_id = []
            for row in conn.execute("SELECT student_id FROM student_data"):
                exisitng_student_id.append(row[0])

            while input_val(student_number, True, False)[0] or int(input_val(student_number, True, False)[1]) not in exisitng_student_id:
                display_student_list()
                print("{:^60}".format("------- Student Number -------\n"))
                if student_number == command_to_return:
                    break
                elif student_number == command_to_quit:
                    end_screen()
                elif student_number.isspace() or student_number == "":
                    print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
                elif input_val(student_number, True, False)[0]:
                    print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]\n"))
                elif int(input_val(student_number, True, False)[1]) not in exisitng_student_id:
                    print("{:^60}".format("[  Student ID does not exist, try again.  ]\n"))

                student_number = str(input("Enter student number: ")).replace(" ","")

            if student_number == command_to_return:
                student_list_main_page = "y"
            else:
                student_number = int(input_val(student_number, True, False)[1])
                student = []
                for row in conn.execute(f"SELECT name FROM student_data where student_id = {student_number}"):
                    student.append(row[0])

                # EDIT STUDENT INFO PAGE
                if decision == 1:
                    student_list_main_page = edit_page()

                # REMOVE STUDENT INFO PAGE
                elif decision == 2:
                    display_student_list()
                    print("{:^60}".format(f"Currently Removing student : {student}\n"))
                    print("{:^60}".format(f"[  Type #back to return  ]\n"))
                    confirmation = str(input("Do you want to remove this student? [y / n] : ")).replace(" ","")

                    while input_val(confirmation, False, True)[0] or str(input_val(confirmation, False, True)[1]) not in ("y","n"):
                        display_student_list()
                        
                        print("{:^60}".format(f"Currently Removing student : {student}\n"))
                        print("{:^60}".format(f"[  Type #back to return  ]\n"))
                        if confirmation == command_to_return:
                            break
                        elif confirmation == command_to_quit:
                            end_screen()
                        elif confirmation.isspace() or confirmation == "":
                            print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
                        elif input_val(confirmation, False, True)[0]:
                            print("{:^60}".format("[  Special characters or numbers detected, try again.  ]\n"))
                        elif str(input_val(confirmation, False, True)[1]) not in ("y","n"):
                            print("{:^60}".format("[  Type either y or n, try again.  ]\n"))

                        confirmation = str(input("Do you want to remove this student? [y / n] : ")).replace(" ","")

                    if confirmation == "y":
                        delete_student(student_number)
                    
                    student_list_main_page = "y"


