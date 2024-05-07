import flet as ft
import sqlite3


class userAvatar(ft.CircleAvatar):
    def __init__(self):
        super().__init__(
            ft.CircleAvatar(
                foreground_image_url="https://avatars.githubusercontent.com/u/5041459?s=88&v=4",
                content=ft.Text("FF"),
                height=40,
                width=40,
            )
        )


def get_avatar():
    db = sqlite3.connect('Entrance.db')
    c = db.cursor()
    c.execute(
        """
        SELECT login FROM initials_ava
        """
    )
    login = c.fetchone()[0]
    initials = login[:2].upper()
    avatar = userAvatar()
    avatar.bgcolor = "#74c1f7"
    avatar.content = ft.Text(initials, size=24, color=ft.colors.WHITE)

    return avatar
