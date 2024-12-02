import flet as ft
import re
from database import Database
from .componentes.campoTexto import CampoTexto
from .componentes.botao import Botao, BotaoTexto
from .telaBase import TelaBase
from .componentes.identidadeVisual import GRADIENTE, exibir_logo
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class TelaCadastro(TelaBase):
    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.db = Database()

        # Configuração do Spotify OAuth
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id="SEU_CLIENT_ID",
            client_secret="SEU_CLIENT_SECRET",
            redirect_uri="http://localhost:3000/callback",
            scope="user-library-read user-top-read user-read-private"
        ))

    def ao_clicar_cadastrar_com_spotify(self, e):
        # Inicia o fluxo de autenticação com o Spotify
        auth_url = self.sp.auth_manager.get_authorize_url()
        self.page.launch_url(auth_url)  # Redireciona o usuário para o Spotify para login

    def ao_clicar_voltar(self, e):
        self.page.clean()
        from .telaLogin import TelaLogin  
        tela_login = TelaLogin(self.page)
        tela_login.mostrar()

    def registrar_usuario_spotify(self, token_info):
        self.sp = spotipy.Spotify(auth_manager=self.sp.auth_manager)
        user_info = self.sp.current_user()  # Obtém as informações do usuário
        spotify_user_id = user_info['id']
        username = user_info['display_name']
        email = user_info.get('email', None)  # O email pode ser None se o usuário não permitir

        if not email:
            self.page.snack_bar = ft.SnackBar(ft.Text("Erro: E-mail não disponível no Spotify."), open=True)
            self.page.update()
            return
        
        # Adiciona o usuário ao banco de dados
        self.db.add_user(username, email, spotify_user_id)

        # Redireciona para a tela principal
        self.page.clean()
        from .telaLogin import TelaLogin
        tela_login = TelaLogin(self.page)
        tela_login.mostrar()

    def mostrar(self):
        self.page.title = "Listen"
        
        # Botão para o cadastro via Spotify
        botao_spotify = Botao("Cadastrar com Spotify", self.ao_clicar_cadastrar_com_spotify, primario=True)
        
        # Layout da tela
        logo = exibir_logo(self.page.window_width)
        
        conteudo = ft.Container(
            expand=True,  
            gradient=GRADIENTE,
            content=ft.Column(
                [
                    ft.Row([logo], alignment=ft.MainAxisAlignment.CENTER),
                    botao_spotify,
                    BotaoTexto("Voltar para Login", self.ao_clicar_voltar),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                expand=True  
            )
        )
        
        self.page.add(conteudo)
