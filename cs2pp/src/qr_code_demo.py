from out.qr_code_print_console import print_on_console
from out.qr_code_print_plot import print_to_plot
from out.qr_code_print_svg import print_to_file, get_svg_str
from core.qr_code_builder import encode_text
from data_logger.data_logger import DataLogger


text0 = "abcdefghijklmno"   

text1 = "known"
text2 = "We've succeeded!"
text3 = "~¡256_-_aA&ñ"
text4 = "From α to ɷ..."
text5 = "Sugarplum_Fairy_Nightmare"
qr = None
with DataLogger(text4) as dl:
    qr = encode_text(text4)
    dl.update_log(qr)

# write(dl.get_log().get_csv_line()) ## write to file
#print_on_console(qr._matrix)
print_to_plot(qr._matrix,"./src/out/qr_code.png")

    

#print_to_file(qr._matrix, "out/qr_code.svg")