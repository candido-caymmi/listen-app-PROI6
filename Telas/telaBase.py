import flet as ft

class TelaBase:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.window_width = 400
        self.page.window_height = 800
        self.page.window_resizable = False 
        self.theme_mode = ft.ThemeMode.DARK
    
    def mostrar(self):
        raise NotImplementedError("A subclasse deve implementar este método")
