import flet as ft

def CampoTexto(rotulo: str, senha: bool = False):
    return ft.TextField(
        label=rotulo,
        width=200,
        border_color='#9ca3af',
        focused_color='#e5e7eb',
        focused_bgcolor=ft.colors.WHITE,
        filled=False,
        cursor_color='#e5e7eb',
        color='#e5e7eb',
        password=senha,
        label_style=ft.TextStyle(color='#e5e7eb')
    )