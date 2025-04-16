#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 25 22:37:40 2025

@author: ouijdanejerid
"""

import flet as ft

def tutorial_window(page: ft.Page):
    """
    This is the code responsible to the tutorial of FaceGen.
    The tutorial appears in a new window, independant from the main one.
    """
    page.title = "Tutorial"
    page.bgcolor = "white"
    page.scroll = "auto"
          
    page.add(
        ft.Column(
            controls=[
                ft.Text("How to use FaceGen", size=24, weight=ft.FontWeight.BOLD, color="black"),
                ft.Container(height=5),
                ft.Text("FaceGen has a limited number of buttons and features in order to make it simpler for every kind of user. " \
                        "\nBut in case you need some informations about what to do and how to do it, here is the options offered by our tool.",
                        size=14),
                        
                ft.Container(height=10),
                ft.Divider(),
                ft.Container(height=10),

                ft.Text("Step 1:", size=16, weight=ft.FontWeight.BOLD),
                ft.Text("Click on the start button !", size=14),
                
                ft.Container(height=10),
                ft.Text("Step 2:", size=16, weight=ft.FontWeight.BOLD),
                ft.Text("First, you need to build the profile. There is a lot of parameters but if you don't want to select all of them by hand, you can confirm without specifying the features"
                        " and pictures will be generated based on default parameters." \
                        "\nWhen you are happy with your choices, you can click on the Confirm choices button.", size=14),

                ft.Container(height=10),
                ft.Text("Step 3:", size=16, weight=ft.FontWeight.BOLD),
                ft.Text("Now you have to select one or more portraits that feat the most with the one you have in mind." \
                        " To do so, you only have to click on it and they will be circled with a blue band, indicating that they are selected." \
                        " If you change your mind, don't worry you still can click again on the picture to deselect it." \
                        "\nWhen you have your final selection, you can confirm your choices and click on the Mutate button.", size=14),

                ft.Container(height=10),
                ft.Text("Step 4:", size=16, weight=ft.FontWeight.BOLD),
                ft.Text("Here is your six brand new generated pictures based on your choices. You have now the possibility to select the ones that fit the most with your initial idea and continue to mutate pictures until you find the perfect match." \
                        " When you find it and you want to save it, click on the bin to clean your history selection and select the picture that you want to download. Then you can click on the Download button.", size=14),

                ft.Container(height=10),
                ft.Divider(),
                ft.Container(height=10),

                ft.Text("Tips:", size=16, weight=ft.FontWeight.BOLD),
                ft.Text("• Keep in mind that different mutations will be made depending on the number of pictures you have selected but also on your run because of the randomness of some mutations." \
                        "\nRerunning the tool with the same input can have different outcomes.", 
                        size=14),
                ft.Text("• Have fun !", 
                        size=14),
            ],
            spacing=0,
            expand=True
        )
    )
    
async def open_tutorial(e):
    await ft.app_async(target=tutorial_window)
    
    
    
    
    