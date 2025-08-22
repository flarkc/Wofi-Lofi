import subprocess as s
from pathlib import Path

directory = Path(__file__).parent.absolute()

s.run(["pkill", "-f", "python.*wofi-radio"])
s.run([f'python3', f'{directory}/wofi-radio.py'])