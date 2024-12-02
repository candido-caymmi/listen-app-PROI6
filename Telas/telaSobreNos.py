import flet as ft
from .telaBase import TelaBase
from .componentes.botao import Botao
from .componentes.identidadeVisual import GRADIENTE, exibir_logo, ALINHAMENTO_COLUNA, ALINHAMENTO_LINHA

class TelaSobreNos(TelaBase):
    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.audio_player = None

    def ao_clicar_volta(self, e):
        
        if self.audio_player:
            self.audio_player.pause()
        
        self.page.clean()
        from .telaLogin import TelaLogin 
        login_screen = TelaLogin(self.page)
        login_screen.mostrar()

    def mostrar(self):
        self.page.title = "Listen"
        logo = exibir_logo(self.page.window_width)

        popular_images = ft.Row(
            wrap=False,
            scroll="always",
            spacing=10,
            controls=[
                ft.Container(
                    content=ft.Image(
                        src="Telas/Imagens/HOTLINEBLING.png", 
                        fit=ft.ImageFit.COVER
                    ),
                    width=350,
                    height=350,
                    border_radius=ft.border_radius.all(10),
                ),
            ],
        )

        # Player de música
        tocador_musica = self.audio_player = ft.Audio(
            src="audio/hotline_bling.mp3",
            autoplay=True,
        )

        conteudo_principal = ft.Container(
            expand = True,
            gradient=GRADIENTE,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    logo,
                                    popular_images,
                                    tocador_musica,
                                    Botao("Sair", self.ao_clicar_volta, True)
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
        self.page.add(conteudo_principal)
        self.page.update()
