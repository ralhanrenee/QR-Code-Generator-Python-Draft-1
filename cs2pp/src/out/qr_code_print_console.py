WHITE 			= "\u2588\u2588"
BLACK 			= "  "
PRINT_BORDER 	= 4


def print_on_console(matrix:list[list[bool]]):
	"""
	Prints a QR code matrix to the console using character representations.
		
		This function takes a 2D boolean matrix representing a QR code and prints it
		to the console, where True values are represented as BLACK characters and 
		False values as WHITE characters. A border of WHITE characters is added around
		the QR code based on the PRINT_BORDER constant.
		
		Args:
			matrix (list[list[bool]]): A 2D list of boolean values where True represents
									   a black module and False represents a white module
									   in the QR code.
		
		Returns:
			None
	"""
	size = len(matrix)
	for r in range(-PRINT_BORDER, size + PRINT_BORDER):
		for c in range(-PRINT_BORDER, size + PRINT_BORDER):
			value = WHITE
			if r >=0  and c >= 0 and r < size and c < size:
				value = BLACK if matrix[r][c] else WHITE
			print(value, end="")
		print()
	print()

			
	


		

	
