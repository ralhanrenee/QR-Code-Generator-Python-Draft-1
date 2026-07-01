def apply_mask(qr_code, mask_function):
	for y in range(qr_code._size):
		for x in range(qr_code._size):
			qr_code._matrix[y][x] ^= (mask_function(x, y) == 0) and (not qr_code._isfunction[y][x])