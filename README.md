# Is Everything ok
**I**s **EV**erything **O**k (ievo for short) is a **Windows only** simple yet powerful python 
script that checks every file, in a given directory, for its intentions.

## How it works
When you run the script, it will recursively get all files in the given directory. Then the fun begins. The check is consisted of 3 phases:
1. Check every file for its digital signature. Since this operation
   uses the `signtool` utility tool provided by Windows SDK, make sure you have it installed and added to your PATH before executing this script
2. The remaining files are sha1 and md5 summed, and their hashes are searched in the [NIST NSRL rdl](https://www.nist.gov/itl/ssd/software-quality-group/national-software-reference-library-nsrl).
   This phase requires the NSRL dataset to be downloaded somewhere in your system but this tool can download it itself. More on that in the instructions below.
3. The files that failed to surpass both above checks are uploaded to virus total.

## Instructions
To run the tool you need python 3.9 installed in your system... or maybe not... I haven't checked. I have been developing the tool with python 3.9, but it most likely will be compatible with older versions as well.
Now, to run the script:
```shell
python3 ievo.py command
```
### Commands
* `-c check "path/to/directory""` check if everything is ok in the files in the specified directory
* `-u update [path/to/NSRLFile.txt]` download the NSRL rds file and update local db. If a path to that file is provided, 
  a new one won't be downloaded, and the one provided will be used instead. *Note* this tool uses the latest modern minimal rds. 
  If you want to use another one you'll have to download and feed it to this command yourself.
