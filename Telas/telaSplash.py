import flet as ft
import time
from .telaLogin import TelaLogin
from .telaBase import TelaBase
from .componentes.identidadeVisual import GRADIENTE, exibir_logo, ALINHAMENTO_COLUNA, ALINHAMENTO_LINHA

class TelaSplash(TelaBase):
    def __init__(self, page: ft.Page):
        super().__init__(page)

    def mostrar(self):
        progress_bar = ft.ProgressBar(width=200, color=ft.colors.WHITE)
        logo = exibir_logo(self.page.window_width)
        self.page.title = "listen"

        gradient_container = ft.Container(
            expand = True,
            gradient=GRADIENTE,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    logo,
                                    progress_bar
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            )
                        ],
                        **ALINHAMENTO_LINHA
                    ),
                ],      
                **ALINHAMENTO_COLUNA
            )
        )

        
        self.page.add(gradient_container)
        
        for i in range(100):
            progress_bar.value = i / 100
            self.page.update()
            time.sleep(0.01)

        self.page.clean()
        tela_login = TelaLogin(self.page)
        tela_login.mostrar()
