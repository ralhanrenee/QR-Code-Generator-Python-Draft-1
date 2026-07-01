from out.qr_code_print_console import print_on_console
from out.qr_code_print_plot import print_to_plot
from out.qr_code_print_svg import print_to_file, get_svg_str
from core.qr_code_builder import encode_text
from data_logger.data_logger import DataLogger

def generate_image(text):
    qr = None
    with DataLogger(text) as dl:
        qr = encode_text(text)
        dl.update_log(qr)

    print_to_plot(qr._matrix,"./src/out/qr_code.png")