import re
import pdfplumber
from utils import normalize_text, parse_amount

def extract_inter_transactions(pdf_path, password):
    pdf = pdfplumber.open(pdf_path, password=password)
    text = ''.join(page.extract_text() for page in pdf.pages)

    pattern = r'(\d{2} de \w+\. \d{4})\s+(.*?)\s+-\s+R\$ ([\d\.,]+)|(\d{2} de \w+\. \d{4})\s+(.*?)\s+R\$ ([\d\.,]+)'
    matches = re.findall(pattern, text)

    raw_transactions = []

    for match in matches:
        date = match[0] or match[3]
        desc = match[1] or match[4]
        value = match[2] or match[5]

        raw_transactions.append({
            "date": date.strip(),
            "description": normalize_text(desc.strip()),
            "value_str": value.strip(),
            "is_refund": '+' in desc
        })

    final_transactions = []
    used_indexes = set()

    for i, t in enumerate(raw_transactions):
        if i in used_indexes:
            continue

        if t["is_refund"]:
            continue

        for j, r in enumerate(raw_transactions):
            if j in used_indexes or i == j:
                continue

            if (r["is_refund"]
                and r["date"] == t["date"]
                and r["value_str"] == t["value_str"]
                and r["description"].replace(' - +', '') == t["description"]):
                used_indexes.update({i, j})
                break
        else:
            final_transactions.append({
                "date": t["date"],
                "description": t["description"],
                "amount": parse_amount(t["value_str"]),
                "source": "Inter"
            })

    return final_transactions