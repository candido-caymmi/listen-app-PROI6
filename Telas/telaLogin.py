import flet as ft
from database import Database
from .telaPrincipal import TelaPrincipal
from .telaCadastro import TelaCadastro
from .telaBase import TelaBase
from .componentes.campoTexto import CampoTexto
from .componentes.identidadeVisual import GRADIENTE, exibir_logo, ALINHAMENTO_COLUNA, ALINHAMENTO_LINHA
from .componentes.botao import Botao, BotaoTexto
from spotipy.oauth2 import SpotifyOAuth
import spotipy


class TelaLogin(TelaBase):
    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.page.snack_bar = ft.SnackBar(content=ft.Text(""))
        self.db = Database()

        # Configuração da autenticação com Spotify
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id="", #SEM CREDENCIAL 
            client_secret="", #SEM CREDENCIAL
            redirect_uri="http://localhost:3000/callback",
            scope="user-library-read user-top-read user-read-private user-read-email user-read-recently-played"
        ))

    def ao_clicar_login_spotify(self, e):
        try:
            # Obter informações do usuário autenticado no Spotify
            user_info = self.sp.current_user()
            spotify_user_id = user_info['id']
            username = user_info['display_name']
            email = user_info.get('email', 'Email não disponível')

            # Verificar se o usuário já existe no banco de dados, e adicioná-lo se não existir
            user = self.db.get_user_by_spotify(spotify_user_id)
            if not user:
                self.db.add_user(username, email, spotify_user_id)

            spotify_token = self.sp.auth_manager.get_access_token(as_dict=False)

            # Transição para TelaPrincipal com dados de usuário e token
            self.page.clean()
            tela_principal = TelaPrincipal(self.page, username=username, email=email, spotify_token=spotify_token)
            tela_principal.mostrar()

        except Exception as e:
            print(f"Erro ao autenticar no Spotify: {e}")
            self.page.snack_bar.content.value = "Erro na autenticação com o Spotify!"
            self.page.snack_bar.open = True
            self.page.update()

    def ao_clicar_registro(self, e):
        # Ir para a próxima página (Tela de Cadastro)
        self.page.clean()
        tela_cadastro = TelaCadastro(self.page)
        tela_cadastro.mostrar()

    def mostrar(self):
        self.page.title = "Listen"

        # Criação do conteúdo da tela de login
        logo = exibir_logo(self.page.window_width)

        conteudo_login = ft.Container(
            expand=True,
            gradient=GRADIENTE,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            logo
                        ],
                        **ALINHAMENTO_LINHA
                    ),
                    ft.Container(height=20),  # Espaço entre a logo e os botões
                    Botao("Login com Spotify", self.ao_clicar_login_spotify, primario=True),
                    # BotaoTexto("Não tem cadastro? Cadastre-se", self.ao_clicar_registro)
                ],
                **ALINHAMENTO_COLUNA
            )
        )

        self.page.add(conteudo_login)

        token_info = self.sp.auth_manager.get_access_token(as_dict=False)
        if not token_info:
            print("Erro ao obter token de autenticação")
        return