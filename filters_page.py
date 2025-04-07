
import flet as ft
import json

def filters_view(page: ft.Page):
    font_family = "Times New Roman"

    # -- Titre et sous-titre
    title = ft.Text("Build profil", size=28, weight=ft.FontWeight.BOLD, text_align="center", font_family=font_family)
    subtitle = ft.Text(
        "You can ",
        spans=[
            ft.TextSpan(
                "Skip this Step",
                on_click=lambda e: page.go("/select"),
                style=ft.TextStyle(color="#1C8EBB", italic=True, decoration="underline")
            )
        ],
        text_align="center",
        size=16
    )

    # -- On crée une variable pour chaque Dropdown
    gender_dropdown = ft.Dropdown(
        label="Gender",
        hint_text="choose",
        options=[ft.dropdown.Option("Male"), ft.dropdown.Option("Female")],
        width=250
    )
    hair_color_dropdown = ft.Dropdown(
        label="Hair color",
        hint_text="choose",
        options=[ft.dropdown.Option("Blonde"), ft.dropdown.Option("Brown")],
        width=250
    )
    teint_peau_dropdown = ft.Dropdown(
        label="Teint de peau",
        hint_text="choose",
        options=[ft.dropdown.Option("Clair"), ft.dropdown.Option("Foncé")],
        width=250
    )

    eye_color_dropdown = ft.Dropdown(
        label="Eye color",
        hint_text="choose",
        options=[ft.dropdown.Option("Blue"), ft.dropdown.Option("Brown")],
        width=250
    )
    hair_length_dropdown = ft.Dropdown(
        label="Hair Length",
        hint_text="choose",
        options=[ft.dropdown.Option("Short"), ft.dropdown.Option("Long")],
        width=250
    )
    accessoire_dropdown = ft.Dropdown(
        label="Accessoire",
        hint_text="choose",
        options=[ft.dropdown.Option("Glasses"), ft.dropdown.Option("Hat")],
        width=250
    )

    # -- Fonction appelée quand l'utilisateur clique sur "Confirm choices"
    def confirm_choices(e):
        # 1. On lit les valeurs choisies par l'utilisateur
        filters_dict = {
            "Gender": gender_dropdown.value,
            "Hair color": hair_color_dropdown.value,
            "Teint de peau": teint_peau_dropdown.value,
            "Eye color": eye_color_dropdown.value,
            "Hair Length": hair_length_dropdown.value,
            "Accessoire": accessoire_dropdown.value
        }

        # 2. On enregistre le dictionnaire dans un fichier JSON
        with open("filtres.json", "w", encoding="utf-8") as fichier_json:
            json.dump(filters_dict, fichier_json, ensure_ascii=False, indent=4)

        # 3. On redirige vers la page suivante (ou on peut rester sur la même page, selon vos besoins)
        page.go("/next")

    # -- Colonnes de gauche et de droite
    col_left = ft.Column([
        gender_dropdown,
        hair_color_dropdown,
        teint_peau_dropdown,
    ], spacing=15)

    col_right = ft.Column([
        eye_color_dropdown,
        hair_length_dropdown,
        accessoire_dropdown,
    ], spacing=15)

    # -- Boutons "Go back" et "Confirm choices"
    button_row = ft.Row([
        ft.FilledButton("Go Back", on_click=lambda e: page.go("/")),
        ft.FilledButton("Confirm choices", on_click=confirm_choices)
    ], alignment="center", spacing=20)

    # -- Mise en page générale
    layout = ft.Column([
        title,
        subtitle,
        ft.Row([col_left, col_right], alignment="center", spacing=60),
        ft.Container(button_row, alignment=ft.alignment.center, padding=20)
    ], horizontal_alignment="center", spacing=20)

    return ft.View(route="/filters", controls=[layout], scroll="auto", bgcolor="white")



# import flet as ft

# def filters_view(page):
#     font_family = "Times New Roman"

#     title = ft.Text("Build profil", size=28, weight=ft.FontWeight.BOLD, text_align="center", font_family=font_family)
#     subtitle = ft.Text(
#         "You can ",
#         spans=[
#             ft.TextSpan(
#                 "Skip this Step",
#                 on_click=lambda e: page.go("/select"),
#                 style=ft.TextStyle(color="#1C8EBB", italic=True, decoration="underline")
#             )
#         ],
#         text_align="center",
#         size=16
#     )

