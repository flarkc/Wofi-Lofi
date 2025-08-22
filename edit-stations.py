import subprocess as s
import json
from pathlib import Path

directory = Path(__file__).parent.absolute()

def add_station():
    name = s.run(['wofi', '--dmenu'], input='Enter the name for the new station\n', capture_output=True, text=True)
    url = s.run(['wofi', '--dmenu'], input='Paste the streaming url for your station\n', capture_output=True, text=True)

    name = name.stdout.strip('\n')
    url = url.stdout.strip('\n')

    if name != 'Enter the name for the new station' and url != 'Paste the streaming url for your station':
        with open(f'{directory}/radios.json', 'r+', encoding='utf-8') as f:
            radios = json.load(f)
            radios[name] = url
            f.seek(0)
            json.dump(radios, f, ensure_ascii=False, indent=4)


def rm_station():
    stations = []
    
    with open(f'{directory}/radios.json', 'r', encoding='utf-8') as f:
        radios = json.load(f)
   
    for i in radios:
        stations.append(i)

    choicelist = '\n'.join(stations)
    p1 = s.Popen(["echo", choicelist], stdout=s.PIPE)
    p2 = s.run(['wofi', '--dmenu'], stdin=p1.stdout, capture_output=True, text=True)
    p1.stdout.close()
    name = p2.stdout.strip('\n')
  
    with open(f'{directory}/radios.json', 'r+', encoding='utf-8') as f:
        radios = json.load(f)
        del radios[name]
        f.seek(0)
        json.dump(radios, f, ensure_ascii=False, indent=4)
        f.truncate()
            

options = {
    'Add a new station': add_station,
    'Remove a station': rm_station  
}

for i in options:
    options_list = '\n'.join(options)

p1 = s.Popen(['echo', options_list], stdout=s.PIPE)
p2 =s.run(['wofi', '--show', 'dmenu', '-i'], stdin=p1.stdout, stdout=s.PIPE)
p1.stdout.close()
output = (p2.stdout).decode()
function_to_call = options[str(output).strip('\n')]
function_to_call()