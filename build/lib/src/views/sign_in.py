import sqlite3
import flet as ft

from State import global_state


def sign_in(_):
    page = global_state.get_state_by_key('page')
    page.title = "Registration"
    page.window_maximized = True
    page.window_resizable = True

    def authorize(_):
        db = sqlite3.connect('Registration.db')
        cur = db.cursor()

        cur.execute("SELECT * FROM users WHERE login = ? AND pass = ?", (user_login.value, user_pass.value))

        user = cur.fetchone()
        if user is not None:
            db_1 = sqlite3.connect('Entrance.db')
            c = db_1.cursor()

            c.execute(
                """
                CREATE TABLE IF NOT EXISTS initials_ava(
                id INTEGER PRIMARY KEY,
                login VARCHAR(30)
                )
                """)

            try:
                c.execute(f"DELETE FROM initials_ava")
                c.execute("INSERT INTO initials_ava (login) VALUES (?)", (user_login.value,))
                db_1.commit()

            except sqlite3.IntegrityError:
                page.snack_bar = ft.SnackBar(
                    ft.Text('Такий користувач вже існує!',
                            size=16,
                            weight=ft.FontWeight.W_700),
                    bgcolor=ft.colors.RED_500,
                    duration=5000,
                )
                page.snack_bar.open = True
                return

            finally:
                db_1.close()

            user_login.value = ''
            user_pass.value = ''
            sign_in_btn.text = 'Авторизовано'
            page.go("/main")
        else:
            page.snack_bar = ft.SnackBar(ft.Text('Введено неправильні дані, спробуйте ще раз!'))
            page.snack_bar.open = True

        db.commit()
        db.close()
        page.update()

    def validat(_):
        if all([user_login.value, user_pass.value]) and len(user_login.value) >= 8 and len(user_pass.value) >= 8:
            sign_in_btn.disabled = False
        else:
            sign_in_btn.disabled = True
        page.update()

    user_login = ft.TextField(label='Логін...',
                              width=350,
                              max_length=25,
                              on_change=validat,
                              input_filter=ft.InputFilter(allow=True,
                                                          regex_string=r"[A-Za-zа-яА-ЯіІЇї0-9_]",
                                                          replacement_string=""),)

    user_pass = ft.TextField(label='Пароль...',
                             width=350,
                             password=True,
                             on_change=validat,
                             can_reveal_password=True,
                             input_filter=ft.InputFilter(allow=True,
                                                         regex_string=r"[A-Za-zа-яА-ЯіІЇї0-9_]",
                                                         replacement_string=""),)

    sign_in_btn = ft.OutlinedButton(text='Вхід', width=350, on_click=authorize, disabled=True)

    def navigate_to_sign_up(_):
        page.go("/sign_up")

    to_sign_up_btn = ft.TextButton("Зареєструватись", on_click=navigate_to_sign_up)

    sign_in_panel = ft.Row(
        [
            ft.Column
            (
                [
                    ft.Container(
                        ft.Text('Вхід', size=30),
                        margin=ft.margin.only(left=145, top=140, bottom=40),
                    ),
                    user_login,
                    user_pass,
                    sign_in_btn,
                    ft.Container(
                        content=to_sign_up_btn,
                        margin=ft.margin.only(left=110, top=200),
                    ),
                ],
            ),
        ], alignment=ft.MainAxisAlignment.CENTER
    )

    return sign_in_panel
