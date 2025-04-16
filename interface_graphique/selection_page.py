#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 10:56:26 2025

@author: ouijdanejerid
"""

import flet as ft
import os
import shutil
from pathlib import Path
import json
from interactions.generator_fusion_images import LatentFusionPipeline


chemin_relatif = f"generate_images"
chemin_absolu = os.path.abspath(chemin_relatif)
IMAGE_DIR = chemin_absolu


def get_generated_images(DIR):
    """
    Recupere les images generees par l'auto-encodeur
    
    """
    all_images = [f for f in os.listdir(DIR) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    return all_images


def bordure_image(img_info):
    """
    Applique ou retire le style de bordure et de zoom selon l'état sélectionné.
    """
    if img_info["selected"]:
        img_info["control"].border = ft.border.all(3, "blue")
        img_info["control"].scale = 0.95
    else:
        img_info["control"].border = None
        img_info["control"].scale = 1

    img_info["control"].update()
    
    
    
def update_selection_list(img_info, selected_names, barre_miniatures, page):
    """
    Ajoute ou retire l'image de la sélection et met à jour la barre de miniatures.
    """
    img_name = img_info["img_name"]

    if img_info["selected"]:
        if img_name not in selected_names:
            selected_names.append(img_name)
            thumb = ft.Image(
                src=os.path.join(IMAGE_DIR, img_name),
                width=40,
                height=40,
                fit=ft.ImageFit.COVER,
                key=img_name
            )
            barre_miniatures.controls.append(thumb)
    else:
        if img_name in selected_names:
            selected_names.remove(img_name)
            barre_miniatures.controls = [
                t for t in barre_miniatures.controls if t.key != img_name
            ]

    page.update()
    

def image_click_state(e, img_info, selected_names, barre_miniatures, page):
    """
    Gère le clic utilisateur : met à jour l'état sélectionné, l'apparence et les miniatures.
    """
    img_info["selected"] = not img_info["selected"]
    bordure_image(img_info)
    update_selection_list(img_info, selected_names, barre_miniatures, page)
    
    
    

def load_images(page,image_container,displayed_images,on_image_click, regenerate=False):
    """
    Parameters
    ----------
    page : objet Flet
         pour pouvoir rafraichir la page a chaque appel de la fonction
    image_container : liste
        DESCRIPTION.
    displayed_images : TYPE
        DESCRIPTION.
    toggle_selection : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    if regenerate :
        mutate()
    image_container.controls.clear()
    displayed_images.clear()
    
    #on affiche chaque image recuperee de generated_images
    images = get_generated_images(IMAGE_DIR)
    for img_name in images:
        img_path = os.path.join(IMAGE_DIR, img_name)
        
        #Transforme l'img en objet flet
        image_control = ft.Image(src=img_path,width=200,height=200,fit=ft.ImageFit.COVER)

        # Conteneur autour de l'image : applique une bordure quand l'image est selectionnée
        container = ft.Container(content=image_control,border=None,)
        
        img_info = {"img_name": img_name, "control": container, "selected": False}
        displayed_images.append(img_info)
        
        #contient le container rendu cliquable oar le GestureDetector
        gd = ft.GestureDetector(
                content=container,
                on_tap=lambda e, img_info=img_info: on_image_click(e, img_info))
        
        image_container.controls.append(gd)
   
    #raffaichit la page
    page.update()
    return img_info 


    
def save_selected_images(page, thumbnail_selected_images, e):
    """
    Sauvegarde les images selectionnees dans une fichier json, puis redirige le user vers la page du resulats de la mutation

    Parameters
    ----------
    page : TYPE
        DESCRIPTION.
    thumbnail_selected_images : liste de str
        coontient les images selectionnees par le user 
    e : objet flet.ControlEvent
        Evenmt declenche lors du clic sur le bouton mutate

    Returns
    -------
    None.

    """
    if not thumbnail_selected_images:
        page.update()
        return
    
    with open("images_selected.json", "w", encoding="utf-8") as fichier_json:
        json.dump({"selected_image": thumbnail_selected_images}, fichier_json, ensure_ascii=False, indent=4)
    
    page.go("/selected")
    
def show_panel(thumbnail_panel, page):
    """
    affiche ou masque le panneau de miniatures 
    inverse l'état de visibilité du composant `thumbnail_panel`
    
    Returns
    -------
    None
    """
    thumbnail_panel.visible = not thumbnail_panel.visible
    page.update()
    
    
