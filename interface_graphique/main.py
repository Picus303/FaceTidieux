#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 00:54:43 2025

@author: ouijdanejerid
"""
from .page_acceuil import *
from .tuto_page import *
from .filters_page import *
from .selection_page import *
import flet as ft

def main(page: ft.Page):
    # Configuration de la fenêtre
    page.title = "FaceGen"
    page.window_maximized = True  
    page.scroll = "auto"
    page.padding = 0

    # Gestion de la navigation
    def route_change(e):
        page.views.clear()
        if page.route == "/":
            page.views.append(accueil_view(page))
        elif page.route == "/filters":
            page.views.append(filters_view(page))
        elif page.route == "/select":
            page.views.append(select_view(page))
        else:
            page.views.append(ft.View(page.route, controls=[ft.Text("Page not found")]))
        page.update()

    page.on_route_change = route_change
    page.go("/")

if __name__ == "__main__":
    ft.app(target=main, view=ft.FLET_APP)