import flet as ft
import json
from interactions.generator_images import ImageGenerator


def confirm_choices(e, page, dropdowns):
    """
    -Enregistre les filtres choisis par l'utilisateur dans un fichier json
    -Genere les images correspondante par l'autoencodeur
    -renvoie vers la page suivante

    Parameters
    ----------
    e : ft.ControlEvent
        Traduit le clic de l'utilisateur sur un bouton'
    page : ft.page

    dropdowns : dict
        {nom_du_filtre: objet_dropdown(contient les differentes versions de l'attribut)}

    Returns
    -------
    None.

    """
    filters_dict = {
        key: dropdown.value if dropdown.value is not None else "Unknown"
        for key, dropdown in dropdowns.items()
    }

    with open("interface_graphique/filtres.json", "w", encoding="utf-8") as fichier_json:
        json.dump(filters_dict, fichier_json, ensure_ascii=False, indent=4)

    # Génération des images filtrees
    generator = ImageGenerator()
    generator.generate_all()
    page.go("/select")
    
    
    
def filters_view(page: ft.Page):
    """
    Affiche la page de sélection des attributs qui vont servir a filtrer les images proposees a l'utilisateur
    Appelle la fonction callback 'confirm_choices' qui est en lien avec l'auto-encodeur au moment de confirmation des choix de l'utilisateur

    """
    
    #choix de la police d'ecriture
    font_family = "Times New Roman"

    #titre 
    title = ft.Text("Build profil", size=28, weight=ft.FontWeight.BOLD, text_align="center", font_family=font_family)


    # Liste des attributs binaires
    binary_attributes = [
        "Sideburns", "Bangs", "No_Beard", "Wearing_Necktie", "Big_Lips",
        "Wearing_Lipstick", "Straight_Hair", "Chubby", "Big_Nose", "Pointy_Nose",
        "Goatee", "Male", "Receding_Hairline", "Wearing_Necklace", "Eyeglasses",
        "Wavy_Hair", "Wearing_Earrings", "Young"
    ]
    
    # Attribut non binaire
    non_binary_attributes = {"Hair_Color": ["Black", "Brown", "Blond", "Unknown"]}
    
    # Options pour les attributs binaires

    binary_options = [
        ft.dropdown.Option("Yes"),
        ft.dropdown.Option("No"),
        ft.dropdown.Option("Unknown")
    ]

    
    # Creation des dropdowns
    dropdowns = {}
    for attr in binary_attributes:
        dropdowns[attr] = ft.Dropdown(
            label=attr.replace("_", " "),
            hint_text="choose",
            options=binary_options,
            width=200
        )
    dropdowns["Hair_Color"] = ft.Dropdown(
                                label="Hair Color",
                                hint_text="choose",
                                options=[ft.dropdown.Option(opt) for opt in non_binary_attributes["Hair_Color"]],
                                width=200
                            )
        
    # Séparer les dropdowns en trois colonnes

    col_left = ft.Column([
        dropdowns["Hair_Color"],
        dropdowns["Sideburns"],
        dropdowns["Bangs"],
        dropdowns["No_Beard"],
        dropdowns["Wearing_Necktie"],
        dropdowns["Big_Lips"],
        dropdowns["Wearing_Lipstick"],
    ], spacing=15)
    
    col_center = ft.Column([
        dropdowns["Straight_Hair"],
        dropdowns["Chubby"],
        dropdowns["Big_Nose"],
        dropdowns["Pointy_Nose"],
        dropdowns["Goatee"],
        dropdowns["Male"],
    ], spacing=15)
    
    col_right = ft.Column([
        dropdowns["Receding_Hairline"],
        dropdowns["Wearing_Necklace"],
        dropdowns["Eyeglasses"],
        dropdowns["Wavy_Hair"],
        dropdowns["Wearing_Earrings"],
        dropdowns["Young"],
    ], spacing=15)


    #Boutons "go back" et "confirm choices"

    button_row = ft.Row([
        ft.FilledButton("Go Back", on_click=lambda e: page.go("/")),
        ft.FilledButton("Confirm choices", on_click=lambda e: confirm_choices(e, page, dropdowns))
        ], alignment="center", spacing=20)


    # layout final
    layout = ft.Column([
        title,
        ft.Row([col_left,col_center, col_right], alignment="center", spacing=60),
        ft.Container(button_row, alignment=ft.alignment.center, padding=20)
    ], horizontal_alignment="center", spacing=20)

    
    return ft.View(route="/filters", controls=[layout], scroll="auto", bgcolor="white")
