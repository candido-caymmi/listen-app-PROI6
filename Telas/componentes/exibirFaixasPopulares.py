import flet as ft
from .identidadeVisual import ALINHAMENTO_COLUNA, ALINHAMENTO_LINHA
import spotipy

def exibir_faixas_populares(spotify_token):
    try:

        sp = spotipy.Spotify(auth=spotify_token)
        # Obtendo as faixas populares do usuário
        user_top_tracks = sp.current_user_top_tracks(limit=50)['items']
        
        # Definindo as colunas da DataTable, incluindo a coluna de Popularidade (número de plays aproximado)
        columns = [
            ft.DataColumn(ft.Text("Capa")),
            ft.DataColumn(ft.Text("Música")),
            ft.DataColumn(ft.Text("Popularidade"))  # Nova coluna para a popularidade
        ]
        
        # Definindo as linhas da DataTable
        rows = []
        for track in user_top_tracks:
            # Popularidade da música (0-100)
            popularity = track['popularity']
            
            rows.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Image(src=track['album']['images'][0]['url'], height=60, width=60)),
                    ft.DataCell(ft.Text(track['name'], style="bodySmall")),
                    ft.DataCell(ft.Text(f"{popularity}%", style="bodySmall"))  # Exibindo a popularidade como porcentagem
                ]
            ))

        faixas_populares_table = ft.DataTable(
            expand=True,
            columns=columns,
            rows=rows
        )

        tabela_scroll = ft.ListView(
            controls=[faixas_populares_table],
            height=300,  
            expand=True  
        )

        tabela_scroll.scrollbar_theme = ft.ScrollbarTheme(
            track_color={
                ft.MaterialState.HOVERED: ft.colors.AMBER,
                ft.MaterialState.DEFAULT: ft.colors.TRANSPARENT,
            },
            track_visibility=True,
            track_border_color=ft.colors.BLUE,
            thumb_visibility=True,
            thumb_color={
                ft.MaterialState.HOVERED: ft.colors.RED,
                ft.MaterialState.DEFAULT: ft.colors.GREY_300,
            },
            thickness=30,
            radius=15,
            main_axis_margin=5,
            cross_axis_margin=10,
        )

        # Container para exibir a tabela
        seccao_faixas_populares = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Suas Faixas Populares", style="titleMedium"),  # Título da seção
                    tabela_scroll
                ], 
                *ALINHAMENTO_COLUNA
            )
        )
        
        return seccao_faixas_populares

    except Exception as e:
        print(f"Erro ao buscar dados das faixas populares: {e}")
        return ft.Container(content=ft.Text("Erro ao carregar as faixas populares.", style="bodyMedium"), padding=15)