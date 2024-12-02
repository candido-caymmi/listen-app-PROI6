import flet as ft
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from .telaBase import TelaBase
from .componentes.identidadeVisual import GRADIENTE, exibir_logo, ALINHAMENTO_COLUNA, ALINHAMENTO_LINHA
from .componentes.elementosResponsivos import TabelaComRolagem
from .componentes.elementosGraficos import LimparAplicarTema
from .componentes.botao import Botao

class TelaMeusArtistas(TelaBase):
    def __init__(self, page: ft.Page, username: str, email: str, spotify_token: str):
        super().__init__(page)
        self.username = username
        self.email = email
        self.spotify_token = spotify_token
        self.sp = spotipy.Spotify(auth=self.spotify_token)

    def obter_artistas_mais_ouvidos(self, time_range: str):
        try:
            user_top_artists = self.sp.current_user_top_artists(limit=10, time_range=time_range)['items']
            return user_top_artists
        except Exception as e:
            print(f"Erro ao obter artistas mais ouvidos: {e}")
            return []

    def criar_tabela_artistas(self, top_artistas):
        colunas = [
            ft.DataColumn(ft.Text("Posição")),
            ft.DataColumn(ft.Text("Foto")),
            ft.DataColumn(ft.Text("Artista")),
        ]
        linhas = []

        for i, artist in enumerate(top_artistas, 1):
            nome_artista = artist['name']
            imagem_artista = artist['images'][0]['url'] if artist['images'] else None

            linhas.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(f"Top {i}", style="bodySmall")),  # Posição
                    ft.DataCell(ft.Image(src=imagem_artista, width=50, height=50) if imagem_artista else ft.Text("Sem imagem")),
                    ft.DataCell(ft.Text(nome_artista, style="bodySmall")),
                ]
            ))

        tabela_com_rolagem = TabelaComRolagem(colunas=colunas, linhas=linhas, altura=300)

        return tabela_com_rolagem
    
    def mostrar(self):
        self.page.title = "Seus Artistas"
        self.page.scroll = ft.ScrollMode.AUTO 

        top_artistas_ultimo_mes = self.obter_artistas_mais_ouvidos('short_term')
        top_artistas_ultimo_6_meses = self.obter_artistas_mais_ouvidos('medium_term')
        top_artistas_ultimo_12_meses = self.obter_artistas_mais_ouvidos('long_term')

        conteudo_status = ft.Container(
        expand=True,
        content=ft.Column(
                [
                    ft.Container(height=20),
                    ft.Text("Artistas Mais Ouvidos no Último Mês", style="headlineMedium"),
                    self.criar_tabela_artistas(top_artistas_ultimo_mes),
                    ft.Container(height=20),
                    ft.Text("Artistas Mais Ouvidos nos Últimos 6 Meses", style="headlineMedium"),
                    self.criar_tabela_artistas(top_artistas_ultimo_6_meses),
                    ft.Container(height=20),
                    ft.Text("Artistas Mais Ouvidos nos Últimos 12 Meses", style="headlineMedium"),
                    self.criar_tabela_artistas(top_artistas_ultimo_12_meses),
                ],
                **ALINHAMENTO_COLUNA
            )
        )

        self.page.add(conteudo_status)