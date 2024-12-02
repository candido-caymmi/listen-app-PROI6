import flet as ft

# Componente reutilizável para exibir DataTables com ListView
class TabelaComRolagem(ft.UserControl):
    def __init__(self, colunas, linhas, altura=300):
        super().__init__()
        self.colunas = colunas
        self.linhas = linhas
        self.altura = altura

    def build(self):
        tabela_scroll = ft.ListView(
            controls=[ft.DataTable(
                columns=self.colunas,
                rows=self.linhas,
                heading_row_height=40,
                divider_thickness=1,
                show_checkbox_column=False
            )],
            height=self.altura,
            expand=True
        )
        return tabela_scroll