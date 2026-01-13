import flet as ft
import subprocess
import sys
from pathlib import Path

def main(page: ft.Page):
    page.title = "PyFlow Suite"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.window_width = 1000
    page.window_height = 800

    # Paths
    BASE_DIR = Path(__file__).parent.parent
    
    # Project Definitions
    projects_optimization = [
        {
            "name": "Product Registration",
            "desc": "Automates product entry from CSV into web forms.",
            "icon": "shopping_cart",
            "path": BASE_DIR / "apps" / "product_registration" / "automacaoCadastro.py",
            "cwd": BASE_DIR / "apps" / "product_registration",
            "color": ft.Colors.BLUE_400
        },
        {
            "name": "Sales Report Generator",
            "desc": "Generates and emails HTML sales reports.",
            "icon": "analytics",
            "path": BASE_DIR / "apps" / "sales_report" / "relatorioVendas.py", 
            "cwd": BASE_DIR / "apps" / "sales_report",
            "color": ft.Colors.RED_400
        }
    ]

    projects_productivity = [
        {
            "name": "Backup Tool",
            "desc": "Automated file backup system with GUI.",
            "icon": "backup",
            "path": BASE_DIR / "apps" / "backup_tool" / "backupAutomation.py",
            "cwd": BASE_DIR / "apps" / "backup_tool",
            "color": ft.Colors.GREEN_400
        }
    ]

    projects_communication = [
        {
            "name": "Real-Time Chat (Web)",
            "desc": "Flask-SocketIO based web chat.",
            "icon": "chat",
            "path": BASE_DIR / "apps" / "realtime_chat" / "chatWebFlask.py",
            "cwd": BASE_DIR / "apps" / "realtime_chat",
            "color": ft.Colors.ORANGE_400
        },
         {
            "name": "Real-Time Chat (Desktop)",
            "desc": "Modern Flet-based desktop chat.",
            "icon": "message",
            "path": BASE_DIR / "apps" / "realtime_chat" / "chatFlet.py",
            "cwd": BASE_DIR / "apps" / "realtime_chat",
            "color": ft.Colors.INDIGO_400
        }
    ]

    def launch_app(e, project):
        try:
            if not project["path"].exists():
                snack = ft.SnackBar(ft.Text(f"Error: File not found at {project['path']}"), bgcolor=ft.Colors.RED_900)
                page.overlay.append(snack)
                snack.open = True
                page.update()
                return

            subprocess.Popen([sys.executable, str(project["path"])], cwd=str(project["cwd"]))
            
            snack = ft.SnackBar(ft.Text(f"Launching {project['name']}..."), bgcolor=ft.Colors.GREEN_900)
            page.overlay.append(snack)
            snack.open = True
            page.update()
            
        except Exception as ex:
            snack = ft.SnackBar(ft.Text(f"Failed to launch: {str(ex)}"), bgcolor=ft.Colors.RED_900)
            page.overlay.append(snack)
            snack.open = True
            page.update()

    # UI Builder
    def create_project_card(project):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(project["icon"], size=40, color=project["color"]),
                    ft.Text(project["name"], size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ], alignment=ft.MainAxisAlignment.START),
                ft.Divider(color=ft.Colors.GREY_800),
                ft.Text(project["desc"], size=13, color=ft.Colors.GREY_400, selectable=True),
                ft.Container(expand=True),
                ft.FilledButton(
                    "Launch",
                    icon="rocket_launch",
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=project["color"],
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    on_click=lambda e: launch_app(e, project)
                )
            ], spacing=10),
            padding=20,
            bgcolor=ft.Colors.GREY_900,
            border_radius=15,
            width=280,
            height=200,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                offset=ft.Offset(0, 5),
            )
        )

    def create_grid(projects):
        return ft.Row(
            controls=[create_project_card(p) for p in projects],
            wrap=True,
            spacing=30,
            run_spacing=30,
            alignment=ft.MainAxisAlignment.START,
        )

    # Tabs
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Optimization",
                icon="flash_on",
                content=ft.Container(
                    content=create_grid(projects_optimization),
                    padding=40,
                    alignment=ft.Alignment(-1, -1)
                )
            ),
            ft.Tab(
                text="Productivity",
                icon="security",
                content=ft.Container(
                    content=create_grid(projects_productivity),
                    padding=40,
                    alignment=ft.Alignment(-1, -1)
                )
            ),
             ft.Tab(
                text="Communication",
                icon="forum",
                content=ft.Container(
                    content=create_grid(projects_communication),
                    padding=40,
                    alignment=ft.Alignment(-1, -1)
                )
            ),
        ],
        expand=1,
    )

    header = ft.Container(
        content=ft.Row([
             ft.Icon("water_drop", size=40, color=ft.Colors.CYAN_400),
             ft.Text("PyFlow Suite", size=40, weight=ft.FontWeight.BOLD),
        ], alignment=ft.MainAxisAlignment.CENTER),
        padding=ft.padding.only(top=30, bottom=20),
        alignment=ft.Alignment(0, 0)
    )
    
    content_area = ft.Container(
        content=ft.Column([
            header,
            tabs
        ]),
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[ft.Colors.BLACK, ft.Colors.GREY_900],
        )
    )

    page.add(content_area)

if __name__ == "__main__":
    ft.app(target=main)
