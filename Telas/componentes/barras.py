import flet as ft

def criar_barra_navegacao(on_change):
    return ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.HOME, label="Home"),
            ft.NavigationDestination(icon=ft.icons.SEARCH, label="Pesquisar"),
            ft.NavigationDestination(icon=ft.icons.STAR, label="Avaliados"),
            ft.NavigationDestination(icon=ft.icons.AUDIOTRACK, label="Recentes")
        ],
        on_change=on_change
    )

def criar_barra_de_titulo(username, email, ao_clicar_opcoes):
    return ft.AppBar(
        leading=ft.PopupMenuButton(
            icon=ft.icons.MENU,
            items=[
                ft.PopupMenuItem(text="Trocar Tema", on_click=lambda _: ao_clicar_opcoes("trocar_tema")),
                ft.PopupMenuItem(text="Minhas Musicas", on_click=lambda _: ao_clicar_opcoes("minhas_musicas")),
                ft.PopupMenuItem(text="Meus Artistas", on_click=lambda _: ao_clicar_opcoes("meus_artistas")),
                ft.PopupMenuItem(text="Meus Generos", on_click=lambda _: ao_clicar_opcoes("meus_generos")),
                ft.PopupMenuItem(text="Sair", on_click=lambda _: ao_clicar_opcoes("sair"))
            ],
        ),
        title=ft.Text("Listen", style="titleLarge"),
        actions=[
            ft.PopupMenuButton(
                icon=ft.icons.PERSON,
                items=[ft.PopupMenuItem(text=f"\nUser: {username} \nConta: {email}\n")]
            )
        ],
        center_title=True,
    )