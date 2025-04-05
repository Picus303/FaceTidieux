import flet as ft



import flet as ft

def filters_view(page):
    font_family = "Times New Roman"

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

    col_left = ft.Column([
        ft.Text("Gender", font_family=font_family, size=18),
        ft.Dropdown(hint_text="choose", options=[ft.dropdown.Option("Male"), ft.dropdown.Option("Female")], width=250),
        ft.Text("Hair color", font_family=font_family, size=18),
        ft.Dropdown(hint_text="choose", options=[ft.dropdown.Option("Blonde"), ft.dropdown.Option("Brown")], width=250),
        ft.Text("Teint de peau", font_family=font_family, size=18),
        ft.Dropdown(hint_text="choose", options=[ft.dropdown.Option("Clair"), ft.dropdown.Option("Foncé")], width=250),
    ], spacing=15)

    col_right = ft.Column([
        ft.Text("Eye color", font_family=font_family, size=18),
        ft.Dropdown(hint_text="choose", options=[ft.dropdown.Option("Blue"), ft.dropdown.Option("Brown")], width=250),
        ft.Text("Hair Length", font_family=font_family, size=18),
        ft.Dropdown(hint_text="choose", options=[ft.dropdown.Option("Short"), ft.dropdown.Option("Long")], width=250),
        ft.Text("Accessoire", font_family=font_family, size=18),
        ft.Dropdown(hint_text="choose", options=[ft.dropdown.Option("Glasses"), ft.dropdown.Option("Hat")], width=250),
    ], spacing=15)

    button_row = ft.Row([
        ft.FilledButton("Go Back", on_click=lambda e: page.go("/") ),
        ft.FilledButton("Confirm choices", on_click=lambda e: page.go("/next"))
    ], alignment="center", spacing=20)

    layout = ft.Column([
        title,
        subtitle,
        ft.Row([col_left, col_right], alignment="center", spacing=60),
        ft.Container(button_row, alignment=ft.alignment.center, padding=20)
    ], horizontal_alignment="center", spacing=20)

    return ft.View(route="/filters", controls=[layout], scroll="auto", bgcolor="white")



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
