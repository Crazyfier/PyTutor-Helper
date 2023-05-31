from mymodule import *

# Display all existing classes empty or not
def main_menu_of_teacher_tab():
    global decision
    global valid_day

    valid_day = []
    print("\n----------------- Class Schedule Handling -----------------\n")
    for row in day:
        print("{:^60}".format(f"[  {day[row].title()}  ]"))
        if len(list(conn.execute(f"SELECT class_no, start, end, teacher from {day[row]}_class"))) == 0:
            print("{:^60}".format("[  No Class Detected  ]\n"))
        else:
            valid_day.append(row)
            print("____________________________________________________________")
            print ("\x1B[4m|{:^11}|{:^20}|{:^25}|\x1B[0m".format("Class No.", "Time", "Teacher"))
            for row in conn.execute(f"SELECT class_no, start, end, teacher from {day[row]}_class ORDER BY class_no ASC"):
                time = row[1] + " - " + row[2]
                print ("|{:^11}|{:^20}|{:^25}| ".format(row[0], time, row[3]))

            print(overline * 60)

    if len(valid_day) == 0:
        option = range(0,2)
        print(textwrap.dedent("""\
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        (1) Add new class

        [0] Back
        """))
    else:
        option = range(0,4)
        print(textwrap.dedent("""\
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        (1) Add new class
        (2) Edit Class
        (3) Remove Class

        [0] Back
        """))
    
    decision = str(input("Enter your option : ")).replace(" ","")
    while input_val(decision, True, False)[0] or int(input_val(decision, True, False)[1]) not in option:
        clear()
        valid_day = []
        print("\n----------------- Class Schedule Handling -----------------\n")
        for row in day:
            print("{:^60}".format(f"[  {day[row].title()}  ]"))
            if len(list(conn.execute(f"SELECT class_no, start, end, teacher from {day[row]}_class"))) == 0:
                print("{:^60}".format("[  No Class Detected  ]\n"))
            else:
                valid_day.append(row)
                print("____________________________________________________________")
                print ("\x1B[4m|{:^11}|{:^20}|{:^25}|\x1B[0m".format("Class No.", "Time", "Teacher"))
                for row in conn.execute(f"SELECT class_no, start, end, teacher from {day[row]}_class ORDER BY class_no ASC"):
                    time = row[1] + " - " + row[2]
                    print ("|{:^11}|{:^20}|{:^25}| ".format(row[0], time, row[3]))
                print(overline * 60)

        if len(valid_day) == 0:
            option = range(0,2)
            print(textwrap.dedent("""\
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            (1) Add new class

            [0] Back
            """))
        else:
            option = range(0,4)
            print(textwrap.dedent("""\
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            (1) Add new class
            (2) Edit Class
            (3) Remove Class

            [0] Back
            """))
    
        if decision == command_to_return:
            return "y"
        elif decision == command_to_quit:
            end_screen()
        elif decision.isspace() or decision == "":
            print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
        elif input_val(decision, True, False)[0]:
            print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]\n"))
        elif int(input_val(decision, True, False)[1]) not in option:
            print("{:^60}".format("[  Enter number between 0 - 3, try again.  ]\n"))

        decision = str(input("Enter your option : ")).replace(" ","")
        
    decision = int(input_val(decision, True, False)[1])

    return decision

