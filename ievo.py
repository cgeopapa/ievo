import csv
import subprocess
import sys
import os
import progressbar
from update import update
import hashlib
from termcolor import colored


# Gets all files in given directory
def get_files(path):
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))
    print("Found {} files in directory {}\n".format(len(files), path))
    return files


# Removes digitally signed files
def verify_files(files):
    print("Checking files for digital signature")
    unver_files = []
    vered = 0
    f = 0
    pb = progressbar.ProgressBar(maxval=len(files), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.SimpleProgress()])
    pb.start()
    for file in files:
        process = subprocess.run(['signtool', 'verify', '/pa', file], stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        if process.returncode == 1:
            unver_files.append(file)
        else:
            vered = vered + 1
        f = f + 1
        pb.update(f)

    pb.finish()
    print("Successfully verified {} files. Remaining {}".format(vered, len(unver_files)))
    return unver_files


# Remove files that are included in the nsrl dataset
def nsrl_verify_files(files):
    print('Generating file hashes')
    fileHash = []
    pb = progressbar.ProgressBar(maxval=len(files), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.SimpleProgress()])
    pb.start()
    for file in files:
        with open(file, 'rb') as f:
            sha1 = str(hashlib.sha1(f.read()).hexdigest()).upper()
            md5 = str(hashlib.md5(f.read()).hexdigest()).upper()
            fileHash.append((sha1, md5, file))
            f.close()
            pb.update(len(fileHash))
    fileHash = sorted(fileHash)
    pb.finish()
    conf = open('ievo.conf', 'r')
    fileLoc = conf.readline()
    conf.close()

    rds = open(fileLoc, 'r', encoding='utf-8')
    nsrl = csv.reader(rds, delimiter=',', quotechar='"')
    next(nsrl, None)

    c = 0
    print("Now searching for hashes in the NSRL rds...")
    for line in nsrl:
        if fileHash[c][0] < line[0]:
            print(colored('File {} not found [❌ ]'.format(fileHash[c][2]), 'red'), '\n\t{} more hashes remaining...'.format(len(fileHash)-(c+1)), end='\r')
            c = c + 1
        if line[0] == fileHash[c][0] and line[1] == fileHash[c][1]:
            print(colored('Found file {} [✔]'.format(fileHash[c][2]), 'green'), '\n\t{} more hashes remaining...'.format(len(fileHash)-(c+1)), end='/r')
            fileHash.pop(c)
        if c == len(fileHash)-1:
            break
    rds.close()
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
    if len(sys.argv) != 3:
        print(r'Usage: ievo PATH_TO_DIRECTORY_TO_CHECK')
        exit(1)
    path = sys.argv[2]
    if not os.path.isdir(path):
        print("The given argument is not a valid path")
        exit(1)
    files = get_files(path)
    if not is_signtool_setupped():
        exit(1)
    if not os.path.isfile('ievo.conf'):
        print('You need to execute "python3 ievo.py -u" before executing a check in order to get the latest NIST NSRL rds dataset.\n'
              'If you already have one downloaded in your system execute "python3 ievo.py -u path/to/NSRLFile.txt".')
        exit(1)
    files = verify_files(files)
    if len(files) == 0:
        print("All files are clear")
        exit(0)
    files = nsrl_verify_files(files)
    if len(files) == 0:
        print("All files are clear")
        exit(0)


def main():
    if sys.argv[1] == '-u' or sys.argv[1] == '--update':
        update()
    elif sys.argv[1] == '-c' or sys.argv[1] == '--check':
        check()


if __name__ == "__main__":
    main()
