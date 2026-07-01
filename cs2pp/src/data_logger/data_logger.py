import time
import uuid


LOG_CSV_FILE_NAME = "./src/data_logger/data_log.csv"

class Log:
    def __init__(self, text_content):
        self.timestamp = time.time()
        self.unique_ID = uuid.uuid4()
        self.text_content = text_content
        self.version = None
        self.error_correction_level = None
        self.mask_pattern = None
        self.user_selected_options = None
        self.generation_success = False

    def get_csv_line(self):
        return f"{self.timestamp},{self.unique_ID},{self.text_content},{self.version},{self.error_correction_level},{self.mask_pattern},{self.user_selected_options},{self.generation_success}\n"
    

class DataLogger:
    def __init__(self, text_content):
        self.text_content = text_content
        
    def __enter__(self):
        self.log = Log(self.text_content)
        return self

    def get_log(self):
        return self.log

    def update_log(self, qr):
        self.log.version = qr._version
        self.log.error_correction_level = qr._error_correction_level
        self.log.mask_pattern = qr._mask
        self.log.generation_success = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(LOG_CSV_FILE_NAME, "a") as f:
            f.write(self.log.get_csv_line())


def from_csv_line(line):
        log = Log("")
        fields = line.strip().split(',')
        log.timestamp = float(fields[0])
        log.unique_ID = uuid.UUID(fields[1])
        log.text_content = fields[2]
        log.version = fields[3]
        log.error_correction_level = fields[4]
        log.mask_pattern = fields[5]
        log.user_selected_options = fields[6]
        log.generation_success = fields[7].lower() == 'true'
        return log