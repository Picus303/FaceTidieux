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
from .options_page import *
from .mutation_page import *
import flet as ft


async def main(page: ft.Page):
    page.title = "FaceGen"
    page.scroll = "auto"
    page.window_width = 1200
    page.window_height = 800
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    # Routeur
    def route_change(e):
        page.views.clear()
        if page.route == "/":
            page.views.append(accueil_view(page))
        elif page.route == "/filters":
            page.views.append(filters_view(page))
        elif page.route == "/select":
            page.views.clear()
            page.views.append(select_portraits_view(page))
        elif page.route == "/selected":
            page.views.append(selected_result_view(page))
        elif page.route == "/mutate":
            page.views.append(mutated_selection_view(page))

        else:
            page.views.append(ft.View(page.route, controls=[ft.Text("Page not found")]))
        page.update()

    page.on_route_change = route_change
    page.go("/")  # Commencer par la page d’accueil

#import asyncio
#asyncio.run(ft.app_async(target=main))
