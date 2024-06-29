import json
from rich.prompt import Prompt, FloatPrompt
import rich

MAX_SUBSTANCES = 100


def calc_2solvents(point1, point2, percentage):
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    x = x1 + (x2 - x1) * percentage
    y = y1 + (y2 - y1) * percentage
    z = z1 + (z2 - z1) * percentage
    return x, y, z


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


def abbreviation(string):
    if ' ' not in string:
        return string
    return ''.join([l[0] for l in string.split()]).upper()


class EntryUI:

    def __init__(self, data_file):
        self._data_file = data_file
        self.data = self.deserialize()

    def deserialize(self) -> dict:
        with open(self._data_file, 'r') as f:
            return json.load(f)

    def serialize(self, data: dict):
        with open(self._data_file, 'w') as f:
            return json.dump(data, f, indent=4)

    # def save(self):
    #     EntryUI.serialize(self.data)

    def print_existing(self):
        idx = 0
        print()
        print("[+] Existing substances:")
        substance_group = 0
        for k, v in self.data.items():
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
        for k, v in self.data.items():
            for substance in v:
                array.update({idx: substance})
                idx += 1
            subs_group += 1
            idx = subs_group * MAX_SUBSTANCES
        return array

    def choose_solvent(self):
        solvents = self.data['solvent']
        print("\n[+] Existing solvents:")
        for idx, sol in enumerate(solvents):
            print(f'\t{idx} - {"✔" if sol["enabled"] else "✖"} - {sol["name"]}')

        try:
            choice = Prompt.ask(f"[0-{len(solvents)}] to select a substance, [X] to exit", default="x")

        finally:
            if choice.lower() == 'x':
                exit()

        # Try parse to int
        try:
            choice = int(choice)
            if choice < 0 or choice > len(solvents):
                print("[!] Out of range")

        finally:
            # Show info about the selected substance
            return solvents[choice]

    def add_substance(self):
        print("[+] Adding new substance")

        c_type = Prompt.ask("Select type: [P] for Polymer, [S] for Solvent, [M] Solvent Mix")
        if c_type.lower() not in ['p', 's', 'm']:
            exit()
        if c_type.lower() == 'm':
            # Mix 2/3 solvents
            # let user choose two (or three) solvents

            print('[?] Choose first solvent:')
            sol1 = self.choose_solvent

            print('[?] Choose second solvent:')
            sol2 = self.choose_solvent

            # Enter percentage for first solvent
            percentage = FloatPrompt.ask('[?] Please enter percentage (0-100) for the first solvent:')

            # generate a name
            combined_name = f'{abbreviation(sol1["name"])} ({int(percentage)}) - ({100 - int(percentage)}) {abbreviation(sol2["name"])}'

            # calculate middle between them
            d, p, h = calc_2solvents(
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
        self.serialize(self.data)

    def delete_substance(self, index):
        for k, v in self.data.items():
            if index >= MAX_SUBSTANCES:
                index -= MAX_SUBSTANCES
                continue
            # if len(v) <= index:
            #     index -= len(v)
            #     continue
            del self.data[k][index]
            break
        self.serialize(self.data)

    def toggle_substance(self, index):
        for k, v in self.data.items():
            if index >= MAX_SUBSTANCES:
                index -= MAX_SUBSTANCES
                continue
            self.data[k][index]['enabled'] = not self.data[k][index]['enabled']
            break
        self.serialize(self.data)

    def __call__(self, **kwargs):
        # show data in a list, separated by the type
        # let user add or select any one from list
        # when selected can be enabled/disabled or deleted
        rich.print_json(json.dumps(self.data))  # DEBUG

        self.print_existing()
        assert 'polymer_type' in kwargs.keys(), "Polymer types missing"
        choice = kwargs.get('polymer_type')

        try:
            choice = Prompt.ask(f"[A] to add, [1-999] to select a substance, [X] to exit", default="x")
        finally:
            print('you chose: ', choice)

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
        finally:
            print('here')
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
