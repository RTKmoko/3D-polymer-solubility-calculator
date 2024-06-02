from cli_parser import parser
from entry import EntryUI

DATA_FILE = 'data.json'


if __name__ == '__main__':
    args = parser()
    my_entry = EntryUI(args.data_file)
    my_entry(**args.__dict__)
