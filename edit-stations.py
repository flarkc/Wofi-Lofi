import subprocess as s
import json
from pathlib import Path
from wofi_radio import RadioPlayer

class StationsConfiguration:
    def __init__(self):
        self.directory = Path(__file__).parent.absolute()
        self.config_file = f'{self.directory}/radios.json'
        self.options = {
            'Add a new station': self.add_station,
            'Remove a station': self.rm_station  
        }
        self.options_list = list(self.options.keys())

    def select_operation(self):
        self.choicelist = '\n'.join(self.options_list)
        opr_choice =s.run(
            ['wofi', '--show', 'dmenu', '-i'],
            input=self.choicelist,
            text=True, stdout=s.PIPE)
        
        if opr_choice.returncode == 0:
            return opr_choice.stdout.strip()

    def call_selected(self):
        function_to_call = self.options[self.select_operation()]
        function_to_call()

    def add_station(self):
        name = s.run(['wofi', '--dmenu'], input='Enter the name for the new station', capture_output=True, text=True)
        url = s.run(['wofi', '--dmenu'], input='Paste the streaming url for your station', capture_output=True, text=True)

        name = name.stdout.strip('\n')
        url = url.stdout.strip('\n')

        if name != 'Enter the name for the new station' and url != 'Paste the streaming url for your station':
            with open(self.config_file, 'r+', encoding='utf-8') as f:
                radios = json.load(f)
                radios[name] = url
                f.seek(0)
                json.dump(radios, f, ensure_ascii=False, indent=4)

    def rm_station(self):
        stations = RadioPlayer.load_stations(self)

        choicelist = '\n'.join(stations)
        choice = s.run(['wofi', '--show', 'dmenu', '-i'], input=choicelist, capture_output=True, text=True)
        name = choice.stdout.strip('\n')

        with open(self.config_file , 'r+', encoding='utf-8') as f:
            radios = json.load(f)
            del radios[name]
            f.seek(0)
            json.dump(radios, f, ensure_ascii=False, indent=4)
            f.truncate()

def main():
    config = StationsConfiguration()
    config.call_selected()

if __name__ == "__main__":
    main()