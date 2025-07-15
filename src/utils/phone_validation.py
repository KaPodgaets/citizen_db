import re
import pandas as pd


def validate_and_format_israeli_phone(phone_str):
    """
    Validate Israeli phone numbers and format them with dashes
    
    Args:
        phone_str: Phone number string to validate and format
        
    Returns:
        tuple: (formatted_number, type) or (None, None) for invalid numbers
        
    Examples:
        >>> validate_and_format_israeli_phone("0501234567")
        ('050-1234567', 'mobile')
        >>> validate_and_format_israeli_phone("021234567")
        ('02-1234567', 'home')
        >>> validate_and_format_israeli_phone("0771234567")
        ('077-1234567', 'digital')
    """
    if pd.isna(phone_str):
        return None, None

    # Clean the input: remove all non-digit characters
    phone = re.sub(r'[^\d]', '', str(phone_str).strip())

    if not phone.isdigit():
        return None, None

    # Normalize mobile (05x)
    if re.match(r'^05\d{8}$', phone):
        return f'{phone[:3]}-{phone[3:]}', 'mobile'

    # Normalize digital (077)
    if re.match(r'^077\d{7}$', phone):
        return f'{phone[:3]}-{phone[3:]}', 'digital'

    # Normalize home (01–09, but not 05 or 077)
    if re.match(r'^0[2-4,6-9]\d{7}$', phone):
        return f'{phone[:2]}-{phone[2:]}', 'home'
    if re.match(r'^[2-4,6-9]\d{6}$', phone):  # local number, like 2123456
        return f'0{phone[0]}-{phone[1:]}', 'home'

    # Edge case: already dashed short mobile format like 5x-xxxxxxx
    if re.match(r'^5\d-\d{7}$', phone_str):
        cleaned = phone.replace('-', '')
        return f'{cleaned[:3]}-{cleaned[3:]}', 'mobile'

    # Edge case: already dashed short home format like 2-xxxxxxx
    if re.match(r'^[2-4,6-9]-\d{7}$', phone_str):
        cleaned = phone.replace('-', '')
        return f'0{cleaned[0]}-{cleaned[1:]}', 'home'

    # Edge case: 77-xxxxxxx
    if re.match(r'^77-\d{7}$', phone_str):
        cleaned = phone.replace('-', '')
        return f'077-{cleaned[2:]}', 'digital'

    return None, None


def process_israeli_phone_numbers(phone_df, phone_number_column='phone_number'):
    """
    Process a DataFrame containing phone numbers to validate and format Israeli numbers
    
    Args:
        phone_df: DataFrame containing phone numbers
        phone_number_column: Name of the column containing phone numbers
        
    Returns:
        DataFrame: Processed DataFrame with formatted numbers and type classification
    """
    if phone_df.empty:
        return pd.DataFrame(columns=['citizen_id', 'phone_number', 'type'])
    
    # Apply validation and formatting
    phone_df[['formatted_number', 'type']] = phone_df[phone_number_column].apply(
        lambda x: pd.Series(validate_and_format_israeli_phone(x))
    )
    
    # Keep only valid Israeli numbers
    phone_df = phone_df.dropna(subset=['formatted_number'])
    phone_df = phone_df.drop(columns=['phone_number'])
    
    # Rename columns and select final structure
    phone_df = phone_df.rename(columns={'formatted_number': 'phone_number'})
    phone_df = phone_df[['citizen_id', 'phone_number', 'type']]
    
    return phone_df 