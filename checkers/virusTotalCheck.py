import json
import os
import time
from zipfile import ZipFile
import threading
import vt
import logging

from update import apikey


def virus_total_check_files(files, z):
    print('--== PHASE 3 ==--')
    global logger
    client = vt.Client(os.environ.get(apikey))

    logpath = "scan_results.json"
    logger = logging.getLogger('log')
    logger.setLevel(logging.INFO)
    ch = logging.FileHandler(logpath)
    ch.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(ch)

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
        threads = list()
        for file in files:
            thread = threading.Thread(target=scan_file, args=(file,))
            threads.append(thread)
            thread.start()
            time.sleep(15.1)
        for index, thread in enumerate(threads):
            thread.join()


def scan_file(file):
    client = vt.Client(os.environ.get(apikey))

    print("Uploading file {}...".format(file), end='\r')
    fileScan = client.scan_file(file)
    print("Uploading file {}...done".format(file))
    while True:
        analysis = client.get_object("/analyses/{}", fileScan.id)
        if analysis.status == "completed":
            j = {
                "id": analysis.id,
                "file": file,
                "results": analysis.results
            }
            logger.info(json.dumps(j, indent=4))
            client.close()
            break
        time.sleep(5)