# Display the days that are ready to be editted
def display_available_days_to_edit():
    global target_day
    clear()
    print()
    print("~~~~~~~~~~~~~~~~~~~~~~~ Day Selection ~~~~~~~~~~~~~~~~~~~~~~")
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
    valid_day.append(0)
    print("\n")
    print("{:^60}".format("[0] Back"))

    target_day = str(input("\nEnter one of the number above: ")).replace(" ","")
    while input_val(target_day, True, False)[0] or int(input_val(target_day, True, False)[1]) not in valid_day:
        clear()
        print()
        print("~~~~~~~~~~~~~~~~~~~~~~~ Day Selection ~~~~~~~~~~~~~~~~~~~~~~")
        valid_day.remove(0)
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
        valid_day.append(0)
        print("\n")
        print("{:^60}".format("[0] Back\n"))

        if target_day == command_to_return:
            return "y"
        elif target_day == command_to_quit:
            end_screen()
        elif target_day.isspace() or target_day == "":
            print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
        elif input_val(target_day, True, False)[0]:
            print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]\n"))
        elif int(input_val(target_day, True, False)[1]) not in valid_day:
            print("{:^60}".format("[  Select the one of the days displayed, try again.  ]\n"))

        target_day = str(input("Enter one of the number above: ")).replace(" ","")

    target_day = int(input_val(target_day, True, False)[1])

    if target_day == 0:
        return "y"
    
