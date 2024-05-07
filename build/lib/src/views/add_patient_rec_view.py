import datetime
import sqlite3
import time

from State import global_state
import flet as ft
from flet import (
    Row,
    Text,
    Column,
    colors,
    Container,
    TextField,
    OutlinedButton)


def add_new_patient_view(_):
    page = global_state.get_state_by_key('page')
    header = Text("Введіть дані нового пацієнта", size=20)

    day = Text("День:    ", size=20)
    month = Text("Місяць: ", size=20)
    year = Text("Рік:        ", size=20)
    hour = Text("Год:       ", size=20)
    minute = Text("Хв:         ", size=20)

    def clean_fields(_):
        input_name.value = ""
        input_surname.value = ""
        input_middle_name.value = ""
        input_complaint.value = ""
        input_doc_name.value = ""
        input_doc_surname.value = ""
        input_doc_middle_name.value = ""

        input_day.value = ""
        input_month.value = ""
        input_year.value = ""
        input_hour.value = ""
        input_minute.value = ""

        main_body.update()

    input_name = TextField(label="Ім'я...", width=300, input_filter=ft.InputFilter(allow=True, regex_string=r"[а-яА-ЯіІЇї]", replacement_string=""), max_length=20)
    input_surname = TextField(label="Прізвище...", width=300, input_filter=ft.InputFilter(allow=True, regex_string=r"[а-яА-ЯіІЇї]", replacement_string=""), max_length=20)
    input_middle_name = TextField(label="По батькові...", width=300, input_filter=ft.InputFilter(allow=True, regex_string=r"[а-яА-ЯіІЇї]", replacement_string=""), max_length=20)
    input_complaint = TextField(label="Cкарга...", width=300, input_filter=ft.InputFilter(allow=True, regex_string=r"[а-яА-ЯіІЇї]", replacement_string=""), max_length=50, max_lines=2)
    input_doc_name = TextField(label="Ім'я лікаря...", width=300, input_filter=ft.InputFilter(allow=True, regex_string=r"[а-яА-ЯіІЇї]", replacement_string=""), max_length=20)
    input_doc_surname = TextField(label="Прізвище лікря...", width=300, input_filter=ft.InputFilter(allow=True, regex_string=r"[а-яА-ЯіІЇї]", replacement_string=""), max_length=20)
    input_doc_middle_name = TextField(label="По батькові лікаря...", width=300, input_filter=ft.InputFilter(allow=True, regex_string=r"[а-яА-ЯіІЇї]", replacement_string=""), max_length=20)

    input_day = TextField(width=100, input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string=""), max_length=2)
    input_month = TextField(width=100, input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string=""), max_length=2)
    input_year = TextField(width=100, input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string=""), max_length=4)
    input_hour = TextField(width=100, input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string=""), max_length=2)
    input_minute = TextField(width=100, input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string=""), max_length=2)

    clean_fields_btn = ft.IconButton(
        icon=ft.icons.DELETE_FOREVER_ROUNDED,
        icon_color="pink600",
        icon_size=40,
        tooltip="Очистити всі поля",
        on_click=clean_fields
    )

    title = Container(
        Row(
            [
                header
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        bgcolor=colors.LIGHT_BLUE_200,
        height=70
    )

    form = Container(
        Row(
            [
                Column(
                    controls=[
                        input_name,
                        input_surname,
                        input_middle_name,
                        input_complaint,
                        input_doc_name,
                        input_doc_surname,
                        input_doc_middle_name,
                    ],
                    width=800,
                    height=570,
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                Column(
                    [
                        Row(
                            [
                                day,
                                input_day,
                            ]
                        ),
                        Row(
                            [
                                month,
                                input_month,
                            ]
                        ),
                        Row(
                            [
                                year,
                                input_year,
                            ]
                        ),
                        Row(
                            [
                                Container(
                                    hour,
                                    margin=ft.margin.only(top=70),
                                ),
                                Container(
                                    input_hour,
                                    margin=ft.margin.only(top=70),
                                ),
                            ],

                        ),
                        Row(
                            [
                                minute,
                                input_minute,
                            ]
                        ),
                    ],
                    spacing=20,
                    width=300,
                ),
            ]
        ),
        alignment=ft.alignment.center,
    )

    def add_to_db(_):
        if all([input_name.value, input_surname.value, input_middle_name.value,
                input_surname.value, input_name.value, input_middle_name.value,
                input_complaint.value, input_doc_surname.value, input_doc_name.value,
                input_doc_middle_name.value, input_year.value,
                input_month.value, input_day.value, input_hour.value, input_minute.value])\
               and 22 >= int(input_hour.value) >= 7 and 59 >= int(input_minute.value) >= 0\
                and 31 >= int(input_day.value) >= 1 and 12 >= int(input_month.value) >= 1\
                and datetime.date.today().year >= int(input_year.value) >= datetime.date.today().year - 1:

            db = sqlite3.connect("clinic.db")
            c = db.cursor()
            try:

                c.execute(
                    """
                    INSERT INTO patients(
                    name, surname, middle_name, full_name, complaint, doc_full_name, registration_date, registration_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                    (
                        input_name.value,
                        input_surname.value,
                        input_middle_name.value,
                        input_surname.value + " " + input_name.value + " " + input_middle_name.value,
                        input_complaint.value,
                        input_doc_surname.value + " " + input_doc_name.value + " " + input_doc_middle_name.value,
                        input_year.value + "-" + input_month.value + "-" + input_day.value,
                        input_hour.value + ":" + input_minute.value + ":00"
                    )
                )

                c.execute(
                    """
                    INSERT INTO records(
                    name, surname, middle_name, full_name, complaint, doc_full_name, registration_date, registration_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                    (
                        input_name.value,
                        input_surname.value,
                        input_middle_name.value,
                        input_surname.value + " " + input_name.value + " " + input_middle_name.value,
                        input_complaint.value,
                        input_doc_surname.value + " " + input_doc_name.value + " " + input_doc_middle_name.value,
                        input_year.value + "-" + input_month.value + "-" + input_day.value,
                        input_hour.value + ":" + input_minute.value + ":00"
                    )
                )
                db.commit()
                page.snack_bar = ft.SnackBar(ft.Text('Додано', size=22))
                page.snack_bar.open = True
                page.update()

            except Exception as e:
                print(e)
            finally:
                db.commit()
                db.close()
        else:
            page.snack_bar = ft.SnackBar(ft.Text('Перевірте правильність введених даних!', size=22))
            page.snack_bar.open = True
            page.update()

    add_doc_btn = OutlinedButton(text="Додати запис", width=400, on_click=add_to_db)

    def navigate_to_index_view(_):
        page.go("/main")

    come_back_btn = ft.IconButton(
        tooltip="На головну",
        icon=ft.icons.ARROW_BACK,
        on_click=navigate_to_index_view
    )

    main_body = Column(
        [
            title,
            form,
            Row(
                [
                    Container(
                        content=come_back_btn,
                    ),
                    Container(
                        content=add_doc_btn,
                    ),
                    Container(
                        content=clean_fields_btn,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ]
    )

    return main_body
