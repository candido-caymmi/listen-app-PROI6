import flet as ft
from .elementosGraficos import GeneroMusical
from .identidadeVisual import ALINHAMENTO_COLUNA
import spotipy

def exibir_generos_populares(page, spotify_token):
    # Função para abrir a URL no Spotify
    def abrir_no_spotify(url: str):
        page.launch_url(url)

    try:
        # Autenticação com o token do Spotify
        sp = spotipy.Spotify(auth=spotify_token)
        # Obtendo os gêneros populares
        genres = sp.categories(limit=50, locale='pt_BR')['categories']['items']
        
        genre_controls = []
        for genre in genres:
            genre_image_url = genre['icons'][0]['url']
            genre_name = genre['name']
            spotify_url = f"https://open.spotify.com/genre/{genre['id']}"  # URL formatada para abrir no Spotify

            # Criação do componente com evento de clique para redirecionar
            genero_com_evento = ft.GestureDetector(
                content=GeneroMusical(genre_image_url, genre_name),
                on_tap=lambda e, url=spotify_url: abrir_no_spotify(url)
            )

            genre_controls.append(genero_com_evento)


        genres_images = ft.Row(
            wrap=False,
            scroll="always",
            spacing=10,
            controls=genre_controls
        )

        seccao_generos = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Gêneros", style="titleMedium"),  # Título da seção
                    genres_images  # Linha com os gêneros
                ],
                *ALINHAMENTO_COLUNA
            ),
            padding=15  # Padding do container
        )
        
        return seccao_generos

    except Exception as e:
        print(f"Erro ao buscar dados dos gêneros: {e}")
        return ft.Container(content=ft.Text("Erro ao carregar os gêneros musicais.", style="bodyMedium"), padding=15)
