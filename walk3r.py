import os
import os.path
import sys
import hashlib
import shutil
from reprint import output

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
    print('    ░          ░  ░    ░  ░░  ░     ░░   ░         ')
    print(f'{bcolors.ENDC}')

extensions = Counter()
hash_dictionary = Counter()
destiny = ''

def destiny_folder():
    destiny = f'{os.getcwd()}\duplicate\\'
    CHECK_FOLDER = os.path.isdir(destiny)
    # If folder doesn't exist, then create it.
    if not CHECK_FOLDER:
        os.makedirs(destiny)
        print("created folder : ", destiny)

def argument():
    try:
        directory=sys.argv[1]
        print(f'Scanning {directory}')
        destiny_folder()
        scan(directory)
    except:
        print('Please pass directory')
    
def show_file_formats():
    print('\nTotal files by format:')
    print ("{:<8} {:<10}".format('Format','Cuantity'))
    for key, value in extensions.items():
        print ("{:<8} {:<10}".format(key, value))

def scan(directory):
    with output(output_type='dict') as output_lines:   # default setting
        for directory_name, dirs, files in os.walk(directory, topdown=False):
            for file_mame in files:
                file_path = os.path.join(directory_name, file_mame)
                extension = os.path.splitext(file_mame)[1].replace('.', '')
                extensions[extension] += 1
                if extension == 'png' or extension == 'jpg' or extension == 'JPG':
                    with open(file_path, "rb") as f:
                        file_hash = hashlib.blake2b()
                        while chunk := f.read(8192):
                            file_hash.update(chunk)

                    if file_hash.hexdigest() in hash_dictionary:
                        with open('log.txt', 'a+') as f:
                            f.write(f'{file_path}\n')
                        shutil.move(file_path, destiny + file_mame)
                    else:
                        hash_dictionary[file_hash.hexdigest()] = file_path

                    output_lines['Cheking file'] = file_path
                    output_lines['Hash'] = "31;1m" + file_hash.hexdigest() + "0m"
    show_file_formats()

if __name__ == '__main__':
    banner()
    argument()