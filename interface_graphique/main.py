#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 00:54:43 2025

@author: ouijdanejerid
"""
from .page_acceuil import accueil_view
from .filters_page import filters_view
from .selection_page import select_view
import flet as ft


def main(page: ft.Page):
    page.title = "FaceGen"
    
    def route_change(e):
        if page.route == "/":
            page.views.append(accueil_view(page))
        elif page.route == "/filters":
            page.views.append(filters_view(page))
        elif page.route == "/select":
            page.views.append(select_view(page))
        page.update()

    page.on_route_change = route_change

    page.go("/")


if __name__ == "__main__":

    ft.app(target=main)

