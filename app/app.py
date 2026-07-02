from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="Coaching Center Schedule Management")

def connect():
    return sqlite3.connect("database.db")


def cr_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS teacher(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        subject TEXT NOT NULL)
    """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS timetable(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        t_id INTEGER NOT NULL,
        std INTEGER NOT NULL,
        class_no TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL)
    """)
    conn.commit()
    conn.close()
cr_tables()


class Teacher(BaseModel):
    name: str
    subject: str


class Timetable(BaseModel):
    t_id: int
    std: int
    class_no: str
    start_time: str
    end_time: str


@app.get("/")
def home():
    return {"message": " Schedule Management API"}


@app.post("/teachers")
def add_teacher(teacher: Teacher):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO teacher(name, subject)
        VALUES(?,?)
    """, (teacher.name, teacher.subject))
    conn.commit()
    conn.close()


    return {"message": "teacher Added Successfully"}


@app.get("/teachers")
def get_teachers():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM teacher")

    data = cursor.fetchall()

    conn.close()

    data = []
    for row in data:
        teacher = {
            "id": row[0],
            "name": row[1],
            "subject": row[2]
        }
        data.append(teacher)

    return data


@app.put("/teachers/{id}")
def update_teacher(id: int, teacher: Teacher):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""UPDATE teacher SET name=?, subject=? WHERE id=?""", 
        (teacher.name, teacher.subject, id))
    conn.commit()
    conn.close()

    return {"message": "teacher Updated Successfully"}


@app.delete("/teachers/{id}")
def delete_teacher(id: int):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(""" DELETE FROM teacher WHERE id=? """, (id,))

    conn.commit()
    conn.close()

    return {"message": "teacher Deleted Successfully"}

@app.post("/timetable")
def add_timetable(data: Timetable):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO timetable
        VALUES(NULL, ?, ?, ?, ?, ?)
    """, (
        data.t_id,
        data.std,
        data.class_no,
        data.start_time,
        data.end_time
    ))

    conn.commit()
    conn.close()

    return {"message": "Timetable Added Successfully"}

@app.get("/timetable")
def get_timetable():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM timetable
    """)

    data = cursor.fetchall()

    conn.close()

    timetables = []
    for row in data:
        timetable = {
            "id": row[0],
            "t_id": row[1],
            "std": row[2],
            "class_no": row[3],
            "start_time": row[4],
            "end_time": row[5]
        }
        timetables.append(timetable)


    return timetables

@app.get("/teacher/{id}")
def teacher_login(id: int):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
        teacher.name,
        teacher.subject,
        timetable.std,
        timetable.class_no,
        timetable.start_time,
        timetable.end_time FROM teacher JOIN timetable ON teacher.id = timetable.t_id
        WHERE teacher.id = ?""", 
        (id,))
    data = cursor.fetchall()
    conn.close()

    teachers = []
    for row in data:
        teacher = {
            "name": row[0],
            "subject": row[1],
            "std": row[2],
            "class_no": row[3],
            "start_time": row[4],
            "end_time": row[5]
        }
        teachers.append(teacher)
    return teachers