# The tab where user gets to add classes
def adding_new_class_tab():
    # Display class list for adding classes
    def display_class_list(target_day):
        global class_no_for_validation
        clear()
        class_no_for_validation = []
        print()
        print("{:^60}".format(f"[  Adding class for {day[target_day].title()}  ]"))
        if len(list(conn.execute(f"SELECT class_no, start, end, teacher from {day[target_day]}_class"))) == 0:
            print("{:^60}".format("[  *INSERT TUMBLEWEED*  ]\n"))
        else:
            print("____________________________________________________________")
            print ("\x1B[4m|{:^11}|{:^20}|{:^25}|\x1B[0m".format("Class No.", "Time", "Teacher"))
            
            for row in conn.execute(f"SELECT class_no, start, end, teacher from {day[target_day]}_class ORDER BY class_no ASC"):
                class_no_for_validation.append(row[0])
                time = row[1] + " - " + row[2]
                print ("|{:^11}|{:^20}|{:^25}| ".format(row[0], time, row[3]))
            print(overline * 60)
        
        print("{:^60}".format("[  #back to return  ]\n"))
    
    clear()
    print("{:^60}".format("[  Add New Classes  ]"))
    print(textwrap.dedent("""
    ~~~~~~~~~~~~~~~~~~~~~~ Day Selection ~~~~~~~~~~~~~~~~~~~~~~~
        (1) Monday  (2) Tuesday  (3) Wednesday  (4) Thursday     
        (5) Friday  (6) Satruday (7) Sunday  
        """))
    print("{:^60}".format("[0] Back"))
    target = str(input("\nEnter one of the number above : ")).replace(" ","")
    while input_val(target, True, False)[0] or int(input_val(target, True, False)[1]) not in range(0, 8):
        clear()
        print("{:^60}".format("[  Adding New Class  ]"))
        print(textwrap.dedent("""
        ~~~~~~~~~~~~~~~~~~~~~~ Day Selection ~~~~~~~~~~~~~~~~~~~~~~~
            (1) Monday  (2) Tuesday  (3) Wednesday  (4) Thursday     
            (5) Friday  (6) Satruday (7) Sunday  
        """))
        print("{:^60}".format("[0] Back\n"))

        if target == command_to_return:
            return "y"
        elif target == command_to_quit:
            end_screen()
        elif target.isspace() or target == "":
            print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
        elif input_val(target, True, False)[0]:
            print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]\n"))
        elif int(input_val(target, True, False)[1]) not in range(0, 8):
            print("{:^60}".format("[  Enter number between 1 - 7, try again.  ]\n"))

        target = str(input("Enter one of the number above : ")).replace(" ","")
    target = int(input_val(target, True, False)[1])

    if target == 0:
        return "y"

    wish_to_continue = "y"
    while wish_to_continue == "y":
        display_class_list(target)

        # PROMPT USER TO ENTER CLASS NUMBER
        class_no = str(input("Enter new class number : ")).replace(" ","")
        while input_val(class_no, True, False)[0] or int(input_val(class_no, True, False)[1]) in class_no_for_validation:
            display_class_list(target)
            if class_no == command_to_return:
                return "y"
            elif class_no == command_to_quit:
                end_screen()
            elif class_no.isspace() or class_no == "":
                print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
            elif input_val(class_no, True, False)[0]:
                print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]\n"))
            elif int(input_val(class_no, True, False)[1]) in class_no_for_validation:
                print("{:^60}".format("[  Number taken, pick another.  ]\n"))
            
            class_no = str(input("Enter new class number : ")).replace(" ","")

        class_no = int(input_val(class_no, True, False)[1])

        # PROMPT USER TO INPUT HOUR, MINUTE AND AM/PM
        Input = ["Start", "End"]
        overlap = True
        while overlap == True:
            count = 1
            for var in Input:
                def temp_display():
                    display_class_list(target)
                    print(f"New class number : {class_no}")
                    if count == 2:
                        print(f"Start of Class   : {start_input}")
                    print("")
                    print("{:^60}".format(f"-------- {var} of class --------"))
                    
                temp_display()
                hour = str(input("Enter hour [1 - 12] : ")).replace(" ","")
                while input_val(hour, True, False)[0] or int(input_val(hour, True, False)[1]) not in range(1, 13):
                    temp_display()
                    if hour == command_to_return:
                        return "y"
                    elif hour == command_to_quit:
                        end_screen()
                    elif hour.isspace() or hour == "":
                        print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
                    elif input_val(hour, True, False)[0]:
                        print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]\n"))
                    elif int(input_val(hour, True, False)[1]) not in range(1, 13):
                        print("{:^60}".format("[  Enter numbers between 1 - 12, try again  ]\n"))

                    hour = str(input("Enter hour [1 - 12] : ")).replace(" ","")                   
                hour = str(input_val(hour, True, False)[1]).zfill(2)

                temp_display()
                print("{:^60}".format(f"Hour : {hour}\n"))
                minute = str(input("Enter minute [0 - 59] : ")).replace(" ","")
                while input_val(minute, True, False)[0] or int(input_val(minute, True, False)[1]) not in range(0, 60):
                    temp_display()
                    print("{:^60}".format(f"Hour : {hour}\n"))
                    if minute == command_to_return:
                        return "y"
                    elif minute == command_to_quit:
                        end_screen()
                    elif minute.isspace() or minute == "":
                        print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
                    elif input_val(minute, True, False)[0]:
                        print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]\n"))
                    elif int(input_val(minute, True, False)[1]) not in range(1, 13):
                        print("{:^60}".format("[  Enter numbers between 0 - 59, try again  ]\n"))

                    minute = str(input("Enter minute [0 - 59] : ")).replace(" ","")
                minute = str(input_val(minute, True, False)[1]).zfill(2)

                temp_display()
                print("{:^60}".format(f"Time : {hour}:{minute}\n"))
                am_or_pm = str(input("Input AM or PM (lower case is accepted) : ")).replace(" ","")
                while input_val(am_or_pm, False, True)[0] or str(input_val(am_or_pm, False, True)[1]).lower() not in ["am", "pm"]:
                    temp_display()
                    print("{:^60}".format(f"Time : {hour}:{minute}\n"))
                    if am_or_pm == command_to_return:
                        return "y"
                    elif am_or_pm == command_to_quit:
                        end_screen()
                    elif am_or_pm.isspace() or am_or_pm == "":
                        print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
                    elif input_val(am_or_pm, False, True)[0]:
                        print("{:^60}".format("[  Special characters or numbers detected, try again.  ]\n"))
                    elif str(input_val(am_or_pm, False, True)[1]).lower() not in ["am", "pm"]:
                        print("{:^60}".format("[  Enter either AM or PM, try again.  ]\n"))

                    am_or_pm = str(input("Input AM or PM (lower case is accepted) : ")).replace(" ","")

                am_or_pm = str(input_val(am_or_pm, False, True)[1]).lower()

                if var == "Start":
                    start_input = hour + ":" + minute +  am_or_pm
                else:
                    end_input = hour + ":" + minute +  am_or_pm

                count += 1
            
            if len(list(conn.execute(f"SELECT start, end from {day[target]}_class"))) == 0:
                overlap = False
            else:
                for row in conn.execute(f"SELECT start, end from {day[target]}_class"):
                    if time_validator(start_input, end_input, row[0], row[1]):
                        clear()
                        display_class_list(target)
                        print("{:^60}".format("[  Error  ]"))
                        print("{:^60}".format("[  Time inputed overlaps with existing classes, try again.  ]\n"))
                        input("{:^60}".format("PRESS ANY KEY TO RETRY"))
                        overlap = True
                        break
                    else:
                        overlap = False
                        
            

        # PROMPT USER TO INPUT TEACHERS NAME
        display_class_list(target)
        print(f"Class No. : {class_no}")
        print(f"Time      : {start_input} - {end_input}")

        teacher_name = str(input("\nTeacher name: "))
        while input_val(teacher_name, False, True)[0]:
            display_class_list(target)

            print(f"Class No. : {class_no}")
            print(f"Time      : {start_input} - {end_input}")
            if teacher_name == command_to_return:
                return "y"
            elif teacher_name == command_to_quit:
                end_screen()
            elif teacher_name.isspace() or teacher_name == "":
                print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
            elif input_val(teacher_name, False, True)[0]:
                print("{:^60}".format("[  Special characters or numbers detected, try again.  ]\n"))

            teacher_name = str(input("\nTeacher name: "))

        add_class_schedule(target, class_no, start_input, end_input, teacher_name)


        display_class_list(target)
        wish_to_continue = str(input("Would you like to add another class? [ y / n ]: ")).replace(" ","")
        while input_val(wish_to_continue, False, True)[0] or str(input_val(wish_to_continue, False, True)[1]) not in ["y", "n"]:
            display_class_list(target)
            if wish_to_continue == command_to_return:
                return "n"
            elif wish_to_continue == command_to_quit:
                end_screen()
            elif wish_to_continue.isspace() or wish_to_continue == "":
                print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
            elif input_val(wish_to_continue, False, True)[0]:
                print("{:^60}".format("[  Special characters or numbers detected, try again.  ]\n"))
            elif str(input_val(wish_to_continue, False, True)[1]) not in ["y", "n"]:
                print("{:^60}".format("[  Type either y or n, try again.  ]\n"))
            wish_to_continue = str(input("Would you like to add another class? [ y / n ]: ")).replace(" ","")

    return "y"

