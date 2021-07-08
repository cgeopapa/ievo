import os
import re
import subprocess
import sys
from checkers.nsrlCheck import nsrl_check_files
from checkers.signtoolCheck import cigntool_check_files
from checkers.virusTotalCheck import virus_total_check_files
import dotenv

from update import rdsloc
from update import update


# Gets all files in given directory
def get_files(path):
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))
    print("Found {} files in directory {}\n".format(len(files), path))
    return files


# Check if signtool is installed
def is_signtool_setupped():
    process = subprocess.run(['signtool'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    stderr = process.stderr.decode('utf8')
    if stderr.startswith("SignTool Error: A required parameter is missing."):
        return True
    else:
        print(
r"""signtool is not properly setup.
Make sure you have it installed.

You can download it either via Visual Studio (Community edition works just fine) or by directly downloading Windows 10 
SDK here: https://go.microsoft.com/fwlink/p/?linkid=2120843.

If you choose to use Visual Studio Installer you can run Visual Studio Installer, go to Modify, then select the tab 
above called Individual Components and then search for the latest Windows 10 SDK.

Finally don't forget to add the executable to your PATH. The executable is usually located at 
'C:\Program Files (x86)\Windows Kits\10\bin\[SDK version]\x64'.""")
        return False


def check():
    dotenv.load_dotenv(dotenv.find_dotenv())
    if 3 >= len(sys.argv) >= 4:
        print(r'Usage: python3 ievo.py (options) PATH_TO_DIRECTORY_TO_CHECK')
        exit(1)
    z = True
    exe1 = True
    exe2 = True
    exe3 = True
    if len(sys.argv) == 3:
        path = sys.argv[2]
        if not os.path.isdir(path):
            print("The given argument is not a valid path")
            exit(1)
    else:
        options = sys.argv[2]
        if re.match(r"-[az123]+", options):
            options = options[1:]
            z = 'a' not in options
            if re.match(r"[123]+", options):
                exe1 = '1' in options
                exe2 = '2' in options
                exe3 = '3' in options
        else:
            print("The given options are not valid")
            exit(1)
        path = sys.argv[3]
        if not os.path.isdir(path):
            print("The given argument is not a valid path")
            exit(1)
    files = get_files(path)
    if not is_signtool_setupped():
        exit(1)
    if rdsloc not in os.environ:
        print('You need to execute "python3 ievo.py -u" before executing a check in order to get the latest NIST NSRL rds dataset.\n'
              'If you already have one downloaded in your system execute "python3 ievo.py -u path/to/NSRLFile.txt".')
        exit(1)
    if exe1:
        files = cigntool_check_files(files)
    if len(files) == 0:
        print("All files are clear")
        exit(0)
    if exe2:
        files = nsrl_check_files(files)
    if len(files) == 0:
        print("All files are clear")
        exit(0)
    if exe3:
        virus_total_check_files(files, z)


def main():
    print('Is EVerything Ok (ievo)')
    if sys.argv[1] == '-u' or sys.argv[1] == '--update':
        update()
    elif sys.argv[1] == '-c' or sys.argv[1] == '--check':
        check()
    else:
        print('''
        Is EVrything Ok (ievo)
        If this is you first time executing ievo you might want to run 'python3 ievo.py -u' to update the configuration.
        
        -u  --update    Update the configuration. Import your Virus Total API key and download or import the path to
                        the NSRL dataset.
        -c  --check (options) [path]    Check all files in the specified directory.
            options:    -z  In phase 3 Zip all remaining files and then make just one upload to Virus Total. Cannot be used with -a.
                        -a  In phase 3 upload one by one All remaining files to Virus Total. Cannot be used with -z.
                        -[1,2,3] Choose which of the 3 phases you want to execute. Order doesn't matter, phase 1 will always be the first. Default all of them (-123).
        ''')


if __name__ == "__main__":
    main()
