#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 25 22:37:40 2025

@author: ouijdanejerid
"""

import flet as ft
import asyncio

async def tutorial_window(page: ft.Page):
    page.title = "Tutorial"
    page.window_width = 500
    page.window_height = 420
    page.bgcolor = "white"
    page.scroll = "auto"

    page.add(
        ft.Text("How to use FaceGen", size=24, weight=ft.FontWeight.BOLD, color = 'Black'),
        

    )
    
async def open_tutorial(e):
    await ft.app_async(target=tutorial_window)