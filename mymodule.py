import os
import textwrap
import sqlite3

conn = sqlite3.connect("yattabase.db")

command_to_quit = "#back"

clear = lambda: os.system("cls")

day = {1 : "monday", 2 : "tuesday", 3 : "wednesday", 4 : "thursday", 5 : "friday", 6 : "saturday", 7 : "sunday"}

month = {1 : "january", 2 : "february", 3 : "march", 4 : "april", 5 : "may", 6 : "june", 7 : "july", 8 : "august", 9 : "september", 10 : "october", 11 : "november", 12 : "december"}

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
    


import sqlite3

def add_student(name, age, contact, month, day, time, teacher, fee):
    conn = sqlite3.connect("yattabase.db")
    conn.execute(f"INSERT INTO student_data (name, age, contact, month, day, time, teacher, fee) \
        VALUES ('{name}', {age}, '{contact}', '{month}', '{day}', '{time}', '{teacher}', {fee})")
    conn.commit()
    conn.close()

def update_student(number, target, correction):
    conn = sqlite3.connect("yattabase.db")
    conn.execute(f"UPDATE student_data set '{target}' = '{correction}' where rowid = {number}")
    conn.commit()
    conn.close()

def delete_student(id):
    conn = sqlite3.connect("yattabase.db")
    conn.execute(f"DELETE from student_data where rowid = {id}")
    conn.commit()
    conn.close()


option = { 1 : "monday_class", 2 : "tuesday_class", 3 : "wednesday_class", 4 : "thurdsday_class", 5 : "friday_class", 6 : "saturday_class", 7 : "sunday_class"}

def add_class_schedule(day, class_no, time, teacher):
        conn = sqlite3.connect("yattabase.db")
        conn.execute(f"INSERT INTO {option[day]} (class_no, time, teacher) \
            VALUES ('{class_no}', '{time}', '{teacher}')")
        conn.commit()
        conn.close()

def update_class_schedule(day, number, target, correction):
    conn = sqlite3.connect("yattabase.db")
    conn.execute(f"UPDATE {option[day]} set {target} = {correction} where class_no = {number}")
    conn.commit()
    conn.close()

def delete_class_schedule(day, id):
    conn = sqlite3.connect("yattabase.db")
    conn.execute(f"DELETE from {option[day]} where class_no = {id}")
    conn.commit()
    conn.close()
