from utils.qr_code_bit_utils import append_bits
from utils.qr_code_text_utils import is_alphanumeric, is_numeric, encode
from core.qr_code_segment import QrSegment, NUMERIC, ALPHANUMERIC, BYTE


def build_segments(text):
	if text == "":
		return []
	elif is_numeric(text):
		return [build_numeric(text)]
	elif is_alphanumeric(text):
		return [build_alphanumeric(text)]
	else:
		return [build_bytes(text.encode("UTF-8"))]
	
def build_numeric(digits):
		bits = list()
		i = 0
		while i < len(digits):  # Consume up to 3 digits per iteration
			n: int = min(len(digits) - i, 3)
			append_bits(bits, int(digits[i : i + n]), n * 3 + 1)
			i += n
		return QrSegment(NUMERIC, len(digits), bits)	

def build_alphanumeric(text):
		bits = list()
		for i in range(0, len(text) - 1, 2):  # Process groups of 2
			temp: int = encode(text[i]) * 45
			temp += encode(text[i + 1])
			append_bits(bits, temp, 11)
		if len(text) % 2 > 0:  # 1 character remaining
			append_bits(bits, encode(text[-1]), 6)
		return QrSegment(ALPHANUMERIC, len(text), bits)

	
def build_bytes(data):
    bits = list()
    for byte in data:
        append_bits(bits, byte, 8)
    return QrSegment(BYTE, len(data), bits)


def get_total_bits(segments):
	result = 0
	for segment in segments:
		ccbits: int = segment.num_char_count_bits()
		if segment.get_num_chars() >= (1 << ccbits):
			return None  # The segment's length doesn't fit the field's bit width
		result += 4 + ccbits + len(segment._bitdata)
	return result
	