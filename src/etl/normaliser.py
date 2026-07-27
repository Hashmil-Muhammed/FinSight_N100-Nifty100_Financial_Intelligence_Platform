import re


def normalize_ticker(ticker: str) -> str:
    """
    Cleans and standardizes the company ticker symbol.
    Example: " tcs " -> "TCS"
    """
    if not isinstance(ticker, str):
        ticker = str(ticker)

    # Remove leading/trailing whitespaces and convert to uppercase
    return ticker.strip().upper()


def normalize_year(year_str) -> str:
    """
    Standardizes various year formats to a uniform 'YYYY-MM' format.
    Examples:
    'Mar-23' -> '2023-03'
    'FY23' -> '2023-03'
    '2023' -> '2023-03'
    'Dec-22' -> '2022-12'
    """
    year_str = str(year_str).strip()

    # Return as-is if it already matches 'YYYY-MM' format
    if re.match(r"^\d{4}-\d{2}$", year_str):
        return year_str

    # Handle 'FY23' or 'FY2023' -> assume March year-end ('2023-03')
    if year_str.upper().startswith("FY"):
        yr = year_str[2:].strip()
        if len(yr) == 2:
            return f"20{yr}-03"
        elif len(yr) == 4:
            return f"{yr}-03"

    # Handle pure year strings like '2023' -> '2023-03'
    if re.match(r"^\d{4}$", year_str):
        return f"{year_str}-03"

    # Handle formats like 'Mar-23', 'March-2023', 'Dec-22'
    month_map = {
        "JAN": "01",
        "FEB": "02",
        "MAR": "03",
        "APR": "04",
        "MAY": "05",
        "JUN": "06",
        "JUL": "07",
        "AUG": "08",
        "SEP": "09",
        "OCT": "10",
        "NOV": "11",
        "DEC": "12",
    }

    match = re.search(r"([A-Za-z]+)[\s\-]*(\d{2,4})", year_str)
    if match:
        month_str = match.group(1)[:3].upper()  # Extract first 3 letters of the month
        year_part = match.group(2)

        month = month_map.get(month_str, "03")

        # Convert 2-digit year to 4-digit year (e.g., 23 -> 2023)
        if len(year_part) == 2:
            year = f"20{year_part}"
        else:
            year = year_part

        return f"{year}-{month}"

    # Return PARSE_ERROR if format is completely unrecognized (Caught later by Validator)
    return "PARSE_ERROR"
