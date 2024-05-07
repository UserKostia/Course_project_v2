import sqlite3
import flet as ft
from flet import (
    Row,
    Text,
    Column,
    margin,
    colors,
    padding,
    Container,
    TextField,
    FontWeight,
    ElevatedButton,
    OutlinedButton)

from State import global_state
from classes.patient import Patient
from consts.record_time import choose_minute
from consts.record_time import choose_hour
from consts.record_time import choose_day
from consts.record_time import choose_month
from components.navigation_bar.nav_bar import show_menu_bar


def patiens_view(_):
    page = global_state.get_state_by_key('page')

    page.title = "Пацієнти"
    page.window_maximizable = True
    page.window_resizable = True

    title = Text("ПАЦІЄНТИ", font_family="Merriweather", size=40, weight=FontWeight.W_600)
    title.text_align = ft.TextAlign.CENTER

    header = ft.Row(
        [
            Container(
                content=title,
                bgcolor=colors.BLUE_GREY_50,
                padding=padding.only(left=20),
                border=ft.border.all(1, ft.colors.GREY),
                height=60,
                width=1250,
            ),
        ],
        width=1210,
    )

    def display_all(_):
        find_pationt_field.value = ""
        choose_day.value = ""
        choose_month.value = ""
        choose_hour.value = ""
        choose_minute.value = ""
        body.clean()
        display_docs_records()
        main_body.update()

    def delete_patient(record_id):
        db = sqlite3.connect("clinic.db")
        try:
            cursor = db.cursor()
            print(f"Deleting record with id={record_id}")
            cursor.execute(
                """
                    DELETE FROM patients
                    WHERE id=?
                """, (record_id,))
            cursor.execute(
                """
                    DELETE FROM records
                    WHERE id=?
                """, (record_id,))
            db.commit()
            print(f"Deleted record with id={record_id}")
        except Exception as e:
            print(f"Error deleting record with id={record_id}: {e}")
        finally:
            db.close()
            body.clean()
            display_docs_records()
            main_body.update()

    def find_record(find_patient_field, choose_day, choose_month, choose_hour, choose_minute):

        if not find_patient_field and not choose_day and not choose_month and not choose_hour and not choose_minute:
            return

        db = sqlite3.connect("clinic.db")
        try:
            c = db.cursor()
            body.controls.clear()

            query_conditions = []
            params = []

            if find_patient_field:
                query_conditions.append("full_name LIKE ?")
                params.append('%' + find_patient_field + '%')

            if choose_day:
                query_conditions.append("strftime('%d', registration_date) = ?")
                params.append(str(choose_day))

            if choose_month:
                query_conditions.append("strftime('%m', registration_date) = ?")
                params.append(str(choose_month))

            if choose_hour:
                query_conditions.append("strftime('%H', registration_time) = ?")
                params.append(str(choose_hour))

            if choose_minute:
                query_conditions.append("strftime('%M', registration_time) = ?")
                params.append(str(choose_minute))

            if query_conditions:
                query = """
                   SELECT 
                   id, name, surname, middle_name, full_name, complaint,
                   doc_full_name, registration_date, registration_time
                   FROM patients
                   WHERE {}
                   """.format(" AND ".join(query_conditions))

                c.execute(query, tuple(params))
                recs = c.fetchall()

                pnts = []
                for pnt in recs:
                    id_val, name_val, surname_val, middle_name_val, full_name_val, \
                        complaint_val, doc_full_name_val, reg_date_val, reg_time_val = pnt

                    record = Patient(id_val,
                                     name_val,
                                     surname_val,
                                     middle_name_val,
                                     full_name_val,
                                     complaint_val,
                                     doc_full_name_val,
                                     reg_date_val,
                                     reg_time_val)
                    pnts.append(record)

                for pnt in pnts:

                    id_val = pnt.get_id()
                    name = Text(value=pnt.get_name(), size=18, font_family="TimesNewRoman")
                    surname = Text(value=pnt.get_surname(), size=18, font_family="TimesNewRoman")
                    middle_name = Text(value=pnt.get_middle_name(), size=18, font_family="TimesNewRoman")

                    reg_date = Text(value=pnt.get_registration_date(), size=18, font_family="TimesNewRoman")
                    reg_time = Text(value=pnt.get_registration_time(), size=18, font_family="TimesNewRoman")

                    delete_patient_btn = ElevatedButton(text="Видалити",
                                                        on_click=lambda record_id=id_val: delete_patient(record_id),
                                                        data=id_val)

                    patient_content = Row(
                        [
                            Container(
                                Row([
                                    Container(
                                        content=surname,
                                        margin=ft.margin.only(left=30),
                                        width=200,
                                    ),
                                    Container(
                                        content=name,
                                        width=200,
                                    ),
                                    Container(
                                        content=middle_name,
                                        width=250,
                                    )
                                ]),
                                margin=margin.only(left=40, top=10),
                                bgcolor=colors.GREY_200,
                                width=650,
                                height=70,
                            ),
                            Container(
                                Row(
                                    [
                                        Container(
                                            content=reg_date,
                                            width=180,
                                        ),
                                        Container(
                                            content=reg_time,
                                            width=180,
                                        ),
                                        Container(
                                            content=delete_patient_btn,
                                            width=120,
                                        )
                                    ],
                                ),
                                margin=ft.margin.only(right=20, top=10),
                                bgcolor=colors.GREY_200,
                                width=515,
                                height=70,
                            ),
                        ],
                        spacing=0,
                    )
                    body.controls.append(patient_content)

        except Exception as e:
            print(e)

        finally:
            if len(body.controls) == 0:
                page.snack_bar = ft.SnackBar(ft.Text('Записів нема!', size=22))
                page.snack_bar.open = True
            db.close()
            page.update()

    find_pationt_field = TextField(label="Пошук по списку: введіть ПІБ пацієнта",
                                   width=690,
                                   height=70,
                                   input_filter=ft.InputFilter(allow=True,
                                                               regex_string=r"[а-яА-ЯіІЇї]",
                                                               replacement_string=""),
                                   max_length=55)

    find_patient_btn = ElevatedButton("Знайти", height=50, on_click=lambda _: find_record(find_pationt_field.value,
                                                                                          choose_day.value,
                                                                                          choose_month.value,
                                                                                          choose_hour.value,
                                                                                          choose_minute.value))

    display_all_records_btn = OutlinedButton(text="   Всі\nзаписи",
                                             height=50,
                                             on_click=display_all)

    navigation = Row(
        [
            Container(content=find_pationt_field),
            Container(content=choose_day),
            Container(content=choose_month),
            Container(content=choose_hour),
            Container(content=choose_minute),
            Container(content=find_patient_btn),
            Container(content=display_all_records_btn),
        ],
        width=3000,
    )

    body = Column(
        spacing=10,
        height=500,
        width=1250,
        adaptive=True,
        scroll=ft.ScrollMode.ALWAYS,
    )

    def display_docs_records():
        db = sqlite3.connect("clinic.db")
        c = db.cursor()
        c.execute(
            """
            SELECT id, name, surname, middle_name, registration_date, registration_time
            FROM patients
            """
        )
        patients = c.fetchall()

        for index, pnt in enumerate(patients):
            id_val, name_val, surname_val, middle_name_val, registration_date_val, registration_time_val = pnt

            name = Text(value=name_val, size=18, font_family="TimesNewRoman")
            surname = Text(value=surname_val, size=18, font_family="TimesNewRoman")
            middle_name = Text(value=middle_name_val, size=18, font_family="TimesNewRoman")

            reg_date = Text(value=registration_date_val, size=18, font_family="TimesNewRoman")
            reg_time = Text(value=registration_time_val, size=18, font_family="TimesNewRoman")

            delete_patient_btn = ElevatedButton(text="Видалити",
                                                on_click=lambda e, record_id=id_val: delete_patient(record_id),
                                                data=id_val)

            patient_content = Row(
                [
                    Container(
                        Row([
                            Container(
                                content=surname,
                                margin=ft.margin.only(left=30),
                                width=200,
                            ),
                            Container(
                                content=name,
                                width=200,
                            ),
                            Container(
                                content=middle_name,
                                width=250,
                            )
                        ]),
                        margin=margin.only(left=40, top=10),
                        bgcolor=colors.GREY_200,
                        width=650,
                        height=70,
                    ),
                    Container(
                        Row(
                            [
                                Container(
                                    content=reg_date,
                                    width=180,
                                ),
                                Container(
                                    content=reg_time,
                                    width=180,
                                ),
                                Container(
                                    content=delete_patient_btn,
                                    width=120,
                                ),
                            ],
                        ),
                        margin=ft.margin.only(right=20, top=10),
                        bgcolor=colors.GREY_200,
                        width=515,
                        height=70,
                    ),
                ],
                spacing=0,
            )
            body.controls.append(patient_content)
        db.close()

    display_docs_records()

    main_body = Row(
        [
            Column(
                [
                    show_menu_bar(page),
                    header,
                    navigation,
                    Container(body, border=ft.border.all(1)),
                ],
            ),
        ],
        height=1500,
        width=3000,
    )

    return main_body
