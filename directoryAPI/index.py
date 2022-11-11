import os, stat
from flask import Flask


app = Flask(__name__)

#create REST endpoint for getting directories / files
@app.route("/<scandir_path>", methods = ['GET'])
def directory():
    dir_list = os.scandir(path)
    res = {}

    # if requesting just a file, only return file contents
    if len(dir_list) == 1 and dir_list.is_file():
        entry = dir_list

        # jsonify return
        res[entry.name] = {
            "contents" : readFile(scandir_path, entry),
            "stats" : getStats(entry)
        }
    else:
    #iterate through the files and directories
        for entry in dir_list:
            name = entry.name
            if entry.is_dir():
                name += "\\"

            res[name] = {
                "stats" : getStats(entry)
            }
        
    
    return res

def getStats(entry):
    #returns the relevant stats on the entry requested
    statinfo = entry.stat()

    return {
        "size" : statinfo.st_size,
        "owner" : statinfo.st_uid,
        "permissions" : stat.S_IMODE(statinfo.st_mode)
    }

def readFile(path, entry):
    #reads file into string for json blob
    file_path = os.path.join(path, entry.name)
    return open(path, 'r').read()