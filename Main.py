
from mymodule import *
from Registration import hey_new_people
from Student_List import oh_look_students
from teacher import teacher_see_teacher_do

decision = -1
while decision != '0':
    clear()
    print(textwrap.dedent(f"""\
    [Commands] Type them into any input to execute.

    #back  =>  To return to previous page
    #quit  =>  To exit anytime

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~       
                            What would you like to do?
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    (1) Register Student            | Add a new student
    (2) Student List                | [ View / Edit ] Student list
    (3) Class Handling              | [ View / Edit ] Classes
    (4) Change Fee                  | [ View / Edit ] Fee

    [0] Exit                        | ESCAPE
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""))

    decision = str(input("Enter your option : ")).replace(" ","")
    while input_val(decision, True, False)[0] or int(input_val(decision, True, False)[1]) not in range(0,5):
        clear()
        print(textwrap.dedent(f"""\
        [Commands] Type them into any input to execute.

        #back  =>  To return to previous page
        #quit  =>  To exit anytime

        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~       
                            What would you like to do?
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        (1) Register Student            | Add a new student
        (2) Student List                | [ View / Edit ] Student list
        (3) Class Handling              | [ View / Edit ] Classes
        (4) Change Fee                  | [ View / Edit ] Fee

        [0] Exit                        | ESCAPE
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """))

        if decision == command_to_return or decision == command_to_quit:
            end_screen()
        elif decision.isspace() or decision == "":
            print("{:^60}".format("[  Come on you didn't even type, try again.  ]"))
        elif input_val(decision, True, False)[0]:
            print("{:^60}".format("[  Special characters or alphbets detected, try again.  ]"))
        elif int(input_val(decision, True, False)[1]) not in range(0,3):
            print("{:^60}".format("[  Type number between 0 - 4, try again.  ]"))

        decision = str(input("\nEnter your option : ")).replace(" ","") 

    clear()
    if decision == '0':
        end_screen()
    elif decision == '1' :
        hey_new_people()
    elif decision == '2' :
        oh_look_students()
    elif decision == '3' :
        teacher_see_teacher_do()
    elif decision == '4' :
        clear()

        current_fee = conn.execute("SELECT year, fee FROM internal_data").fetchone()[1]
        print("{:^60}".format(f"Current fee is {locale.currency(current_fee)} per session.\n"))
        print("{:^60}".format(f"[  Type #back to return  ]\n"))

        new_fee = str(input("Enter in new fee (numbers only) : ")).replace(" ","")
        while isfloat(new_fee) == False:
            clear()
            print("{:^60}".format(f"Current fee is {locale.currency(current_fee)} per session.\n"))
            print("{:^60}".format(f"[  Type #back to return  ]\n"))

            if new_fee == command_to_return:
                    break
            elif new_fee == command_to_quit:
                end_screen()
            elif new_fee.isspace() or new_fee == "":
                print("{:^60}".format("[  Come on you didn't even type, try again.  ]\n"))
            elif isfloat(new_fee):
                print("{:^60}".format("[  Special characters or alphbets detected, try again.  ]\n"))
                
            new_fee = str(input("Enter in new fee (numbers only) : ")).replace(" ","")

        if new_fee != command_to_return:
            new_fee = float(input_val(new_fee, False, True)[1])

            confirmation = str(input("\nAre you sure? [y / n]: ")).replace(" ","")
            while input_val(confirmation, False, True)[0] or str(input_val(confirmation, False, True)[1]) not in ("y","n"):
                clear()
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
                confirmation = str(input("\nAre you sure? [y / n] : ")).replace(" ","")

            clear()
            if confirmation == "y":
                conn.execute(f"UPDATE internal_data set fee = {new_fee}")
                conn.commit()

                print("{:^60}".format(f"[  Fee changed to {locale.currency(new_fee)}  ]\n"))
                input("{:^60}".format("PRESS ANY KEY TO RETURN"))
            elif confirmation == "n":
                print("{:^60}".format("[  Changed Cancelled  ]\n"))
                input("{:^60}".format("PRESS ANY KEY TO RETURN"))
        


