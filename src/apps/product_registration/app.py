import pyautogui
import pandas as pd
import time
import logging
import keyboard
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


def load_products(csv_path):
    """Load products from CSV file"""
    if not csv_path.exists():
        logging.error(f"CSV file not found at: {csv_path}")
        return None

    tabela = pd.read_csv(csv_path)
    logging.info(f"Loaded {len(tabela)} products from CSV.")
    return tabela


def open_browser_and_login():
    """Open browser and perform login"""
    logging.info("Opening Edge browser...")
    pyautogui.press("win")
    pyautogui.write("edge")
    pyautogui.press("enter")
    time.sleep(1)

    logging.info("Navigating to login page...")
    pyautogui.write("https://dlp.hashtagtreinamentos.com/python/intensivao/login")
    pyautogui.press("enter")
    time.sleep(3)

    logging.info("Performing login...")
    pyautogui.press("tab")
    pyautogui.click(x=607, y=508)
    pyautogui.write("emailteste@gmail.com")
    pyautogui.press("tab")
    pyautogui.write("senhateste")
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

        # Setup
        setup_automation()

        # Paths
        base_dir = Path(__file__).parent
        src_dir = base_dir.parent.parent
        csv_path = src_dir / "data" / "products.csv"

        # Load products
        tabela = load_products(csv_path)
        if tabela is None:
            return

        # Open browser and login
        open_browser_and_login()

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
