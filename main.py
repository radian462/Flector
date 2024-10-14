from dataclasses import dataclass
import flet as ft
import os
from youtube_dl import youtube_dl, dd

class option:
    def __init__(self):
        self.url = ""
        self.format_index = 0
        self.ext_index = 0
        self.quality_index = 5
        self.title = ""
        self.storage = os.path.normpath(os.path.expandvars("%USERPROFILE%/Downloads"))
        self.overwrite_index = 0
        self.filetime_index = 0

    def textfield(self, var):
        def set_value(e):
            setattr(self, var, e.control.value)
        return set_value

    def tab(self, var):
        def set_value(e):
            setattr(self, var, e.control.selected_index)
        return set_value

def main(page: ft.Page):
    def main_page():
        url_tf = ft.TextField(
            label="URL",
            border="underline",
            prefix_icon=ft.icons.LINK,
            value=op.url,
            on_change=lambda _: op.textfield("url"),
            expand=True,
        )

        download_b = ft.TextButton(
            "ダウンロード", 
            icon="download", 
            on_click=lambda _: page.go("/download")
        )

        format_tab = ft.Tabs(
            selected_index=op.format_index,
            on_change=op.tab("format_index"),
            tabs=[
                ft.Tab(text="動画"),
                ft.Tab(icon=ft.icons.VOLUME_OFF, text="動画"),
                ft.Tab(text="音声"),
            ],
        )

        setting_b = ft.TextButton(
            "設定", 
            icon=ft.icons.SETTINGS, 
            on_click=lambda _: page.go("/settings"),
        )

        page.views.append(
            ft.View(
            "/",
            [
                ft.Container(
                    ft.Column(
                        [
                            ft.Row(
                                [url_tf, download_b],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            ft.Row(
                                [
                                    format_tab,
                                    ft.Container(
                                        setting_b,
                                        alignment=ft.alignment.center_right,
                                        expand=True,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        expand=True,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                )
            ]
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