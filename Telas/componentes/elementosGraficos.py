import flet as ft
from .identidadeVisual import COR_PRIMARIA 

class GeneroMusical(ft.UserControl):
    def __init__(self, imagem: str, nome: str):
        super().__init__()
        self.imagem = imagem
        self.nome = nome

    def build(self):
        return ft.Stack(
            controls=[
                ft.Image(
                    src=self.imagem,
                    fit=ft.ImageFit.COVER,
                    width=300,
                    height=300,
                    border_radius=ft.border_radius.all(10),
                ),
                ft.Container(
                    content=ft.Text(self.nome, color="white", style="headlineSmall"),
                    alignment=ft.alignment.center,
                    padding=10,
                ),
            ]
        )
    
class ImagensPopulares(ft.UserControl):
    def __init__(self, imagens: list):
        super().__init__()
        self.imagens = imagens  # Lista de URLs das imagens

    def build(self):
        # Cria os containers com as imagens
        containers = [
            ft.Container(
                content=ft.Image(src=imagem, fit=ft.ImageFit.COVER),
                width=150,
                height=150,
                border_radius=ft.border_radius.all(10),
            ) for imagem in self.imagens
        ]

        return ft.Row(
            wrap=False,
            scroll="always",
            spacing=10,
            controls=containers
        )

class MensagemSemAvaliacoes(ft.UserControl):
    """
    Componente que exibe uma mensagem indicando que não há avaliações.
    """

    def build(self):
        return ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.icons.ERROR, size=40, color=ft.colors.GREY),
                        ft.Text("Sem Avaliações", weight="bold"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )


class MusicaAvaliada(ft.UserControl):
    """
    Componente que exibe detalhes de uma música avaliada, incluindo capa,
    título, artista, avaliação por estrelas e a funcionalidade de exclusão.
    """

    def __init__(self, detalhes, rating, on_excluir):
        super().__init__()
        self.detalhes = detalhes
        self.rating = rating
        self.on_excluir = on_excluir

    def build(self):
        return ft.Dismissible(
            key=self.detalhes["nome"],
            on_dismiss=self.on_excluir,
            content=ft.Row(
                [
                    ft.Image(src=self.detalhes["capa"], width=60, height=60),
                    ft.Column(
                        [
                            ft.Text(self.detalhes["nome"], weight="bold"),
                            ft.Text(self.detalhes["artista"], color=ft.colors.GREY),
                            EstrelasAvaliacao(self.rating),
                        ],
                        spacing=5,
                    ),
                ],
                spacing=10,
                alignment="start",
            ),
            background=ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.icons.DELETE, color=ft.colors.WHITE),
                        ft.Text("Excluir", color=ft.colors.WHITE, weight="bold"),
                    ],
                    spacing=10,
                    alignment="center",
                ),
                bgcolor=ft.colors.RED,
                padding=ft.padding.all(10),
            ),
        )


class EstrelasAvaliacao(ft.UserControl):
    """
    Componente que exibe estrelas de avaliação de 0 a 5.
    """

    def __init__(self, rating: int):
        super().__init__()
        self.rating = rating

    def build(self):
        return ft.Row(
            [
                ft.Icon(ft.icons.STAR, COR_PRIMARIA) for _ in range(self.rating)
            ] + [
                ft.Icon(ft.icons.STAR_BORDER, color=ft.colors.GREY) for _ in range(5 - self.rating)
            ]
        )


def LimparAplicarTema(page: ft.Page):
    page.clean()
    page.appbar = None
    page.navigation_bar = None
    theme_mode = ft.ThemeMode.DARK  # Altere para o tema desejado
    page.theme_mode = theme_mode  # Aplica o tema
    page.update()

def LimparAtualizar(page: ft.Page):
    page.clean()
    # page.navigation_bar = None
    page.update()