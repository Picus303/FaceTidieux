import shutil
import asyncio
import flet as ft
from pathlib import Path

from interface_graphique.main import main


if __name__ == "__main__":

    asyncio.run(ft.app_async(target=main))

    dossier = Path("generate_images")
    if dossier.exists() and dossier.is_dir():
        shutil.rmtree(dossier)
