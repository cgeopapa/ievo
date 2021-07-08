import json
import os
import time
from zipfile import ZipFile

import vt

from update import apikey


def virus_total_check_files(files, z):
    print('--== PHASE 3 ==--')
    client = vt.Client(os.environ.get(apikey))
    if z:
        print("Generating zip file...")
        with ZipFile('tmp.zip', 'w') as zipObj:
            for file in files:
                zipObj.write(file)
        print('Uploading files to virus total...')
        with open('tmp.zip', "rb") as f:
            fileScan = client.scan_file(f)
            print("Upload complete. Waiting for Virus Total analysis results...")
            while True:
                analysis = client.get_object("/analyses/{}", fileScan.id)
                print(analysis.status, end='\r')
                if analysis.status == "completed":
                    with open("scan_results.json", 'w') as res:
                        j = analysis.results
                        j["id"] = analysis.results
                        json.dump(j, res)
                    break
                time.sleep(5)
    else:
        #upload one-by-one
        pass
