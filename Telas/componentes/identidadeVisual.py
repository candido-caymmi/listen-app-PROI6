import flet as ft

GRADIENTE = ft.LinearGradient(
    colors=["#150c14", "#150c14"],
    begin=ft.Alignment(-1, -1),
    end=ft.Alignment(1, 1)
)

COR_PRIMARIA = '#C73EAF'
COR_TEXTO_CLARO = ft.colors.WHITE
COR_TEXTO_ESCURO = ft.colors.BLACK

ESTILO_BOTAO_PRIMARIO = ft.ButtonStyle(
    color=COR_TEXTO_CLARO,
    bgcolor=COR_PRIMARIA,
    shape=ft.RoundedRectangleBorder(radius=5),
)

ESTILO_BOTAO_SECUNDARIO = ft.ButtonStyle(
    color=COR_PRIMARIA,
    shape=ft.RoundedRectangleBorder(radius=5),
)

LOGO_CAMINHO = "Telas/Imagens/logo.png"

#dicionario
ALINHAMENTO_COLUNA = {
    "alignment": ft.MainAxisAlignment.CENTER,
    "horizontal_alignment": ft.CrossAxisAlignment.CENTER,
    "spacing": 20
}
#dicionario
ALINHAMENTO_LINHA = {
    "alignment": ft.MainAxisAlignment.CENTER,
    "vertical_alignment": ft.CrossAxisAlignment.CENTER
}

def exibir_logo(page_width: int):
    print(page_width)
    if page_width > 1200:
        width, height = 300, 300
    elif 800 < page_width <= 1200:
        width, height = 200, 200
    else:
        width, height = 150, 150
     
    return ft.Image(
        src=LOGO_CAMINHO,
        width=width,
        height=height
    )