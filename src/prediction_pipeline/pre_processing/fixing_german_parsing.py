import pandas as pd
import re

def parse_german_dates_regex(
    df: pd.DataFrame,
    date_column_name: str
) -> pd.DataFrame:
    """
    Parses German dates in the specified date column of the DataFrame using regex,
    including hours and minutes if available.

    Args:
        df (pd.DataFrame): The DataFrame containing the date column.
        date_column_name (str): The name of the date column.

    Returns:
        pd.DataFrame: The DataFrame with parsed German dates.
    """
    
    # Define a mapping of German month names to their numeric values
    month_map = {
        "Jan.": "01",
        "Feb.": "02",
        "März": "03",
        "Apr.": "04",
        "Mai": "05",
        "Juni": "06",
        "Juli": "07",
        "Aug.": "08",
        "Sep.": "09",
        "Okt.": "10",
        "Nov.": "11",
        "Dez.": "12"
    }

    # Create a regex pattern for replacing months and capturing time
    pattern = re.compile(r'(\d{1,2})\.\s*(' + '|'.join(month_map.keys()) + r')\s*(\d{4})\s*(\d{2}):(\d{2})')

    # Function to replace the month in the matched string and keep the time part
    def replace_month(match):
        day = match.group(1)
        month = month_map[match.group(2)]
        year = match.group(3)
        hour = match.group(4)
        minute = match.group(5)
        return f"{year}-{month}-{day} {hour}:{minute}:00"

    # Apply regex replacement and convert to datetime
    df[date_column_name] = df[date_column_name].apply(lambda x: replace_month(pattern.search(x)) if pattern.search(x) else x)
    df[date_column_name] = pd.to_datetime(df[date_column_name], errors='coerce')

    return df