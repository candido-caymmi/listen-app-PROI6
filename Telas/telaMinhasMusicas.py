import flet as ft
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from .telaBase import TelaBase
from .componentes.identidadeVisual import GRADIENTE, exibir_logo, ALINHAMENTO_COLUNA, ALINHAMENTO_LINHA
from .componentes.elementosResponsivos import TabelaComRolagem
from .componentes.elementosGraficos import LimparAplicarTema
from .componentes.botao import Botao

class TelaMinhasMusicas(TelaBase):
    def __init__(self, page: ft.Page, username: str, email: str, spotify_token: str):
        super().__init__(page)
        self.username = username
        self.email = email
        self.spotify_token = spotify_token
        self.sp = spotipy.Spotify(auth=self.spotify_token)

    def obter_musicas_mais_ouvidas(self, time_range: str):
        try:
            user_top_tracks = self.sp.current_user_top_tracks(limit=10, time_range=time_range)['items']
            return user_top_tracks
        except Exception as e:
            print(f"Erro ao obter músicas mais ouvidas: {e}")
            return []

    def criar_tabela_musicas(self, top_musicas):
        colunas = [
            ft.DataColumn(ft.Text("Capa")),
            ft.DataColumn(ft.Text("Música")),
            ft.DataColumn(ft.Text("Artista")),
        ]
        linhas = []

        for track in top_musicas:
            nome_faixa = track['name']
            artista = track['artists'][0]['name']
            capa_url = track['album']['images'][0]['url']
            spotify_url = track['external_urls']['spotify']

            capa_musica = ft.Image(
                src=capa_url,
                width=50,
                height=50
            )

            capa_com_evento = ft.GestureDetector(
                content=capa_musica,
                on_tap=lambda e, url=spotify_url: self.abrir_no_spotify(url)
            )

            linhas.append(ft.DataRow(
                cells=[
                    ft.DataCell(capa_com_evento),
                    ft.DataCell(ft.Text(nome_faixa, style="bodySmall")),
                    ft.DataCell(ft.Text(artista, style="bodySmall")),
                ]
            ))

        tabela_com_rolagem = TabelaComRolagem(colunas=colunas, linhas=linhas, altura=300)

        return tabela_com_rolagem
    
    def abrir_no_spotify(self, url: str):
        self.page.launch_url(url)

    def mostrar(self):
        self.page.title = "Suas Musicas"
        self.page.scroll = ft.ScrollMode.AUTO 

        top_musicas_ultimo_mes = self.obter_musicas_mais_ouvidas('short_term')
        top_musicas_6_meses = self.obter_musicas_mais_ouvidas('medium_term')
        top_musicas_12_meses = self.obter_musicas_mais_ouvidas('long_term')
       
        conteudo_status = ft.Container(
        expand=True,
        content=ft.Column(
                [
                    ft.Container(height=20),
                    ft.Text("Músicas Mais Ouvidas no Último Mês", style="headlineMedium"),
                    self.criar_tabela_musicas(top_musicas_ultimo_mes),
                    ft.Container(height=20),
                    ft.Text("Músicas Mais Ouvidas nos Ultimos 6 Meses", style="headlineMedium"),
                    self.criar_tabela_musicas(top_musicas_6_meses),
                    ft.Container(height=20),
                    ft.Text("Músicas Mais Ouvidas nos Ultimos 12 Meses", style="headlineMedium"),
                    self.criar_tabela_musicas(top_musicas_12_meses),
                ],
                **ALINHAMENTO_COLUNA
            )
        )

        self.page.add(conteudo_status)