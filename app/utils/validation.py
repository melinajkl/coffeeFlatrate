"""Validators for bank details such as IBAN and BIC formats."""
import re


def validate_iban_format(iban: str) -> bool:
    """
    Validates the format and checksum of an IBAN (International Bank Account Number).

    Args:
        iban (str): The IBAN string to validate.

    Returns:
        bool: True if the IBAN is valid, False otherwise.
    """
    iban = iban.replace(" ", "").upper()
    if not re.match(r"^[A-Z]{2}[0-9]{2}[A-Z0-9]{11,30}$", iban):
        return False

    # Rearrange and convert to integer string
    rearranged = iban[4:] + iban[:4]
    numeric_iban = ''
    for c in rearranged:
        numeric_iban += str(ord(c) - 55) if c.isalpha() else c

    # Modulo 97 check
    return int(numeric_iban) % 97 == 1


def validate_bic_format(bic: str) -> bool:
    """
    Validates the format of a BIC (Bank Identifier Code, also known as SWIFT code).

    Args:
        bic (str): The BIC string to validate.

    Returns:
        bool: True if the BIC format is valid, False otherwise.
    """
    bic = bic.strip().upper()
    return bool(re.match(r"^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?$", bic))
