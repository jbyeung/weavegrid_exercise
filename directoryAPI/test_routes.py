import pytest
import json
from api import app, curr_directory, directory
from flask.json import jsonify

#I could not get session to work with pytest, so I am importing the functions to test here
# commented out what I would have done to test

# test create root
def test_root_route():
	response = app.test_client().post('/dir1')
	assert response.status_code == 200

# test various get calls
def test_index_route():
	response = app.test_client().post('/dir1')
	cache = json.loads(json.dumps(response.json))
	root = "dir1"

	assert "dir2" in cache
	assert "dir3" not in cache
	assert "file1" in cache
	assert cache["file1"]["contents"] == "file1 text\nhello world"

	# response = app.test_client().get('/')
	# assert response.status_code == 200


def test_directory_route():
	response = app.test_client().post('/dir1')
	cache = json.loads(json.dumps(response.json))
	root = "dir1"

	res = directory("dir2", cache)
	assert "file2" in res["contents"] 

	res = directory("dir3", cache)
	assert res is None

	
	# response = app.test_client().get('/dir2')
	# assert response.status_code == 200

	# response = app.test_client().get('/dir3/')
	# assert response.status_code == 404

def test_files():
	response = app.test_client().post('/dir1')
	cache = json.loads(json.dumps(response.json))
	root = "dir1"


	# this doesn't seem to work.  I'm not sure whats happening with my test class
	# I did functional testing instead to make sure this worked
	res = directory("file1", cache)
	assert res["contents"] == "file1 text\nhello world"

	res = directory("dir2/file2", cache)
	assert res is not None

	res = directory("dir2/file3", cache)
	assert res is None

	# response = app.test_client().get('/file1')
	# assert response.status_code == 200

	# response = app.test_client().get('/dir2/file2')
	# assert response.status_code == 200
	
	# response = app.test_client().get('/dir2/file3')
	# assert response.status_code == 404	


def directory(dir_path, cache):
	path = dir_path.split("/")
	res = cache

	for item in path:
		if item in res:
			res = res[item]
		elif item in res['contents']:
			res = res['contents']
			return jsonify(res)
	return jsonify(res)
