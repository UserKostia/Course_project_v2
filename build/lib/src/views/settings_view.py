import flet as ft
from flet import Icon, icons, Text, Row, Column, TextButton

from pythonflet.src.components.navigation_bar.nav_bar import show_menu_bar
from State import global_state


def settings_view(_):
    page = global_state.get_state_by_key('page')

    def toggle_dark_mode(_):
        if page.theme_mode == "light":
            page.theme_mode = "dark"
            page.update()
        else: 
            page.theme_mode = "light"
            page.update()

    def exit_app(_):
        page.window_destroy()

    def block_app(_):
        page.go("/")
    
    content = Column(
        [
            show_menu_bar(page),
            Row(
            [
                Text("My Settings", size=30),
                Icon(icons.SETTINGS, size=30),
            ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            Row(
                [
                    TextButton("Light/Dark Mode", icon=ft.icons.WB_SUNNY_OUTLINED, on_click=toggle_dark_mode)
                ],
            ),
            Row(
                [
                    TextButton("Exit Application", icon=ft.icons.CLOSE, on_click=exit_app, icon_color="red")
                ],
            ),
            Row(
                [
                    TextButton("Зупинити сесію", icon=ft.icons.BLOCK, on_click=block_app, icon_color="red")
                ],
            ),
        ],
    )

    return content
