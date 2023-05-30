from mymodule import *

# For displays
def display_student_list():
    clear()
    if len(conn.execute("SELECT student_id FROM student_data").fetchall()) == 0:
        print("{:^184}".format("[  Student List  ]"))  
        print("{:^184}".format("[  Yup, it's empty. What to do?  ]"))  
    else:
        print("{:^184}".format("[  Student List  ]"))     
        print ("\x1B[4m{:^183}_\x1B[0m".format(""))
        print ("\x1B[4m|{:<4}|{:^31}|{:^5}|{:^12}|{:^12}|{:^13}|{:^19}|{:^18}| {:^60}|\x1B[0m".format("ID", "Name", "Age", "Contact", "Fee", "Day", "Time", "Teacher", "Month"))
        for row in conn.execute("SELECT student_id, name, day, class_no FROM student_data ORDER BY student_id ASC"):
            for row in conn.execute(f"SELECT student_id, name, age, contact, day, fee, start, end, teacher FROM student_data LEFT OUTER JOIN {row[2]}_class ON student_data.class_no = {row[2]}_class.class_no where student_id = {row[0]}"):
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

                if len(attend_month) == 0:
                    attend_month = "Empty"

                print ("| {:<3}| {:<30}| {:<3} |{:^12}| {:<11}|{:^13}| {:^17} |{:^18}| {:<60}|".format(student_id, name.title(), age, contact, locale.currency(fee), attend_day.capitalize(), time, teacher, attend_month))

        print(overline*184)

