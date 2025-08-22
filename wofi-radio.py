import subprocess as s
import mpv
import json
from pathlib import Path

choicelist = []
stations = []
directory = Path(__file__).parent.absolute()

player = mpv.MPV()

with open(f'{directory}/radios.json', 'r', encoding='utf-8') as f:
    radios = json.load(f)

for i in radios:
    stations.append(i)

stations.append('⚙️ CONFIGURE STATIONS')
choicelist = '\n'.join(stations)

p1 = s.Popen(["echo", choicelist], stdout=s.PIPE)
p2 = s.Popen(["wofi", "-dmenu", "-i"], stdin=p1.stdout, stdout=s.PIPE)
p1.stdout.close()

output = p2.communicate()[0].decode()[:-1]

if output == '⚙️ CONFIGURE STATIONS':
    s.run(['python3', f'{directory}/edit-stations.py'])
else:
    stream_url = str((radios.get(output)))

    def track_title_observer(property, value):
        if property == 'metadata' and value:
            try:
                if len(str(value['icy-title']).split(' ')) != 1: 
                    print(value['icy-title'])
                    s.run(['notify-send', f"{output} Radio", f'Now playing: {value['icy-title']}', "--icon=media-tape"])
            except KeyError as ex:
                print('Key error')

    player.play(stream_url)
    player.observe_property('metadata', track_title_observer)

    player.wait_for_playback()