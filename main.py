import flet as ft
import math
import asyncio
import aiohttp

pokemon_actual = 0
total_pokemon = 1017

async def main(page: ft.Page):
    page.title = 'Pokedex'

    page.window_width = 540
    page.window_height = 960
    page.window_resizable = False
    page.padding = 0
    page.fonts = {
        'zpix': 'https://github.com/SolidZORO/zpix-pixel-font/releases/download/v3.1.8/zpix.ttf'
    }
    page.theme = ft.Theme(font_family='zpix')

    # Eventos

    async def peticion(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None


    async def getPokemon(e: ft.ContainerTapEvent):
        global pokemon_actual
        global total_pokemon

        if e.control == flecha_superior:
            pokemon_actual += 1
        elif e.control == search_pokemon.content:
            search_pokemon.open = False
            pokemon_actual = int(search_pokemon.content.value) - 1
        else:
            pokemon_actual -= 1

        numero = (pokemon_actual % total_pokemon) + 1
        resultado = await peticion(f'https://pokeapi.co/api/v2/pokemon/{numero}')

        datos = f"ID: {numero}\nName: {resultado['name'].capitalize()}\n\nAbilities:"
        for Elemento in resultado['abilities']:
            habilidad = Elemento['ability']['name']
            datos += f"\n{habilidad.capitalize()}"
        if len(resultado['abilities']) == 2:
            datos += "\n"
        elif len(resultado['abilities']) == 1:
            datos += "\n\n"
        elif len(resultado['abilities']) == 0:
            datos += "\n\n\n"
            
        datos += f"\n\nHeight: {resultado['height']}\nWeight: {resultado['weight']}"
        texto.value = datos

        if numero < 1011:
            imagen.src = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{numero}.png"
        elif numero == 1013:
            imagen.src = "https://archives.bulbagarden.net/media/upload/9/98/HOME1013.png"
        else:
            imagen.src = resultado['sprites']['other']['official-artwork']['front_default']
        
        await page.update_async()

    search_pokemon = ft.AlertDialog(
        content=ft.TextField(
            label='Pokemon ID',  
            keyboard_type=ft.KeyboardType.NUMBER, 
            on_submit=getPokemon
            ),
        content_padding=ft.padding.all(15),
        title=ft.Text(value='Search Pokemon', size=20),
    )

    async def open_search(e):
        page.dialog = search_pokemon
        search_pokemon.open = True
        await page.update_async()
    
    async def Blink():
        while True:
            await asyncio.sleep(1)
            luz_azul.bgcolor = ft.colors.BLUE_200
            await page.update_async()
            await asyncio.sleep(0.1)
            luz_azul.bgcolor = ft.colors.BLUE
            await page.update_async()


    # Parte superior de la pokedex

    luz_azul = ft.Container(width=75, height=75, border_radius=50, bgcolor=ft.colors.BLUE, margin=ft.margin.all(5))
    boton_azul = ft.Stack([
        ft.Container(width=80, height=80, border_radius=50, bgcolor=ft.colors.WHITE),
        luz_azul,
    ])

    green_button = ft.Container(width=40, height=40, border_radius=50, bgcolor=ft.colors.GREEN, on_click=open_search)
    items_superior = [
        ft.Container(boton_azul, width=80, height=80),
        ft.Container(width=40, height=40, border_radius=50, bgcolor=ft.colors.RED_200),
        ft.Container(width=40, height=40, border_radius=50, bgcolor=ft.colors.YELLOW),
        green_button,
    ]

    superior = ft.Container(
        ft.Row(items_superior), 
        width=420,
        height=80,
        margin=ft.margin.only(top=40)
    )

    # Parte central de la pokedex

    sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png"
    imagen = ft.Image(
        src=sprite_url,
        scale=5,
        width=50,
        height=50,
        top=250/2, 
        left=370/2,
    )

    pantalla_central = ft.Stack([
        ft.Container(width=420, height=300, bgcolor=ft.colors.WHITE, border_radius=20),
        ft.Container(width=370, height=250, bgcolor=ft.colors.BLACK, margin=ft.margin.all(25)),
        imagen,
    ])

    centro = ft.Container(
        pantalla_central,
        width=420, 
        height=300, 
        margin=ft.margin.only(top=40),
        alignment=ft.alignment.center
    )

    # Parte inferior de la pokedex

    triangulo = ft.canvas.Canvas([
        ft.canvas.Path([
            ft.canvas.Path.MoveTo(25/2,0),
            ft.canvas.Path.LineTo(0,25),
            ft.canvas.Path.LineTo(25,25),
        ],
        paint=ft.Paint(
            style=ft.PaintingStyle.FILL,
            )
        )
    ],
    width=25,
    height=25,
    )

    flecha_superior = ft.Container(triangulo,width=25, height=25, on_click=getPokemon)
    items_flechas = ft.Row([
        ft.Container(width=15, height=25),
        ft.Container(triangulo, width=25, height=25, rotate=math.radians(270)),
        ft.Column([
            ft.Container(width=25, height=25),
            flecha_superior,
            ft.Container(width=25, height=25),
            ft.Container(triangulo, rotate=math.radians(180), width=25, height=25, on_click=getPokemon),
            ft.Container(width=25, height=25),
        ], spacing=0.5),
        ft.Container(triangulo, rotate=math.radians(90), width=25, height=25),
        ft.Container(width=15, height=25)
    ], spacing=0)

    texto = ft.Text(
        value="...",
        color=ft.colors.BLACK,
        size=12,
        )

    items_inferior = [
        ft.Container(width=20),
        ft.Container(texto, padding=10, width=250, height=200, bgcolor=ft.colors.GREEN, border_radius=25),
        ft.Container(width=10),
        ft.Container(items_flechas, width=106, height=127),
    ]

    inferior = ft.Container(
        content=ft.Row(items_inferior),
        width=420, 
        height=300, 
        margin=ft.margin.only(top=40), 
    )

    col = ft.Column(spacing=0, controls=[
        superior,
        centro,
        inferior
    ])

    

    container = ft.Container(col, width=540, height=960, bgcolor=ft.colors.RED, alignment=ft.alignment.top_center)

    await page.add_async(container)
    await Blink()
    
    

if __name__ == '__main__':
    ft.app(target=main)