"""
UI Builder for PyFlow Suite Launcher
Handles all visual construction and layout
"""

import flet as ft


def create_app_card(app, on_click_callback):
    """Create app card with preview image"""

    # Header with Icon and Title
    header_content = ft.Row(
        [
            ft.Icon(app["icon"], color=app["color"], size=24),
            ft.Text(app["name"], size=16, weight=ft.FontWeight.W_500, expand=True),
        ],
        spacing=12,
    )

    # Card Content (Image + Header)
    card_content = ft.Column(
        [
            # Preview Image
            ft.Image(
                src=str(app.get("image_path", "")),
                height=150,
                width=1000,  # Fill width
                fit=ft.ImageFit.COVER,
                border_radius=ft.border_radius.vertical(top=12),
                opacity=0.9,
            ),
            # Title Section
            ft.Container(
                content=header_content,
                padding=20,
            ),
        ],
        spacing=0,
    )

    return ft.Container(
        content=card_content,
        bgcolor=ft.colors.with_opacity(0.05, ft.colors.WHITE),
        border=ft.border.all(1, ft.colors.with_opacity(0.1, ft.colors.WHITE)),
        border_radius=12,
        # Padding removed to let image fill top
        padding=0,
        ink=True,
        on_click=lambda e: on_click_callback(app),
    )


def create_category_column(title, color, apps_list, on_click_callback):
    """Create a column for a specific app category"""

    # Create cards for this category
    app_cards = []
    for app in apps_list:
        app_cards.append(create_app_card(app, on_click_callback))

    return ft.Column(
        controls=[
            ft.Container(
                content=ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=color),
                margin=ft.margin.only(bottom=10),
                alignment=ft.alignment.center,
            ),
            ft.Column(
                controls=app_cards,
                spacing=20,
            ),
        ],
    )


def create_header():
    """Create header with logo and title"""
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon("dashboard", size=36, color=ft.colors.CYAN_400),
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


def build_ui(page, apps, dialog_manager):
    """Build the complete UI"""
    # Clear page
    page.controls.clear()

    # Header
    page.add(create_header())

    # Main Content Row with 3 Columns
    main_content = ft.ResponsiveRow(
        controls=[
            # Optimization Column
            ft.Column(
                controls=[
                    create_category_column(
                        "Otimização",
                        ft.colors.CYAN_300,
                        apps["optimization"],
                        dialog_manager.show_app_dialog,
                    )
                ],
                col={"md": 12, "lg": 6},  # Full width on small/med, 1/2 on large
            ),
            # Productivity Column
            ft.Column(
                controls=[
                    create_category_column(
                        "Produtividade",
                        ft.colors.GREEN_300,
                        apps["productivity"],
                        dialog_manager.show_app_dialog,
                    )
                ],
                col={
                    "md": 12,
                    "lg": 6,
                },  # Adjusted from lg:4 to lg:6 for balanced 2-column layout
            ),
        ],
        spacing=30,
        run_spacing=30,
    )

    page.add(main_content)

    page.add(ft.Divider(height=40, color=ft.colors.TRANSPARENT))
    page.add(create_footer())

    page.update()


def create_footer():
    """Create minimalist footer"""
    return ft.Container(
        content=ft.Row(
            [
                ft.Text(
                    "Desenvolvido por github.com/vitoriapguimaraes",
                    size=12,
                    color=ft.colors.GREY_500,
                    weight=ft.FontWeight.W_400,
                    text_align=ft.TextAlign.CENTER,
                    italic=True,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.padding.only(bottom=20),
    )
