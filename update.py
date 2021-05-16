import sys

import requests
import io
import progressbar
import os
from contextlib import closing
from zipfile import ZipFile


# url = r'http://www.pythonchallenge.com/pc/def/channel.zip'
url = 'https://s3.amazonaws.com/rds.nsrl.nist.gov/RDS/current/rds_modernm.zip'


def update():
    if len(sys.argv) == 3:
        if not os.path.isfile(sys.argv[2]):
            print('You need to provide the path to the NSRLFile.txt')
    else:
        print('You did not specify the path for the NSRLFile.txt. If you do not have that file downloaded it can be downloaded now. Do you want to proceed? (Y/n)')
        done = False
        while not done:
            download = input().lower()
            if download == 'y':
                done = True
                print('NIST NSRL rds download now starting. This process can take from a few minutes to even more than an hour depending on your internet connection speed.')

                r = requests.get(url, stream=True)
                total_size_in_bytes = int(r.headers.get('content-length', 0))
                pb = progressbar.ProgressBar(maxval=total_size_in_bytes,
                                             widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
                pb.start()
                zipfile = io.BytesIO(r.content)
                for data in r.iter_content(1024):
                    pb.update(len(data))
                    zipfile = io.BytesIO(r.content)
                pb.finish()
                with closing(r), ZipFile(zipfile) as archive:
                    print({member.filename: archive.read(member) for member in archive.infolist()})
                # open('test.zip', 'wb').write(r.content)
            elif download == 'n':
                done = True
                print('Aborting...')
                exit(0)
