import matplotlib.pyplot as plt

SVG_BORDER 				= 4
BLACK_SQUARE_BLOCK		= "h1v1h-1z"
MOVE_COMMAND_FORMAT		= " M{col},{row}"
XML_HEADER 				= """<?xml version="1.0" encoding="UTF-8"?>"""
DOC_TYPE 				= """<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">"""
SVG_HEADER_FORMAT 		= """<svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="0 0 {svg_size} {svg_size}" stroke="none">"""
RECT_HEADER		 		= """<rect width="100%" height="100%" fill="#FFFFFF"/>"""
PATH_CONTENT 			= """<path d="{svg_path}" fill="#000000"/>"""
SVG_END 				= """</svg>"""

def get_svg_str(matrix) :
	size = len(matrix)
	svg_size = size + (2 * SVG_BORDER) # account for border on all sides
	svg_header =  SVG_HEADER_FORMAT.format(svg_size= svg_size) # format svg header with size
	svg_path = get_svg_path(matrix)
	path_content = PATH_CONTENT.format(svg_path = svg_path)
	return "\n".join([XML_HEADER, DOC_TYPE, svg_header, RECT_HEADER, path_content, SVG_END])

def get_svg_path(matrix) :
	size = len(matrix)
	blocks = []
	for r in range(size):
		for c in range(size):
			if matrix[r][c]:
				row = r + SVG_BORDER
				col = c + SVG_BORDER
				move_command = MOVE_COMMAND_FORMAT.format(row=row, col=col)
				blocks.append(move_command + BLACK_SQUARE_BLOCK)
	return "".join(blocks)

def print_to_file(matrix:list[list[bool]], file_path: str) -> None:
	svg_str = get_svg_str(matrix)
	print_image_to_file(svg_str, file_path)

def print_image_to_file(data, file_path: str) -> None:
	with open(file_path, "w", encoding="utf-8") as f:
		f.write(data)