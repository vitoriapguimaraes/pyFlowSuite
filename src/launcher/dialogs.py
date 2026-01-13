"""
Dialog management for PyFlow Suite Launcher
Handles all modal dialogs (app info, configuration, errors)
"""

import flet as ft
import subprocess
import sys


class DialogManager:
    """Manages all dialogs in the launcher"""

    def __init__(self, page, config_mgr, refresh_callback):
        self.page = page
        self.config_mgr = config_mgr
        self.refresh_callback = refresh_callback

        # Create dialog instances
        self.info_dialog = ft.AlertDialog(
            modal=True, title=ft.Text(""), content=ft.Text(""), actions=[]
        )

        self.config_dialog = ft.AlertDialog(
            modal=True, title=ft.Text(""), content=ft.Text(""), actions=[]
        )

        self.error_dialog = ft.AlertDialog(
            modal=True, title=ft.Text(""), content=ft.Text(""), actions=[]
        )

        # Add to overlay
        page.overlay.extend([self.info_dialog, self.config_dialog, self.error_dialog])

    def launch_app(self, app_info):
        """Launch the application"""
        # Check if config is required and present
        if app_info.get("requires_config"):
            config = self.config_mgr.load_config(app_info["id"])
            if not config:
                self.show_error(
                    "Configuração necessária",
                    f"Por favor, configure o app '{app_info['name']}' antes de iniciar.",
                )
                return

        try:
            subprocess.Popen(
                [sys.executable, str(app_info["path"])], cwd=str(app_info["cwd"])
            )
            # Close modal
            self.info_dialog.open = False
            self.page.update()
            print(f"✓ Launched: {app_info['name']}")
        except Exception as e:
            self.show_error("Erro ao Iniciar", f"Falha ao iniciar aplicação: {e}")

    def show_app_dialog(self, app_info):
        """Show app description dialog"""
        self.info_dialog.title = ft.Row(
            [
                ft.Icon(app_info["icon"], color=app_info["color"], size=28),
                ft.Text(app_info["name"], size=20, weight=ft.FontWeight.BOLD),
            ],
            spacing=10,
        )

        # Check if configured
        is_configured = False
        if app_info.get("requires_config"):
            required_keys = list(app_info["config_fields"].keys())
            is_configured = self.config_mgr.is_configured(app_info["id"], required_keys)

        content_items = [
            ft.Text(app_info["description"], size=14, color=ft.colors.GREY_300),
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
            ft.Text("✨ Funcionalidades:", size=16, weight=ft.FontWeight.BOLD),
            *[
                ft.Text(f"  {feature}", size=13, color=ft.colors.GREY_400)
                for feature in app_info["features"]
            ],
        ]

        # Add config status if app requires config
        if app_info.get("requires_config"):
            content_items.extend(
                [
                    ft.Divider(height=15, color=ft.colors.TRANSPARENT),
                    ft.Row(
                        [
                            ft.Icon(
                                "check_circle" if is_configured else "warning",
                                size=18,
                                color=(
                                    ft.colors.GREEN_400
                                    if is_configured
                                    else ft.colors.ORANGE_400
                                ),
                            ),
                            ft.Text(
                                (
                                    "Configurado"
                                    if is_configured
                                    else "Requer configuração"
                                ),
                                size=13,
                                color=(
                                    ft.colors.GREEN_400
                                    if is_configured
                                    else ft.colors.ORANGE_400
                                ),
                            ),
                        ],
                        spacing=8,
                    ),
                ]
            )

        self.info_dialog.content = ft.Container(
            content=ft.Column(content_items, spacing=8, tight=True),
            width=500,
        )

        # Build actions list
        actions = [ft.TextButton("Fechar", on_click=lambda e: self._close_info())]

        # Add Configure button if app requires config
        if app_info.get("requires_config"):
            actions.append(
                ft.OutlinedButton(
                    "Configurar",
                    icon="settings",
                    on_click=lambda e: self._show_config_from_info(app_info),
                )
            )

        # Add Launch button
        actions.append(
            ft.FilledButton(
                "Iniciar Aplicação",
                icon="rocket_launch",
                on_click=lambda e: self.launch_app(app_info),
            )
        )

        self.info_dialog.actions = actions
        self.info_dialog.open = True
        self.page.update()

    def show_config_dialog(self, app_info):
        """Show configuration dialog for app"""
        if not app_info.get("requires_config"):
            return

        # Load existing config
        current_config = self.config_mgr.load_config(app_info["id"])

        # Create input fields
        fields = {}
        field_controls = []

        for field_id, field_info in app_info["config_fields"].items():
            value = current_config.get(field_id, field_info["default"])

            # Check if it's a password field
            is_password = field_info.get("type") == "password"

            text_field = ft.TextField(
                label=field_info["label"],
                value=str(value),
                width=450,
                password=is_password,
                can_reveal_password=is_password,
            )
            fields[field_id] = text_field
            field_controls.append(text_field)

        # Add coordinate capture button for Product Registration
        if app_info["id"] == "product_registration":
            field_controls.append(ft.Divider(height=10, color=ft.colors.TRANSPARENT))
            field_controls.append(
                ft.OutlinedButton(
                    "🎯 Capturar Coordenadas do Formulário",
                    icon="location_on",
                    on_click=lambda e: self._launch_coordinate_picker(app_info),
                    width=450,
                )
            )
            field_controls.append(
                ft.Text(
                    "Abre ferramenta para capturar posições dos campos",
                    size=11,
                    color=ft.colors.GREY_500,
                    italic=True,
                )
            )

        def save_configuration(e):
            # Collect values
            new_config = {field_id: field.value for field_id, field in fields.items()}

            # Save
            if self.config_mgr.save_config(app_info["id"], new_config):
                self.config_dialog.open = False
                self.page.update()
                # Refresh the UI
                self.refresh_callback()
            else:
                self.show_error("Erro", "Falha ao salvar configuração")

        self.config_dialog.title = ft.Row(
            [
                ft.Icon("settings", color=app_info["color"], size=24),
                ft.Text(
                    f"Configurar {app_info['name']}",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
            ],
            spacing=10,
        )

        self.config_dialog.content = ft.Container(
            content=ft.Column(field_controls, spacing=15, tight=True),
            width=500,
        )

        self.config_dialog.actions = [
            ft.TextButton("Cancelar", on_click=lambda e: self._close_config()),
            ft.FilledButton("Salvar", icon="save", on_click=save_configuration),
        ]

        self.config_dialog.open = True
        self.page.update()

    def show_error(self, title, message):
        """Show error dialog"""
        self.error_dialog.title = ft.Text(title)
        self.error_dialog.content = ft.Text(message)
        self.error_dialog.actions = [
            ft.TextButton("OK", on_click=lambda e: self._close_error())
        ]
        self.error_dialog.open = True
        self.page.update()

    def _close_info(self):
        """Close info dialog"""
        self.info_dialog.open = False
        self.page.update()

    def _close_config(self):
        """Close config dialog"""
        self.config_dialog.open = False
        self.page.update()

    def _close_error(self):
        """Close error dialog"""
        self.error_dialog.open = False
        self.page.update()

    def _show_config_from_info(self, app_info):
        """Show config dialog and close info dialog"""
        self.info_dialog.open = False
        self.page.update()
        self.show_config_dialog(app_info)

    def _launch_coordinate_picker(self, app_info):
        """Launch coordinate picker utility"""
        script_path = app_info["cwd"] / "capture_coordinates.py"

        if not script_path.exists():
            self.show_error(
                "Arquivo não encontrado",
                f"Script de captura não encontrado em:\n{script_path}",
            )
            return

        try:
            # Launch in new terminal window
            subprocess.Popen(
                ["start", "cmd", "/k", sys.executable, str(script_path)],
                shell=True,
                cwd=str(app_info["cwd"]),
            )

            # Show info
            self.show_error(
                "Captura Iniciada",
                "O capturador de coordenadas foi aberto em uma nova janela.\n\n"
                "Siga as instruções no terminal para capturar as posições dos campos.",
            )
        except Exception as e:
            self.show_error("Erro", f"Falha ao iniciar capturador: {e}")
