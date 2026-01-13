import flet as ft
import inspect

print("Flet version:", ft.version)
print("Tab args:", inspect.signature(ft.Tab.__init__))
