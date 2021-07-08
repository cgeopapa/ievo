import subprocess

import progressbar


def cigntool_check_files(files):
    print('--== PHASE 1 ==--')
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
