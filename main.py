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
    class on_change_class:
        def textfield(self, var):
            def set_value(e):
                setattr(op, var, e.control.value)
            return set_value

        def tab(self, var):
            def set_value(e):
                setattr(op, var, e.control.selected_index)
            return set_value

    def main_page():
        url_tf = ft.TextField(
            label="URL",
            border="underline",
            prefix_icon=ft.icons.LINK,
            value=op.url,
            on_change=lambda _: on_change.textfield("url"),
            expand=True,
        )

        download_b = ft.TextButton(
            "ダウンロード", 
            icon="download", 
            on_click=lambda _: page.go("/download")
        )

        format_tab = ft.Tabs(
            selected_index=op.format_index,
            on_change=on_change.tab("format_index"),
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
                    ft.Column(
                        [
                            ft.Row([url_tf, download_b]),
                            ft.Row(
                                [
                                    format_tab, 
                                    ft.Container(
                                        setting_b,
                                        alignment=ft.alignment.center_right,
                                        expand=True,
                                    ),
                                ]
                            ),
                        ]
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
    on_change = on_change_class()
    page.title = "Flector"
    page.on_route_change = route_change
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main)