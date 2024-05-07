import ast
import random
import datetime
import sqlite3
from faker import Faker
import pythonflet.src.consts.docs as docs
import pythonflet.src.consts.patients as pt

faker = Faker()


def fill_docs():
    db = sqlite3.connect("../clinic.db")
    c = db.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS docs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(30),
        surname VARCHAR(40),
        middle_name VARCHAR(30),
        full_name VARCHAR(100),
        place VARCHAR,
        specialty VARCHAR,
        schedule TEXT
        )
        """
    )

    query = """
      INSERT INTO docs (name, surname, middle_name, full_name, place, specialty, schedule)
      VALUES (?, ?, ?, ?, ?, ?, ?)
      """

    schedule_list = ast.literal_eval(docs.schedule)

    for _ in range(30):
        random_schedule = random.choice(schedule_list)

        schedule_str = ""
        for day, time in random_schedule.items():
            schedule_str += f"{day}: {time}\n"

        doc_data = (
            faker.random_element(elements=docs.docs_names),
            faker.random_element(elements=docs.docs_surnames),
            faker.random_element(elements=docs.docs_middle_names),
            faker.random_element(elements=docs.docs_places),
            faker.random_element(elements=docs.docs_specialty),
            schedule_str,
        )
        full_name = doc_data[1] + " " + doc_data[0] + " " + doc_data[2]

        new_doc_data = (
            doc_data[0],
            doc_data[1],
            doc_data[2],
            full_name,
            doc_data[3],
            doc_data[4],
            doc_data[5],
        )
        c.execute(query, new_doc_data)

    db.commit()


def fill_patients_and_records():
    db = sqlite3.connect("../clinic.db")
    c = db.cursor()
    c.execute(
         """
         CREATE TABLE IF NOT EXISTS patients(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         name VARCHAR(30),
         surname VARCHAR(40),
         middle_name VARCHAR(30),
         full_name VARCHAR(90),
         complaint VARCHAR,
         doc_full_name VARCHAR(90),
         registration_date TEXT,
         registration_time TEXT)
         """
    )

    c.execute(
         """
         CREATE TABLE IF NOT EXISTS records(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         name VARCHAR(30),
         surname VARCHAR(40),
         middle_name VARCHAR(30),
         full_name VARCHAR(90),
         complaint VARCHAR,
         doc_full_name VARCHAR(90),
         registration_date TEXT,
         registration_time TEXT)
         """
    )

    query = """
      INSERT INTO patients(
      name, surname, middle_name, full_name, complaint, doc_full_name, registration_date, registration_time)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
      """

    query_1 = """
      INSERT INTO records(
      name, surname, middle_name, full_name, complaint, doc_full_name, registration_date, registration_time)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
      """

    for _ in range(30):

        # Generate a random datetime object between now and two years from now
        now = datetime.datetime.now()
        # two_years = datetime.timedelta(days=365 * 2)
        random_datetime = now + datetime.timedelta(seconds=random.randint(0, 2 * 365 * 24 * 60 * 60))

        # Format the datetime object as a string in the desired format
        date_str = random_datetime.strftime("%Y-%m-%d")
        time_str = random_datetime.strftime("%H:%M:%S")

        doc = c.execute("""
            SELECT *
            FROM docs
            ORDER BY RANDOM()
            LIMIT 1
        """)

        doc_row = doc.fetchone()
        doc_full_name = doc_row[2] + " " + doc_row[1] + " " + doc_row[3]

        patients_data = (
            faker.random_element(elements=pt.patients_names),
            faker.random_element(elements=pt.patints_surnames),
            faker.random_element(elements=pt.patients_middle_names),
            faker.random_element(elements=pt.diagnoses),
            doc_full_name,
            date_str,
            time_str,
        )
        full_name = patients_data[1] + " " + patients_data[0] + " " + patients_data[2]

        new_patient_data = (
            patients_data[0],
            patients_data[1],
            patients_data[2],
            full_name,
            patients_data[3],
            patients_data[4],
            patients_data[5],
            patients_data[6],
        )

        c.execute(query, new_patient_data)
        c.execute(query_1, new_patient_data)

    db.commit()


fill_docs()
fill_patients_and_records()
