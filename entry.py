import json
from rich.prompt import Prompt, FloatPrompt
import numpy as np


MAX_SUBSTANCES = 100




def closest_point_percentage(center, point1, point2):
        name, enabled, x1, y1, z1 = list(point1.values())
        name, enabled, x2, y2, z2 = list(point2.values())
        name, enabled, x3, y3, z3, r3 = list(center.values())

        point1 = np.array((x1, y1, z1))
        print(x1, y1, z1, point1)
        point2 = np.array((x2, y2, z2))
        point3 = np.array((x3, y3, z3))

        # Calculate the vector from point1 to point2
        vec = point2 - point1
        
        # Calculate the vector from point1 to the center
        vec_to_center = point3 - point1
        
        # Calculate the projection of vec_to_center onto vec
        projection = np.dot(vec_to_center, vec) / np.dot(vec, vec)
        
        # Clamp the projection to the range [0, 1] to ensure that the
        # resulting point is on the line segment between point1 and point2
        projection = max(0, min(projection, 1))
        
        # Calculate the closest point on the line segment between point1 and point2
        closest = point1 + projection * vec
        
        # Calculate the percentage of how much you went to each side between
        # point1 and point2 to get to the closest point
        percentage = projection * 100
        
        return percentage , closest


def calc_2solvents(point1, point2, percentage):
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    x = x1 + (x2 - x1) * percentage
    y = y1 + (y2 - y1) * percentage
    z = z1 + (z2 - z1) * percentage
    return (x, y, z)


# def calc_3solvents(point1, point2, point3, percentage1, percentage2, percentage3):
#   data = load_data()
#   for sol in data['solvent']:
#         if not sol['enabled']:
#             continue
        
#   x1, y1, z1 = point1
#   x2, y2, z2 = point2
#   x3, y3, z3 = point3
#   x = x1 * percentage1 + x2 * percentage2 + x3 * percentage3
#   y = y1 * percentage1 + y2 * percentage2 + y3 * percentage3
#   z = z1 * percentage1 + z2 * percentage2 + z3 * percentage3
#   return (x, y, z)


