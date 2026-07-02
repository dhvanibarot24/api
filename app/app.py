from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class Teacher(BaseModel):
    name: str
    subject: str

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
                        teacher_id INTEGER NOT NULL,
                        standard INTEGER NOT NULL,
                         room_no TEXT NOT NULL,
                         start_time TEXT NOT NULL,
                         end_time TEXT NOT NULL
    
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


@app.get("/")
def home():
    return {"message": "API is running"}