# The tab where user gets to remove classes
def removing_class_tab(target_day):
    # Display class list for removing classes
    def display__remove_class_list():
        global use_for_validation
        clear()
        print("{:^60}".format(f"[  Currently Removing Class {day[target_day].title()}  ]"))
        print("____________________________________________________________")
        print ("\x1B[4m|{:^11}|{:^19}|{:^26}|\x1B[0m".format("Class No.", "Time", "Teacher"))
        use_for_validation = []
        for row in conn.execute(f"SELECT class_no, start, end, teacher from {day[target_day]}_class ORDER BY class_no ASC"):
            use_for_validation.append(row[0])
            time = row[1] + " - " + row[2]
            print ("|{:^11}|{:^19}|{:^26}| ".format(row[0], time, row[3]))
        print(overline * 60)
        print("{:^60}".format(f"[  #back to return  ]\n"))

    display__remove_class_list()
    class_no = str(input("Enter class number : ")).replace(" ","")
    while input_val(class_no, True, False)[0] or int(input_val(class_no, True, False)[1]) not in use_for_validation:
        display__remove_class_list()
        if class_no == command_to_return:
            return "y"
        elif class_no == command_to_quit:
            end_screen()
        elif class_no.isspace() or class_no == "":
            print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
        elif input_val(class_no, True, False)[0]    :
            print("{:^60}".format("[  Special characters or alphbets detected, try again.  ]\n"))
        elif int(input_val(class_no, True, False)[1]) not in use_for_validation:
            print("{:^60}".format("[  Class number does not exist, try again.  ]\n"))

        class_no = str(input("Enter class number : ")).replace(" ","")
    class_no = int(input_val(class_no, True, False)[1])

    display__remove_class_list()
    print("{:^60}".format(f"Are you sure you want to remove class number [ {class_no} ]?\n"))
    confirmation = str(input(f"                    Enter [y / n] : ")).replace(" ","")
    while input_val(confirmation, False, True)[0] or str(input_val(confirmation, False, True)[1]) not in ("y","n"):
        display__remove_class_list()
        if confirmation == command_to_return:
            break
        elif confirmation == command_to_quit:
            end_screen()
        elif confirmation.isspace() or confirmation == "":
            print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
        elif input_val(confirmation, False, True)[0]:
            print("{:^60}".format("[  Special characters or alphbets detected, try again.  ]\n"))
        elif str(input_val(confirmation, False, True)[1]) not in ("y","n"):
            print("{:^60}".format("[  Type either y or n, try again.  ]\n"))

        print("{:^60}".format(f"Are you sure you want to remove class number [ {class_no} ]?\n"))
        confirmation = str(input(f"                      Enter [y / n] : ")).replace(" ","")
    
    confirmation = str(input_val(confirmation, False, True)[1])

    if confirmation in (command_to_return, "n"):
        return "y"
    else:      
        delete_class_schedule(target_day, class_no)

    return "y"

