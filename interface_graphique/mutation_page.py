import os
import shutil
import flet as ft
from interactions.generator_fusion_images import LatentFusionPipeline
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GENERATED_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "generate_images"))

displayed_images = []

def get_next_mutation_folder(base="mutated_images"):
    i = 1
    while True:
        folder_name = os.path.join(os.path.dirname(GENERATED_DIR), f"{base}{i}")
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            return folder_name
        i += 1

def regenerate_and_store_mutation():
    pipeline = LatentFusionPipeline(n_outputs=6)
    pipeline.run()


def mutated_selection_view(page: ft.Page):
    #global current_mutation_dir
    image_container = ft.Row(wrap=True, alignment="center", spacing=10)

    dropdown_visible = False
    selected_file = ft.Dropdown(label="Choose an image", options=[], width=250)
    download_button = ft.ElevatedButton("Download", disabled=True)

    def load_mutated_images(dir_path):
        image_container.controls.clear()
        displayed_images.clear()
        selected_file.options.clear()
        download_button.disabled = True

        all_images = [
            f for f in os.listdir(dir_path)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]

        for img_name in all_images:
            abs_path = os.path.abspath(os.path.join(dir_path, img_name))

            image_control = ft.Image(
                src=abs_path,
                width=140,
                height=140,
                fit=ft.ImageFit.COVER
            )

            container = ft.Container(
                content=image_control,
                width=150,
                height=150,
                padding=5,
                alignment=ft.alignment.center,
                border_radius=12,
            )

            displayed_images.append({
                "img_name": img_name,
                "path": abs_path,
                "control": container
            })

            image_container.controls.append(container)
            selected_file.options.append(ft.dropdown.Option(img_name))

        page.update()

    def on_mutate_again(e):
        regenerate_and_store_mutation()
        current_mutation_dir = Path(__file__).parent / ".." / "generate_images"
        load_mutated_images(current_mutation_dir)

    def on_go_back(e):
        page.go("/select")

    def show_dropdown(e):
        dropdown_row.visible = True
        page.update()

    def on_dropdown_change(e):
        download_button.disabled = selected_file.value is None
        page.update()

    def on_download(e):
        img = next((img for img in displayed_images if img["img_name"] == selected_file.value), None)
        if img:
            page.launch_url(f"file://{img['path']}")

    regenerate_and_store_mutation()
    current_mutation_dir = Path(__file__).parent / ".." / "generate_images"
    load_mutated_images(current_mutation_dir)




# --- Dropdown + download section ---
    selected_file = ft.Dropdown(label="Choose an image", options=[], width=250)
    selected_file.on_change = on_dropdown_change  # Tu dois avoir cette fonction définie
    
    download_button = ft.FilledButton("Download", on_click=on_download)
    
    dropdown_row = ft.Row(
        [selected_file, download_button],
        alignment="center",
        spacing=10,
        visible=False
    )
    
    # --- Boutons ---
    mutate_button = ft.TextButton(
        "Mutate Again",
        on_click=on_mutate_again,
        style=ft.ButtonStyle(
            padding=20,
            bgcolor="green",
            color="white",
            shape=ft.RoundedRectangleBorder(radius=12),
            text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)
        )
    )
    
    toggle_dropdown_button = ft.TextButton(
        "Select one portrait to download",
        on_click=lambda e: toggle_dropdown(),
        style=ft.ButtonStyle(
            padding=20,
            bgcolor="green",
            color="white",
            shape=ft.RoundedRectangleBorder(radius=12),
            text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)
        )
    )
    
    go_back_button = ft.FilledButton("Go Back", on_click=on_go_back)
    
    # --- Fonction pour afficher la dropdown_row ---
    def toggle_dropdown():
        dropdown_row.visible = not dropdown_row.visible
        page.update()
    
    # --- Layout final ---
    layout = ft.Column(
        [
            ft.Text(
                "Here are your mutated portraits",
                size=26,
                font_family="Times New Roman",
                weight=ft.FontWeight.BOLD,
                color="black",
                text_align=ft.TextAlign.CENTER
            ),
            image_container,
            ft.Row([mutate_button], alignment="center"),
            ft.Row([toggle_dropdown_button], alignment="center"),
            dropdown_row,  # ← visible uniquement après clic
            ft.Container(go_back_button, alignment=ft.alignment.bottom_left, padding=10)
        ],
        spacing=25,
        horizontal_alignment="center"
    )
    
    return ft.View(route="/mutate", controls=[layout], scroll="auto", bgcolor="white")