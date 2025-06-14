import os
import pandas as pd
from inter_parser import extract_inter_transactions
from nubank_parser import extract_nubank_transactions
from utils import categorize
from datetime import datetime
import xlsxwriter

def parse_invoice(file_path, invoice_type, password=None):
    try:
        if invoice_type == "Inter":
            transactions = extract_inter_transactions(file_path, password)
        elif invoice_type == "Nubank":
            transactions = extract_nubank_transactions(file_path)
        else:
            return pd.DataFrame()  # tipo inválido
    except Exception as e:
        print("Erro ao extrair fatura:", e)
        return pd.DataFrame()

    if not transactions:
        return pd.DataFrame(columns=["date", "description", "amount", "category", "source"])

    for t in transactions:
        t["category"] = categorize(t["description"])

    return pd.DataFrame(transactions)
