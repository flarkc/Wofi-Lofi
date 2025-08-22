import subprocess as s
import mpv
import json
from pathlib import Path

class RadioPlayer:
    def __init__(self):
        self.directory = Path(__file__).parent.absolute()
        self.config_file = f'{self.directory}/radios.json'
        self.player = mpv.MPV()
        self.radios = self.load_stations()
    
    def load_stations(self) -> dict:
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading radios: {e}")
            return {}
    
    def get_choicelist(self):
        stations = list(self.radios.keys())
        stations.append('⚙️ CONFIGURE STATIONS')
        return '\n'.join(stations)

    def show_menu(self):        
        self.choicelist = self.get_choicelist()
        self.menu = s.run(
            ["wofi", "--show", "dmenu", "-i", "Select radio station:"],
            input=self.choicelist,
            capture_output=True,
            text=True)

        if self.menu.returncode == 0:
            return self.menu.stdout.strip()

    def track_title_observer(self, property, value) -> None:
        
        if property == 'metadata' and value:
            try:
                if len(str(value['icy-title']).split(' ')) != 1: 
                    print(value['icy-title'])
                    s.run(['notify-send', f"{self.current_station} Radio", f'Now playing: {value['icy-title']}', "--icon=media-tape"])
            except KeyError as ex:
                print('Metadata not available yet')

    def configure_stations(self):
        s.run(['python3', f'{self.directory}/edit-stations.py'])

    def play_selected(self, station_name):
        self.current_station = station_name
        stream_url = self.radios.get(station_name)
        
        self.player.play(stream_url)
        self.player.observe_property('metadata', self.track_title_observer)
        self.player.wait_for_playback()


    def run(self) -> None:
        selection = self.show_menu()
        print(selection)
        if not selection:
            return
        if selection == '⚙️ CONFIGURE STATIONS':
            self.configure_stations()
            pass
        else:
            self.play_selected(selection)

def main():
    player = RadioPlayer()
    player.run()

if __name__ == "__main__":
    main()