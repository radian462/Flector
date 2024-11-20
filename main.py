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
            "ダウンロード", icon="download", on_click=lambda _: page.go("/download")
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
                                    alignment=ft.MainAxisAlignment.CENTER,
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
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            expand=True,
                        ),
                        alignment=ft.alignment.center,
                        expand=True,
                        padding=ft.padding.only(bottom=75),
                    )
                ],
            )
        )

    def setting_page():
        back_button = ft.TextButton(icon="arrow_back", on_click=lambda _: page.go("/"))

        ext_list = ["mp3", "wav", "m4a", "aac", "flac"]
        ext_tab = ft.Tabs(
            on_change=op.tab("ext_index"),
            selected_index=op.ext_index,
            tabs=[ft.Tab(text=e) for e in ext_list],
        )

        quality_list = ["240p", "360p", "480p", "720p", "1080p", "最高画質"]
        quality_tab = ft.Tabs(
            on_change=op.tab("quality_index"),
            selected_index=op.quality_index,
            tabs=[ft.Tab(text=e) for e in quality_list],
        )

        title_tf = ft.TextField(
            value=op.title,
            on_change=op.textfield("title"),
            border="underline",
        )

        storage_tf = ft.TextField(
            value=op.storage,
            on_change=op.textfield("storage"),
            border="underline",
        )

        overwrite_list = ["True", "False"]
        overwrite_tab = ft.Tabs(
            on_change=op.tab("overwrite_index"),
            selected_index=op.overwrite_index,
            tabs=[ft.Tab(text=e) for e in overwrite_list],
        )

        filetime_list = ["現在時刻", "投稿時刻"]
        filetime_tab = ft.Tabs(
            on_change=op.tab("filetime_index"),
            selected_index=op.filetime_index,
            tabs=[ft.Tab(text=e) for e in filetime_list],
        )

        setting_elements = [
            {"text": "画質", "widget": quality_tab},
            {"text": "タイトル", "widget": title_tf},
            {"text": "保存場所", "widget": storage_tf},
            {"text": "同じファイル名がある場合上書きする", "widget": overwrite_tab},
            {"text": "ファイルの更新日時", "widget": filetime_tab},
        ]
        if op.format_index == 2:
            setting_elements.insert(0, {"text": "拡張子", "widget": ext_tab})

        page.views.append(
            ft.View(
                "/settings",
                [
                    ft.Column(
                        [
                            ft.Row([back_button, ft.Text("設定", size=20)]),
                            ft.Column(
                                [
                                    ft.Container(
                                        ft.Column(
                                            [
                                                ft.Text(
                                                    e["text"],
                                                    size=20,
                                                    weight=ft.FontWeight.BOLD,
                                                    ),
                                                    e["widget"],
                                            ]
                                        ),
                                        margin=ft.margin.only(top=30 if i != 0 else 0),
                                    )
                                    for i, e in enumerate(setting_elements)
                                ]
                            ),
                        ],
                        scroll=ft.ScrollMode.ALWAYS, 
                        expand=True
                    )
                ],
            )
        )
    
    def download_page():
        def progress_hook(d):
            pass

        format_dict = {
            "format": ["movie", "movie_mute", "audio"],
            "ext": ["mp3", "wav", "m4a", "aac", "flac", None],
            "quality": [240, 360, 480, 720, 1080, "Best"],
            "overwrite": [True, False],
            "timestamp": ["Now", "posted"],
        }

        format_dict = {
            "format": ["movie", "movie_mute", "audio"],
            "ext": ["mp3", "wav", "m4a", "aac", "flac", None],
            "quality": [240, 360, 480, 720, 1080, "Best"],
            "overwrite": [True, False],
            "timestamp": ["Now", "posted"],
        }

        if not op.title:
            op.title = "%(title)s"

        if op.format_index != 2:
            op.ext_index = 5

        youtube_dl(
            url=op.url,
            format=format_dict["format"][op.format_index],
            quality=format_dict["quality"][op.quality_index],
            ext=format_dict["ext"][op.ext_index],
            title=op.title,
            storage=op.storage,
            overwrite=format_dict["overwrite"][op.overwrite_index],
            timestamp=format_dict["timestamp"][op.filetime_index],
            progress_hooks=[progress_hook],
        )

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            main_page()
        elif page.route == "/settings":
            setting_page()
        elif page.route == "/download":
            download_page()
        page.update()

    op = option()
    page.title = "Flector"
    page.on_route_change = route_change
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main)
