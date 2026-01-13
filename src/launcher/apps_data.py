"""
App definitions for PyFlow Suite
Contains all app metadata, descriptions, and configuration requirements
"""

import flet as ft
from pathlib import Path


def get_apps(base_dir: Path) -> dict:
    """Get all app definitions with their metadata"""
    return {
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
                "path": base_dir / "apps" / "product_registration" / "app.py",
                "cwd": base_dir / "apps" / "product_registration",
                "requires_config": True,
                "config_fields": {
                    "csv_path": {
                        "label": "Caminho do CSV",
                        "type": "file",
                        "default": str(base_dir / "data" / "products.csv"),
                    },
                    "site_url": {
                        "label": "URL do Site",
                        "type": "text",
                        "default": "https://dlp.hashtagtreinamentos.com/python/intensivao/login",
                    },
                    "email": {
                        "label": "Email de Login",
                        "type": "text",
                        "default": "",
                    },
                    "password": {
                        "label": "Senha de Login",
                        "type": "password",
                        "default": "",
                    },
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
                "path": base_dir / "apps" / "sales_report" / "app.py",
                "cwd": base_dir / "apps" / "sales_report",
                "requires_config": True,
                "config_fields": {
                    "excel_path": {
                        "label": "Caminho do Excel",
                        "type": "file",
                        "default": str(base_dir / "data" / "sales_data.xlsx"),
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
                "path": base_dir / "apps" / "backup_tool" / "app.py",
                "cwd": base_dir / "apps" / "backup_tool",
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
                "path": base_dir / "apps" / "realtime_chat" / "app_web.py",
                "cwd": base_dir / "apps" / "realtime_chat",
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
                "path": base_dir / "apps" / "realtime_chat" / "app_desktop.py",
                "cwd": base_dir / "apps" / "realtime_chat",
                "requires_config": False,
            },
        ],
    }
