# Sales Report Generator

import pandas as pd
import win32com.client as win32
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        logging.info("Starting Sales Report Generator...")

        # Paths
        base_dir = Path(__file__).parent
        # Go up to src/ directory (app.py -> sales_report -> apps -> src)
        src_dir = base_dir.parent.parent
        data_path = src_dir / "data" / "sales_data.xlsx"

        if not data_path.exists():
            logging.error(f"Data file not found at: {data_path}")
            return

        # Load Data
        logging.info("Loading sales data...")
        tabela_vendas = pd.read_excel(data_path)

        # Analysis
        logging.info("Processing data...")
        # Faturamento por loja
        faturamento_loja = tabela_vendas[['ID Loja', 'Valor Final']].groupby('ID Loja').sum()

        # Quantidade de produtos vendidos por loja
        quantidade_prod_loja = tabela_vendas[['ID Loja', 'Quantidade']].groupby('ID Loja').sum()

        # Ticket médio por produto em cada loja
        ticket_medio = (faturamento_loja['Valor Final'] / quantidade_prod_loja['Quantidade']).to_frame()
        ticket_medio = ticket_medio.rename(columns={0: 'Ticket Médio'})

        # Send Email
        logging.info("Preparing email...")
        try:
            outlook = win32.Dispatch('outlook.application')
            mail = outlook.CreateItem(0)
            mail.To = 'vipistori@gmail.com' # Could be argument or input
            mail.Subject = 'Relatório de Vendas por Loja'
            mail.HTMLBody = f'''
            <p>Prezados,</p>

            <p>Segue o Relatório de Vendas por cada Loja.</p>

            <p>Faturamento:</p>
            {faturamento_loja.to_html(formatters={'Valor Final': 'R${:,.2f}'.format})}

            <p>Quantidade Vendida:</p>
            {quantidade_prod_loja.to_html()}

            <p>Ticket Médio dos Produtos em cada Loja:</p>
            {ticket_medio.to_html(formatters={'Ticket Médio': 'R${:,.2f}'.format})}

            <p>Qualquer dúvida, estou a disposição.</p>

            <p>Att,</p>
            <p>Vitória.</p>
            '''

            logging.info("Sending email via Outlook...")
            mail.Send()
            logging.info("Email sent successfully!")

        except Exception as e:
            logging.error(f"Failed to send email via Outlook. Ensure Outlook is installed and configured. Error: {e}")
            logging.info("Generated Report Preview:")
            print("-" * 30)
            print("FATURAMENTO:")
            print(faturamento_loja)
            print("-" * 30)

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()