def edit_page():
    # Prompt to edit name of student
    def editing_name():
        current_name = (conn.execute(f"SELECT name FROM student_data where student_id = {student_number}").fetchone()[0]).title()

        clear()
        print()
        print("{:^60}".format(f"Currently Editting student : {current_name}")) 
        print("{:^60}".format("[  #back to return  ]\n"))
        print("{:^60}".format("--------- Edit Name ---------\n"))
        update_name = str(input("New name : "))

        while input_val(update_name, False, True)[0]:
            clear()
            print()
            print("{:^60}".format(f"Currently Editting student : {current_name}")) 
            print("{:^60}".format("[  #back to return  ]\n")) 
            print("{:^60}".format("--------- Edit Name ---------\n"))

            if update_name == command_to_return:
                return "y"
            elif update_name == command_to_quit:
                end_screen()
            elif update_name.isspace() or update_name == "":
                print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
            else:
                print("{:^60}".format("[  Special characters or numbers detected, try again.  ]\n"))
            
            update_name = str(input("New name : "))
        
        update_name = str(input_val(update_name, False, True)[1]).lower()

        for row in month:
            if list(conn.execute(f"SELECT student_id, name FROM {month[row]} where student_id = {student_number}")) != []:
                conn.execute(f"UPDATE {month[row]} set name = '{update_name}' where student_id = {student_number}")
                conn.commit()
        update_student(student_number, "name", update_name)

    # Prompt to edit age of student
    def editing_age(): 
        current_name = (conn.execute(f"SELECT name FROM student_data where student_id = {student_number}").fetchone()[0]).title()
        current_age = conn.execute(f"SELECT age FROM student_data where student_id = {student_number}").fetchone()[0]

        clear()
        print()
        print("{:^60}".format(f"Currently Editting student : {current_name}")) 
        print("{:^60}".format("[  #back to return  ]\n"))
        print("{:^60}".format(f"------- Current age is {current_age} -------\n"))

        update_age = str(input("Change age to : ")).replace(" ","")

        while input_val(update_age, True, False)[0] or int(input_val(update_age, False, True)[1]) > 50:
            clear()
            print()
            print("{:^60}".format(f"Currently Editting student : {current_name}")) 
            print("{:^60}".format("[  #back to return  ]\n"))
            print("{:^60}".format(f"------- Current age is {current_age} -------\n"))
            
            if update_age == command_to_return:
                return "y"
            elif update_age == command_to_quit:
                end_screen()
            elif update_age.isspace() or update_age == "":
                print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
            elif input_val(update_age, True, False)[0]:
                print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]\n"))
            elif int(input_val(update_age, False, True)[1]) > 50:
                print("{:^60}".format("[  Exceed age limit 50 years old, try again.  ]\n"))
                
            update_age = str(input("Change age to : ")).replace(" ","")
        
        update_age = int(input_val(update_age, False, True)[1])
        update_student(student_number, "age", update_age)

    # Prompt to edit contact of student
    def editing_contact():
        current_name = (conn.execute(f"SELECT name FROM student_data where student_id = {student_number}").fetchone()[0]).title()
        current_contact = conn.execute(f"SELECT contact FROM student_data where student_id = {student_number}").fetchone()[0]

        clear()
        print()
        print("{:^60}".format(f"Currently Editting student : {current_name}")) 
        print("{:^60}".format("[  #back to return  ]\n"))
        print("{:^60}".format(f"------- Current contact is {current_contact} -------\n"))

        update_contact = str(input("Phone Number : ")).replace(" ","")

        while input_val(update_contact, True, False)[0] or phone_val(update_contact) == False:
            clear()
            print()
            print("{:^60}".format(f"Currently Editting student : {current_name}")) 
            print("{:^60}".format("[  #back to return  ]\n"))
            print("{:^60}".format(f"------- Current contact is {current_contact} -------\n"))

            if update_contact == command_to_return:
                return "y"
            elif update_contact == command_to_quit:
                end_screen()
            elif update_contact.isspace() or update_contact == "":
                print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
            elif input_val(update_contact, True, False)[0]:
                print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]\n"))
            elif phone_val(update_contact) == False:
                print("{:^60}".format("[  Input must be 10-digit and begin with 0.  ]\n"))
                print("{:^60}".format("[   eg. 0XX XXX XXXX   ]\n"))
            
            update_contact = str(input("Phone Number : ")).replace(" ","")
        
        update_student(student_number, "contact", update_contact)

    # Prompt to edit the day of student
    def editing_day():
        current_name = (conn.execute(f"SELECT name FROM student_data where student_id = {student_number}").fetchone()[0]).title()
        current_day = conn.execute(f"SELECT day FROM student_data where student_id = {student_number}").fetchone()[0]

        # For class display after selecting the day
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
       
        clear()
        print()
        print("{:^60}".format(f"Currently Editting student : {current_name}")) 
        print("{:^60}".format("[  #back to return  ]\n"))
        print("{:^60}".format("--------- Editing Day --------\n"))
        print("{:^60}".format(f"Switching {current_day.title()} to ..."))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        valid_day = []
        for row in day:
            cursor = conn.execute(f"SELECT class_no, start, end, teacher from {day[row]}_class")
            if len(list(cursor)) != 0:
                valid_day.append(row)
        # Display Available day for selection
        line_length = 0
        for row in valid_day:
            day_with_number = f"  ({row}) {day[row].capitalize()}"
            day_length = len(day_with_number)

            if line_length + day_length > 60:
                print()
                line_length = 0

            padding = ' ' * (13 - day_length)
            print(f"{day_with_number}{padding}", end=' ')
            line_length += day_length + 10

        # Chooose which day to change too
        update_day = str(input("\n\nEnter number of the day : ")).replace(" ","")

        while input_val(update_day, True, False)[0] or int(input_val(update_day, True, False)[1]) not in valid_day:
            clear()
            print()
            print("{:^60}".format(f"Currently Editting student : {current_name}")) 
            print("{:^60}".format("--------- Editing Day --------\n"))
            print("{:^60}".format("[  #back to return  ]\n")) 
            print("{:^60}".format(f"Switching {current_day.title()} to ..."))
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            line_length = 0
            for row in valid_day:
                day_with_number = f"  ({row}) {day[row].capitalize()}"
                day_length = len(day_with_number)

                if line_length + day_length > 60:
                    print()
                    line_length = 0

                padding = ' ' * (13 - day_length)
                print(f"{day_with_number}{padding}", end=' ')
                line_length += day_length + 10
            print("\n")
            if update_day == command_to_return:
                return "y"
            elif update_day == command_to_quit:
                end_screen()
            elif update_day.isspace() or update_day == "":
                print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
            elif input_val(update_day, True, False)[0]:
                print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]\n"))
            else:
                if int(input_val(update_day, True, False)[1]) in range(1,8) and int(input_val(update_day, True, False)[1]) not in valid_day:
                    print("{:^60}".format("[  No classes available for selected day, try again.  ]\n"))
                else:
                    print("{:^60}".format("[  Enter numbers between 1 and 7, try again.  ]\n"))

            
            update_day = str(input("Enter number of the day : ")).replace(" ","")
            
        update_day = int(input_val(update_day, True, False)[1])


        # Display Class time to select
        display_class_list(update_day)
        print("{:^60}".format("------------- Select a time ------------"))
        print("{:^60}".format("[  Type #back to return  ]\n"))
        update_class_no = str(input("Enter class number: ")).replace(" ","")

        while input_val(update_class_no, True, False)[0] or int(input_val(update_class_no, True, False)[1]) not in class_no_for_validation:
            display_class_list(update_day)
            print("{:^60}".format("------------- Select a time ------------"))
            print("{:^60}".format("[  Type #back to return  ]\n"))
            if update_class_no == command_to_return:
                return "y"
            elif update_class_no == command_to_quit:
                end_screen()
            elif update_class_no.isspace() or update_class_no == "":
                print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
            elif input_val(update_class_no, True, False)[0]:
                print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]\n"))
            elif int(input_val(update_class_no, True, False)[1]) not in class_no_for_validation:
                print("{:^60}".format("[  Type the available class number.  ]\n"))
        
            update_class_no = str(input("Enter class number: ")).replace(" ","")

        update_class_no = int(input_val(update_class_no, True, False)[1])

        update_student(student_number, "day", update_day)
        update_student(student_number, "class_no", update_class_no)

    # Prompt to edit the time of student
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

        if len(list(conn.execute(f"SELECT class_no, start, end, teacher from {edit_day[0]}_class"))) == 0:
            clear()
            print("{:^60}".format(f"[  No class on {edit_day[0].title()}, please change to another day  ]\n"))
            input("{:^60}".format("PRESS ANY KEY TO CONTINUE"))

        else:
            display_class_list(edit_day)     
            print("{:^60}".format("------------- Select a time ------------"))
            print("{:^60}".format("[  #back to return  ]\n")) 
            update_class_no = str(input("Enter class number: ")).replace(" ","")

            while input_val(update_class_no, True, False)[0] or int(input_val(update_class_no, True, False)[1]) not in class_no_for_validation:
                display_class_list(edit_day)
                print("{:^60}".format("------------- Select a time ------------"))
                print("{:^60}".format("[  #back to return  ]\n")) 

                if update_class_no == command_to_return:
                    return "y"
                elif update_class_no == command_to_quit:
                    end_screen()
                elif update_class_no.isspace() or update_class_no == "":
                    print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
                elif input_val(update_class_no, True, False)[0]:
                    print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]\n"))
                elif int(input_val(update_class_no, True, False)[1]) not in class_no_for_validation:
                    print("{:^60}".format("[  Type the available class number.  ]\n"))
                
                update_class_no = str(input("Enter class number: ")).replace(" ","")

            update_class_no = int(input_val(update_class_no, True, False)[1])
            update_student(student_number, "class_no", update_class_no)

    # Prompt to add or remove student from month
    def editing_month():
        wish_to_continue = "y"
        while wish_to_continue == "y":
            display_student_list()
            print("{:^60}".format("------------ Select an option ------------"))
            print("{:^60}".format("[  #back to return  ]"))
            print(textwrap.dedent("""
            (1) Add student to month
            (2) Remove student from month
            
            [0] Back
            """))

            decision = str(input("Enter your option : ")).replace(" ","")

            while input_val(decision, True, False)[0] or int(input_val(decision, True, False)[1]) not in range(0,3):
                display_student_list()
                print("{:^60}".format("------------ Select an option ------------"))
                print("{:^60}".format("[  #back to return  ]"))
                print(textwrap.dedent("""
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
                print("{:^60}".format("------- Add into month -------"))
                print(textwrap.dedent("""
                ~~~~~~~~~~~~~~~~~~~~~~ Select a month ~~~~~~~~~~~~~~~~~~~~~~
                  (1) January    (4) April   (7) July        (10) October
                  (2) February   (5) May     (8) August      (11) November
                  (3) March      (6) June    (9) September   (12) December
                """))

                add_month = str(input("Enter number of the month : ")).replace(" ","")
                in_month = []
                for row in month:
                    if list(conn.execute(f"SELECT student_id, name FROM {month[row]} where student_id = {student_number}")) != []:
                        in_month.append(row)
            
                while input_val(add_month, True, False)[0] or int(input_val(add_month, True, False)[1]) not in month or int(input_val(add_month, True, False)[1]) in in_month:
                    display_student_list()
                    print("{:^60}".format("------ Adding into month -----"))
                    print(textwrap.dedent("""
                    ~~~~~~~~~~~~~~~~~~~~~~ Select a month ~~~~~~~~~~~~~~~~~~~~~~
                      (1) January    (4) April   (7) July        (10) October
                      (2) February   (5) May     (8) August      (11) November
                      (3) March      (6) June    (9) September   (12) December
                    """))

                    if add_month == command_to_return:
                        return "y"
                    elif add_month == command_to_quit:
                        end_screen()
                    elif add_month.isspace() or add_month == "":
                        print("{:^60}".format("[  Come on you didn't even type, try again.  ]"))
                    elif input_val(add_month, True, False)[0]:
                        print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]"))
                    elif int(input_val(add_month, True, False)[1]) in in_month:
                        print("{:^60}".format(f"[  Already added to {month[int(add_month)].title()}, try again.  ]"))
                    elif int(input_val(add_month, True, False)[1]) not in month:
                        print("{:^60}".format("[  Enter numbers between 1 and 12, try again.  ]"))

                    add_month = str(input("\nEnter number of the month : ")).replace(" ","")
                
                add_month = int(input_val(add_month, True, False)[1])
                
                # Calculate the fee needed to add onto the exisiting fee
                day_category = {"monday" : 1, "tuesday" : 2, "wednesday" : 3, "thursday" : 4, "friday" : 5, "saturday" : 6, "sunday" : 7}
                fee_for_calc = conn.execute(f"SELECT fee FROM student_data where student_id = {student_number}").fetchone()[0]
                current_day = conn.execute(f"SELECT day FROM student_data where student_id = {student_number}").fetchone()[0]

                count = 0
                for row in range (1, calendar.monthrange(datetime.date.today().year, add_month)[1] + 1):
                    if datetime.date(current_year, add_month, row).isoweekday() == day_category[current_day]:
                        count += 1
                fee =  fee_for_calc + (count * current_fee)

                # Change the fee of the student and add the student info into the respective month
                current_name = conn.execute(f"SELECT name FROM student_data where student_id = {student_number}").fetchone()[0]
                update_student(student_number, "fee", fee)
                conn.execute(f"INSERT INTO {month[add_month]}(student_id, name) VALUES ({student_number}, '{current_name}')")
                conn.commit()

            elif decision == 2:

                temp_var_month = []
                for row in month:
                    if list(conn.execute(f"SELECT name FROM {month[row]} where student_id = {student_number}")) != []:
                        temp_var_month.append(row)

                
                display_student_list()
                print("{:^60}".format("------ Remove from month -----"))
                print("\n~~~~~~~~~~~~~~~~~~~~~~~ Select month ~~~~~~~~~~~~~~~~~~~~~~~")
                line_length = 0
                for row in temp_var_month:
                    day_with_number = f"({row}) {month[row].capitalize()}"
                    day_length = len(day_with_number)

                    if line_length + day_length > 80:
                        print()
                        line_length = 0

                    padding = ' ' * (14 - day_length)
                    print(f"{day_with_number}{padding}", end=' ')
                    line_length += day_length + 10
                print("\n")
                print("{:^60}".format("[0] Back\n"))
                remove_month = str(input("Enter number : ")).replace(" ","")

                while input_val(remove_month, True, False)[0] or int(input_val(remove_month, True, False)[1]) not in temp_var_month:
                    display_student_list()
                    print("{:^60}".format("------ Remove from month -----"))
                    print("\n~~~~~~~~~~~~~~~~~~~~~~~ Select month ~~~~~~~~~~~~~~~~~~~~~~~")
                    line_length = 0
                    for row in temp_var_month:
                        day_with_number = f"({row}) {month[row].capitalize()}"
                        day_length = len(day_with_number)

                        if line_length + day_length > 80:
                            print()
                            line_length = 0

                        padding = ' ' * (14 - day_length)
                        print(f"{day_with_number}{padding}", end=' ')
                        line_length += day_length + 10
                    print("\n")
                    print("{:^60}".format("[0] Back\n"))

                    if remove_month == command_to_return:
                        return "y"
                    elif remove_month == 0:
                        return "y"
                    elif remove_month == command_to_quit:
                        end_screen()
                    elif remove_month.isspace() or remove_month == "":
                        print("{:^60}".format("[  Come on you didn't even type, try again.  ]"))
                    elif input_val(remove_month, True, False)[0]:
                        print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]"))
                    elif int(input_val(remove_month, True, False)[1]) not in temp_var_month:
                        print("{:^60}".format("[  Enter one of the numbers displayed, try again.  ]"))

                    remove_month = str(input("\nEnter number : ")).replace(" ","")
                
                remove_month = int(input_val(remove_month, True, False)[1])

                if remove_month != 0:
                    # Calculate the fee needed to add onto the exisiting fee
                    day_category = {"monday" : 1, "tuesday" : 2, "wednesday" : 3, "thursday" : 4, "friday" : 5, "saturday" : 6, "sunday" : 7}
                    fee_for_calc = conn.execute(f"SELECT fee FROM student_data where student_id = {student_number}").fetchone()[0]
                    current_day = conn.execute(f"SELECT day FROM student_data where student_id = {student_number}").fetchone()[0]

                    count = 0
                    for row in range (1, calendar.monthrange(datetime.date.today().year, remove_month)[1] + 1):
                        if datetime.date(current_year, remove_month, row).isoweekday() == day_category[current_day]:
                            count += 1
                    fee =  fee_for_calc - (count * current_fee)

                    # Change the fee of the student and add the student info into the respective month
                    update_student(student_number, "fee", fee)
                    conn.execute(f"DELETE FROM {month[remove_month]} where student_id = {student_number}")
                    conn.commit()

                else:
                    return "y"
                
            elif decision == 0 :
                return "y"

    # Prompt to subtract or add fee to student
    def editing_fee():
        fee = conn.execute(f"SELECT fee FROM student_data where student_id = {student_number}").fetchone()[0]

        clear()
        print()
        print("{:^60}".format(f"Current Fee : {locale.currency(fee)}\n"))
        print("{:^60}".format("------------ Select an option ------------"))
        print(textwrap.dedent("""
        (1) Pay
        (2) Add additional payment
        
        [0] Back
        """))

        decision = str(input("Enter your option : ")).replace(" ","")
        while input_val(decision, True, False)[0] or int(input_val(decision, True, False)[1]) not in range(0,3):
            clear()
            print()
            print("{:^60}".format(f"Current Fee : {locale.currency(fee)}\n"))
            print("{:^60}".format("------------ Select an option ------------"))
            print(textwrap.dedent("""
            (1) Pay
            (2) Add additional payment
            
            [0] Back
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

        if decision == 0:
            return "y"
        
        else:
            clear()
            print()
            print("{:^60}".format(f"Current Fee : {locale.currency(fee)}\n"))
            print("{:^60}".format("[  Enter ammount  ]\n"))

            ammount_entered = str(input("Accepts numbers only : ")).replace(" ","")
            while isfloat(ammount_entered) == False:
                clear()
                print()
                print("{:^60}".format(f"Current Fee : {locale.currency(fee)}\n"))
                print("{:^60}".format("[  Enter ammount  ]\n"))

                if ammount_entered == command_to_return:
                    return "y"
                elif ammount_entered.isspace() or ammount_entered == "":
                    print("{:^60}".format("[  Come on you didn't even type, try again.  ]"))
                elif isfloat(ammount_entered):
                    print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]"))
                    
                ammount_entered = str(input("\nAccepts numbers only) : ")).replace(" ","")

            ammount_entered = float(input_val(ammount_entered, False, True)[1])

            fee_for_calc = conn.execute(f"SELECT fee FROM student_data where student_id = {student_number}").fetchone()

            if decision == 1:
                updated_fee =  fee_for_calc[0] - ammount_entered
            elif decision == 2:
                updated_fee =  fee_for_calc[0] + ammount_entered

            update_student(student_number, "fee", updated_fee)


    # Where the all for the edit page function is executed
    student_list_edit_page = "y"
    while student_list_edit_page == "y":
        target_student = conn.execute(f"SELECT name, age, contact, day, class_no, fee FROM student_data where student_id = {student_number}").fetchone()
        target_student_class = conn.execute(f"SELECT start, end, teacher FROM {target_student[3]}_class where class_no = {target_student[4]}").fetchone()
        target_student_month = []
        for row in month:
            if list(conn.execute(f"SELECT student_id, name FROM {month[row]} where student_id = {student_number}")) != []:
                target_student_month.append((month[row])[:3].capitalize())
        target_student_month = ', '.join(target_student_month)
        if len(target_student_month) == 0:
            target_student_month = "Empty"

        clear()
        print(textwrap.dedent(f"""
        Name    : {target_student[0].title()}
        Age     : {target_student[1]}
        Contact : {target_student[2]}

        Month   : {target_student_month}

        Day     : {target_student[3].title()}
        Time    : {target_student_class[0]} - {target_student_class[1]}
        Teacher : {target_student_class[2]}
            
        Fee     : {locale.currency(target_student[4])}
        """))
        print("{:^60}".format("[  Will only change selected category  ]"))  
        print(textwrap.dedent("""\
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                 (1) Name   (3) Contact   (5) Day   (7) Fee
                 (2) Age    (4) Month     (6) Time 

                                 [0] Back
        """))

        target = str(input("Input category number : ")).replace(" ","")
        
        while input_val(target, True, False)[0] or int(input_val(target, True, False)[1]) not in range(0,8):
            clear()
            print(textwrap.dedent(f"""
            Name    : {target_student[0].title()}
            Age     : {target_student[1]}
            Contact : {target_student[2]}

            Month   : {target_student_month}

            Day     : {target_student[3].title()}
            Time    : {target_student_class[0]} - {target_student_class[1]}
            Teacher : {target_student_class[2]}
                
            Fee     : {locale.currency(target_student[4])}
            """))
            print("{:^60}".format("[  Will only change selected category  ]"))  
            print(textwrap.dedent("""\
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                     (1) Name   (3) Contact   (5) Day   (7) Fee
                     (2) Age    (4) Month     (6) Time 
                                    
                                     [0] Back
            """))

            if target == command_to_return:
                return "y"
            elif target == command_to_quit:
                end_screen()
            elif target.isspace() or target == "":
                print("{:^60}".format("[  Come on you didn't even type, try again.  ]"))
            elif input_val(target, True, False)[0]:
                print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]"))
            elif int(input_val(target, True, False)[1]) not in range(0,8):
                print("{:^60}".format("[  Invalid Option, try again.  ]"))

            target = str(input("\nInput category number : ")).replace(" ","")

        target = int(input_val(target, True, False)[1])
        
        if target == 1:
            editing_name()
        elif target == 2:
            editing_age()
        elif target == 3:
            editing_contact()
        elif target == 4:
            editing_month()
        elif target == 5:
            editing_day()
        elif target == 6:
            editing_time()
        elif target == 7:
            editing_fee()
        
        elif target == 0:
            student_list_edit_page = "n"
            
    return "y"




