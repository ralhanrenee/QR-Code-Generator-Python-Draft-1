
import itertools
from utils.qr_code_bit_utils import append_bits
from extensions.qr_code_extension_utils import *
from core.qr_code import QrCode
from core.qr_code_segment_builder import build_segments

from schema.qr_code_masking import DEFAULT_MASK
from schema.qr_code_error_correction_level import DEFAULT_ERROR_CORRECTION_LEVEL
from schema.qr_code_version import DEFAULT_VERSION, MIN_VERSION, MAX_VERSION


def encode_text(text: str):
    segments = build_segments(text)
    return encode_segments(segments, DEFAULT_ERROR_CORRECTION_LEVEL, DEFAULT_VERSION, DEFAULT_MASK, False, False, False)

def encode_segments(segments, error_correction_level, version, mask, 
                    optimize_error_code_level, optimize_version, optimize_mask):
    bits = []
    version = get_optimized_version(segments, version, error_correction_level, MIN_VERSION, MAX_VERSION) if optimize_version else version
    error_correction_level = get_optimized_error_correction_level(segments, version, error_correction_level) if optimize_error_code_level else error_correction_level
    append_segments_bits(bits, segments, version)
    append_terminator_bits(bits, version, error_correction_level)
    append_alignment_bits(bits)
    append_padding_bits(bits, version, error_correction_level)
    bytes = bits_to_bytes(bits)
	# Create the QR Code object
    return QrCode(version, error_correction_level, mask, bytes, optimize_mask)


def append_segments_bits(bits, segments, version):
    # Concatenate all segments to create the data bit string
    for segment in segments:
        append_bits(bits, segment.get_mode(), 4) # Mode indicator is 4 bits
        append_bits(bits, segment.get_num_chars(), num_char_count_bits(segment.get_mode(), version)) # Character count indicator
        bits.extend(segment._bits)


def append_terminator_bits(bits, version, error_correction_level):
    datacapacitybits = get_data_capacity_bits(version, error_correction_level)
    # Add terminator and pad up to a byte if applicable
    reminingbits = datacapacitybits - len(bits)
    reminingbits = min(4, reminingbits) # Terminator is at most 4 bits
    append_bits(bits, 0, reminingbits) # Terminator remaining bits
    

def append_alignment_bits(bits):
    # Byte-align the data
    alignment_bits_length = 8 - (len(bits) % 8) if len(bits) % 8 != 0 else 0
    append_bits(bits, 0, alignment_bits_length)  # Byte alignment


def append_padding_bits(bits, version, error_correction_level):
    datacapacitybits = get_data_capacity_bits(version, error_correction_level)
    # Pad with alternating bytes until data capacity is reached
    for padbyte in itertools.cycle((0xEC, 0x11)):
        if len(bits) >= datacapacitybits:
            break
        append_bits(bits, padbyte, 8)


def bits_to_bytes(bits):
    # Pack bits into bytes in big endian
    bytes = bytearray([0] * (len(bits) // 8))
    for (i, bit) in enumerate(bits):
        bytes[i >> 3] |= bit << (7 - (i & 7))
    return bytes