from dataclasses import dataclass
import flet as ft
import os
from youtube_dl import youtube_dl, dd

@dataclass
class option:
    url: str = ""
    format_index: int = 0
    ext_index: int = 0
    quality_index: int = 5
    title: str = ""
    storage: str = os.path.normpath(os.path.expandvars("%USERPROFILE%/Downloads"))
    overwrite_index: int = 0
    filetime_index: int = 0



def main(page: ft.Page):
    def main_page():
        url_tf = ft.TextField(
            label="URL",
            border="underline",
            prefix_icon=ft.icons.LINK,
            value=op.url,
            expand=True,
        )
        page.views.append(
            ft.View(
                "/",
                [url_tf]
            )
        )
    
    def route_change(route):
        page.views.clear()
        if page.route == "/":
            main_page()
        page.update()
        
    op = option()
    page.title = "Flector"
    page.on_route_change = route_change
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main)