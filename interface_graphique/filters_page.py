
import flet as ft
import json

from interactions.generator_images import ImageGenerator


def filters_view(page: ft.Page):
    font_family = "Times New Roman"

    # -- Titre 
    title = ft.Text("Build profil", size=28, weight=ft.FontWeight.BOLD, text_align="center", font_family=font_family)


# -- Dropdowns compatibles avec l'autoencodeur
    binary_options = [
        ft.dropdown.Option("Yes"),
        ft.dropdown.Option("No"),
        ft.dropdown.Option("Unknown")
    ]

    hair_color_dropdown = ft.Dropdown(
        label="Hair Color",
        hint_text="choose",
        options=[
            ft.dropdown.Option("Black"),
            ft.dropdown.Option("Brown"),
            ft.dropdown.Option("Blond"),
            ft.dropdown.Option("Unknown")
        ],
        width=250
    )

    sideburns_dropdown = ft.Dropdown(label="Sideburns", hint_text="choose", options=binary_options, width=250)
    bangs_dropdown = ft.Dropdown(label="Bangs", hint_text="choose", options=binary_options, width=250)
    no_beard_dropdown = ft.Dropdown(label="No Beard", hint_text="choose", options=binary_options, width=250)
    wearing_necktie_dropdown = ft.Dropdown(label="Wearing Necktie", hint_text="choose", options=binary_options, width=250)
    big_lips_dropdown = ft.Dropdown(label="Big Lips", hint_text="choose", options=binary_options, width=250)
    wearing_lipstick_dropdown = ft.Dropdown(label="Wearing Lipstick", hint_text="choose", options=binary_options, width=250)
    straight_hair_dropdown = ft.Dropdown(label="Straight Hair", hint_text="choose", options=binary_options, width=250)
    chubby_dropdown = ft.Dropdown(label="Chubby", hint_text="choose", options=binary_options, width=250)
    big_nose_dropdown = ft.Dropdown(label="Big Nose", hint_text="choose", options=binary_options, width=250)
    pointy_nose_dropdown = ft.Dropdown(label="Pointy Nose", hint_text="choose", options=binary_options, width=250)
    goatee_dropdown = ft.Dropdown(label="Goatee", hint_text="choose", options=binary_options, width=250)
    male_dropdown = ft.Dropdown(label="Male", hint_text="choose", options=binary_options, width=250)
    receding_hairline_dropdown = ft.Dropdown(label="Receding Hairline", hint_text="choose", options=binary_options, width=250)
    wearing_necklace_dropdown = ft.Dropdown(label="Wearing Necklace", hint_text="choose", options=binary_options, width=250)
    eyeglasses_dropdown = ft.Dropdown(label="Eyeglasses", hint_text="choose", options=binary_options, width=250)
    wavy_hair_dropdown = ft.Dropdown(label="Wavy Hair", hint_text="choose", options=binary_options, width=250)
    wearing_earrings_dropdown = ft.Dropdown(label="Wearing Earrings", hint_text="choose", options=binary_options, width=250)
    young_dropdown = ft.Dropdown(label="Young", hint_text="choose", options=binary_options, width=250)

    # -- Fonction appelée quand l'utilisateur clique sur "Confirm choices"
    def confirm_choices(e):
        dropdowns = {
            "Hair_Color": hair_color_dropdown,
            "Sideburns": sideburns_dropdown,
            "Bangs": bangs_dropdown,
            "No_Beard": no_beard_dropdown,
            "Wearing_Necktie": wearing_necktie_dropdown,
            "Big_Lips": big_lips_dropdown,
            "Wearing_Lipstick": wearing_lipstick_dropdown,
            "Straight_Hair": straight_hair_dropdown,
            "Chubby": chubby_dropdown,
            "Big_Nose": big_nose_dropdown,
            "Pointy_Nose": pointy_nose_dropdown,
            "Goatee": goatee_dropdown,
            "Male": male_dropdown,
            "Receding_Hairline": receding_hairline_dropdown,
            "Wearing_Necklace": wearing_necklace_dropdown,
            "Eyeglasses": eyeglasses_dropdown,
            "Wavy_Hair": wavy_hair_dropdown,
            "Wearing_Earrings": wearing_earrings_dropdown,
            "Young": young_dropdown
        }
        
        filters_dict = {
            key: dropdown.value if dropdown.value is not None else "Unknown"
            for key, dropdown in dropdowns.items()
        }
        with open("interface_graphique/filtres.json", "w", encoding="utf-8") as fichier_json:
            json.dump(filters_dict, fichier_json, ensure_ascii=False, indent=4)
        generator = ImageGenerator()
        generator.generate_all()
        page.go("/select")


    # -- Colonnes (à répartir comme tu préfères)
    col_left = ft.Column([
        hair_color_dropdown,
        sideburns_dropdown,
        bangs_dropdown,
        no_beard_dropdown,
        wearing_necktie_dropdown,
        big_lips_dropdown,
        wearing_lipstick_dropdown
    ], spacing=15)

    col_center = ft.Column([
        straight_hair_dropdown,
        chubby_dropdown,
        big_nose_dropdown,
        pointy_nose_dropdown,
        goatee_dropdown,
        male_dropdown
    ], spacing=15)

    col_right = ft.Column([
        receding_hairline_dropdown,
        wearing_necklace_dropdown,
        eyeglasses_dropdown,
        wavy_hair_dropdown,
        wearing_earrings_dropdown,
        young_dropdown
    ], spacing=15)


    # -- Boutons
    button_row = ft.Row([
        ft.FilledButton("Go Back", on_click=lambda e: page.go("/")),
        ft.FilledButton("Confirm choices", on_click=confirm_choices)
    ], alignment="center", spacing=20)

    # -- Mise en page finale
    layout = ft.Column([
        title,
        ft.Row([col_left,col_center, col_right], alignment="center", spacing=60),
        ft.Container(button_row, alignment=ft.alignment.center, padding=20)
    ], horizontal_alignment="center", spacing=20)

    return ft.View(route="/filters", controls=[layout], scroll="auto", bgcolor="white")
