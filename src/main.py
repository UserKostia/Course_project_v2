import flet as ft
# from flet_core.types import WEB_BROWSER

from routes import router
from State import global_state


def main(page: ft.Page):
    page.on_route_change = router.route_change
    router.page = page
    page.add(router.body)
    global_state.set_state_by_key('page', page)
    page.go('/')


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
