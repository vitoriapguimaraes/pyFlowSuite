import flet as ft
import subprocess
import sys
from pathlib import Path


def main(page: ft.Page):
    page.title = "PyFlow Suite"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 900
    page.window.height = 700
    page.padding = 40
    page.bgcolor = "#0a0a0a"

    # Paths
    BASE_DIR = Path(__file__).parent.parent

    # App definitions with descriptions
    apps = {
        "optimization": [
            {
                "name": "Product Registration",
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
            },
            {
                "name": "Sales Report Generator",
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
            },
        ],
        "productivity": [
            {
                "name": "Backup Tool",
                "icon": "backup",
                "color": ft.colors.GREEN_400,
                "description": "Cria backups automáticos de pastas selecionadas com timestamp. Preserva estrutura de arquivos e subpastas.",
                "features": [
                    "💾 Backup completo de diretórios",
                    "� Timestamp automático",
                    "📁 Preserva estrutura de pastas",
                ],
                "path": BASE_DIR / "apps" / "backup_tool" / "app.py",
                "cwd": BASE_DIR / "apps" / "backup_tool",
            },
        ],
        "communication": [
            {
                "name": "Real-Time Chat (Web)",
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
            },
            {
                "name": "Real-Time Chat (Desktop)",
                "icon": "message",
                "color": ft.colors.INDIGO_400,
                "description": "Aplicação de chat desktop com interface Flet. Comunicação instantânea entre usuários na mesma rede.",
                "features": [
                    "� Interface desktop nativa",
                    "⚡ Mensagens instantâneas",
                    "🎨 Design moderno e responsivo",
                ],
                "path": BASE_DIR / "apps" / "realtime_chat" / "app_desktop.py",
                "cwd": BASE_DIR / "apps" / "realtime_chat",
            },
        ],
    }

    def launch_app(app_info):
        """Launch the application"""
        try:
            subprocess.Popen(
                [sys.executable, str(app_info["path"])], cwd=str(app_info["cwd"])
            )
            # Close modal
            dialog.open = False
            page.update()
            print(f"✓ Launched: {app_info['name']}")
        except Exception as e:
            print(f"✗ Error: {e}")

    def show_app_dialog(app_info):
        """Show app description dialog"""
        dialog.title = ft.Row(
            [
                ft.Icon(app_info["icon"], color=app_info["color"], size=28),
                ft.Text(app_info["name"], size=20, weight=ft.FontWeight.BOLD),
            ],
            spacing=10,
        )

        dialog.content = ft.Container(
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

        dialog.actions = [
            ft.TextButton("Cancelar", on_click=lambda e: close_dialog()),
            ft.FilledButton(
                "Iniciar Aplicação",
                icon="rocket_launch",
                on_click=lambda e: launch_app(app_info),
            ),
        ]

        dialog.open = True
        page.update()

    def close_dialog():
        dialog.open = False
        page.update()

    # Dialog instance - initialize with empty content to avoid error
    dialog = ft.AlertDialog(
        modal=True, title=ft.Text(""), content=ft.Text(""), actions=[]
    )
    page.overlay.append(dialog)

    # Build UI
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
            "� Otimização",
            size=22,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.CYAN_300,
        )
    )

    for app in apps["optimization"]:
        page.add(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(app["icon"], color=app["color"], size=24),
                        ft.Text(app["name"], size=16, weight=ft.FontWeight.W_500),
                    ],
                    spacing=12,
                ),
                bgcolor=ft.colors.with_opacity(0.05, ft.colors.WHITE),
                border=ft.border.all(1, ft.colors.with_opacity(0.1, ft.colors.WHITE)),
                border_radius=12,
                padding=20,
                ink=True,
                on_click=lambda e, app=app: show_app_dialog(app),
                width=600,
            )
        )

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
        page.add(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(app["icon"], color=app["color"], size=24),
                        ft.Text(app["name"], size=16, weight=ft.FontWeight.W_500),
                    ],
                    spacing=12,
                ),
                bgcolor=ft.colors.with_opacity(0.05, ft.colors.WHITE),
                border=ft.border.all(1, ft.colors.with_opacity(0.1, ft.colors.WHITE)),
                border_radius=12,
                padding=20,
                ink=True,
                on_click=lambda e, app=app: show_app_dialog(app),
                width=600,
            )
        )

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
        page.add(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(app["icon"], color=app["color"], size=24),
                        ft.Text(app["name"], size=16, weight=ft.FontWeight.W_500),
                    ],
                    spacing=12,
                ),
                bgcolor=ft.colors.with_opacity(0.05, ft.colors.WHITE),
                border=ft.border.all(1, ft.colors.with_opacity(0.1, ft.colors.WHITE)),
                border_radius=12,
                padding=20,
                ink=True,
                on_click=lambda e, app=app: show_app_dialog(app),
                width=600,
            )
        )


if __name__ == "__main__":
    ft.app(target=main)
