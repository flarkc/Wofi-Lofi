import subprocess as s
from pathlib import Path

directory = Path(__file__).parent.absolute()

s.run(["pkill", "-f", "python.*wofi_radio"])
s.run([f'python3', f'{directory}/wofi_radio.py'])