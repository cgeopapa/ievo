import csv
import hashlib
import os

import progressbar
from termcolor import colored

from update import rdsloc


def nsrl_check_files(files):
    print('--== PHASE 2 ==--')
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
    fileLoc = os.environ.get(rdsloc)

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
