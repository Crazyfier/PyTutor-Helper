import sqlite3
import mymodule
import textwrap
import Registration

decision = -1

while decision != 0:
    mymodule.clear()
    print(textwrap.dedent("""
    What would you like to do?
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    (1) Register Student  | Register a new student
    (2) Student List      | View/edit student list
    (3) Student Fee       |

    [0] Exit
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""))

    decision = str(input("Enter your option [0/1/2/3]: "))

    while (mymodule.input_val(decision, True, False)[0]) or int(mymodule.input_val(decision, True, False)[1]) not in [0, 1, 2, 3]:
        decision = str(input("Invalid option, try again [0/1/2/3]: "))

    decision = int(mymodule.input_val(decision, True, False)[1]) 

    mymodule.clear()

    proceed = "y"
    if decision == 1:
        while proceed == "y":
            print("~~~~~Registration~~~~~\n")
            proceed = Registration.registration()

    elif decision == 2:
        conn = sqlite3.connect('Student_Data.db')
        cursor = conn.execute("SELECT rowid, name, age, contact, month, day, time, teacher from student_data")
        print ("{:<3} {:<20} {:<3} {:<11} {:<9} {:<12} {:<15} {:<30}".format("ID", "Name", "Age", "Contact", "Month", "Day", "Time", "Teacher"))

        id = {}
        for row in cursor:
            id[row[0]] = row[1], row[2], row[3], row[4], row[5], row[6], row[7]
            print ("{:<3} {:<20} {:<3} {:<11} {:<9} {:<12} {:<15} {:<30}".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        
        while proceed == "y":
            print(textwrap.dedent("""
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            (1) Edit Student Info
            (2) Remove Student
            
            [0] Back
            """))

            decision = str(input("Enter your option [0/1/2]: "))
            while (mymodule.input_val(decision, True, False)[0]) or int(mymodule.input_val(decision, True, False)[1]) not in [0, 1, 2]:
                decision = str(input("Invalid option, try again [0/1/2]: "))
            decision = str(mymodule.input_val(decision, True, False)[1])

            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            if decision == "1":

                student_number = str(input("Enter student number: ")).replace(" ","")
                while (mymodule.input_val(student_number, True, False)[0]) or int(mymodule.input_val(student_number, True, False)[1]) not in id:
                    student_number = str(input("Invalid student number, try again: "))

                student_number = str(mymodule.input_val(student_number, True, False)[1])

                print(textwrap.dedent("""
                (1) Name       (5) Day
                (2) Age        (6) Time
                (3) Contact    (7) Teacher
                (4) Month      
                """))
                target = str(input("Enter the number of the category one wish to change: ")).replace(" ","")
                
                category = {1 : "name", 2 : "age", 3 : "contact", 4 : "month", 5 : "day", 6 : "time", 7 : "teacher"}
                while (mymodule.input_val(target, True, False)[0]) or int(mymodule.input_val(target, True, False)[1]) not in category:
                    target = str(input("Invalid option, its up there: "))

                target = int(mymodule.input_val(target, True, False)[1])
            
                if target == "name":

                    correction = str(input("Enter change: ")).replace(" ","")
                    while (mymodule.input_val(correction, False, True)[0]):
                        correction = str(input("Invalid input, try again: "))

                    correction = str(mymodule.input_val(correction, False, True)[1])

                elif target == "age":

                    correction = str(input("Age: ")).replace(" ","")
                    while (mymodule.input_val(correction, True, False)[0]) or int(mymodule.input_val(correction, False, True)[1]) > 50:
                        print("Input only accepts numbers.")
                        correction = str(input("Age: ")).replace(" ","")

                    correction = int(mymodule.input_val(correction, False, True)[1])

                elif target == "contact":

                    correction = str(input("Phone Number: ")).replace(" ","")
                    while (mymodule.input_val(correction, True, False)[0]) or mymodule.phone_val(correction) == False:
                        print("Input 10-digit mobile number.")
                        correction = str(input("Phone Number: ")).replace(" ","")

                elif target == "month":

                    correction = str(input("Enter the number of month [1 - 12]: ")).replace(" ","")
                    while (mymodule.input_val(correction, True, False)[0]) or str(mymodule.input_val(correction, True, False)[1]) not in mymodule.month:
                        print("Enter a number from 1 - 12.")
                        correction = str(input("Enter the number of month [1 -12]: ")).replace(" ","")

                elif target == "day":

                    correction = str(input("Enter day of the week [1 - 7]: ")).replace(" ","")
                    while (mymodule.input_val(correction, True, False)[0]) or str(mymodule.input_val(correction, True, False)[1]) not in mymodule.day:
                        print("Enter a number from 1 - 7.")
                        correction = str(input("Enter day of the week [1 - 7]: ")).replace(" ","")

                elif target == "time":
                    # Getting a specific data from the data base that is the students schedule day
                    conn = sqlite3.connect('Student_Data.db')
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT * from Student_Data where rowid = {student_number}")
                    record = cursor.fetchone()

                    conn = sqlite3.connect('Class_Schedule.db')
                    cursor = conn.execute(f"SELECT class_no, time, teacher from {mymodule.day[record[4].lower()]}_class")
                    print ("\x1B[4m  {:<1} |{:^15} |{:^19} \x1B[0m".format("", "Time", "Teacher"))

                    #Classifying time and teacher into a dictionary to store in mymodule
                    class_data = {}
                    for row in cursor:
                        class_data[row[0]] = row[1], row[2]
                        print ("({:<1}) |{:^15} |{:^19}".format(row[0], row[1], row[2]))
                    print("")

                    # Entering Time
                    correction = str(input("Enter Number: ")).replace(" ","")
                    while (mymodule.input_val(correction, True, False)[0]) or str(mymodule.input_val(correction, True, False)[1]) not in class_data:
                        print("I want you to think again.")
                        correction = str(input("Enter Number: ")).replace(" ","")
                    
                    correction = int(mymodule.input_val(correction, True, False)[1])

                    mymodule.update_student(student_number, "teacher", class_data[correction][2])
                mymodule.update_student(student_number, category[target], correction)

            elif decision =="2":

                mymodule.delete_student()
            

print("PyTutor Helper wishes you a safe travels!")
print("""                                                                                
████████                      ██  ██                                  
██                            ██  ██                                  
██  ▓▓▓▓  ▓▓▓▓▓▓  ██▓▓▓▓  ▓▓▓▓██  ██▓▓▓▓  ▓▓  ██  ▓▓▓▓▓▓              
██    ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██              
████████  ██████  ██████  ██████  ██████  ██████  ██████              
                                              ██  ██                  
████████████████████████████████████████  ██████  ██████    ██  ██  ██
                                                                         
""")















