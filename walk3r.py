import logging
import os
import os.path
import sys
import hashlib
import shutil
from reprint import output

logging.basicConfig(level=logging.DEBUG, filename='logs.log',
                    format='%(asctime)s :: %(message)s',
                    filemode='w')
current_version = "1.0.0"

class Counter(dict):
    def __missing__(self, key):
        return 0

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def banner():
    print(f'{bcolors.OKCYAN}')
    print(' █     █░ ▄▄▄       ██▓     ██ ▄█▀ █████▓  ██▀███  ')
    print('▓█░ █ ░█░▒████▄    ▓██▒     ██▄█▒  ▀   █▓ ▓██ ▒ ██▒')
    print('▒█░ █ ░█ ▒██  ▀█▄  ▒██░    ▓███▄░    ███▒ ▓██ ░▄█ ▒')
    print('░█░ █ ░█ ░██▄▄▄▄██ ▒██░    ▓██ █▄  ▄  █▓▒ ▒██▀▀█▄  ')
    print('░░██▒██▓  ▓█   ▓██▒░██████▒▒██▒ █▄▒████▒░▒░██▓ ▒██▒')
    print('░ ▓░▒ ▒   ▒▒   ▓▒█░░ ▒░▓  ░▒ ▒▒ ▓▒░░▒ ░░░░ ▒▓ ░▒▓░ ')
    print('  ▒ ░ ░    ▒   ▒▒ ░░ ░ ▒  ░░ ░▒ ▒░  ░ ░░  ░▒ ░ ▒░  ')
    print('  ░   ░    ░   ▒     ░ ░   ░ ░░ ░   ░   ░░   ░     ')
    print(f'    ░          ░  ░    ░  ░░  ░     ░░   ░              v {current_version}')
    print(f'{bcolors.ENDC}')

extensions = Counter()
hash_dictionary = Counter()
destiny = ''
duplicates = 0
files_size = 0

def destiny_folder():
    destiny = f'{os.getcwd()}//duplicate'
    CHECK_FOLDER = os.path.isdir(destiny)
    # If folder doesn't exist, then create it.
    if not CHECK_FOLDER:
        os.makedirs(destiny)
        print("created folder : ", destiny)

def argument():
    try:
        directory=sys.argv[1]
        print(f'Scanning {directory}\n')
        destiny_folder()
        scan(directory)
    except:
        print(f'{bcolors.WARNING} Please pass directory {bcolors.ENDC}')
    
def show_file_formats():
    print(f'\nTotal files duplicated: {duplicates}\n')
    print(f'\nTotal files size: {files_size/1024}KB\n')
    print('\nTotal files by format:\n')
    print ("{:<8} {:<10}".format('Format','Cuantity'))
    for key, value in extensions.items():
        print ("{:<8} {:<10}".format(key, value))

def scan(directory):
    global duplicates
    global files_size
    with output(output_type='dict') as output_lines:   # default setting
        for directory_name, dirs, files in os.walk(directory, topdown=False):
            for file_mame in files:
                file_path = os.path.join(directory_name, file_mame)
                extension = os.path.splitext(file_mame)[1].replace('.', '')
                extensions[extension] += 1
                if extension == 'png' or extension == 'jpg' or extension == 'JPG' or extension == 'mp4':
                    with open(file_path, "rb") as f:
                        file_hash = hashlib.blake2b()
                        while chunk := f.read(8192):
                            file_hash.update(chunk)

                    if file_hash.hexdigest() in hash_dictionary:
                        logging.info(f'{file_path}\n')
                        files_size += os.stat(file_path).st_size
                        shutil.move(file_path, destiny + 'duplicate//' + file_mame)
                        duplicates += 1
                    else:
                        hash_dictionary[file_hash.hexdigest()] = file_path

                    output_lines['Cheking file'] = bcolors.OKCYAN + file_path + bcolors.ENDC
                    output_lines['Hash'] = bcolors.OKCYAN + file_hash.hexdigest() + bcolors.ENDC
    show_file_formats()

if __name__ == '__main__':
    banner()
    argument()