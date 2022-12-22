import json
import rich



class EntryUI():
    
    DATA_FILE_NAME = 'data.json'
        
    @staticmethod
    def read_data() -> dict:
        with open(EntryUI.DATA_FILE_NAME,'r') as f:
            return json.load(f)

    @staticmethod
    def save_data(data: dict):
        with open(EntryUI.DATA_FILE_NAME,'w') as f:
            return json.dump(data ,f, indent=4)

    def __init__(self) -> None:
        self.data = EntryUI.read_data()
        self.main()
    
    def save(self):
        EntryUI.save_data(self.data)
    
    def print_existing(self):
        idx = 1
        print()
        print("[+] Existing substances:")
        for k,v in self.data.items():
            print(f'➡  {k.capitalize()}:')
            for subs in v:
                name = subs['name']
                enabled = subs['enabled']
                print(f'\t{idx} - {"✔" if enabled else "✖"} - {name}')
                idx += 1

    def list_data(self):
        array = []
        for k,v in self.data.items():
            for substance in v:
                array.append(substance)
        return array

    def add_substance(self):
        print("[+] Adding new substance")

        c_type = Prompt.ask("Select type: [P] for Polymer, [S] for Solvent")
        if c_type.lower() not in ['p', 's']:
            exit()
        _type = 'polymer' if c_type.lower() == 'p' else 'solvent'

        substanceData = {
            'name': Prompt.ask("Enter name for new substance"),
            'enabled': True,
            'd': FloatPrompt.ask("Enter D (decimal)"),
            'p': FloatPrompt.ask("Enter P (decimal)"),
            'h': FloatPrompt.ask("Enter H (decimal)"),
        }
        if _type == 'polymer':
            substanceData.update({
                'r': FloatPrompt.ask("Enter R (decimal)"),
            })

        self.data[_type].append(substanceData)
        self.save()

    
    def delete_substance(self, index):
        for k,v in self.data.items():
            if len(v) <= index:
                index -= len(v)
                continue
            del self.data[k][index]
            break
        self.save()
    
    def toggle_substance(self, index):
        for k,v in self.data.items():
            if len(v) <= index:
                index -= len(v)
                continue
            self.data[k][index]['enabled'] = not self.data[k][index]['enabled']
            break
        self.save()
    
    def main(self):
        # show data in a list, separated by the type
        # let user add or select any one from list
        # when selected can be enabled/disabled or deleted
        
        # rich.print_json(json.dumps(self.data)) # DEBUG
        
        self.print_existing()
        
        data_listing = self.list_data()
        try:
            choice = Prompt.ask(f"[A] to add, [1-{len(data_listing)}] to select a substance, [X] to exit", default="x")
        except:
            exit()
        
        # print('you chose: ', choice)
        
        if choice.lower() == 'a':
            # Add
            return self.add_substance()
        elif choice.lower() == 'x':
            exit()
        
        # Try parse to int
        try:
            choice = int(choice)
            if choice < 0 or choice > len(data_listing):
                print("Out of range")
            idx = choice -1 

            # Show info about the selected substance
            subs = data_listing[idx]
            try:
                radius = f'\n\tR: {subs["r"]}'
            except:
                radius = ''

            print(f"\n[>] Selected substance is: '{subs['name']}'\n" + 
                  f"\tEnabled?: {'ENABLED' if subs['enabled'] else 'DISABLED'}\n" +
                  f"\tD: {subs['d']}\n" +
                  f"\tP: {subs['p']}\n" +
                  f"\tH: {subs['h']}" + radius)
            
            _c2 = Prompt.ask("[T] To toggle (enabled/disabled) , [D] to delete")
            if _c2.lower() == 't':
                # Toggle
                self.toggle_substance(idx)
            elif _c2.lower() == 'd':
                # Delete
                self.delete_substance(idx)
        except:
            exit()
#TODO need to move the solvents to start at 100 and so on(easier way of working if your checking the same solvent agian and agian and addig polymers)
#TODO do an analitic tool to check where a mixture of solvents will solidify the polymer

from rich.prompt import Prompt, FloatPrompt

if __name__ == '__main__':
    EntryUI()
