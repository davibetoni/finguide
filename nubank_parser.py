import fitz
import re
from utils import normalize_text, parse_amount

def extract_nubank_transactions(pdf_path):
    doc = fitz.open(pdf_path)
    lines = [line.strip() for page in doc for line in page.get_text().splitlines()]
    transactions = []

    month_map = {
        'JAN': '01', 'FEV': '02', 'MAR': '03', 'ABR': '04',
        'MAI': '05', 'JUN': '06', 'JUL': '07', 'AGO': '08',
        'SET': '09', 'OUT': '10', 'NOV': '11', 'DEZ': '12'
    }

    ignore_if_description_contains = [
        'saldo em aberto',
        'fatura anterior',
        'proxima fatura',
        'valor total',
        'encargos',
        'pagamento recebido',
        'pagamento em',
        'saldo restante',
        'resumo da fatura',
        'pagamento minimo']
    
    i = 0
    while i < len(lines):
        line = lines[i]
        match_date = re.match(r'(\d{2}) (\w{3})', line) 

        if match_date:
            day, mon = match_date.groups() 
            month = month_map.get(mon.upper(), '01')
            date_str = f"{day}/{month}/2025"

            chunk = [line]
            for j in range(1, 4):
                if i + j < len(lines):
                    next_line = lines[i + j].strip()
                    if not next_line or re.match(r'^\d{2} \w{3}', next_line):
                        break
                    chunk.append(next_line)

            full_text = ' '.join(chunk)
            match = re.search(r'\d{2} \w{3}.*?([\w\s\-\*\.\!]+?)\s*(?:- Parcela \d+/\d+)?\s*R\$ ([\d.,]+)', full_text)
            if match:
                desc, amount = match.groups()

                if any(kw in desc.lower() for kw in ignore_if_description_contains):
                    i += len(chunk)
                    continue

                transactions.append({
                    'date': date_str,
                    'description': normalize_text(desc.strip()),
                    'amount': parse_amount(amount),
                    'source': 'Nubank'
                })

            i += len(chunk)
        else:
            i += 1

    return transactions
