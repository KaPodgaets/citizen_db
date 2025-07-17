import pandas as pd
import re

def clean_phone_number(series: pd.Series) -> pd.Series:
    """
    Cleans phone numbers by removing non-numeric characters and standardizing format.
    """
    return series.astype(str).str.replace(r'\D', '', regex=True)

def clean_email(series: pd.Series) -> pd.Series:
    """
    Cleans email addresses by trimming whitespace and converting to lowercase.
    """
    return series.astype(str).str.strip().str.lower()

# Add more cleansing functions as needed for other business rules 