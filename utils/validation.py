import re

def validate_iban_format(iban: str) -> bool:
    iban = iban.replace(" ", "").upper()
    if not re.match(r"^[A-Z]{2}[0-9]{2}[A-Z0-9]{11,30}$", iban):
        return False
    rearranged = iban[4:] + iban[:4]
    numeric_iban = ''
    for c in rearranged:
        numeric_iban += str(ord(c) - 55) if c.isalpha() else c
    return int(numeric_iban) % 97 == 1

def validate_bic_format(bic: str) -> bool:
    bic = bic.strip().upper()
    return bool(re.match(r"^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?$", bic))
