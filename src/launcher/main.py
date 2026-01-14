"""
PyFlow Suite - Main Launcher
A unified launcher for all PyFlow Suite applications
"""

import flet as ft
from pathlib import Path

from config_manager import ConfigManager
from apps_data import get_apps
from dialogs import DialogManager
from ui_builder import build_ui


def main(page: ft.Page):
    """Main launcher entry point"""
    # Page configuration
    page.title = "PyFlow Suite"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 1100
    page.window.height = 900
    page.window.min_width = 800
    page.window.min_height = 600
    page.padding = 40
    page.bgcolor = "#0a0a0a"
    page.scroll = ft.ScrollMode.AUTO  # Adiciona scroll automático
    page.window.maximized = True  # Começar maximizado para ver todo o conteúdo

    # Paths
    BASE_DIR = Path(__file__).parent.parent
    CONFIG_DIR = BASE_DIR / "data" / "config"

    # Initialize managers
    config_mgr = ConfigManager(CONFIG_DIR)
    apps = get_apps(BASE_DIR)

    # Refresh UI callback
    def refresh_ui():
        build_ui(page, apps, dialog_mgr)

    # Initialize dialog manager
    dialog_mgr = DialogManager(page, config_mgr, refresh_ui)

    # Build UI
    build_ui(page, apps, dialog_mgr)


if __name__ == "__main__":
    ft.app(target=main)
