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
    
    # Convert to string and clean
    phone = str(phone_str).strip()
    
    # Remove any existing dashes, spaces, or other separators
    phone = re.sub(r'[^\d]', '', phone)
    
    # Israeli phone number patterns:
    # 05X-XXXXXXX (mobile: 10 digits total)
    # 0X-XXXXXXX (home: 9 digits total) 
    # 077-XXXXXXX (digital: 10 digits total)
    
    mobile_pattern = r'^05[0-9](\d{7})$'  # 05X + 7 digits
    home_pattern = r'^0[1-9](\d{7})$'     # 0X + 7 digits (X != 0)
    digital_pattern = r'^077(\d{7})$'     # 077 + 7 digits
    
    # Check patterns and format
    if re.match(mobile_pattern, phone):
        match = re.match(mobile_pattern, phone)
        formatted = f"05{phone[2]}-{match.group(1)}"
        return formatted, 'mobile'
    elif re.match(home_pattern, phone):
        match = re.match(home_pattern, phone)
        formatted = f"0{phone[1]}-{match.group(1)}"
        return formatted, 'home'
    elif re.match(digital_pattern, phone):
        match = re.match(digital_pattern, phone)
        formatted = f"077-{match.group(1)}"
        return formatted, 'digital'
    else:
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