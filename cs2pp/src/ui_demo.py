import tkinter as tk
import os
from data_logger.data_logger import DataLogger
from core.qr_code_builder import encode_text
from out.qr_code_print_plot import print_to_plot

QR_CODE_PNG_FILE_PATH = "./src/out/qr_code.png"


def button_clicked(root, text):
    if text is None or text.strip() == "":
        return
    qr = None
    with DataLogger(text) as dl:
        qr = encode_text(text)
        dl.update_log(qr)
    print_to_plot(qr._matrix,QR_CODE_PNG_FILE_PATH)
    if os.path.exists(QR_CODE_PNG_FILE_PATH):
        qr_code_image = tk.PhotoImage(file=QR_CODE_PNG_FILE_PATH)
        image_label = tk.Label(root, image=qr_code_image)
        image_label.grid(row=3,column=0)
        root.pack()

os.remove(QR_CODE_PNG_FILE_PATH) if os.path.exists(QR_CODE_PNG_FILE_PATH) else None
root = tk.Tk()
root.title("First Tkinter Window")

message_label = tk.Label(root, text = 'Enter Text', font=('calibre',12, 'bold'))
message_label.grid(row=0,column=0)

text_box = tk.Text(root, height = 1, width = 30, font = ('calibre',20))
text_box.grid(row=1,column=0)

create_qr = tk.Button(root, text = "Generate Qr Code", command=lambda :button_clicked(root, text_box.get("1.0",'end-1c')))
create_qr.grid(row=2,column=0)

if os.path.exists(QR_CODE_PNG_FILE_PATH):
    qr_code_image = tk.PhotoImage(file=QR_CODE_PNG_FILE_PATH)
    image_label = tk.Label(root, image=qr_code_image)
    image_label.grid(row=5,column=0)


#optimise for center window
root.geometry(f"+600+400")
root.minsize(400, 400)


root.mainloop()