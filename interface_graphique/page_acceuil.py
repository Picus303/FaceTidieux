import flet as ft
import os
from .tuto_page import open_tutorial



def accueil_view(page):
    """
    Cree et affiche la page d'accueil du logiciel
    
    Objts flet utilises :
	-	ft.Row : pour aligner plusieurs elts cote a cote horizontalement 
	-	ft.Column : pour aligner plusieurs elts verticalement
	-	ft.Container : pour positionner les elts avec plusieurs attribut pour ameliorer le design
	-	ft.Text : pour afficher du texte
	-	ft.ElevatedButton : Bouton avec une ombre pour le mettre en évidence
	-	ft.Stack : pour superposer plusieurs images les unes au-dessus des autres
	-	ft.Divider : une ligne de separation 
	-	ft.View : represente la page complete
  
    """
    
    # Choix de la police d'ecriture
    font_family = "Times New Roman"
    
    # TITRE et SOUS-TITRE
    title = ft.Text("Welcome to FaceGen !", size=30, weight=ft.FontWeight.BOLD, text_align="center", color="black", font_family=font_family)
    subtitle = ft.Text("An interactive tool to explore, combine and evolve human faces", size=16, text_align="center", color="black", font_family=font_family)

    # Option pour afficher le tutoriel
    tutoriel = ft.Row([
        ft.TextButton(
            content=ft.Text("Tutorial", font_family=font_family, size=14, weight=ft.FontWeight.BOLD),
            on_click=open_tutorial
            )
        ], alignment="start")


    
    # Description globale du fonctionnement du logiciel
    description = ft.Column([
    ft.Text("• Start by applying filters (optional) to narrow down the portraits.", italic=True, color="black", font_family=font_family, size=15),
    ft.Text("• Then select one or more portraits from the filtered results.", italic=True, color="black", font_family=font_family, size=15),
    ft.Text("• With a single portrait, generate multiple variations through mutation.", italic=True, color="black", font_family=font_family, size=15),
    ft.Text("• With multiple portraits, combine them to evolve new faces.", italic=True, color="black", font_family=font_family, size=15),
    ], spacing=5, alignment="start")


    # Ajout du bouton start qui renvoie vers la page du choix des filtres
    start_btn = ft.ElevatedButton(
    content=ft.Text("Start →", font_family="Times New Roman", size=16, weight=ft.FontWeight.BOLD),
    style=ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=30),
        padding=20,
        bgcolor="white",
        side=ft.BorderSide(2, "black"),
        color="black"),
        on_click=lambda e: page.go("/filters")
        )

    
    #Ajout des images d'accueil
    # Récupération des chemins absolus pour accéder aux images 
    liste_chemins_absolus = []
    for i in range(3):
        chemin_relatif = f"interface_graphique/im{i+1}.png"
        chemin_absolu = os.path.abspath(chemin_relatif)
        liste_chemins_absolus.append(chemin_absolu)
        
    img_stack = ft.Stack([
        ft.Image(src=liste_chemins_absolus[2], width=510, top=10, left=25 ,bottom = 3),
        ft.Image(src=liste_chemins_absolus[0], width=500, top=3, left=15,bottom = 50),
        ft.Image(src=liste_chemins_absolus[1],  width=480, top=11, left=10, bottom =0),
                ], width=470, height=290)

    
    # Organisation de l'affichege du texte et des images
    content = ft.Row([
        ft.Column([description,
                   ft.Container(start_btn, padding=20)
                   ], expand=1, alignment="start", spacing=30),
        img_stack], alignment="center", spacing=0)

    # Layout final
    page.add(
    tutoriel,
    ft.Container(title, alignment=ft.alignment.center, padding=0),
    ft.Container(subtitle, alignment=ft.alignment.center, padding=5),
    ft.Divider(thickness=1),
    ft.Container(content, padding=ft.padding.only(top=20)))
    controls=[tutoriel,
            ft.Container(title, alignment=ft.alignment.center, padding=0),
            ft.Container(subtitle, alignment=ft.alignment.center, padding=5),
            ft.Divider(thickness=1),
            ft.Container(content, padding=ft.padding.only(top=20))]

    
    return ft.View( route="/",controls = controls ,scroll="auto",padding=15,bgcolor="white")
