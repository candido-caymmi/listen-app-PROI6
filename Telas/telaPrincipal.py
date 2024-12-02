import flet as ft
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from database import Database
from .telaBase import TelaBase
from .componentes.campoTexto import CampoTexto
from .componentes.identidadeVisual import GRADIENTE, exibir_logo, ALINHAMENTO_COLUNA, ALINHAMENTO_LINHA
from .componentes.elementosGraficos import GeneroMusical, LimparAplicarTema, LimparAtualizar
from .componentes.exibirFaixasPopulares import exibir_faixas_populares
from .componentes.exibirGenerosPopulares import exibir_generos_populares
from .componentes.barras import criar_barra_de_titulo, criar_barra_navegacao

class TelaPrincipal(TelaBase):
    def __init__(self, page: ft.Page, username: str, email: str, spotify_token: str):
        super().__init__(page)
        self.username = username
        self.email = email
        self.spotify_token = spotify_token
        self.db = Database()

        try:
            # Inicializa a conexão com o Spotify
            self.sp = spotipy.Spotify(auth=self.spotify_token)
            self.sp.current_user()  # Verifica se o token é válido
            print("DEBUG - Conexão com o Spotify bem-sucedida.")
        except Exception as e:
            print(f"Erro ao conectar com o Spotify: {e}")
            self.page.snack_bar = ft.SnackBar(ft.Text("Erro ao conectar com o Spotify!"), open=True)
            self.page.update()
            self.sp = None

        self.user_id = self.obter_user_id_spotify()

    def obter_user_id_spotify(self):
        if not self.sp:
            print("DEBUG - Não foi possível obter Spotify User ID: conexão com o Spotify não inicializada.")
            return None
        try:
            user_info = self.sp.current_user()
            spotify_user_id = user_info.get("id")
            print(f"DEBUG - Spotify User ID obtido: {spotify_user_id}")

            user = self.db.get_user_by_spotify(spotify_user_id)
            return user[0] if user else None
        except Exception as e:
            print(f"Erro ao obter Spotify User ID: {e}")
            return None

    def ao_clicar_opcoes(self, opcao):
        if opcao == "trocar_tema":
            self.ao_clicar_trocar_tema(None)
        elif opcao == "minhas_musicas":
            self.ao_clicar_minhas_musicas(None)
        elif opcao == "meus_artistas":
            self.ao_clicar_meus_artistas(None)
        elif opcao == "meus_generos":
            self.ao_clicar_meus_generos(None)
        elif opcao == "sair":
            self.ao_clicar_login(None)

    def ao_clicar_login(self, e):
        LimparAplicarTema(self.page)
        from .telaLogin import TelaLogin
        TelaLogin(self.page).mostrar()

    def ao_clicar_minhas_musicas(self, e):
        LimparAtualizar(self.page)
        from .telaMinhasMusicas import TelaMinhasMusicas
        TelaMinhasMusicas(self.page, self.username, self.email, self.spotify_token).mostrar()

    def ao_clicar_meus_artistas(self, e):
        LimparAtualizar(self.page)
        from .telaMeusArtistas import TelaMeusArtistas
        TelaMeusArtistas(self.page, self.username, self.email, self.spotify_token).mostrar()

    def ao_clicar_meus_generos(self, e):
        LimparAtualizar(self.page)
        from .telaMeusGeneros import TelaMeusGeneros
        TelaMeusGeneros(self.page, self.username, self.email, self.spotify_token).mostrar()

    def ao_clicar_tela_principal(self):
        LimparAtualizar(self.page)
        TelaPrincipal(self.page, self.username, self.email, self.spotify_token).mostrar()

    def ao_clicar_tela_pesquisar(self):
        LimparAtualizar(self.page)
        from .telaPesquisar import TelaPesquisar
        TelaPesquisar(self.page, self.username, self.email, self.spotify_token, self.db).mostrar()

    def ao_clicar_tela_avaliados(self):
        LimparAtualizar(self.page)
        from .telaAvaliados import TelaAvaliados
        print(f"DEBUG - Chamando TelaAvaliados com user_id={self.user_id}")
        TelaAvaliados(self.page, self.username, self.email, self.spotify_token, self.db, self.user_id).mostrar()

    def ao_clicar_tela_tocados_recentemente(self):
        LimparAtualizar(self.page)
        from .telaTocadosRecentemente import TelaTocadosRecentemente
        TelaTocadosRecentemente(self.page, self.username, self.email, self.spotify_token).mostrar()

    def ao_clicar_barra_navegacao(self, e):
        if e.control.selected_index == 0:
            self.ao_clicar_tela_principal()
        elif e.control.selected_index == 1:
            self.ao_clicar_tela_pesquisar()
        elif e.control.selected_index == 2:
            self.ao_clicar_tela_avaliados()
        elif e.control.selected_index == 3:
            self.ao_clicar_tela_tocados_recentemente()

    def ao_clicar_trocar_tema(self, e):
        self.page.theme_mode = (
            ft.ThemeMode.LIGHT if self.page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        )
        self.page.update()

    def mostrar(self):
        self.page.title = "Listen"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.update()

        # Criação da AppBar
        self.page.appbar = criar_barra_de_titulo(self.username, self.email, self.ao_clicar_opcoes)

        # Criação das seções de conteúdo
        try:
            seccao_generos = exibir_generos_populares(self.page, self.spotify_token)
            seccao_faixas_populares = exibir_faixas_populares(self.spotify_token)
        except Exception as e:
            print(f"Erro ao buscar dados do Spotify: {e}")
            self.page.snack_bar = ft.SnackBar(ft.Text("Erro ao buscar dados do Spotify!"), open=True)
            self.page.update()
            return

        # Criação da NavigationBar
        self.page.navigation_bar = criar_barra_navegacao(self.ao_clicar_barra_navegacao)

        # Conteúdo principal
        conteudo_principal = ft.Container(
            expand=True,
            content=ft.Column([seccao_generos, seccao_faixas_populares]),
            padding=20
        )

        self.page.add(conteudo_principal)