def clear_thumbnail(e, selected_names, barre_miniatures, page):
    """
    Vide la sélection actuelle : noms sélectionnés + barre visuelle.
    """
    selected_names.clear()  # vide la liste des noms sélectionnés
    barre_miniatures.controls.clear()  # vide les miniatures affichées
    page.update()
        
    
def mutate():
    pipeline = LatentFusionPipeline(n_outputs=6)
    pipeline.run()
    #print("Images après mutation :", os.listdir(IMAGE_DIR))
    
    
def handle_single_download(image_name, page):
    src = Path(IMAGE_DIR) / image_name
    dst_dir = Path("downloads")
    dst_dir.mkdir(exist_ok=True)
    dst = dst_dir / image_name

    if not src.exists():
        page.snack_bar = ft.SnackBar(ft.Text("Image not found."))
        page.snack_bar.open = True
        page.update()
        return

    shutil.copy2(src, dst)
    page.launch_url(f"file://{dst.resolve()}")


    
def afficher_message(text_widget, message, page, color=ft.colors.RED):
    text_widget.value = message
    text_widget.color = color
    text_widget.visible = True
    page.update()

def close_dialog(page):
    page.dialog.open = False
    page.update()
    
def handle_mutate_click(page, selected_names, image_container, displayed_images, barre_miniatures, message_text):
    if len(selected_names) >= 1:
        load_images(
            page,
            image_container,
            displayed_images,
            lambda e, img_info: image_click_state(e, img_info, selected_names, barre_miniatures, page),
            regenerate=True
        )
    else:
        afficher_message(message_text, "Mutation Error : Select images to mutate.", page)

def handle_download_click(page, selected_names,message_text):
    if len(selected_names) == 1:
        handle_single_download(selected_names[0], page)
    else:
        afficher_message(message_text, "Download Error: Please select exactly one image to download.",page)
    
def reset_message(text_widget, page):
    text_widget.value = ""
    text_widget.visible = False
    page.update()
    
    
def select_view(page: ft.Page):
    font_family = "Times New Roman"

    displayed_images = []
    selected_names = []
    barre_miniatures = ft.Column(wrap=True, spacing=5) #wrap = True => 
    image_container = ft.Row(wrap=True, alignment="center", spacing=10)
    
    
    load_images(page,
                image_container,
                displayed_images,
                lambda e, img_info: image_click_state(e, img_info, selected_names, barre_miniatures, page),
                regenerate=False)
    
    
    
    title = ft.Text(
        "Select one ore more portraits to mutate",
        size=22,
        weight=ft.FontWeight.BOLD,
        font_family=font_family
    )
    
    barre_miniatures_container = ft.Container(
        content=barre_miniatures,visible=False,width=200,height=200,
        padding=10,bgcolor=ft.colors.WHITE,alignment=ft.alignment.top_left)
    
    #bouton qui permet d'afficher ou masquer la barre des miniatures
    barre_button = ft.IconButton(icon=ft.icons.IMAGE,on_click=lambda e: show_panel(barre_miniatures_container, page))

    # Bouton pour vider la sélection
    clear_button = ft.IconButton(icon=ft.icons.DELETE,tooltip="Clear selected",on_click=lambda e: clear_thumbnail(e, selected_names, barre_miniatures, page))

    # Texte d'information / erreur
    message_text = ft.Text("", color=ft.colors.RED, size=16, visible=False)
    button_row = ft.Row(
    [
        ft.FilledButton("Go Back", on_click=lambda e: page.go("/filters")),
        ft.FilledButton(
            "Mutate",
            reset_message(message_text, page),
            on_click=lambda e: handle_mutate_click(
                page, selected_names, image_container, displayed_images, barre_miniatures, message_text
            )
        ),
        ft.FilledButton(
            "Download",
            reset_message(message_text, page),
            on_click=lambda e: handle_download_click(page, selected_names, message_text)
        )
    ],
    alignment="center",
    spacing=20
)

    layout = ft.Column(
        [
            ft.Container(title, alignment=ft.alignment.center, padding=20),
            message_text,  # ← Message visible ici
            image_container,
            ft.Container(button_row, alignment=ft.alignment.center, padding=20)
        ],
        horizontal_alignment="center",
        spacing=20
    )



    
    # Positionner en haut a droite
    page.overlay.append(barre_miniatures_container)
    page.overlay.append(barre_button)
    page.overlay.append(clear_button)
    barre_button.top = 20
    barre_button.right = 20
    barre_miniatures_container.top = 60
    barre_miniatures_container.right = 20
    clear_button.top = 20
    clear_button.right = 60 
    

    return ft.View(route="/select", controls=[layout], scroll="auto", bgcolor="white")