#     col_left = ft.Column([
#         ft.Text("Gender", font_family=font_family, size=18),
#         ft.Dropdown(hint_text="choose", options=[ft.dropdown.Option("Male"), ft.dropdown.Option("Female")], width=250),
#         ft.Text("Hair color", font_family=font_family, size=18),
#         ft.Dropdown(hint_text="choose", options=[ft.dropdown.Option("Blonde"), ft.dropdown.Option("Brown")], width=250),
#         ft.Text("Teint de peau", font_family=font_family, size=18),
#         ft.Dropdown(hint_text="choose", options=[ft.dropdown.Option("Clair"), ft.dropdown.Option("Foncé")], width=250),
#     ], spacing=15)

#     col_right = ft.Column([
#         ft.Text("Eye color", font_family=font_family, size=18),
#         ft.Dropdown(hint_text="choose", options=[ft.dropdown.Option("Blue"), ft.dropdown.Option("Brown")], width=250),
#         ft.Text("Hair Length", font_family=font_family, size=18),
#         ft.Dropdown(hint_text="choose", options=[ft.dropdown.Option("Short"), ft.dropdown.Option("Long")], width=250),
#         ft.Text("Accessoire", font_family=font_family, size=18),
#         ft.Dropdown(hint_text="choose", options=[ft.dropdown.Option("Glasses"), ft.dropdown.Option("Hat")], width=250),
#     ], spacing=15)

#     button_row = ft.Row([
#         ft.FilledButton("Go Back", on_click=lambda e: page.go("/") ),
#         ft.FilledButton("Confirm choices", on_click=lambda e: page.go("/next"))
#     ], alignment="center", spacing=20)

#     layout = ft.Column([
#         title,
#         subtitle,
#         ft.Row([col_left, col_right], alignment="center", spacing=60),
#         ft.Container(button_row, alignment=ft.alignment.center, padding=20)
#     ], horizontal_alignment="center", spacing=20)

#     return ft.View(route="/filters", controls=[layout], scroll="auto", bgcolor="white")



# # def filters_view(page):
# #     font_family = "Times New Roman"

# #     title = ft.Text("Build profil", size=28, weight=ft.FontWeight.BOLD, text_align="center", font_family=font_family)
# #     subtitle = ft.Text(
# #         "You can ",
# #         spans=[
# #             ft.TextSpan(
# #                 "Skip this Step",
# #                 on_click=lambda e: page.go("/select"),
# #                 style=ft.TextStyle(color="#1C8EBB", italic=True, decoration="underline")
# #             )
# #         ],
# #         text_align="center",
# #         size=16
# #     )

# #     col_left = ft.Column([
# #         ft.Text("Gender", font_family=font_family, size=18),
# #         ft.Dropdown(hint_text="choose", options=[ft.dropdown.Option("Male"), ft.dropdown.Option("Female")], width=250),
# #         ft.Text("Hair color", font_family=font_family, size=18),
# #         ft.Dropdown(hint_text="choose", options=[ft.dropdown.Option("Blonde"), ft.dropdown.Option("Brown")], width=250),
# #         ft.Text("Teint de peau", font_family=font_family, size=18),
# #         ft.Dropdown(hint_text="choose", options=[ft.dropdown.Option("Clair"), ft.dropdown.Option("Foncé")], width=250),
# #     ], spacing=15)

# #     col_right = ft.Column([
# #         ft.Text("Eye color", font_family=font_family, size=18),
# #         ft.Dropdown(hint_text="choose", options=[ft.dropdown.Option("Blue"), ft.dropdown.Option("Brown")], width=250),
# #         ft.Text("Hair Length", font_family=font_family, size=18),
# #         ft.Dropdown(hint_text="choose", options=[ft.dropdown.Option("Short"), ft.dropdown.Option("Long")], width=250),
# #         ft.Text("Accessoire", font_family=font_family, size=18),
# #         ft.Dropdown(hint_text="choose", options=[ft.dropdown.Option("Glasses"), ft.dropdown.Option("Hat")], width=250),
# #     ], spacing=15)