def oh_look_students():
    global student_number, student, current_fee, current_year

    current_fee = conn.execute("SELECT fee FROM internal_data").fetchone()[0]
    current_year = conn.execute("SELECT year FROM internal_data").fetchone()[0]

    # The begininning of the student list page (where all functions above are executed)
    student_list_main_page = "y"
    while student_list_main_page == "y":
        if len(conn.execute("SELECT student_id FROM student_data").fetchall()) == 0:
            clear()
            print("----------------------- Student List ----------------------\n")

            input("      ¯\_(ツ)_/¯   Student list is empty   ¯\_(ツ)_/¯  \n\n                  PRESS ANY KEY TO RETURN")
            return "n"
        display_student_list()
        print("{:^60}".format(f"[  Type #back to return  ]"))
        print(textwrap.dedent("""   
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        (1) Edit Student Info
        (2) Remove Student
        
        [0] Back
        """))

        decision = str(input("Enter your option : ")).replace(" ","")
        while input_val(decision, True, False)[0] or int(input_val(decision, True, False)[1]) not in range(0,3):
            display_student_list()
            print("{:^60}".format(f"[  Type #back to return  ]"))

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
        
        if decision == command_to_return or int(input_val(decision, True, False)[1]) == 0:
            student_list_main_page = "n"
        else:
            # PROMPT USER TO INPUT THE STUDENT NUMBER THEY WISH TO EDIT / REMOVE
            decision = int(input_val(decision, True, False)[1])

            display_student_list()
            print("{:^60}".format("------- Student Number ------\n"))
            print("{:^60}".format("[  #back to return  ]\n")) 
            student_number = str(input("Enter student number: ")).replace(" ","")

            exisitng_student_id = []
            for row in conn.execute("SELECT student_id FROM student_data"):
                exisitng_student_id.append(row[0])

            while input_val(student_number, True, False)[0] or int(input_val(student_number, True, False)[1]) not in exisitng_student_id:
                display_student_list()
                print("{:^60}".format("------- Student Number ------\n"))
                print("{:^60}".format("[  #back to return  ]\n")) 

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

                # EDIT STUDENT INFO PAGE
                if decision == 1:
                    student_list_main_page = edit_page()

                # REMOVE STUDENT INFO PAGE
                elif decision == 2:
                    display_student_list()
                    current_name = conn.execute(f"SELECT name FROM student_data where student_id = {student_number}")
                    print("{:^60}".format(f"Currently Removing student : {current_name.title()}\n"))
                    
                    confirmation = str(input("Do you want to remove this student? [y / n] : ")).replace(" ","")

                    while input_val(confirmation, False, True)[0] or str(input_val(confirmation, False, True)[1]) not in ("y","n"):
                        display_student_list()
                        
                        print("{:^60}".format(f"Currently Removing student : {current_name.title()}\n"))
                        
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


