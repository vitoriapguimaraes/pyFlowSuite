"""
Coordinate Picker Utility for Product Registration
Helps user capture mouse coordinates for form automation
"""

import time
import pyautogui
import json
from pathlib import Path


def get_position_with_countdown(field_name, countdown=5):
    """Get mouse position after countdown"""
    print(f"\n📍 Posicione o mouse sobre: {field_name}")

    for i in range(countdown, 0, -1):
        print(f"   {i}...")
        time.sleep(1)

    pos = pyautogui.position()
    print(f"   ✓ Capturado: x={pos.x}, y={pos.y}")
    return {"x": pos.x, "y": pos.y}


def main():
    """Main coordinate picker"""
    print("=" * 60)
    print("🎯 Capturador de Coordenadas - Product Registration")
    print("=" * 60)
    print("\nEste utilitário vai capturar as coordenadas dos campos")
    print("do formulário de cadastro de produtos.\n")
    print("Instruções:")
    print("  1. Abra o site de cadastro no navegador")
    print("  2. Quando solicitado, posicione o mouse sobre o campo")
    print("  3. Aguarde a contagem regressiva")
    print("  4. A posição será capturada automaticamente")
    print("\nPressione ENTER para começar...")
    input()

    # Campos a serem capturados
    fields = {
        "email_login": "Campo de EMAIL (na página de login)",
        "password_login": "Campo de SENHA (na página de login)",
        "submit_login": "Botão de LOGIN",
        "codigo": "Campo CÓDIGO do produto",
        "marca": "Campo MARCA do produto",
        "tipo": "Campo TIPO do produto",
        "categoria": "Campo CATEGORIA do produto",
        "preco_unitario": "Campo PREÇO UNITÁRIO",
        "custo": "Campo CUSTO",
        "obs": "Campo OBSERVAÇÕES",
        "submit_product": "Botão de ENVIAR produto",
    }

    coordinates = {}

    for field_id, field_description in fields.items():
        coordinates[field_id] = get_position_with_countdown(field_description)

    # Save to config file
    config_dir = Path(__file__).parent.parent / "data" / "config"
    config_dir.mkdir(parents=True, exist_ok=True)

    config_file = config_dir / "product_registration_coordinates.json"

    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(coordinates, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 60)
    print("✅ Coordenadas salvas com sucesso!")
    print(f"📁 Arquivo: {config_file}")
    print("=" * 60)
    print("\nCoordenadas capturadas:")
    for field_id, coords in coordinates.items():
        print(f"  {field_id}: x={coords['x']}, y={coords['y']}")

    print("\n💡 Dica: Use essas coordenadas na configuração do Product Registration")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
