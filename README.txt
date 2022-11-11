# Thought process

Since this is an application where your user is setting a root directory and then engaging with the API, I am assuming this is a single user instance.
In that case, I am letting the user set the root via POST, and then saving this to the server.  I then fetch all the files and directories of the root to cache to make GET requests fast.  

I would normally prefer to keep the server stateless, but as described, the prompt seems to assume a single user instance with no unforeseen locking issues.  I am assuming this could be used as some sort of remote access method or similar.

This exercise took approximately 5 hours to do.  


# HOW TO RUN APP
This app can be run by initiating Docker image via the bash shell script.
> sudo bash start.sh

This will start the Docker container.  Make sure the container is running to start the Python API.  Run this code to run the python script in the container:
> docker run docker.weavegrid_exercise

Then you can run the unit tests.  I had some issues with using the unit tests due to the sessioning, which I had never done before.  In retrospect, maybe this design was not the best for testing.  However, I ran out of time as life demands had to have me complete the assignment.  I did functional testing with Postman to ensure the API worked appropriately.
> python -m pytest test_routes.py 

For API calls, here are some examples.  Indicate the root directory first:
> curl -X POST 127.0.0.1:5000/dir1

Then you can GET the various directories:
> curl -X GET 127.0.0.1:5000/
> curl -X GET 127.0.0.1:5000/file1
> curl -X GET 127.0.0.1:5000/dir2/
> curl -X GET 127.0.0.1:5000/dir2/file2
