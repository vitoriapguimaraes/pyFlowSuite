"""
UI Builder for PyFlow Suite Launcher
Handles all visual construction and layout
"""

import flet as ft


def create_app_card(app, on_click_callback):
    """Create app card"""
    card_content = ft.Row(
        [
            ft.Icon(app["icon"], color=app["color"], size=24),
            ft.Text(app["name"], size=16, weight=ft.FontWeight.W_500, expand=True),
        ],
        spacing=12,
    )

    return ft.Container(
        content=card_content,
        bgcolor=ft.colors.with_opacity(0.05, ft.colors.WHITE),
        border=ft.border.all(1, ft.colors.with_opacity(0.1, ft.colors.WHITE)),
        border_radius=12,
        padding=20,
        ink=True,
        on_click=lambda e: on_click_callback(app),
        width=650,
    )


def create_header():
    """Create header with logo and title"""
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon("water_drop", size=36, color=ft.colors.CYAN_400),
                ft.Text(
                    "PyFlow Suite",
                    size=36,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.WHITE,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        margin=ft.margin.only(bottom=30),
    )


def create_section_title(title, emoji, color):
    """Create section title"""
    return ft.Text(
        f"{emoji} {title}",
        size=22,
        weight=ft.FontWeight.BOLD,
        color=color,
    )


def build_ui(page, apps, dialog_manager):
    """Build the complete UI"""
    # Clear page
    page.controls.clear()

    # Header
    page.add(create_header())

    # Optimization Section
    page.add(create_section_title("Otimização", "🔥", ft.colors.CYAN_300))

    for app in apps["optimization"]:
        page.add(create_app_card(app, dialog_manager.show_app_dialog))

    page.add(ft.Divider(height=30, color=ft.colors.TRANSPARENT))

    # Productivity Section
    page.add(create_section_title("Produtividade", "💼", ft.colors.GREEN_300))

    for app in apps["productivity"]:
        page.add(create_app_card(app, dialog_manager.show_app_dialog))

    page.add(ft.Divider(height=30, color=ft.colors.TRANSPARENT))

    # Communication Section
    page.add(create_section_title("Comunicação", "💬", ft.colors.ORANGE_300))

    for app in apps["communication"]:
        page.add(create_app_card(app, dialog_manager.show_app_dialog))

    page.update()
