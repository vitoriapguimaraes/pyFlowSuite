import flet as ft
import subprocess
import sys
from pathlib import Path
from config_manager import ConfigManager


def main(page: ft.Page):
    page.title = "PyFlow Suite"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 900
    page.window.height = 700
    page.padding = 40
    page.bgcolor = "#0a0a0a"

    # Paths
    BASE_DIR = Path(__file__).parent.parent
    CONFIG_DIR = BASE_DIR / "data" / "config"

    # Config Manager
    config_mgr = ConfigManager(CONFIG_DIR)

    # App definitions with descriptions and config requirements
    apps = {
        "optimization": [
            {
                "name": "Product Registration",
                "id": "product_registration",
                "icon": "shopping_cart",
                "color": ft.colors.BLUE_400,
                "description": "Automatiza o cadastro de produtos em formulários web a partir de arquivos CSV. Ideal para registrar grandes volumes de produtos rapidamente.",
                "features": [
                    "📄 Importa dados de CSV",
                    "🌐 Preenche formulários web automaticamente",
                    "⚡ Processa centenas de produtos",
                ],
                "path": BASE_DIR / "apps" / "product_registration" / "app.py",
                "cwd": BASE_DIR / "apps" / "product_registration",
                "requires_config": True,
                "config_fields": {
                    "csv_path": {
                        "label": "Caminho do CSV",
                        "type": "file",
                        "default": str(BASE_DIR / "data" / "products.csv"),
                    },
                    "site_url": {
                        "label": "URL do Site",
                        "type": "text",
                        "default": "https://dlp.hashtagtreinamentos.com/python/intensivao/login",
                    },
                    "email": {"label": "Email de Login", "type": "text", "default": ""},
                },
            },
            {
                "name": "Sales Report Generator",
                "id": "sales_report",
                "icon": "analytics",
                "color": ft.colors.RED_400,
                "description": "Gera relatórios de vendas detalhados e envia por email via Outlook. Analisa faturamento, quantidade e ticket médio por loja.",
                "features": [
                    "📊 Análise automática de vendas",
                    "📧 Envio por email (Outlook)",
                    "💰 Cálculo de métricas-chave",
                ],
                "path": BASE_DIR / "apps" / "sales_report" / "app.py",
                "cwd": BASE_DIR / "apps" / "sales_report",
                "requires_config": True,
                "config_fields": {
                    "excel_path": {
                        "label": "Caminho do Excel",
                        "type": "file",
                        "default": str(BASE_DIR / "data" / "sales_data.xlsx"),
                    },
                    "recipient_email": {
                        "label": "Email Destinatário",
                        "type": "text",
                        "default": "",
                    },
                },
            },
        ],
        "productivity": [
            {
                "name": "Backup Tool",
                "id": "backup_tool",
                "icon": "backup",
                "color": ft.colors.GREEN_400,
                "description": "Cria backups automáticos de pastas selecionadas com timestamp. Preserva estrutura de arquivos e subpastas.",
                "features": [
                    "💾 Backup completo de diretórios",
                    "🕐 Timestamp automático",
                    "📁 Preserva estrutura de pastas",
                ],
                "path": BASE_DIR / "apps" / "backup_tool" / "app.py",
                "cwd": BASE_DIR / "apps" / "backup_tool",
                "requires_config": False,
            },
        ],
        "communication": [
            {
                "name": "Real-Time Chat (Web)",
                "id": "realtime_chat_web",
                "icon": "chat",
                "color": ft.colors.ORANGE_400,
                "description": "Chat em tempo real baseado em Flask e SocketIO. Acessa via navegador web em rede local.",
                "features": [
                    "💬 Mensagens em tempo real",
                    "🌐 Acesso via navegador",
                    "👥 Múltiplos usuários",
                ],
                "path": BASE_DIR / "apps" / "realtime_chat" / "app_web.py",
                "cwd": BASE_DIR / "apps" / "realtime_chat",
                "requires_config": False,
            },
            {
                "name": "Real-Time Chat (Desktop)",
                "id": "realtime_chat_desktop",
                "icon": "message",
                "color": ft.colors.INDIGO_400,
                "description": "Aplicação de chat desktop com interface Flet. Comunicação instantânea entre usuários na mesma rede.",
                "features": [
                    "💬 Interface desktop nativa",
                    "⚡ Mensagens instantâneas",
                    "🎨 Design moderno e responsivo",
                ],
                "path": BASE_DIR / "apps" / "realtime_chat" / "app_desktop.py",
                "cwd": BASE_DIR / "apps" / "realtime_chat",
                "requires_config": False,
            },
        ],
    }

    def launch_app(app_info):
        """Launch the application"""
        # Check if config is required and present
        if app_info.get("requires_config"):
            config = config_mgr.load_config(app_info["id"])
            if not config:
                show_error(
                    "Configuração necessária",
                    f"Por favor, configure o app '{app_info['name']}' antes de iniciar.",
                )
                return

        try:
            subprocess.Popen(
                [sys.executable, str(app_info["path"])], cwd=str(app_info["cwd"])
            )
            # Close modal
            info_dialog.open = False
            page.update()
            print(f"✓ Launched: {app_info['name']}")
        except Exception as e:
            show_error("Erro ao Iniciar", f"Falha ao iniciar aplicação: {e}")

    def show_app_dialog(app_info):
        """Show app description dialog"""
        info_dialog.title = ft.Row(
            [
                ft.Icon(app_info["icon"], color=app_info["color"], size=28),
                ft.Text(app_info["name"], size=20, weight=ft.FontWeight.BOLD),
            ],
            spacing=10,
        )

        info_dialog.content = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        app_info["description"],
                        size=14,
                        color=ft.colors.GREY_300,
                    ),
                    ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                    ft.Text("✨ Funcionalidades:", size=16, weight=ft.FontWeight.BOLD),
                    *[
                        ft.Text(f"  {feature}", size=13, color=ft.colors.GREY_400)
                        for feature in app_info["features"]
                    ],
                ],
                spacing=8,
                tight=True,
            ),
            width=500,
        )

        info_dialog.actions = [
            ft.TextButton("Cancelar", on_click=lambda e: close_info_dialog()),
            ft.FilledButton(
                "Iniciar Aplicação",
                icon="rocket_launch",
                on_click=lambda e: launch_app(app_info),
            ),
        ]

        info_dialog.open = True
        page.update()

    def show_config_dialog(app_info):
        """Show configuration dialog for app"""
        if not app_info.get("requires_config"):
            return

        # Load existing config
        current_config = config_mgr.load_config(app_info["id"])

        # Create input fields
        fields = {}
        field_controls = []

        for field_id, field_info in app_info["config_fields"].items():
            value = current_config.get(field_id, field_info["default"])

            text_field = ft.TextField(
                label=field_info["label"],
                value=str(value),
                width=450,
            )
            fields[field_id] = text_field
            field_controls.append(text_field)

        def save_configuration(e):
            # Collect values
            new_config = {field_id: field.value for field_id, field in fields.items()}

            # Save
            if config_mgr.save_config(app_info["id"], new_config):
                config_dialog.open = False
                page.update()
                # Refresh the card to show configured status
                refresh_ui()
            else:
                show_error("Erro", "Falha ao salvar configuração")

        config_dialog.title = ft.Row(
            [
                ft.Icon("settings", color=app_info["color"], size=24),
                ft.Text(
                    f"Configurar {app_info['name']}", size=18, weight=ft.FontWeight.BOLD
                ),
            ],
            spacing=10,
        )

        config_dialog.content = ft.Container(
            content=ft.Column(field_controls, spacing=15, tight=True),
            width=500,
        )

        config_dialog.actions = [
            ft.TextButton("Cancelar", on_click=lambda e: close_config_dialog()),
            ft.FilledButton("Salvar", icon="save", on_click=save_configuration),
        ]

        config_dialog.open = True
        page.update()

    def show_error(title, message):
        """Show error dialog"""
        error_dialog.title = ft.Text(title)
        error_dialog.content = ft.Text(message)
        error_dialog.actions = [
            ft.TextButton("OK", on_click=lambda e: close_error_dialog())
        ]
        error_dialog.open = True
        page.update()

    def close_info_dialog():
        info_dialog.open = False
        page.update()

    def close_config_dialog():
        config_dialog.open = False
        page.update()

    def close_error_dialog():
        error_dialog.open = False
        page.update()

    def create_app_card(app):
        """Create app card with config button if needed"""
        is_configured = False
        if app.get("requires_config"):
            required_keys = list(app["config_fields"].keys())
            is_configured = config_mgr.is_configured(app["id"], required_keys)

        # Config indicator
        config_indicator = None
        if app.get("requires_config"):
            config_indicator = ft.Container(
                content=ft.Icon(
                    "check_circle" if is_configured else "settings",
                    size=16,
                    color=ft.colors.GREEN_400 if is_configured else ft.colors.GREY_600,
                ),
                tooltip="Configurado" if is_configured else "Requer configuração",
            )

        card_content = ft.Row(
            [
                ft.Icon(app["icon"], color=app["color"], size=24),
                ft.Text(app["name"], size=16, weight=ft.FontWeight.W_500, expand=True),
                config_indicator if config_indicator else ft.Container(),
                ft.IconButton(
                    icon="settings",
                    icon_color=ft.colors.GREY_400,
                    on_click=lambda e, app=app: show_config_dialog(app),
                    tooltip="Configurar",
                    visible=app.get("requires_config", False),
                ),
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
            on_click=lambda e, app=app: show_app_dialog(app),
            width=650,
        )

    def refresh_ui():
        """Refresh the entire UI"""
        page.controls.clear()
        build_ui()
        page.update()

    def build_ui():
        """Build the complete UI"""
        # Header
        page.add(
            ft.Container(
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
        )

        # Optimization Section
        page.add(
            ft.Text(
                "🔥 Otimização",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.CYAN_300,
            )
        )

        for app in apps["optimization"]:
            page.add(create_app_card(app))

        page.add(ft.Divider(height=30, color=ft.colors.TRANSPARENT))

        # Productivity Section
        page.add(
            ft.Text(
                "💼 Produtividade",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.GREEN_300,
            )
        )

        for app in apps["productivity"]:
            page.add(create_app_card(app))

        page.add(ft.Divider(height=30, color=ft.colors.TRANSPARENT))

        # Communication Section
        page.add(
            ft.Text(
                "💬 Comunicação",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.ORANGE_300,
            )
        )

        for app in apps["communication"]:
            page.add(create_app_card(app))

    # Dialog instances
    info_dialog = ft.AlertDialog(
        modal=True, title=ft.Text(""), content=ft.Text(""), actions=[]
    )

    config_dialog = ft.AlertDialog(
        modal=True, title=ft.Text(""), content=ft.Text(""), actions=[]
    )

    error_dialog = ft.AlertDialog(
        modal=True, title=ft.Text(""), content=ft.Text(""), actions=[]
    )

    page.overlay.extend([info_dialog, config_dialog, error_dialog])

    # Build initial UI
    build_ui()


if __name__ == "__main__":
    ft.app(target=main)
