import os, stat
from flask import Flask, session, abort, make_response
from flask.json import jsonify


app = Flask(__name__)
app.secret_key = b'randomkey'

root = None
cache = {} 


#------------------ routes

#path for setting root directory and creating cache of all files
@app.route("/<path:root_path>", methods = ['POST'])
def set_root(root_path):
    cwd = os.getcwd()
    root_path = os.path.join(cwd, root_path)
    if os.path.exists(root_path):
        root = root_path

        # read in everything in current and all sub directories into cache
        cache = getContents(root)

        session['root'] = root
        session['cache'] = cache
    else:
        return "Bad root path"


    return cache, 200


#route for current directory (path is empty)
@app.route("/", methods = ['GET'])
def curr_directory():
    root = session.get('root')
    cache = session.get('cache')

    if not root:
        abort(404)

    return jsonify(cache), 200

#create REST endpoint for getting directories / files
@app.route("/<path:dir_path>", methods = ['GET'])
def directory(dir_path):
    root = session.get('root')
    cache = session.get('cache')

    if not root:
        abort(404)

    # walk down the path
    path = dir_path.split("/")
    res = cache

    for item in path:
        if item in res:
            #found directory, so path down to subdir
            res = res[item]
        elif item in res['contents']:
            #found file, so return
            res = res['contents']
            return jsonify(res), 200
        else:
            abort(404)

    return jsonify(res)


#error handling
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Bad path!"}), 404)

#---------------------------- helper functions

def getContents(path):
    # read in files and subdirectories
    it = os.scandir(path)
    res = {}

    for entry in it:
        name = entry.name
        if entry.is_dir():
            res[name] = {
                "stats" : getStats(entry),
                "contents" : getContents(os.path.join(path, entry.name))
            }
        else:
            res[name] = {
                "stats" : getStats(entry),
                "contents" : readFile(path, entry)
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
    return open(file_path, 'r').read()




if __name__ == '__main__':
    app.run(debug=True)