# The tab where user edits the existing page
def editing_class_tab(target_day):
    # Display the class list for the edit page
    def display_edit_class_list():
        global use_for_validation
        clear()
        print("{:^59}".format(f"[{day[target_day].title()}]"))
        print("____________________________________________________________")
        print ("\x1B[4m|{:^11}|{:^20}|{:^25}|\x1B[0m".format("Class No.", "Time", "Teacher"))
        
        use_for_validation = []
        for row in conn.execute(f"SELECT class_no, start, end, teacher from {day[target_day]}_class ORDER BY class_no ASC"):
            use_for_validation.append(row[0])
            time = row[1] + " - " + row[2]
            print ("|{:^11}|{:^20}|{:^25}| ".format(row[0], time, row[3]))

        print(overline * 60)
        print("{:^60}".format(f"[  #back to return  ]\n"))

    wish_to_continue = "y"
    while wish_to_continue == "y":
        display_edit_class_list()
        class_no = str(input("Enter class number : ")).replace(" ","")

        while input_val(class_no, True, False)[0] or int(input_val(class_no, True, False)[1]) not in use_for_validation:
            display_edit_class_list()
            if class_no == command_to_return:
                return "y"
            elif class_no == command_to_quit:
                end_screen()
            elif class_no.isspace() or class_no == "":
                print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
            elif input_val(class_no, True, False)[0]:
                print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]\n"))
            elif int(input_val(class_no, True, False)[1]) not in use_for_validation:
                print("{:^60}".format("[  Enter number between 1 - 3, try again.  ]\n"))

            class_no = str(input("Enter class number : ")).replace(" ","")

        class_no = int(input_val(class_no, True, False)[1])

        use_for_validation.remove(class_no)
        
        display_edit_class_list()
        print(textwrap.dedent("""\
        ~~~~~~~~~~~~~~~~~~~~  Option Selection  ~~~~~~~~~~~~~~~~~~~~
        (1) Class Number       
        (2) Time
        (3) Teacher        

        [0] Back
        """))

        target_option = str(input("Enter the category (number) you wish to change : ")).replace(" ","")
        
        while input_val(target_option, True, False)[0] or int(input_val(target_option, True, False)[1]) not in range(0,4):
            display_edit_class_list()
            print(textwrap.dedent("""\
            ~~~~~~~~~~~~~~~~~~~~  Option Selection  ~~~~~~~~~~~~~~~~~~~~
            (1) Class Number       
            (2) Time
            (3) Teacher
                        
            [0] Back
            """))
            if target_option == command_to_return:
                return "y"
            elif target_option == command_to_quit:
                end_screen()
            elif target_option.isspace() or target_option == "":
                print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
            elif input_val(target_option, True, False)[0]:
                print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]\n"))
            elif int(input_val(target_option, True, False)[1]) not in range(0,4):
                print("{:^60}".format("[  Enter number between 1 - 3, try again.  ]\n"))

            target_option = str(input("Enter the category (number) you wish to change : ")).replace(" ","")

        target_option = int(input_val(target_option, True, False)[1])

        if target_option == 0:
            return "y"

        elif target_option == 1:
            display_edit_class_list()
            edited_class_no = str(input("Enter new class number : ")).replace(" ","")
            while input_val(edited_class_no, True, False)[0] or int(input_val(edited_class_no, True, False)[1]) in use_for_validation:
                display_edit_class_list()
                if edited_class_no == command_to_return:
                    return "y"
                elif edited_class_no == command_to_quit:
                    end_screen()
                elif edited_class_no.isspace() or edited_class_no == "":
                    print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
                elif input_val(edited_class_no, True, False)[0]:
                    print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]\n"))
                elif int(input_val(edited_class_no, True, False)[1]) in use_for_validation:
                    print("{:^60}".format("[  Number taken, try again.  ]\n"))
                
                edited_class_no = str(input("Enter new class number : ")).replace(" ","")

            edited_class_no = int(input_val(edited_class_no, True, False)[1])
        
            update_class_schedule(target_day, class_no, "class_no", edited_class_no) 

        elif target_option == 2:
            Input = ["Start", "End"]
            overlap = True
            while overlap == True:
                count = 1
                for var in Input:
                    def temp_display():
                        display_edit_class_list()
                        print("{:^60}".format(f"Currently editting class [ {class_no} ]\n"))
                        if count == 2:
                            print(f"Start of Class   : {start_input}\n")
                        print("{:^60}".format(f"-------- {var} of class --------"))
                        
                    temp_display()
                    hour = str(input("Enter hour [1 - 12] : ")).replace(" ","")
                    while input_val(hour, True, False)[0] or int(input_val(hour, True, False)[1]) not in range(1, 13):
                        temp_display()
                        if hour == command_to_return:
                            return "y"
                        elif hour == command_to_quit:
                            end_screen()
                        elif hour.isspace() or hour == "":
                            print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
                        elif input_val(hour, True, False)[0]:
                            print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]\n"))
                        elif int(input_val(hour, True, False)[1]) not in range(1, 13):
                            print("{:^60}".format("[  Enter numbers between 1 - 12, try again  ]\n"))

                        hour = str(input("Enter hour [1 - 12] : ")).replace(" ","")                   
                    hour = str(input_val(hour, True, False)[1]).zfill(2)

                    temp_display()
                    print("{:^60}".format(f"Hour : {hour}\n"))
                    minute = str(input("Enter minute [0 - 59] : ")).replace(" ","")
                    while input_val(minute, True, False)[0] or int(input_val(minute, True, False)[1]) not in range(0, 60):
                        temp_display()
                        print("{:^60}".format(f"Hour : {hour}\n"))
                        if minute == command_to_return:
                            return "y"
                        elif minute == command_to_quit:
                            end_screen()
                        elif minute.isspace() or minute == "":
                            print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
                        elif input_val(minute, True, False)[0]:
                            print("{:^60}".format("[  Special characters or alphabets detected, try again.  ]\n"))
                        elif int(input_val(minute, True, False)[1]) not in range(1, 13):
                            print("{:^60}".format("[  Enter numbers between 0 - 59, try again  ]\n"))

                        minute = str(input("Enter minute [0 - 59] : ")).replace(" ","")
                    minute = str(input_val(minute, True, False)[1]).zfill(2)

                    temp_display()
                    print("{:^60}".format(f"Time : {hour}:{minute}\n"))
                    am_or_pm = str(input("Input AM or PM (lower case is accepted) : ")).replace(" ","")
                    while input_val(am_or_pm, False, True)[0] or str(input_val(am_or_pm, False, True)[1]).lower() not in ["am", "pm"]:
                        temp_display()
                        print("{:^60}".format(f"Time : {hour}:{minute}\n"))
                        if am_or_pm == command_to_return:
                            return "y"
                        elif am_or_pm == command_to_quit:
                            end_screen()
                        elif am_or_pm.isspace() or am_or_pm == "":
                            print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
                        elif input_val(am_or_pm, False, True)[0]:
                            print("{:^60}".format("[  Special characters or numbers detected, try again.  ]\n"))
                        elif str(input_val(am_or_pm, False, True)[1]).lower() not in ["am", "pm"]:
                            print("{:^60}".format("[  Enter either AM or PM, try again.  ]\n"))

                        am_or_pm = str(input("Input AM or PM (lower case is accepted) : ")).replace(" ","")

                    am_or_pm = str(input_val(am_or_pm, False, True)[1]).lower()

                    if var == "Start":
                        start_input = hour + ":" + minute +  am_or_pm
                    else:
                        end_input = hour + ":" + minute +  am_or_pm

                    count += 1
                
                if len(list(conn.execute(f"SELECT start, end from {day[target_day]}_class"))) == 0:
                    overlap = False
                else:
                    for row in conn.execute(f"SELECT start, end from {day[target_day]}_class"):
                        if time_validator(start_input, end_input, row[0], row[1]):
                            clear()
                            display_edit_class_list()
                            print("{:^60}".format("[  Error  ]"))
                            print("{:^60}".format("[  Time inputed overlaps with existing classes, try again.  ]\n"))
                            input("{:^60}".format("PRESS ANY KEY TO RETRY"))
                            overlap = True
                            break
                        else:
                            overlap = False

            update_class_schedule(target_day, class_no, "start", start_input)
            update_class_schedule(target_day, class_no, "end", end_input)

        elif target_option == 3:
            display_edit_class_list()
            teacher_name = str(input("\nNew teacher name : "))
            while input_val(teacher_name, False, True)[0]:
                display_edit_class_list()
                if teacher_name == command_to_return:
                    return "n"
                elif teacher_name == command_to_quit:
                    end_screen()
                elif teacher_name.isspace() or teacher_name == "":
                    print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
                elif input_val(teacher_name, False, True)[0]:
                    print("{:^60}".format("[  Special characters or numbers detected, try again.  ]\n"))
                teacher_name = str(input("New teacher name : "))

            update_class_schedule(target_day, class_no, "teacher", teacher_name)

        display_edit_class_list()
        wish_to_continue = str(input("Would you like to edit another class? [ y / n ]: ")).replace(" ","")
        while input_val(wish_to_continue, False, True)[0] or str(input_val(wish_to_continue, False, True)[1]) not in ["y", "n"]:
            display_edit_class_list()
            if wish_to_continue == command_to_return:
                return "n"
            elif wish_to_continue == command_to_quit:
                end_screen()
            elif wish_to_continue.isspace() or wish_to_continue == "":
                print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
            elif input_val(wish_to_continue, False, True)[0]:
                print("{:^60}".format("[  Special characters or numbers detected, try again.  ]\n"))
            elif str(input_val(wish_to_continue, False, True)[1]) not in ["y", "n"]:
                print("{:^60}".format("[  Type either y or n, try again.  ]\n"))

            wish_to_continue = str(input("Would you like to edit another class? [ y / n ]: ")).replace(" ","")

    return "y"



# Main part of the class handling function
def Class_Handling_Page(): 
    resume_input = "y"

    while resume_input == "y":
        clear()
        decision = main_menu_of_teacher_tab()
        if decision == 0 or decision == "y":
            resume_input = "n"
            break
        elif decision == 1: 
            resume_input  = adding_new_class_tab()
        else:
            if display_available_days_to_edit() == "y":
                resume_input = "y"
            else:
                if decision == 2:
                    resume_input = editing_class_tab(target_day)
                elif decision == 3:
                    resume_input = removing_class_tab(target_day)