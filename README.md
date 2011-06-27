# Setup
## Download the Python dependencies
* Make sure you have the Python dev headers on your platform (I already had these on OSX)
        sudo apt-get install python2.7-dev
* Make sure you have pip installed on your platform
        sudo easy_install pip
* Create a virtualenv for Python. Optional, but recommended step. See [virtualenv](http://pypi.python.org/pypi/virtualenv) and [virtualenvwrapper](http://www.doughellmann.com/docs/virtualenvwrapper/)   
        mkvirtualenv twitter_stream_example --no-site-packages
* Install the dependencies
        cd twitter-oauth-streaming
        pip install --requirement=requirements.txt

## Register an application with Twitter
* Register an application with Twitter here: https://dev.twitter.com/apps/new
* Then you will need to add your consumer key and secret to the script.

## Run
    python twitter-oauth-streaming.py