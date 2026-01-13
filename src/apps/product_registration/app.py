import pyautogui
import pandas as pd
import time
import logging
import keyboard
import json
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Global stop flag
stop_requested = False


def on_esc_press(event):
    """ESC key event handler"""
    global stop_requested
    if event.name == "esc":
        logging.warning("⚠️  ESC pressed - Stopping automation...")
        stop_requested = True


def setup_automation():
    """Configure PyAutoGUI and keyboard listener"""
    global stop_requested
    stop_requested = False

    pyautogui.PAUSE = 0.5
    pyautogui.FAILSAFE = True

    keyboard.on_press(on_esc_press)

    logging.info("⚙️  Sistema de parada ativo:")
    logging.info("   - Pressione ESC para parar a automação")
    logging.info("   - Ou mova o mouse para o canto superior esquerdo")


def load_config():
    """Load configuration from JSON file"""
    base_dir = Path(__file__).parent
    src_dir = base_dir.parent.parent
    config_file = src_dir / "data" / "config" / "product_registration.json"

    if not config_file.exists():
        logging.error("⚠️  Configuração não encontrada!")
        logging.error(f"   Configure o app no launcher primeiro: {config_file}")
        return None

    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        logging.info("✅ Configuração carregada com sucesso")
        return config
    except Exception as e:
        logging.error(f"Erro ao carregar config: {e}")
        return None


def load_products(csv_path):
    """Load products from CSV file"""
    if not csv_path.exists():
        logging.error(f"CSV file not found at: {csv_path}")
        return None

    tabela = pd.read_csv(csv_path)
    logging.info(f"Loaded {len(tabela)} products from CSV.")
    return tabela


def open_browser_and_login(site_url, email, password):
    """Open browser and perform login"""
    logging.info("Opening Edge browser...")
    pyautogui.press("win")
    pyautogui.write("edge")
    pyautogui.press("enter")
    time.sleep(1)

    logging.info("Navigating to login page...")
    pyautogui.write(site_url)
    pyautogui.press("enter")
    time.sleep(3)

    logging.info("Performing login...")
    pyautogui.press("tab")
    pyautogui.click(x=607, y=508)
    pyautogui.write(email)
    pyautogui.press("tab")
    pyautogui.write(password)
    pyautogui.press("tab")
    pyautogui.press("enter")
    time.sleep(3)


def register_product(linha, index, total):
    """Register a single product"""
    logging.info(f"Registering Product {index+1}/{total}: {linha['codigo']}")

    # Click first field
    pyautogui.click(x=619, y=353)

    # Fill fields
    pyautogui.write(str(linha["codigo"]))
    pyautogui.press("tab")
    pyautogui.write(str(linha["marca"]))
    pyautogui.press("tab")
    pyautogui.write(str(linha["tipo"]))
    pyautogui.press("tab")
    pyautogui.write(str(linha["categoria"]))
    pyautogui.press("tab")
    pyautogui.write(str(linha["preco_unitario"]))
    pyautogui.press("tab")
    pyautogui.write(str(linha["custo"]))
    pyautogui.press("tab")

    obs = linha["obs"]
    if not pd.isna(obs):
        pyautogui.write(str(obs))

    pyautogui.press("tab")
    pyautogui.press("enter")
    pyautogui.scroll(5000)


def main():
    """Main automation entry point"""
    global stop_requested

    try:
        logging.info("Starting Product Registration Automation...")

        # Load configuration
        config = load_config()
        if config is None:
            logging.error("❌ Não é possível continuar sem configuração.")
            input("Pressione ENTER para sair...")
            return

        # Setup
        setup_automation()

        # Get paths from config
        csv_path = Path(config.get("csv_path", ""))
        site_url = config.get("site_url", "")
        email = config.get("email", "")
        password = config.get("password", "")

        # Validate config
        if not all([csv_path, site_url, email, password]):
            logging.error("❌ Configuração incompleta!")
            logging.error("   Configure todos os campos no launcher.")
            input("Pressione ENTER para sair...")
            return

        # Load products
        tabela = load_products(csv_path)
        if tabela is None:
            input("Pressione ENTER para sair...")
            return

        # Open browser and login
        open_browser_and_login(site_url, email, password)

        # Register products
        for i, linha in tabela.iterrows():
            if stop_requested:
                logging.warning("🛑 Automação interrompida pelo usuário")
                break

            register_product(linha, i, len(tabela))

        # Cleanup
        keyboard.unhook_all()

        if not stop_requested:
            logging.info("✅ Automation completed successfully!")

    except KeyboardInterrupt:
        logging.warning("Automation stopped by user.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        keyboard.unhook_all()


if __name__ == "__main__":
    main()