def abbrevation(string):
    if ' ' not in string:
        return string
    return ''.join([l[0] for l in string.split()]).upper()

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
        idx = 0
        print()
        print("[+] Existing substances:")
        substance_group = 0
        for k,v in self.data.items():
            print(f'➡  {k.capitalize()}:')
            for subs in v:
                name = subs['name']
                enabled = subs['enabled']
                print(f'\t{idx} - {"✔" if enabled else "✖"} - {name}')
                idx += 1
            substance_group += 1
            idx = substance_group * MAX_SUBSTANCES

    def list_data(self):
        array = {}
        idx = 0
        subs_group = 0
        for k,v in self.data.items():
            for substance in v:
                array.update({idx: substance})
                idx += 1
            subs_group += 1
            idx = subs_group * MAX_SUBSTANCES
        return array

    def choose_polymer(self):
        polymer = self.data['polymer']
        print("\n[+] Existing polymer:")
        for idx, pol in enumerate(polymer):
            print(f'\t{idx} - {"✔" if pol["enabled"] else "✖"} - {pol["name"]}')

        try:
            choice = Prompt.ask(f"[0-{len(polymer)}] to select a substance, [X] to exit", default="x")
        except:
            exit()
        if choice.lower() == 'x':
            exit()

        # Try parse to int
        try:
            choice = int(choice)
            if choice < 0 or choice > len(polymer):
                print("[!] Out of range")
        except:
            exit()

        # Show info about the selected substance
        return polymer[choice]

    def choose_solvent(self):
        solvents = self.data['solvent']
        print("\n[+] Existing solvents:")
        for idx, sol in enumerate(solvents):
            print(f'\t{idx} - {"✔" if sol["enabled"] else "✖"} - {sol["name"]}')

        try:
            choice = Prompt.ask(f"[0-{len(solvents)}] to select a substance, [X] to exit", default="x")
        except:
            exit()
        if choice.lower() == 'x':
            exit()

        # Try parse to int
        try:
            choice = int(choice)
            if choice < 0 or choice > len(solvents):
                print("[!] Out of range")
        except:
            exit()

        # Show info about the selected substance
        return solvents[choice]



    def add_substance(self):
        print("[+] Adding new substance")

        c_type = Prompt.ask("Select type: [P] for Polymer, [S] for Solvent, [M] Solvent Mix, [C] calculate the best mix")
        if c_type.lower() not in ['p', 's', 'm', 'c']:
            exit()
        if c_type.lower() == 'c':
            print('[?] Choose first polymer:')
            pol1 = self.choose_polymer()
            
            print('[?] Choose first solvent:')
            sol1 = self.choose_solvent()
            
            print('[?] Choose second solvent:')
            sol2 = self.choose_solvent()
            
            percentage, closest = closest_point_percentage(pol1 ,sol1 ,sol2)
            print("[+] Calcultaed percentage is: ", percentage)

            print("closest: ", closest)

            d ,p ,h = closest

            # generate a name by percentage
            combined_name = f'{abbrevation(sol1["name"])} ({int(percentage)}) - ({100-int(percentage)}) {abbrevation(sol2["name"])}'
            
            newSubstance = {
                'name': combined_name,
                'enabled': True,
                'd': d,
                'p': p,
                'h': h,
            }
            _type = 'solvent'
            
        elif c_type.lower() == 'm':
            # Mix 2/3 solvents
            # let user choose two (or three) solvents

            print('[?] Choose first solvent:')
            sol1 = self.choose_solvent()
            
            print('[?] Choose second solvent:')
            sol2 = self.choose_solvent()
            
            # Enter percentage for first solvent
            percentage = FloatPrompt.ask('[?] Please enter percentage (0-100) for the first solvent:')
            
            # generate a name
            combined_name = f'{abbrevation(sol1["name"])} ({int(percentage)}) - ({100-int(percentage)}) {abbrevation(sol2["name"])}'
            
            # calcultate middle between them
            d, p, h  = calc_2solvents(
                (sol1['d'], sol1['p'], sol1['h']),
                (sol2['d'], sol2['p'], sol2['h']),
                percentage / 100
            )

            newSubstance = {
                'name': combined_name,
                'enabled': True,
                'd': d,
                'p': p,
                'h': h,
            }
            _type = 'solvent'
        else:
            _type = 'polymer' if c_type.lower() == 'p' else 'solvent'

            newSubstance = {
                'name': Prompt.ask("Enter name for new substance"),
                'enabled': True,
                'd': FloatPrompt.ask("Enter D (decimal)"),
                'p': FloatPrompt.ask("Enter P (decimal)"),
                'h': FloatPrompt.ask("Enter H (decimal)"),
            }
            if _type == 'polymer':
                newSubstance.update({
                    'r': FloatPrompt.ask("Enter R (decimal)"),
                })

        print('[+] Saving new substance:')
        print(json.dumps(newSubstance, indent=4))
        self.data[_type].append(newSubstance)
        self.save()

    
    def delete_substance(self, index):
        for k,v in self.data.items():
            if index >= MAX_SUBSTANCES:
                index -= MAX_SUBSTANCES
                continue
            # if len(v) <= index:
            #     index -= len(v)
            #     continue
            del self.data[k][index]
            break
        self.save()
    
    def toggle_substance(self, index):
        for k,v in self.data.items():
            if index >= MAX_SUBSTANCES:
                index -= MAX_SUBSTANCES
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
        
        try:
            choice = Prompt.ask(f"[A] to add, [1-999] to select a substance, [X] to exit", default="x")
        except:
            exit()
        
        # print('you chose: ', choice)
        
        if choice.lower() == 'a':
            # Add
            return self.add_substance()
        elif choice.lower() == 'x':
            exit()
        
        data_listing = self.list_data()
        # print(data_listing)

        # Try parse to int
        try:
            choice = int(choice)
            if choice < 0 or choice > 999:
                print("[!] Out of range")
        except:
            exit()

        # Show info about the selected substance
        subs = data_listing[choice]
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
            self.toggle_substance(choice)
        elif _c2.lower() == 'd':
            # Delete
            self.delete_substance(choice)

#TODO need to move the solvents to start at 100 and so on(easier way of working if your checking the same solvent agian and agian and addig polymers)
#TODO do an analitic tool to check where a mixture of solvents will solidify the polymer



if __name__ == '__main__':
    EntryUI()
