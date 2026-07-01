import re
NUMERIC_REGEX: re.Pattern[str] = re.compile(r"[0-9]*")
ALPHANUMERIC_REGEX: re.Pattern[str] = re.compile(r"[A-Z0-9 $%*+./:-]*")
# Dictionary of "0"->0, "A"->10, "$"->37, etc.
ALPHANUMERIC_ENCODING_TABLE: dict[str,int] = {ch: i for (i, ch) in enumerate("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:")}

def is_numeric(text):
	return NUMERIC_REGEX.fullmatch(text) is not None
	
def is_alphanumeric(text):
		return ALPHANUMERIC_REGEX.fullmatch(text) is not None

def encode(ch):
    return ALPHANUMERIC_ENCODING_TABLE.get(ch)

