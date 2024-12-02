import flet as ft
import spotipy
from .telaBase import TelaBase   
from .componentes.identidadeVisual import ALINHAMENTO_COLUNA, ALINHAMENTO_LINHA

class TelaTocadosRecentemente(TelaBase):
    def __init__(self, page: ft.Page, username: str, email: str, spotify_token: str):
        super().__init__(page)
        self.username = username
        self.email = email
        self.spotify_token = spotify_token
        self.sp = spotipy.Spotify(auth=self.spotify_token)

    def obter_musicas_recentes(self, limite=30):
        try:
            limite = min(limite, 50)
            
            faixas_recentes = self.sp.current_user_recently_played(limit=limite)
            
            musicas = []
            for item in faixas_recentes['items']:
                faixa = item['track']
                nome = faixa['name']
                artista = ", ".join([art['name'] for art in faixa['artists']])
                album = faixa['album']['name']
                imagem_url = faixa['album']['images'][0]['url'] if faixa['album']['images'] else None
                musicas.append({
                    'nome': nome,
                    'artista': artista,
                    'album': album,
                    'imagem': imagem_url
                })

            return musicas

        except spotipy.exceptions.SpotifyException as e:
            print(f"Erro ao obter músicas recentes: {e}")
            return []
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return []

    def criar_cartoes_musicas(self, musicas):
        cartoes = []
        for musica in musicas:
            cartao = ft.Row(
                controls=[
                    ft.Image(src=musica['imagem'], width=60, height=60) if musica['imagem'] else ft.Text("Sem imagem"),
                    ft.Column([
                        ft.Text(f"{musica['nome']}", style="bodyMedium", weight="bold"),
                        ft.Text(f"{musica['artista']}", style="bodyMedium", color=ft.colors.GREY),
                        ft.Text(f"{musica['album']}", style="bodyMedium"),
                    ])
                ],
                spacing=10,
                alignment="start",
            )
            cartoes.append(ft.Container(content=cartao, padding=10))

        return ft.Column(controls=cartoes, spacing=5)

    def mostrar(self):
        self.page.scroll = ft.ScrollMode.AUTO
        musicas = self.obter_musicas_recentes()
        cartoes_musicas = self.criar_cartoes_musicas(musicas)
        
        # Adiciona os cartões à página
        self.page.add(cartoes_musicas)
        self.page.update()