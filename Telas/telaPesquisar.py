import flet as ft
import spotipy
from .telaBase import TelaBase
from .componentes.identidadeVisual import ALINHAMENTO_COLUNA, ALINHAMENTO_LINHA, COR_PRIMARIA
from .componentes.elementosResponsivos import TabelaComRolagem
import time
from database import Database  # Certifique-se de que o caminho está correto

class TelaPesquisar(TelaBase):
    def __init__(self, page: ft.Page, username: str, email: str, spotify_token: str, db: Database):
        super().__init__(page)
        self.username = username
        self.email = email
        self.spotify_token = spotify_token
        self.db = db
        self.sp = spotipy.Spotify(auth=self.spotify_token)
        self.termo_busca_anterior = ""
        self.tempo_ultima_pesquisa = time.time()

        # Obter o ID do usuário do Spotify
        try:
            user_profile = self.sp.current_user()
            self.spotify_user_id = user_profile['id']
            user = self.db.get_user_by_spotify(self.spotify_user_id)
            if user:
                self.user_id = user[0]  # Assumindo que 'id' é o primeiro campo
            else:
                # Adicionar usuário ao banco de dados se não existir
                self.db.add_user(self.username, self.email, self.spotify_user_id)
                user = self.db.get_user_by_spotify(self.spotify_user_id)
                self.user_id = user[0]
        except Exception as e:
            print(f"Erro ao obter perfil do usuário: {e}")
            self.user_id = None  # Tratar adequadamente se não conseguir obter o ID

    def avaliar_item(self, item_id, tipo_item):
        """Abrir um diálogo para avaliar uma música, álbum ou artista, se ainda não foi avaliado."""
        # Verifica no banco de dados se já existe uma avaliação para o item
        avaliacao_existente = self.db.get_rating(self.user_id, item_id, tipo_item)

        if avaliacao_existente:
            # Exibir SnackBar informando que a música já foi avaliada
            snackbar = ft.SnackBar(
                content=ft.Text(f"Você já avaliou este {tipo_item}.", color=ft.colors.WHITE),
                bgcolor=ft.colors.RED,
            )
            self.page.snack_bar = snackbar
            self.page.snack_bar.open = True
            self.page.update()
            return  # Impede a abertura do diálogo

        # Cria uma lista para armazenar os botões de estrela
        self.estrelas = [
            ft.IconButton(
                icon=ft.icons.STAR_BORDER,
                icon_color=COR_PRIMARIA,
                on_click=lambda e, r=i: self.definir_avaliacao(item_id, tipo_item, r)  # Define o valor da avaliação ao clicar
            )
            for i in range(1, 6)
        ]

        # Cria o diálogo
        dialog = ft.AlertDialog(
            title=ft.Text(f"Avalie o {tipo_item.capitalize()}"),
            content=ft.Column([
                ft.Text(f"Dê uma nota de 0 a 5 estrelas para o {tipo_item}:", style="bodySmall"),
                ft.Row(controls=self.estrelas)
            ]),
        )

        self.page.dialog = dialog
        self.page.show_dialog(dialog)


    def definir_avaliacao(self, item_id, tipo_item, rating):
        """Atualizar a avaliação e colorir as estrelas de acordo com o rating"""
        # Atualiza as estrelas, colorindo as selecionadas
        for i in range(5):
            self.estrelas[i].icon = ft.icons.STAR if i < rating else ft.icons.STAR_BORDER
            self.estrelas[i].icon_color = COR_PRIMARIA  # Certifique-se de que a cor seja a correta

        # Salva a avaliação no banco de dados
        self.db.add_rating(self.user_id, item_id, tipo_item, rating)
            
        # Atualiza a interface
        self.page.update()

        # Adiciona SnackBar para confirmação
        # Corrigir a linha da duração da SnackBar
        snackbar = ft.SnackBar(
            content=ft.Text("Avaliação salva com sucesso!", color=ft.colors.WHITE),
            bgcolor=COR_PRIMARIA,
            # duration=ft.Duration(seconds=2)  # Usando o tipo correto para a duração
        )

        self.page.snack_bar = snackbar
        self.page.snack_bar.open = True
        self.page.update()

        # Fecha o diálogo após a confirmação
        # self.page.dialog.close()


    def criar_tabela_musicas(self, top_musicas):
        colunas = [
            ft.DataColumn(ft.Text("Capa")),
            ft.DataColumn(ft.Text("Música")),
            ft.DataColumn(ft.Text("Avaliar"))
        ]
        linhas = []

        for track in top_musicas:
            nome_musica = track['name']
            imagem_musica = track['album']['images'][0]['url'] if track['album']['images'] else None
            music_id = track['id']  # ID único da música no Spotify

            # Botão para abrir o diálogo de avaliação
            botao_avaliar = ft.IconButton(
                icon=ft.icons.STAR_BORDER,
                icon_color=COR_PRIMARIA,
                on_click=lambda e, m=music_id: self.avaliar_item(m, 'música')
            )

            linhas.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Image(src=imagem_musica, width=50, height=50) if imagem_musica else ft.Text("Sem imagem")),
                    ft.DataCell(ft.Text(nome_musica, style="bodySmall")),
                    ft.DataCell(botao_avaliar)
                ]
            ))

        # Cria a tabela
        tabela_com_rolagem = ft.DataTable(
            columns=colunas,
            rows=linhas,
            expand=True  # Isso vai permitir que a tabela ocupe o espaço disponível
        )

        # Coloca a tabela em um Container com rolagem
        tabela_com_rolagem_container = ft.Container(
            content=tabela_com_rolagem,
            expand=True,  # O container vai expandir e ocupar o espaço restante
            # scroll=True  # Ativa a rolagem interna
        )

        return tabela_com_rolagem_container



    def buscar_musicas(self, e):
        termo_busca = e.control.value  

        if termo_busca != self.termo_busca_anterior:
            self.termo_busca_anterior = termo_busca
            self.resultados.controls.clear()  

        corrente_de_tempo = time.time()
        if corrente_de_tempo - self.tempo_ultima_pesquisa < 1:  
            return
        self.tempo_ultima_pesquisa = corrente_de_tempo

        if termo_busca:
            try:
                resultados = self.sp.search(q=termo_busca, limit=20, type='track,artist,album')

                musicas = resultados['tracks']['items']

                # Adicionar resultados à tela
                if musicas:
                    self.resultados.controls.append(ft.Text("Músicas Encontradas", style="headlineSmall"))
                    tabela_musicas = self.criar_tabela_musicas(musicas)
                    self.resultados.controls.append(tabela_musicas)

                if not (musicas):
                    self.resultados.controls.append(ft.Text("Nenhum resultado encontrado.", style="bodyMedium"))

                self.page.update()

            except Exception as e:
                print(f"Erro ao buscar: {e}")
                self.resultados.controls.append(ft.Text("Erro ao buscar resultados.", style="bodyMedium"))
                self.page.update()

    def mostrar(self):
        self.page.scroll = ft.ScrollMode.AUTO
        self.barra_busca = ft.TextField(
            label="Buscar Música",
            border = COR_PRIMARIA,
            on_change=self.buscar_musicas,
            autofocus=True
        )

        self.resultados = ft.Column(expand=True)
        self.page.add(
            self.barra_busca,
            self.resultados
        )
