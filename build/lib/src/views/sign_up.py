import flet as ft
import sqlite3

from State import global_state


def sign_up(_):
    page = global_state.get_state_by_key('page')
    page.title = "Registration"
    page.theme_mode = 'light'

    page.window_maximized = True
    page.window_resizable = True

    def register(_):
        db = sqlite3.connect('Registration.db')
        cur = db.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY,
                login VARCHAR(30),
                pass VARCHAR(30)
            )
            """
        )

        cur.execute("SELECT COUNT(*) FROM users WHERE login=?", (user_login.value,))
        if cur.fetchone()[0] > 0:
            page.snack_bar = ft.SnackBar(
                ft.Text('Такий користувач вже існує! Змініть логін.',
                        size=16,
                        weight=ft.FontWeight.W_700),
                bgcolor=ft.colors.RED_500,
                duration=5000,
            )
            page.snack_bar.open = True
            page.update()
        else:
            cur.execute(f"INSERT INTO users VALUES (NULL, ?, ?)", (user_login.value, user_pass.value))
            db.commit()
            db.close()

            db_1 = sqlite3.connect('Entrance.db')
            try:
                c = db_1.cursor()

                c.execute(
                """
                    CREATE TABLE IF NOT EXISTS initials_ava(
                    id INTEGER PRIMARY KEY,
                    login VARCHAR(30)
                    )
                """
                )

                c.execute(f"DELETE FROM initials_ava")
                c.execute("INSERT INTO initials_ava (login) VALUES (?)", (user_login.value,))
                db_1.commit()
            except sqlite3.IntegrityError:
                pass
            finally:
                db_1.close()

            user_login.value = ''
            user_pass.value = ''
            sign_up_btn.text = 'Вас зареєстровано!'
            page.update()
            page.go("/main")

    def validat(_):
        if all([user_login.value, user_pass.value]) and len(user_login.value) >= 8 and len(user_pass.value) >= 8:
            sign_up_btn.disabled = False
        else:
            sign_up_btn.disabled = True
        page.update()

    user_login = ft.TextField(label='Логін... (мінімально 8 символів)',
                              width=350,
                              max_length=25,
                              on_change=validat,
                              input_filter=ft.InputFilter(allow=True,
                                                          regex_string=r"[A-Za-zа-яА-ЯіІЇї0-9_]",
                                                          replacement_string=""),)

    user_pass = ft.TextField(label='Пароль... (мінімально 8 символів)',
                             password=True,
                             width=350,
                             max_length=30,
                             on_change=validat,
                             can_reveal_password=True,
                             input_filter=ft.InputFilter(allow=True,
                                                         regex_string=r"[A-Za-zа-яА-ЯіІЇї0-9_]",
                                                         replacement_string=""),)

    sign_up_btn = ft.OutlinedButton(text='Зареєструватись', width=350, on_click=register, disabled=True)

    def navigate_to_sign_in(_):
        page.go("/")

    already_registered = ft.TextButton("Вже зареєстровані?", on_click=navigate_to_sign_in)

    sign_up_panel = ft.Row(
        [
            ft.Column
            (
                [
                    ft.Container(
                        content=ft.Text('Реєстрація', size=30),
                        margin=ft.margin.only(left=100, top=140, bottom=40),
                    ),
                    user_login,
                    user_pass,
                    sign_up_btn,
                    ft.Container(
                        content=already_registered,
                        margin=ft.margin.only(left=95, top=200),
                    ),
                ],
            ),
        ], alignment=ft.MainAxisAlignment.CENTER,
    )

    return sign_up_panel