#     # footer_links = ft.Column([
#     #     ft.Text(
#     #         spans=[
#     #             ft.TextSpan(
#     #                 "Confirm choices",
#     #                 on_click=lambda e: page.go("/next"),
#     #                 style=ft.TextStyle(
#     #                     color="#D17927",
#     #                     weight=ft.FontWeight.BOLD,
#     #                     size=20
#     #                 )
#     #             )
#     #         ]
#     #     ),
#     #     ft.Text(
#     #         spans=[
#     #             ft.TextSpan(
#     #                 "Go Back",
#     #                 on_click=lambda e: page.go("/accueil"),
#     #                 style=ft.TextStyle(
#     #                     color="#D17927",
#     #                     weight=ft.FontWeight.BOLD,
#     #                     size=20
#     #                 )
#     #             )
#     #         ]
#     #     )
#     # ], spacing=10, alignment="center")

#     # return ft.View(
#     #     route="/filters",
#     #     controls=[
#     #         ft.Column([
#     #             title,
#     #             subtitle,
#     #             ft.Row([col_left, col_right], alignment="center", spacing=60),
#     #             ft.Container(footer_links, alignment=ft.alignment.center, padding=20)
#     #         ], horizontal_alignment="center", spacing=30)
#     #     ],
#     #     padding=20,
#     #     bgcolor="white"
#     # )



# def filters_view(page):
#     font_family = "Times New Roman"

#     title = ft.Text("Build profil", size=28, weight=ft.FontWeight.BOLD, text_align="center", font_family=font_family)
#     subtitle = ft.Text(
#         "You can ",
#         spans=[
#             ft.TextSpan(
#                 "Skip this Step",
#                 on_click=lambda e: page.go("/select"),
#                 style=ft.TextStyle(color="#1C8EBB", italic=True, decoration="underline")
#             )
#         ],
#         text_align="center",
#         size=16
#     )

#     col_left = ft.Column([
#         ft.Text("Gender", font_family=font_family, size=18),
#         ft.Dropdown(hint_text="choose", options=[ft.dropdown.Option("Male"), ft.dropdown.Option("Female")], width=250),
#         ft.Text("Hair color", font_family=font_family, size=18),
#         ft.Dropdown(hint_text="choose", options=[ft.dropdown.Option("Blonde"), ft.dropdown.Option("Brown")], width=250),
#         ft.Text("Teint de peau", font_family=font_family, size=18),
#         ft.Dropdown(hint_text="choose", options=[ft.dropdown.Option("Clair"), ft.dropdown.Option("Foncé")], width=250),
#     ], spacing=15)

#     col_right = ft.Column([
#         ft.Text("Eye color", font_family=font_family, size=18),
#         ft.Dropdown(hint_text="choose", options=[ft.dropdown.Option("Blue"), ft.dropdown.Option("Brown")], width=250),
#         ft.Text("Hair Length", font_family=font_family, size=18),
#         ft.Dropdown(hint_text="choose", options=[ft.dropdown.Option("Short"), ft.dropdown.Option("Long")], width=250),
#         ft.Text("Accessoire", font_family=font_family, size=18),
#         ft.Dropdown(hint_text="choose", options=[ft.dropdown.Option("Glasses"), ft.dropdown.Option("Hat")], width=250),
#     ], spacing=15)



    # footer_links = ft.Column([
    #     ft.Text(
    #         spans=[
    #             ft.TextSpan(
    #                 "Confirm choices",
    #                 on_click=lambda e: page.go("/next"),
    #                 style=ft.TextStyle(
    #                     color="#D17927",
    #                     weight=ft.FontWeight.BOLD,
    #                     size=20
    #                 )
    #             )
    #         ]
    #     ),
    #     ft.Text(
    #         spans=[
    #             ft.TextSpan(
    #                 "Go Back",
    #                 on_click=lambda e: page.go("/accueil"),
    #                 style=ft.TextStyle(
    #                     color="#D17927",
    #                     weight=ft.FontWeight.BOLD,
    #                     size=20
    #                 )
    #             )
    #         ]
    #     )
    # ], spacing=10, alignment="center")

    # return ft.View(
    #     route="/filters",
    #     controls=[
    #         ft.Column([
    #             title,
    #             subtitle,
    #             ft.Row([col_left, col_right], alignment="center", spacing=60),
    #             ft.Container(footer_links, alignment=ft.alignment.center, padding=20)
    #         ], horizontal_alignment="center", spacing=30)
    #     ],
    #     padding=20,
    #     bgcolor="white"
    # )
