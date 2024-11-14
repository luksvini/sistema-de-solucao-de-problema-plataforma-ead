import flet as ft
import json
import difflib

# Função para carregar a base de conhecimento
def carregar_conhecimento():
    try:
        with open("conhecimento.json", "r",  encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
         print("Arquivo conhecimento.json não encontrado!")
         return []
    
    
    # Função para buscar a solução na base de conhecimento
def buscar_solucao(problema_descrito, base_de_conhecimento):
    problemas = [item["problema"] for item in base_de_conhecimento]
    # Usando difflib para encontrar item mais próximo
    correspondencia = difflib.get_close_matches(problema_descrito, problemas, n=1, cutoff=0.5)

    if correspondencia:
        problema_encontrado = correspondencia[0]
        for item in base_de_conhecimento:
            if item["problema"] == problema_encontrado:
                return item["solucao"]
    return "Solução não encontrada. Tente descrever o problema de outra forma."


   

# Interface web com o Flet

def main(page: ft.Page):
    page.title = "Sistema de Suporte Técnico"
    
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 20
    page.bgcolor = "#f3f4f6"  
    
    # Carregar a base de conhecimento 
    base_de_conhecimento = carregar_conhecimento()

    
    # Título estilizado
    titulo = ft.Text(
        "PLATAFORMA DE ENSINO EAD - SUPORTE TÉCNICO",
        size=30,
        weight="bold",
        color="#1e3a8a",  
    )
   
    # Caixa de entrada do problema
    problema_input = ft.TextField(
        label=None,
        width=500,
        filled=True,
        border_radius=8,
        autofocus=True,
        bgcolor="black",
        hint_text="Digite o problema aqui...",
        prefix_icon=ft.icons.HELP_OUTLINE,
    )

    
    # Área para exibir a solução
    solucao_card = ft.Card(
        content=ft.Container(
            content=ft.Text(
                value="",
                size=16,
                color="black",
                selectable=True  # Permitir que o usuário selecione o texto para copiar
            ),
            bgcolor="white",
            border_radius=10,
            padding=20,
            width=500,
        ),
        elevation=2
    )
    solucao_text = solucao_card.content.content
    
    # Função que será chamada ao clicar no botão "Buscar"
    def buscar_click(e):
        problema_descrito = problema_input.value
        if problema_descrito.strip():
            solucao = buscar_solucao(problema_descrito, base_de_conhecimento)
            solucao_text.value = solucao
        else:
            solucao_text.value = "Por favor, insira um problema para buscar uma solução."
        page.update()
    
    # Botão de busca 
    buscar_button = ft.ElevatedButton(
        text="Buscar Solução",
        icon=ft.icons.SEARCH,
        bgcolor="#1e3a8a",
        color="white",
        on_click=buscar_click,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
    )
    
    # Colocar os elementos em um layout 
    page.add(
        ft.Column(
            [
                titulo,
                problema_input,
                buscar_button,
                ft.Text("Solução:", size=18, weight="bold", color="#1e3a8a"),
                solucao_card
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    )
if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)