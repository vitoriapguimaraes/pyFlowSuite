import pyautogui
import pandas as pd
import time
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        logging.info("Starting Product Registration Automation...")

        # Paths
        base_dir = Path(__file__).parent
        # Go up to src/ directory (app.py -> product_registration -> apps -> src)
        src_dir = base_dir.parent.parent
        csv_path = src_dir / "data" / "products.csv"

        if not csv_path.exists():
            logging.error(f"CSV file not found at: {csv_path}")
            return

        # Load Data
        tabela = pd.read_csv(csv_path)
        logging.info(f"Loaded {len(tabela)} products from CSV.")

        # PyAutoGUI Config
        pyautogui.PAUSE = 0.5

        # Open System
        logging.info("Opening Edge browser...")
        pyautogui.press("win")
        pyautogui.write("edge")
        pyautogui.press("enter")
        time.sleep(1) # Wait for run dialog/start menu

        logging.info("Navigating to login page...")
        pyautogui.write("https://dlp.hashtagtreinamentos.com/python/intensivao/login")
        pyautogui.press("enter")

        time.sleep(3) # Wait for page load

        # Login
        logging.info("Performing login...")
        pyautogui.press("tab") # Usually focus starts on URL or body, tab to fields
        # Note: Original code used hardcoded coordinates. 
        # We will try to rely on tabs if possible, or warn user about coordinates.
        # Since I can't guarantee coordinates, I'll attempt a TAB sequence.
        # Typically: Click -> Email -> Tab -> Password -> Tab -> Enter

        # Coordinates from original (User might need to adjust these!)
        # pyautogui.click(x=607, y=508) 

        # Trying a robust TAB approach (assuming page focus):
        # 1. Click center of screen to ensure focus? 
        # For now, let's keep original coordinates but commented out and try safe tabs?
        # Actually, without coordinates, automating a specific web form is hard with just PyAutoGUI.
        # I will keep the COORDINATES but verify if they are valid or ask user to re-calibrate.
        # Since this is a "Refactoring", I should make it cleaner but preserve behavior.
        # Original: click(607, 508) -> write email -> tab -> password -> tab -> enter

        pyautogui.click(x=607, y=508)
        pyautogui.write("emailteste@gmail.com")
        pyautogui.press("tab")
        pyautogui.write("senhateste")
        pyautogui.press("tab")
        pyautogui.press("enter")

        time.sleep(3)

        # Register Products
        for i, linha in tabela.iterrows():
            logging.info(f"Registering Product {i+1}/{len(tabela)}: {linha['codigo']}")

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
            pyautogui.press("enter") # Submit

            pyautogui.scroll(5000) # Scroll up

        logging.info("Automation completed successfully!")

    except KeyboardInterrupt:
        logging.warning("Automation stopped by user.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()