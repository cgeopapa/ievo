import sys
import requests
import progressbar
import os
from zipfile import ZipFile


url = 'https://s3.amazonaws.com/rds.nsrl.nist.gov/RDS/current/rds_modernm.zip'
tempNSRL = "tempNSRL.zip"
apikey = 'vt_api_key'


def update():
    if os.getenv(apikey) is not None:
        print('Do you want to update your Virus Total API key? (Y/n)', end= ' ')
        updateKey = input().lower()
        if updateKey == 'y':
            print('Please provide you new Virus Total API key')
            newKey = input()
            os.environ[apikey] = newKey
    else:
        print('Please provide you Virus Total API key')
        newKey = input()
        os.environ[apikey] = newKey
    if len(sys.argv) == 3:
        if not os.path.isfile(sys.argv[2]):
            print('You need to provide the path to the NSRLFile.txt')
            exit(1)
        else:
            rds_loc(sys.argv[2])
            print("Updated rds location")
    else:
        print('You did not specify the path for the NSRLFile.txt.\n If you do not have that file downloaded it can be '
              'downloaded now. Do you want to proceed? (Y/n)', end=' ')
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
                with open(tempNSRL, 'wb') as file:
                    for data in r.iter_content(1024):
                        pb.update(os.path.getsize(file.name))
                        file.write(data)
                    pb.finish()
                    file.close()
                print("Download complete. Extracting rds...")
                with ZipFile(tempNSRL, 'r') as zipFile:
                    zipFile.extract(r'rds_modernm/NSRLFile.txt')
                rds_loc(r'rds_modernm/NSRLFile.txt')
            elif download == 'n':
                done = True
                print('Aborting...')
                exit(0)


def rds_loc(path):
    with open('ievo.conf', 'w') as conf:
        conf.write(path)
        conf.close()
