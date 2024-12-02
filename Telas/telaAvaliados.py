import flet as ft
from .componentes.identidadeVisual import COR_PRIMARIA
from database import Database
import spotipy
from .componentes.elementosGraficos import MensagemSemAvaliacoes, MusicaAvaliada


class TelaAvaliados:
    def __init__(self, page: ft.Page, username: str, email: str, spotify_token: str, db: Database, user_id: int):
        self.page = page
        self.username = username
        self.email = email
        self.spotify_token = spotify_token
        self.db = db
        self.user_id = user_id
        self.sp = spotipy.Spotify(auth=spotify_token)

        # Container dedicado para as avaliações
        self.avaliacoes_container = ft.Column()

    def alterar_ordenacao(self, e):
        """Alterna a ordem de classificação e atualiza a lista."""
        self.ordenar_decrescente = not self.ordenar_decrescente

        # Alterar ícone com base na ordem atual
        self.icone_ordenacao.icon = (
            ft.icons.ARROW_UPWARD if self.ordenar_decrescente else ft.icons.ARROW_DOWNWARD
        )
        self.icone_ordenacao.update()

        # Atualizar a lista de avaliações com a nova ordem
        self.atualizar_avaliacoes()

    def buscar_detalhes_musica(self, item_id):
        if not item_id:
            print("Erro: ID da música não pode ser vazio.")
            return None
        
        try:
            track = self.sp.track(item_id)
            if not track:
                print(f"Erro: Detalhes da música não encontrados para o ID: {item_id}")
                return None
            
            return {
                "nome": track["name"],
                "artista": ", ".join([artist["name"] for artist in track["artists"]]),
                "capa": track["album"]["images"][0]["url"] if track["album"]["images"] else None,
            }
        except Exception as e:
            print(f"Erro ao buscar detalhes da música: {e}")
            return None

    def atualizar_avaliacoes(self):
        """Atualiza a lista de músicas avaliadas no container."""
        self.avaliacoes_container.controls.clear()

        # Recupera avaliações e ordena conforme a flag `ordenar_decrescente`
        avaliacoes = sorted(
            self.db.get_ratings(self.user_id),
            key=lambda x: x[1],  # Classifica pelo rating
            reverse=self.ordenar_decrescente,
        )

        for item_id, rating, comment, timestamp in avaliacoes:
            detalhes = self.buscar_detalhes_musica(item_id)
            if detalhes:
                def excluir_avaliacao(e, item_id=item_id):
                    self.db.cursor.execute(
                        "DELETE FROM ratings WHERE user_id = ? AND music_id = ?",
                        (self.user_id, item_id),
                    )
                    self.db.conn.commit()
                    print(f"Música {item_id} excluída com sucesso.")
                    self.atualizar_avaliacoes()  # Atualiza a página

                self.avaliacoes_container.controls.append(
                    MusicaAvaliada(
                        detalhes=detalhes,
                        rating=rating,
                        on_excluir=lambda e: excluir_avaliacao(e, item_id),
                    )
                )
        self.avaliacoes_container.update()

    def mostrar(self):
        self.page.clean()

        # Cria o botão de ordenação
        self.icone_ordenacao = ft.IconButton(
            icon=ft.icons.ARROW_DOWNWARD,
            on_click=self.alterar_ordenacao
        )
        self.ordenar_decrescente = False  # Inicialmente, ordem crescente

        # Adiciona os controles à página antes de atualizar
        self.page.controls.append(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("Avaliações", size=20, weight="bold"),
                            self.icone_ordenacao,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    self.avaliacoes_container,  # Adiciona o container à página
                ]
            )
        )
        self.page.update()  # Atualiza a página para refletir os controles adicionados

        # Agora que o container está na página, podemos atualizá-lo
        self.atualizar_avaliacoes()

