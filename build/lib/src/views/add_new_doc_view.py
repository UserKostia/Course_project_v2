import sqlite3
import flet as ft
from State import global_state
from flet import (
    Row,
    Text,
    Column,
    colors,
    Container,
    TextField,
    OutlinedButton)


def add_new_doc_view(_):
    page = global_state.get_state_by_key('page')

    header = Text("Введіть дані нового лікаря", size=20)

    monday = Text("Пн.", size=20)
    tuesday = Text("Вт.", size=20)
    wednesday = Text("Ср.", size=20)
    thursday = Text("Чт.", size=20)
    friday = Text("Пт.", size=20)

    def clean_fields(_):
        input_name.value = ""
        input_surname.value = ""
        input_middle_name.value = ""
        input_place_building.value = ""
        input_place_floor.value = ""
        input_place_cabinet.value = ""
        input_spacialty.value = ""

        from_hour_schedule_monday.value = ""
        from_hour_schedule_tuesday.value = ""
        from_hour_schedule_wednesday.value = ""
        from_hour_schedule_thursday.value = ""
        from_hour_schedule_friday.value = ""

        from_minute_schedule_monday.value = ""
        from_minute_schedule_tuesday.value = ""
        from_minute_schedule_wednesday.value = ""
        from_minute_schedule_thursday.value = ""
        from_minute_schedule_friday.value = ""

        to_hour_schedule_monday.value = ""
        to_hour_schedule_tuesday.value = ""
        to_hour_schedule_wednesday.value = ""
        to_hour_schedule_thursday.value = ""
        to_hour_schedule_friday.value = ""

        to_minute_schedule_monday.value = ""
        to_minute_schedule_tuesday.value = ""
        to_minute_schedule_wednesday.value = ""
        to_minute_schedule_thursday.value = ""
        to_minute_schedule_friday.value = ""

        main_body.update()

    input_name = TextField(label="Ім'я...", width=300, input_filter=ft.InputFilter(allow=True, regex_string=r"[а-яА-ЯіІЇї]", replacement_string=""), max_length=20)
    input_surname = TextField(label="Прізвище...", width=300, input_filter=ft.InputFilter(allow=True, regex_string=r"[а-яА-ЯіІЇї]", replacement_string=""), max_length=20)
    input_middle_name = TextField(label="По батькові...", width=300, input_filter=ft.InputFilter(allow=True, regex_string=r"[а-яА-ЯіІЇї]", replacement_string=""), max_length=20)
    input_place_building = TextField(label="Корпус...", width=300, input_filter=ft.NumbersOnlyInputFilter(), max_length=2)
    input_place_floor = TextField(label="Поверх", width=300, input_filter=ft.NumbersOnlyInputFilter(), max_length=2)
    input_place_cabinet = TextField(label="Кабінет", width=300, input_filter=ft.NumbersOnlyInputFilter(), max_length=2)
    input_spacialty = TextField(label="Спеціальність", width=300, input_filter=ft.InputFilter(allow=True, regex_string=r"[а-яА-ЯіІЇї]", replacement_string=""), max_length=40)

    # timetables "from"
    from_hour_schedule_monday = TextField(label="год.", text_size=16, width=60, input_filter=ft.NumbersOnlyInputFilter(), max_length=2)
    from_hour_schedule_tuesday = TextField(label="год.", text_size=16, width=60, input_filter=ft.NumbersOnlyInputFilter(), max_length=2)
    from_hour_schedule_wednesday = TextField(label="год.", text_size=16, width=60, input_filter=ft.NumbersOnlyInputFilter(), max_length=2)
    from_hour_schedule_thursday = TextField(label="год.", text_size=16, width=60, input_filter=ft.NumbersOnlyInputFilter(), max_length=2)
    from_hour_schedule_friday = TextField(label="год.", text_size=16, width=60, input_filter=ft.NumbersOnlyInputFilter(), max_length=2)

    separator = Text(":", size=16)

    from_minute_schedule_monday = TextField(label="хв.", text_size=16, width=60, input_filter=ft.NumbersOnlyInputFilter(), max_length=2)
    from_minute_schedule_tuesday = TextField(label="хв.", text_size=16, width=60, input_filter=ft.NumbersOnlyInputFilter(), max_length=2)
    from_minute_schedule_wednesday = TextField(label="хв.", text_size=16, width=60, input_filter=ft.NumbersOnlyInputFilter(), max_length=2)
    from_minute_schedule_thursday = TextField(label="хв.", text_size=16, width=60, input_filter=ft.NumbersOnlyInputFilter(), max_length=2)
    from_minute_schedule_friday = TextField(label="хв.", text_size=16, width=60, input_filter=ft.NumbersOnlyInputFilter(), max_length=2)

    # timetables "to"
    to_hour_schedule_monday = TextField(label="год.", text_size=16, width=60, input_filter=ft.NumbersOnlyInputFilter(), max_length=2)
    to_hour_schedule_tuesday = TextField(label="год.", text_size=16, width=60, input_filter=ft.NumbersOnlyInputFilter(), max_length=2)
    to_hour_schedule_wednesday = TextField(label="год.", text_size=16, width=60, input_filter=ft.NumbersOnlyInputFilter(), max_length=2)
    to_hour_schedule_thursday = TextField(label="год.", text_size=16, width=60, input_filter=ft.NumbersOnlyInputFilter(), max_length=2)
    to_hour_schedule_friday = TextField(label="год.", text_size=16, width=60, input_filter=ft.NumbersOnlyInputFilter(), max_length=2)

    desh = Text(" - ", size=16)

    to_minute_schedule_monday = TextField(label="хв.", text_size=16, width=60, input_filter=ft.NumbersOnlyInputFilter(), max_length=2)
    to_minute_schedule_tuesday = TextField(label="хв.", text_size=16, width=60, input_filter=ft.NumbersOnlyInputFilter(), max_length=2)
    to_minute_schedule_wednesday = TextField(label="хв.", text_size=16, width=60, input_filter=ft.NumbersOnlyInputFilter(), max_length=2)
    to_minute_schedule_thursday = TextField(label="хв.", text_size=16, width=60, input_filter=ft.NumbersOnlyInputFilter(), max_length=2)
    to_minute_schedule_friday = TextField(label="хв.", text_size=16, width=60, input_filter=ft.NumbersOnlyInputFilter(), max_length=2)

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
                        input_place_building,
                        input_place_floor,
                        input_place_cabinet,
                        input_spacialty,
                    ],
                    width=600,
                    height=570,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                ),
                Column(
                    [
                        Row(
                            [
                                monday,
                                from_hour_schedule_monday,
                                separator,
                                from_minute_schedule_monday,
                                desh,
                                to_hour_schedule_monday,
                                separator,
                                to_minute_schedule_monday,
                            ]
                        ),
                        Row(
                            [
                                tuesday,
                                from_hour_schedule_tuesday,
                                separator,
                                from_minute_schedule_tuesday,
                                desh,
                                to_hour_schedule_tuesday,
                                separator,
                                to_minute_schedule_tuesday,
                            ]
                        ),
                        Row(
                            [
                                wednesday,
                                from_hour_schedule_wednesday,
                                separator,
                                from_minute_schedule_wednesday,
                                desh,
                                to_hour_schedule_wednesday,
                                separator,
                                to_minute_schedule_wednesday,
                            ]
                        ),
                        Row(
                            [
                                thursday,
                                from_hour_schedule_thursday,
                                separator,
                                from_minute_schedule_thursday,
                                desh,
                                to_hour_schedule_thursday,
                                separator,
                                to_minute_schedule_thursday,
                            ]
                        ),
                        Row(
                            [
                                friday,
                                from_hour_schedule_friday,
                                separator,
                                from_minute_schedule_friday,
                                desh,
                                to_hour_schedule_friday,
                                separator,
                                to_minute_schedule_friday,
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

    def add_to_db(e):
        db = sqlite3.connect("clinic.db")
        c = db.cursor()

        c.execute("SELECT COUNT(*) FROM docs WHERE full_name=?",
                  (input_surname.value + " " + input_name.value + " " + input_middle_name.value,))
        result = c.fetchone()
        if result[0] > 0:
            add_doc_btn.text = "Помилка"
            page.snack_bar = ft.SnackBar(ft.Text('Лікар з таким ім\'ям вже існує'))
            page.snack_bar.open = True
            page.update()
        else:
            try:
                c.execute(
                    """
                    INSERT INTO docs (name, surname, middle_name, full_name, place, specialty, schedule)
                    VALUES (?, ?, ?, ?, ?, ?, ?);
                    """,
                    (
                        input_name.value,
                        input_surname.value,
                        input_middle_name.value,
                        input_surname.value + " " + input_name.value + " " + input_middle_name.value,
                        input_place_building.value + " корпус, " + input_place_floor.value + " поверх, " + input_place_cabinet.value + " кабінет",
                        input_spacialty.value,
                        "Пн: " + from_hour_schedule_monday.value + ":" + from_minute_schedule_monday.value + " - " + to_hour_schedule_monday.value + ":" + to_minute_schedule_monday.value + "."
                        "Вт: " + from_hour_schedule_tuesday.value + ":" + from_minute_schedule_tuesday.value + " - " + to_hour_schedule_tuesday.value + ":" + to_minute_schedule_tuesday.value + "."
                        "Ср: " + from_hour_schedule_wednesday.value + ":" + from_minute_schedule_wednesday.value + " - " + to_hour_schedule_wednesday.value + ":" + to_minute_schedule_wednesday.value + "."
                        "Чт: " + from_hour_schedule_thursday.value + ":" + from_minute_schedule_thursday.value + " - " + to_hour_schedule_thursday.value + ":" + to_minute_schedule_thursday.value + "."
                        "Пт: " + from_hour_schedule_friday.value + ":" + from_minute_schedule_friday.value + " - " + to_hour_schedule_friday.value + ":" + to_minute_schedule_friday.value + "."
                    )
                )
                db.commit()

                add_doc_btn.text = "Додано"
                page.snack_bar = ft.SnackBar(ft.Text('Лікаря додано'))
                page.snack_bar.open = True
                page.update()

            except Exception as e:
                print(e)
            finally:
                db.close()

    add_doc_btn = OutlinedButton(text="Додати лікаря", width=400, on_click=add_to_db)

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
