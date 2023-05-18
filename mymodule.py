import os
import textwrap
import sqlite3
import random
import datetime
import calendar
import locale

locale.setlocale(locale.LC_ALL,"")

conn = sqlite3.connect("yattabase.db")
clear = lambda: os.system("cls")

command_to_return = "#back"
command_to_quit = "#quit"

overline = "\u203E" # Used to make overlines in tables

day = {1 : "monday", 2 : "tuesday", 3 : "wednesday", 4 : "thursday", 5 : "friday", 6 : "saturday", 7 : "sunday"}
month = {1 : "january", 2 : "february", 3 : "march", 4 : "april", 5 : "may", 6 : "june", 7 : "july", 8 : "august", 9 : "september", 10 : "october", 11 : "november", 12 : "december"}

past_year = conn.execute("SELECT year FROM internal_data").fetchone()

if past_year[0] < datetime.date.today().year:
    conn.execute(f"UPDATE internal_data set 'year' = {datetime.date.today().year}")
    conn.execute("DELETE from student_data")
    for row in month:
        conn.execute(f"DELETE from {month[row]}")
    conn.commit()

cursor = conn.execute("SELECT year, fee FROM internal_data").fetchone()
current_year = cursor[0]
current_fee = cursor[1]

def phone_val(number):
    if len(number) == 10:
        return number[0] == "0" and number.isnumeric()
    else:
        return False

def input_val(input, IfWord, IfNum):
    if input.isspace() or input == "":
        return True, input
    else:
        tempvar = input.replace(" ", "")
        return (tempvar.isalpha() == IfWord or tempvar.isnumeric() == IfNum), input.replace("  "," ")

def add_student(student_id, name, age, contact, day, class_no, fee, month_no):
    conn = sqlite3.connect("yattabase.db")
    conn.execute(f"INSERT INTO student_data (student_id, name, age, contact, day, class_no, fee) \
        VALUES ({student_id}, '{name}', {age}, '{contact}', '{day}', {class_no}, {fee})")
    
    conn.execute(f"INSERT INTO {month[month_no]} (student_id, name) VALUES ({student_id}, '{name}')")

    conn.commit()

def update_student(id, target, correction):
    conn = sqlite3.connect("yattabase.db")
    conn.execute(f"UPDATE student_data set '{target}' = '{correction}' where student_id = {id}")
    conn.commit()

def delete_student(id):
    conn = sqlite3.connect("yattabase.db")
    conn.execute(f"DELETE from student_data where student_id = {id}")
    for row in month:
        conn.execute(f"DELETE from {row[month]} wheres student_id = {id}")
    conn.commit()

def add_class_schedule(day_no, class_no, start, end, teacher):
        conn = sqlite3.connect("yattabase.db")
        conn.execute(f"INSERT INTO {day[day_no]}_class (class_no, start, end, teacher) \
            VALUES ('{class_no}', '{start}', '{end}', '{teacher}')")
        conn.commit()

def update_class_schedule(day_no, class_no, target, correction):
    conn = sqlite3.connect("yattabase.db")
    conn.execute(f"UPDATE {day[day_no]}_class set {target} = '{correction}' where class_no = {class_no}")
    conn.commit()

def delete_class_schedule(day_no, class_no):
    conn = sqlite3.connect("yattabase.db")
    conn.execute(f"DELETE from {day[day_no]}_class where class_no = {class_no}")
    conn.commit()

def time_validator(input_1_start, input_1_end, input_2_start, input_2_end):
    
    def check_overlap(input_1_start, input_1_end, input_2_start, input_2_end):
        if input_1_start < input_2_start:
            return input_1_end > input_2_start
        elif input_1_start > input_2_start:
            return input_2_end > input_1_start
        else:
            return True

    # Extract the hours and minutes from the time strings
    input_1_start_hour, input_1_start_minute = map(int, input_1_start[:-2].split(':'))
    input_1_end_hour, input_1_end_minute = map(int, input_1_end[:-2].split(':'))

    input_2_start_hour, input_2_start_minute = map(int, input_2_start[:-2].split(':'))
    input_2_end_hour, input_2_end_minute = map(int, input_2_end[:-2].split(':'))

    # Adjust the hours for PM times
    if input_1_start[-2:] == 'pm' and input_1_start_hour < 12:
        input_1_start_hour += 12
    if input_1_end[-2:] == 'pm' and input_1_end_hour < 12:
        input_1_end_hour += 12

    if input_2_start[-2:] == 'pm' and input_2_start_hour < 12:
        input_2_start_hour += 12
    if input_2_end[-2:] == 'pm' and input_2_end_hour < 12:
        input_2_end_hour += 12

    # Check if the intervals overlap
    overlap = check_overlap(
        input_1_start_hour * 60 + input_1_start_minute,
        input_1_end_hour * 60 + input_1_end_minute,
        input_2_start_hour * 60 + input_2_start_minute,
        input_2_end_hour * 60 + input_2_end_minute
    )

    if overlap:
        return True
    else:
        return False

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
    
def end_screen():
    clear()
    print(textwrap.dedent("""

               [  PyTutor Helper wishes you a safe travels!  ]          


    ████████                      ██  ██                                 
    ██                            ██  ██                          ██  ██
    ██  ▓▓▓▓  ▓▓▓▓▓▓  ██▓▓▓▓  ▓▓▓▓██  ██▓▓▓▓  ▓▓  ██  ▓▓▓▓▓▓      ██  ██
    ██    ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██           
    ████████  ██████  ██████  ██████  ██████  ██████  ██████   ██        ██
                                                  ██  ██         ████████       
    ████████████████████████████████████████  ██████  ██████       """))

    quit()

