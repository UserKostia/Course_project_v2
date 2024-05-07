import flet as ft
from flet import IconButton, AppBar


def navigation_bar(page):
    nav_bar = AppBar(
            leading_width=40,
            center_title=False,
            title=ft.Text("Medicine"),
            leading=ft.Icon(ft.icons.PEOPLE),
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                IconButton(ft.icons.HOME, on_click=lambda _: page.go('/main')),
                IconButton(ft.icons.PEOPLE_OUTLINE, on_click=lambda _: page.go('/doc_rec')),
                IconButton(ft.icons.PERSON_2_OUTLINED, on_click=lambda _: page.go('/patient')),
                IconButton(ft.icons.SETTINGS, on_click=lambda _: page.go('/settings'))
            ]
    )

    return nav_bar
