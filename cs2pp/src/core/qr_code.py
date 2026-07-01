from __future__ import annotations
from collections.abc import Sequence
from utils.qr_code_bit_utils import get_bit
from extensions.qr_code_extension_utils import *
from utils.qr_code_masking_utils import apply_mask
from utils.qr_code_solomon_utils import *


class QrCode:
	def __init__(self, version, error_correction_level, mask,  datacodewords, optimize_mask):
		self._version = version
		self._error_correction_level = error_correction_level
		self._mask = mask
		self._size = get_size(version)
		
		# Initialize both grids to be size*size arrays of Boolean false
		self._matrix    = [[False] * self._size for _ in range(self._size)]  # Initially all light
		# Indicates function modules that are not subjected to masking.
		self._isfunction = [[False] * self._size for _ in range(self._size)]
		
		# draw modules            
		self._draw_function_patterns()
		allcodewords: bytes = self._add_ecc_and_interleave(bytearray(datacodewords))
		self._draw_codewords(allcodewords)

		self._mask = get_optimized_mask(self) if optimize_mask else mask
		apply_mask(self, get_mask_function(mask))  # Apply the final choice of mask
		self._draw_format_bits(mask)  # Overwrite old format bits
		
	
	def _draw_function_patterns(self):
		# Draw horizontal and vertical timing patterns
		for i in range(self._size):
			self._set_function_module(6, i, i % 2 == 0)
			self._set_function_module(i, 6, i % 2 == 0)
		
		# Draw 3 finder patterns (all corners except bottom right; overwrites some timing modules)
		self._draw_finder_pattern(3, 3)
		self._draw_finder_pattern(self._size - 4, 3)
		self._draw_finder_pattern(3, self._size - 4)
		
		# Draw numerous alignment patterns
		alignpatpos: list[int] = get_alignment_pattern_positions(self._version)
		numalign: int = len(alignpatpos)
		skips: Sequence[tuple[int,int]] = ((0, 0), (0, numalign - 1), (numalign - 1, 0))
		for i in range(numalign):
			for j in range(numalign):
				if (i, j) not in skips:  # Don't draw on the three finder corners
					self._draw_alignment_pattern(alignpatpos[i], alignpatpos[j])
		
		# Draw configuration data
		self._draw_format_bits(0)  # Dummy mask value; overwritten later in the constructor
		
	
	def _draw_format_bits(self, mask: int) -> None:
		"""
		Draws the format bits for the QR code, encoding the error correction level and mask pattern.
		
		The format bits consist of 15 bits: 5 data bits (2 for error correction level, 3 for mask pattern)
		followed by 10 error correction bits using BCH code with generator polynomial x^10 + x^8 + x^5 + x^4 + x^2 + x + 1.
		These bits are XORed with a fixed mask (0x5412) and placed in two redundant locations on the QR code matrix
		for robustness against damage and reading errors.
		
		The first copy is drawn around the top-left finder pattern, and the second copy along the bottom and right edges.
		
		Args:
		    mask (int): The mask pattern index (0-7) used for data masking.
		
		Note:
		    This method overwrites any existing format bits and sets function modules accordingly.
		"""
		# Calculate error correction code and pack bits
		data: int = get_format_bits(self._error_correction_level) | mask  # errCorrLvl is uint2, mask is uint3
		rem: int = data
		for _ in range(10):
			rem = (rem << 1) ^ ((rem >> 9) * 0x537)
		bits: int = (data << 10 | rem) ^ 0x5412  # uint15
		assert bits >> 15 == 0
		
		# Draw first copy
		for i in range(0, 6):
			self._set_function_module(8, i, get_bit(bits, i))
		self._set_function_module(8, 7, get_bit(bits, 6))
		self._set_function_module(8, 8, get_bit(bits, 7))
		self._set_function_module(7, 8, get_bit(bits, 8))
		for i in range(9, 15):
			self._set_function_module(14 - i, 8, get_bit(bits, i))
		
		# Draw second copy
		for i in range(0, 8):
			self._set_function_module(self._size - 1 - i, 8, get_bit(bits, i))
		for i in range(8, 15):
			self._set_function_module(8, self._size - 15 + i, get_bit(bits, i))
		self._set_function_module(8, self._size - 8, True)  # Always dark
	
	
	def _draw_finder_pattern(self, x: int, y: int) -> None:
		"""Draws a 9*9 finder pattern including the border separator,
		with the center module at (x, y). Modules can be out of bounds."""
		for dy in range(-4, 5):
			for dx in range(-4, 5):
				xx, yy = x + dx, y + dy
				if (0 <= xx < self._size) and (0 <= yy < self._size):
					# Chebyshev/infinity norm
					self._set_function_module(xx, yy, max(abs(dx), abs(dy)) not in (2, 4))
	
	
	def _draw_alignment_pattern(self, x: int, y: int) -> None:
		"""Draws a 5*5 alignment pattern, with the center module
		at (x, y). All modules must be in bounds."""
		for dy in range(-2, 3):
			for dx in range(-2, 3):
				self._set_function_module(x + dx, y + dy, max(abs(dx), abs(dy)) != 1)
	
	
	def _set_function_module(self, x: int, y: int, isdark: bool) -> None:
		"""Sets the color of a module and marks it as a function module.
		Only used by the constructor. Coordinates must be in bounds."""
		assert type(isdark) is bool
		self._matrix[y][x] = isdark
		self._isfunction[y][x] = True
	

	def _add_ecc_and_interleave(self, data: bytearray) -> bytes:
		# Calculate parameter numbers
		numblocks: int = get_num_error_correction_blocks(self._version, self._error_correction_level)
		blockecclen: int = get_error_codewords_per_block(self._version, self._error_correction_level)
		rawcodewords: int = get_num_raw_data_modules(self._version) // 8
		numshortblocks: int = numblocks - rawcodewords % numblocks
		shortblocklen: int = rawcodewords // numblocks
		
		# Split data into blocks and append ECC to each block
		blocks: list[bytes] = []
		rsdiv: bytes = reed_solomon_compute_divisor(blockecclen)
		k: int = 0
		for i in range(numblocks):
			dat: bytearray = data[k : k + shortblocklen - blockecclen + (0 if i < numshortblocks else 1)]
			k += len(dat)
			ecc: bytes = reed_solomon_compute_remainder(dat, rsdiv)
			if i < numshortblocks:
				dat.append(0)
			blocks.append(dat + ecc)
				
		# Interleave (not concatenate) the bytes from every block into a single sequence
		result = bytearray()
		for i in range(len(blocks[0])):
			for (j, blk) in enumerate(blocks):
				# Skip the padding byte in short blocks
				if (i != shortblocklen - blockecclen) or (j >= numshortblocks):
					result.append(blk[i])
		assert len(result) == rawcodewords
		return result
	
	
	def _draw_codewords(self, data: bytes) -> None:
		"""Draws the given sequence of 8-bit codewords (data and error correction) onto the entire
		data area of this QR Code. Function modules need to be marked off before this is called."""
		assert len(data) == get_num_raw_data_modules(self._version) // 8
		
		i: int = 0  # Bit index into the data
		# Do the zigzag pattern 
		for right in range(self._size - 1, 0, -2):  # Index of right column in each column pair
			if right <= 6:
				right -= 1
			for vert in range(self._size):  # Vertical counter
				for j in range(2):
					x: int = right - j  # Actual x coordinate
					upward: bool = (right + 1) & 2 == 0
					y: int = (self._size - 1 - vert) if upward else vert  # Actual y coordinate
					if (not self._isfunction[y][x]) and (i < len(data) * 8):
						self._matrix[y][x] = get_bit(data[i >> 3], 7 - (i & 7))
						i += 1
					# If this QR Code has any remainder bits (0 to 7), they were assigned as
					# 0/false/light by the constructor and are left unchanged by this method
		assert i == len(data) * 8
	
	