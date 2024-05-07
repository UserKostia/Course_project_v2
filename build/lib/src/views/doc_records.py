import sqlite3
import datetime
import flet as ft
from datetime import datetime
from flet import IconButton

from components.navigation_bar.nav_bar import show_menu_bar
from consts.record_time import choose_minute
from consts.record_time import choose_hour
from consts.person_immage import person_img
from consts.record_time import choose_day
from consts.record_time import choose_month
from classes.patient import Patient
from State import global_state

from flet import (
    Row,
    Text,
    Image,
    Column,
    colors,
    padding,
    Container,
    TextField,
    TextButton,
    FontWeight,
    OutlinedButton)


def doc_records_view(_):
    page = global_state.get_state_by_key('page')
    page.title = "Записи"
    page.window_maximizable = True
    page.window_resizable = True

    title = Text("Записи до лікарів", font_family="Merriweather", size=40, weight=FontWeight.W_600)
    title.text_align = ft.TextAlign.CENTER

    header = ft.Row(
        [
            Container(
                content=title,
                bgcolor=colors.BLUE_GREY_50,
                padding=padding.only(left=20),
                border=ft.border.all(1, ft.colors.GREY),
                height=60,
                width=1250
            ),
        ],
        width=1250
    )

    find_record_by_name_field = TextField(label="Пошук по списку: введіть ПІБ пацієнта",
                                          width=400,
                                          height=70,
                                          input_filter=ft.InputFilter(allow=True,
                                                                      regex_string=r"[а-яА-ЯіІЇї]",
                                                                      replacement_string=""),
                                          max_length=55)

    find_record_by_complaint_field = TextField(label="Пошук: введіть діагноз",
                                               width=300,
                                               height=70,
                                               input_filter=ft.InputFilter(allow=True,
                                                                           regex_string=r"[а-яА-ЯіІЇї]",
                                                                           replacement_string=""),
                                               max_length=50)

    def display_all(_):
        find_record_by_name_field.value = ""
        find_record_by_complaint_field.value = ""
        choose_day.value = ""
        choose_month.value = ""
        choose_hour.value = ""
        choose_minute.value = ""
        body.clean()
        display_docs_records()
        main_body.update()

    display_all_records_btn = OutlinedButton(text="   Всі\nзаписи",
                                             height=50,
                                             on_click=display_all)

    def find_record(find_record_by_name,
                    find_record_by_complaint,
                    choose_day,
                    choose_month,
                    choose_hour,
                    choose_minute):

        db = sqlite3.connect("clinic.db")
        try:
            c = db.cursor()
            body.controls.clear()

            query_conditions = []
            params = []

            if find_record_by_name:
                query_conditions.append("full_name LIKE ?")
                params.append('%' + find_record_by_name + '%')

            if find_record_by_complaint:
                query_conditions.append("complaint LIKE ?")
                params.append('%' + find_record_by_complaint + '%')

            if choose_day and choose_month:
                query_conditions.append("registration_date = ?")
                test_date = f'{datetime.now().year}-{choose_month}-{choose_day}'
                params.append(test_date)

            if choose_day and not choose_month:
                query_conditions.append("strftime('%d', registration_date) = ?")
                params.append(str(choose_day))

            if choose_month and not choose_day:
                query_conditions.append("strftime('%m', registration_date) = ?")
                params.append(str(choose_month))

            if choose_hour and not choose_minute:
                query_conditions.append("strftime('%H', registration_time) = ?")
                params.append(str(choose_hour))

            if choose_minute and not choose_hour:
                query_conditions.append("strftime('%M', registration_time) = ?")
                params.append(str(choose_minute))

            if find_record_by_name and find_record_by_complaint and\
                    choose_day and choose_month and choose_hour and choose_minute:
                query_conditions.append("full_name LIKE ?")
                query_conditions.append("complaint LIKE ?")
                query_conditions.append("registration_date = ?")
                query_conditions.append("strftime('%H', registration_time) = ?")
                query_conditions.append("strftime('%M', registration_time) = ?")

                params.extend(['%' + find_record_by_name + '%',
                               '%' + find_record_by_complaint + '%',
                               f'{datetime.now().year}-{choose_month}-{choose_day}',
                               str(choose_hour),
                               str(choose_minute)])

            if find_record_by_name and find_record_by_complaint and choose_day and choose_month:
                query_conditions.append("full_name LIKE ?")
                query_conditions.append("complaint LIKE ?")
                query_conditions.append("registration_date = ?")

                params.extend(['%' + find_record_by_name + '%',
                               '%' + find_record_by_complaint + '%',
                               f'{datetime.now().year}-{choose_month}-{choose_day}'])

            if find_record_by_name and find_record_by_complaint and choose_hour and choose_minute:
                query_conditions.append("full_name LIKE ?")
                query_conditions.append("complaint LIKE ?")
                query_conditions.append("strftime('%H', registration_time) = ?")
                query_conditions.append("strftime('%M', registration_time) = ?")

                params.extend(['%' + find_record_by_name + '%',
                               '%' + find_record_by_complaint + '%',
                               str(choose_hour),
                               str(choose_minute)])

            if query_conditions:
                query = """
                    SELECT 
                    id, name, surname, middle_name, full_name, complaint,
                    doc_full_name, registration_date, registration_time
                    FROM records
                    WHERE {}
                    """.format(" AND ".join(query_conditions))

                c.execute(query, tuple(params))
                recs = c.fetchall()

                records = []
                for rec in recs:
                    id_val, name_val, surname_val, middle_name_val, full_name_val, \
                        complaint_val, doc_full_name_val, reg_date_val, reg_time_val = rec

                    record = Patient(id_val,
                                     name_val,
                                     surname_val,
                                     middle_name_val,
                                     full_name_val,
                                     complaint_val,
                                     doc_full_name_val,
                                     reg_date_val,
                                     reg_time_val)
                    records.append(record)

                for rec in records:
                    doc_full_name = rec.get_doc_full_name()
                    doc_full_name = doc_full_name.split(" ")

                    print(rec.get_id())
                    new_id = rec.get_id()
                    new_name = Text(value=rec.get_name(), size=18, font_family="TimesNewRoman")
                    new_surname = Text(value=rec.get_surname(), size=18, font_family="TimesNewRoman")
                    new_middle_name = Text(value=rec.get_middle_name(), size=18, font_family="TimesNewRoman")
                    new_complaint = Text(value=rec.get_complaint(), size=16, font_family="TimesNewRoman")
                    new_doc_name = Text(value=doc_full_name[0], size=18, font_family="TimesNewRoman")
                    new_doc_surname = Text(value=doc_full_name[1], size=18, font_family="TimesNewRoman")
                    new_doc_middle_name = Text(value=doc_full_name[2], size=18, font_family="TimesNewRoman")
                    new_reg_date = Text(value=rec.get_registration_date(), size=16, font_family="TimesNewRoman")
                    new_reg_time = Text(value=rec.get_registration_time(), size=16, font_family="TimesNewRoman")

                    record_title = Text("Запис до:", size=16, font_family="TimesNewRoman")

                    delete_rec_btn = ft.IconButton(
                        icon=ft.icons.DELETE_FOREVER_ROUNDED,
                        icon_size=40,
                        icon_color="pink600",
                        tooltip="Видалити лікаря",
                        on_click=lambda e, record_id=rec.get_id(): delete_record(record_id), data=rec.get_id()
                    )

                    new_patient_record_content = Row(
                        [
                            Container(
                                content=Image(
                                    src=person_img,
                                    width=150,
                                    height=150,
                                ),
                                height=150,
                                padding=ft.padding.only(left=10, top=10, bottom=10, right=20),
                                bgcolor=colors.GREY_200,
                                alignment=ft.alignment.center,
                                margin=ft.margin.only(left=30),
                            ),
                            Container(
                                Column([
                                    Container(
                                        content=new_surname,
                                        margin=ft.margin.only(top=20),
                                    ),
                                    Container(
                                        content=new_name,
                                    ),
                                    Container(
                                        content=new_middle_name,
                                    )
                                ]),
                                width=300,
                                bgcolor=colors.GREY_200,
                                height=150,
                            ),
                            Container(
                                Column(
                                    [
                                        new_complaint,
                                        delete_rec_btn,
                                    ],
                                ),
                                padding=padding.only(top=50),
                                bgcolor=colors.GREY_200,
                                height=150,
                                width=280,
                            ),
                            Container(
                                Column([
                                    record_title,
                                    Container(
                                        content=new_doc_name,
                                        margin=ft.margin.only(top=7),
                                    ),
                                    Container(
                                        content=new_doc_surname,
                                    ),
                                    Container(
                                        content=new_doc_middle_name,
                                    )
                                ]),
                                width=200,
                                height=150,
                                bgcolor=colors.GREY_200,
                            ),
                            Container(
                                Column(
                                    [
                                        Container(
                                            content=new_reg_date,
                                        ),
                                        Container(
                                            content=new_reg_time,
                                            padding=ft.padding.only(top=20, left=13),
                                        ),
                                    ]
                                ),
                                margin=ft.margin.only(right=20),
                                padding=ft.padding.only(top=25, left=50),
                                width=230,
                                height=150,
                                bgcolor=colors.GREY_200,
                            ),
                        ],
                        spacing=0,
                    )
                    body.controls.append(new_patient_record_content)

        except Exception as e:
            print(e)

        finally:
            if len(body.controls) == 0:
                page.snack_bar = ft.SnackBar(ft.Text('Записів нема!', size=22))
                page.snack_bar.open = True
            db.close()
            page.update()

    find_rec_btn = TextButton("Знайти", width=71, height=50,
                              on_click=lambda _: find_record(
                                  find_record_by_name_field.value,
                                  find_record_by_complaint_field.value,
                                  choose_day.value,
                                  choose_month.value,
                                  choose_hour.value,
                                  choose_minute.value
                              ))

    navigation = Row(
        [
        Container(content=find_record_by_name_field),
        Container(content=find_record_by_complaint_field),
        Container(content=choose_day),
        Container(content=choose_month),
        Container(content=choose_hour),
        Container(content=choose_minute),
        Container(content=find_rec_btn),
        Container(content=display_all_records_btn),
        ],
        width=3000
    )

    body = Column(
        spacing=10,
        height=500,
        width=1250,
        scroll=ft.ScrollMode.ALWAYS,
        adaptive=True
    )

    main_body = Row(
        [
            Column(
                [
                    show_menu_bar(page),
                    header,
                    navigation,
                    Container(body, border=ft.border.all(1)),
                ]
            ),
        ],
        height=1500,
        width=3000
    )

    def delete_record(record_id):
        db = sqlite3.connect("clinic.db")
        try:
            cursor = db.cursor()
            print(f"Deleting record with id={record_id}")
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

    def display_docs_records():
        db = sqlite3.connect("clinic.db")
        c = db.cursor()
        c.execute(
            """
            SELECT 
            id, name, surname, middle_name, complaint, doc_full_name, registration_date, registration_time
            FROM records
            """)
        patient_rec = c.fetchall()

        for index, rec in enumerate(patient_rec):
            id_val, name_val, surname_val, middle_name_val, complaint_val,\
                doc_full_name_val, registration_date_val, registration_time_val = rec

            doc_full_name = doc_full_name_val.split(" ")

            new_name = Text(value=name_val, size=18, font_family="TimesNewRoman")
            new_surname = Text(value=surname_val, size=18, font_family="TimesNewRoman")
            new_middle_name = Text(value=middle_name_val, size=18, font_family="TimesNewRoman")
            new_complaint = Text(value=complaint_val, size=18, font_family="TimesNewRoman")
            new_doc_name = Text(value=doc_full_name[0], size=18, font_family="TimesNewRoman")
            new_doc_surname = Text(value=doc_full_name[1], size=18, font_family="TimesNewRoman")
            new_doc_middle_name = Text(value=doc_full_name[2], size=18, font_family="TimesNewRoman")
            new_reg_date = Text(value=registration_date_val, size=18, font_family="TimesNewRoman")
            new_reg_time = Text(value=registration_time_val, size=18, font_family="TimesNewRoman")

            record_title = Text("Запис до:", size=16, font_family="TimesNewRoman")

            delete_rec_btn = ft.IconButton(
                icon=ft.icons.DELETE_FOREVER_ROUNDED,
                icon_size=40,
                icon_color="pink600",
                tooltip="Видалити лікаря",
                on_click=lambda e, record_id=id_val: delete_record(record_id), data=id_val
            )

            new_patient_record_content = Row(
                [
                    Container(
                        content=Image(
                            src=person_img,
                            width=150,
                            height=150,
                        ),
                        height=150,
                        padding=ft.padding.only(left=10, top=10, bottom=10, right=20),
                        bgcolor=colors.GREY_200,
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(left=30),
                    ),
                    Container(
                        Column([
                            Container(
                                content=new_surname,
                                margin=ft.margin.only(top=20),
                            ),
                            Container(
                                content=new_name,
                            ),
                            Container(
                                content=new_middle_name,
                            )
                        ]),
                        width=300,
                        bgcolor=colors.GREY_200,
                        height=150,
                    ),
                    Container(
                        Column(
                            [
                                new_complaint,
                                delete_rec_btn,
                            ]
                        ),
                        padding=padding.only(top=50),
                        bgcolor=colors.GREY_200,
                        height=150,
                        width=280,
                    ),
                    Container(
                        Column([
                            record_title,
                            Container(
                                content=new_doc_name,
                                margin=ft.margin.only(top=7),
                            ),
                            Container(
                                content=new_doc_surname,
                            ),
                            Container(
                                content=new_doc_middle_name,
                            )
                        ]),
                        width=200,
                        bgcolor=colors.GREY_200,
                        height=150,
                    ),
                    Container(
                        Column(
                            [
                                Container(
                                    content=new_reg_date,
                                ),
                                Container(
                                    content=new_reg_time,
                                    padding=ft.padding.only(top=20, left=13),
                                ),
                            ]
                        ),
                        margin=ft.margin.only(right=20),
                        padding=ft.padding.only(top=25, left=50),
                        width=230,
                        height=150,
                        bgcolor=colors.GREY_200,
                    ),
                ],
                spacing=0,
            )
            body.controls.append(new_patient_record_content)
        db.close()

    display_docs_records()

    return main_body
