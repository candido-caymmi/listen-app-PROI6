import flet as ft
import spotipy
from .componentes.botao import Botao
from .telaBase import TelaBase
from spotipy.oauth2 import SpotifyOAuth
from .componentes.identidadeVisual import ALINHAMENTO_COLUNA
from .componentes.elementosGraficos import LimparAplicarTema
from .componentes.elementosResponsivos import TabelaComRolagem 

class TelaMeusGeneros(TelaBase):
    def __init__(self, page: ft.Page, username: str, email: str, spotify_token: str):
        super().__init__(page)
        self.username = username
        self.email = email
        self.spotify_token = spotify_token
        self.sp = spotipy.Spotify(auth=self.spotify_token)

    def obter_generos_mais_ouvidos(self, time_range: str, limite=10):
        top_artists = self.sp.current_user_top_artists(limit=50, time_range=time_range)['items']
        generos = []
        for artist in top_artists:
            generos.extend(artist['genres'])
        generos_unicos = list(set(generos))
        return generos_unicos[:limite]  

    def criar_tabela_generos(self, generos, titulo):
        colunas = [
            ft.DataColumn(ft.Text("Posição")),
            ft.DataColumn(ft.Text("Gênero"))
        ]
        linhas = []

        for i, genero in enumerate(generos, 1):
            linhas.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(f"Top {i}", style="bodySmall")),
                    ft.DataCell(ft.Text(genero, style="bodySmall")),
                ]
            ))

        tabela_com_rolagem = TabelaComRolagem(colunas=colunas, linhas=linhas, altura=300)

        # Retorna a tabela com título centralizado
        return tabela_com_rolagem

    def mostrar(self):
        self.page.scroll = ft.ScrollMode.AUTO

        generos_4_semanas = self.obter_generos_mais_ouvidos('short_term')
        generos_6_meses = self.obter_generos_mais_ouvidos('medium_term')
        generos_12_meses = self.obter_generos_mais_ouvidos('long_term')

        tabela_4_semanas = self.criar_tabela_generos(generos_4_semanas, "Gêneros Mais Ouvidos - Últimas 4 Semanas")
        tabela_6_meses = self.criar_tabela_generos(generos_6_meses, "Gêneros Mais Ouvidos - Últimos 6 Meses")
        tabela_12_meses = self.criar_tabela_generos(generos_12_meses, "Gêneros Mais Ouvidos - Últimos 12 Meses")

        self.page.add(
            ft.Column(
                [
                    ft.Text("Artistas Mais Ouvidos no Último Mês", style="headlineMedium"),
                    tabela_4_semanas,
                    ft.Text("Gêneros Mais Ouvidos nos Últimos 6 Meses", style="headlineMedium"),
                    tabela_6_meses,
                    ft.Text("Gêneros Mais Ouvidos nos Últimos 12 Meses", style="headlineMedium"),
                    tabela_12_meses,
                ],
                **ALINHAMENTO_COLUNA
            )
        )
