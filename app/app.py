from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class Teacher(BaseModel):
    name: str
    subject: str

class timetable(BaseModel):
    t_id: int
    std: int
    class_no: str
    start: str
    end: str

def connect():
    return sqlite3.connect('database.db')   

def cr_tables():
    conn = connect()
    cursor=conn.cursor()
    cursor.execute(''' create table if not exists teacher   
                    (id integer primary key autoincrement,
                    name text ,
                    subject text )''')
    
    cursor.execute(''' CREATE TABLE IF NOT EXISTS schedule(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        t_id INTEGER NOT NULL,
                        std INTEGER NOT NULL,
                         class_no TEXT NOT NULL,
                         start TEXT NOT NULL,
                         end TEXT NOT NULL

    )''')

@app.post("/teachers")
def add(teacher: Teacher):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO teacher(name, subject)
        VALUES(?, ?)
        """,
        (teacher.name, teacher.subject)
    )
    conn.commit()
    conn.close()

    return {"message": "Teacher added successfully"}

cr_tables()

@app.get("/teachers")
def get_data():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM teacher")
    teachers = cursor.fetchall()
    conn.close()

    return {"teachers": teachers}

@app.put("/techers/{name}")
def update(name : str, teacher : Teacher):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(""" UPDATE teacher SET subject = ? WHERE name = ? """,
                   (teacher.subject, name))
    conn.commit()
    conn.close()

    return {"message": "Teacher updated successfully"}
@app.delete("/teachers/{name}")
def delete(name : str):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(""" DELETE FROM teacher WHERE name = ? """, (name,))
    conn.commit()
    conn.close()

    return {"message": "Teacher deleted successfully"}

@app.post("/timetable")
def add(data :timetable):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(("""
        INSERT INTO schedule(t_id, std, class_no, start, end)
        VALUES(?, ?, ?, ?, ?)
    """), (data.t_id, data.std, data.class_no, data.start, data.end))
    conn.commit()
    conn.close()

    return {"message": "Schedule added successfully"}

@app.get("/timetable")
def get_data():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM timetable")
    timetable = cursor.fetchall()
    conn.close()

    return {"timetable": timetable}

@app.get("/")
def home():
    return {"message": "API is running"}

