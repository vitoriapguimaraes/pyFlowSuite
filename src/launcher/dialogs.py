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
            ft.Text("Funcionalidades:", size=16, weight=ft.FontWeight.BOLD),
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

            # Create input field using helper
            input_field = self._create_input_field(field_id, field_info, value, fields)

            # If not multiselect (which saves to fields internally), add to fields dict
            if field_info.get("type") != "multiselect":
                fields[field_id] = input_field

            field_controls.append(input_field)

        # Add tools for Product Registration
        if app_info["id"] == "product_registration":
            field_controls.append(ft.Divider(height=10, color=ft.colors.TRANSPARENT))

            # Coordinate picker
            field_controls.append(
                ft.OutlinedButton(
                    "Capturar Coordenadas do Formulário",
                    icon="location_on",
                    on_click=lambda e: self._launch_coordinate_picker(app_info),
                    width=450,
                )
            )
            field_controls.append(
                ft.Text(
                    "Captura posições X,Y dos campos no formulário",
                    size=11,
                    color=ft.colors.GREY_500,
                    italic=True,
                )
            )

            field_controls.append(ft.Divider(height=5, color=ft.colors.TRANSPARENT))

            # Workflow recorder
            field_controls.append(
                ft.OutlinedButton(
                    "Gravar Workflow Personalizado",
                    icon="video_camera_back",
                    on_click=lambda e: self._launch_workflow_recorder(app_info),
                    width=450,
                )
            )
            field_controls.append(
                ft.Text(
                    "Define o fluxo completo da automação (navegação, login, etc.)",
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

    def _launch_workflow_recorder(self, app_info):
        """Launch workflow recorder utility"""
        script_path = app_info["cwd"] / "record_workflow.py"

        if not script_path.exists():
            self.show_error(
                "Arquivo não encontrado",
                f"Gravador de workflow não encontrado em:\n{script_path}",
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
                "Gravador Iniciado",
                "O gravador de workflow foi aberto em uma nova janela.\n\n"
                "Grave o fluxo completo da sua automação:\n"
                "   - Execute ações manualmente\n"
                "   - Pressione teclas F1-F8 para marcar etapas\n"
                "   - Use Ctrl+E e Ctrl+P para campos configuráveis\n"
                "   - Pressione F9 para finalizar",
            )
        except Exception as e:
            self.show_error("Erro", f"Falha ao iniciar gravador: {e}")

    def _create_input_field(self, field_id, field_info, value, fields_dict):
        """Create appropriate input field control based on type"""
        field_type = field_info.get("type", "text")

        if field_type == "select":
            options = [
                (
                    ft.dropdown.Option(k, v)
                    if isinstance(v, str)
                    else ft.dropdown.Option(str(k))
                )
                for k, v in field_info.get("options", {}).items()
            ]

            return ft.Dropdown(
                label=field_info["label"],
                value=str(value),
                width=450,
                options=options,
            )

        elif field_type == "multiselect":
            return self._create_multiselect_field(
                field_id, field_info, value, fields_dict
            )

        else:
            # Create TextField for text/password types
            is_password = field_type == "password"
            return ft.TextField(
                label=field_info["label"],
                value=str(value),
                width=450,
                password=is_password,
                can_reveal_password=is_password,
            )

    def _create_multiselect_field(self, field_id, field_info, value, fields_dict):
        """Create manual checkbox group for multiselect"""
        # Value must be a list
        current_val = value if isinstance(value, list) else [str(value)]

        # Create a hidden field to store the actual list value for saving
        # We will update this value whenever a checkbox changes
        value_store = ft.Text(value=str(current_val), visible=False)
        fields_dict[field_id] = value_store  # Save this control to read value later

        checkboxes = []
        for k, v in field_info.get("options", {}).items():

            def on_change(e, key=k):
                # Update the stored list
                current_list = eval(value_store.value)
                if e.control.value:
                    if key not in current_list:
                        current_list.append(key)
                else:
                    if key in current_list:
                        current_list.remove(key)
                value_store.value = str(current_list)

            cb = ft.Checkbox(label=v, value=(k in current_val), on_change=on_change)
            checkboxes.append(cb)

        return ft.Column(
            controls=[
                ft.Text(field_info["label"], size=12, color=ft.colors.GREY_400),
                *checkboxes,
                value_store,
            ],
            spacing=5,
        )
