def get_bit(value, position):
    return (value >> position) & 1 != 0


def get_bits(value, count):
	bits = []
	for i in reversed(range(count)):
		bits.append((value >> i) & 1)
	return bits

def append_bits(bits, value, count) :
	bits.extend(get_bits(value, count))
	return bits