from utils.qr_code_text_utils import is_numeric, is_alphanumeric, encode
from collections.abc import Sequence
from utils.qr_code_bit_utils import append_bits, get_bit

NUMERIC 		= 1
ALPHANUMERIC 	= 2
BYTE 			= 4


class QrSegment:
	_mode: int
	_numchars: int
	_bits: list[int]
	
	def __init__(self, mode, numchars, bits):
		self._mode = mode
		self._numchars = numchars
		self._bits = list(bits)  # Make defensive copy
	
	def get_mode(self):
		return self._mode
	
	def get_num_chars(self):
		return self._numchars
	
	def get_bits(self):
		return list(self._bitdata)  # Make defensive copy
	