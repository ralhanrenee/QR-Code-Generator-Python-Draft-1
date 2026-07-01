def reed_solomon_compute_divisor(degree):
	"""Returns a Reed-Solomon ECC generator polynomial for the given degree. This could be
	implemented as a lookup table over all possible parameter values, instead of as an algorithm."""
	# Polynomial coefficients are stored from highest to lowest power, excluding the leading term which is always 1.
	# For example the polynomial x^3 + 255x^2 + 8x + 93 is stored as the uint8 array [255, 8, 93].
	result = bytearray([0] * (degree - 1) + [1])  # Start off with the monomial x^0
	
	# Compute the product polynomial (x - r^0) * (x - r^1) * (x - r^2) * ... * (x - r^{degree-1}),
	# and drop the highest monomial term which is always 1x^degree.
	# Note that r = 0x02, which is a generator element of this field GF(2^8/0x11D).
	root: int = 1
	for _ in range(degree):  # Unused variable i
		# Multiply the current product by (x - r^i)
		for j in range(degree):
			result[j] = reed_solomon_multiply(result[j], root)
			if j + 1 < degree:
				result[j] ^= result[j + 1]
		root = reed_solomon_multiply(root, 0x02)
	return result
	
	
	
def reed_solomon_compute_remainder(data, divisor):
	"""Returns the Reed-Solomon error correction codeword for the given data and divisor polynomials."""
	result = bytearray([0] * len(divisor))
	for b in data:  # Polynomial division
		factor: int = b ^ result.pop(0)
		result.append(0)
		for (i, coef) in enumerate(divisor):
			result[i] ^= reed_solomon_multiply(coef, factor)
	return result
	
	
	
def reed_solomon_multiply(x, y):
	"""Returns the product of the two given field elements modulo GF(2^8/0x11D). The arguments and result
	are unsigned 8-bit integers. This could be implemented as a lookup table of 256*256 entries of uint8."""
	# Russian peasant multiplication
	z: int = 0
	for i in reversed(range(8)):
		z = (z << 1) ^ ((z >> 7) * 0x11D)
		z ^= ((y >> i) & 1) * x
	assert z >> 8 == 0
	return z