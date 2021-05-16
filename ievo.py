import subprocess
import sys
import os
import progressbar
from update import update


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
            unver_files.append(files)
        else:
            vered = vered + 1
        f = f + 1
        pb.update(f)

    pb.finish()
    print("Successfully verified {} files. Remaining {}".format(vered, len(unver_files)))
    return unver_files


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
    unver_files = verify_files(files)
    if len(unver_files) == 0:
        print("All files are clear")
        exit(0)


def main():
    if sys.argv[1] == '-u' or sys.argv[1] == '--update':
        update()
    elif sys.argv[1] == '-c' or sys.argv[1] == '--check':
        check()


if __name__ == "__main__":
    main()
