from . import *

DATA_FILE = 'data.json'


if __name__ == '_˚_main__':
    args = cli_parser.parser()
    my_entry = entry.EntryUI(args.data_file)
    my_entry(**args.__dict__)
