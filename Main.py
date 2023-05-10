from mymodule import *
from Registration import hey_new_people
from Student_List import oh_look_students

conn.execute('''CREATE TABLE IF NOT EXISTS student_data(name TEXT age INT contact TEXT month TEXT day TEXT class_no INT fee FLOAT)''')

decision = -1

while decision != 0:
    clear()
    print(textwrap.dedent("""
    [Commands] Type in #back into any input to return to previous page.
               
    What would you like to do?
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    (1) Register Student  | Register a new student
    (2) Student List      | View/edit student list
    (3) Student Fee       |

    [0] Exit
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""))

    decision = str(input("Enter your option [0/1/2/3]: ")).replace(" ","")
    while (input_val(decision, True, False)[0]) or int(input_val(decision, True, False)[1]) not in [0, 1, 2, 3]:
        
        decision = str(input("Invalid option, try again [0/1/2/3]: ")).replace(" ","")

    
    decision = int(input_val(decision, True, False)[1]) 

    clear()

    proceed = "y"
    if decision == 1:
        while proceed == "y":
            proceed = hey_new_people()

    elif decision == 2:
        while proceed == "y":
            proceed = oh_look_students()
            
print(int(input_val(decision, True, False)[1]))
print("PyTutor Helper wishes you a safe travels!")
print("""                                                                                
████████                      ██  ██                                 
██                            ██  ██                          ██  ██
██  ▓▓▓▓  ▓▓▓▓▓▓  ██▓▓▓▓  ▓▓▓▓██  ██▓▓▓▓  ▓▓  ██  ▓▓▓▓▓▓      ██  ██
██    ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██           
████████  ██████  ██████  ██████  ██████  ██████  ██████   ██        ██
                                              ██  ██         ████████       
████████████████████████████████████████  ██████  ██████       
                                                                         
""")

