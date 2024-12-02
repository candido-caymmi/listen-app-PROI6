import flet as ft
from .identidadeVisual import COR_PRIMARIA, GRADIENTE

def Botao(rotulo: str, acao, primario: bool = False):
    if primario:
        return ft.ElevatedButton(
            rotulo,
            on_click=acao,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor=COR_PRIMARIA,
                shape=ft.RoundedRectangleBorder(radius=5),
            )
        )
    else:
        return ft.ElevatedButton(
            rotulo,
            on_click=acao
        )

def BotaoTexto(rotulo: str, acao):
    return ft.TextButton(
        rotulo,
        on_click=acao,
        style=ft.ButtonStyle(color=COR_PRIMARIA)
    )

def BotaoGeneros(page, text, time_range, mostrar_popup):
        return ft.ElevatedButton(
            text,
            on_click=lambda e: mostrar_popup(e, time_range),
            width=300,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor=COR_PRIMARIA,
                shape=ft.RoundedRectangleBorder(radius=5),
            )
        )

