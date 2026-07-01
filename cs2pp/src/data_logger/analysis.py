from .data_logger import *
import pandas as pd
import matplotlib.pyplot as plt

def get_logs_from_file():
    logs = []
    with open(LOG_CSV_FILE_NAME, "r") as f:
        for line in f:
            log = from_csv_line(line)
            logs.append(log)
    return logs

def show_bar_chart():
    #bar chart is for ECC only
    logs = get_logs_from_file()
    df = pd.DataFrame([{
        "timestamp": log.timestamp,
        "version": log.version,
        "error_correction_level": log.error_correction_level,
        "mask_pattern": log.mask_pattern,
        "generation_success": log.generation_success
    } for log in logs])
    
    error_counts = df['error_correction_level'].value_counts()
    error_counts.plot(kind='bar', title='QR Code Error Correction Level Counts')
    #success_counts = df['generation_success'].value_counts()
    #success_counts.plot(kind='bar', title='QR Code Generation Success Counts')

    
    plt.show()

def show_line_chart():
    logs = get_logs_from_file()
    df = pd.DataFrame([{
        "timestamp": log.timestamp,
        "version": log.version,
        "error_correction_level": log.error_correction_level,
        "mask_pattern": log.mask_pattern,
        "generation_success": log.generation_success
    } for log in logs])

    #success_counts = df['generation_success'].value_counts()
    success_counts = df.groupby('timestamp')['generation_success'].sum()
    success_counts.plot(kind='line', title='QR Code Generation Success Counts')
    plt.show()

if __name__ == "__main__":
    #show_bar_chart()
    show_line_chart()