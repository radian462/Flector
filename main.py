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

op = option()

'''
def main(page: ft.Page):
'''

if __name__ == "__main__":
    ft.app(target=main)