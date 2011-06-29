# Setup
## Download the Python dependencies
* Make sure you have the Python dev headers on your platform (I already had these on OSX)

    ```sudo apt-get install python2.7-dev```
* Make sure you have pip installed on your platform

    ```sudo easy_install pip```
* Create a virtualenv for Python. Optional, but recommended step. See [virtualenv](http://pypi.python.org/pypi/virtualenv) and [virtualenvwrapper](http://www.doughellmann.com/docs/virtualenvwrapper/) for info on how to install these tools.
   
    ```mkvirtualenv twitter_stream_example --no-site-packages```
* Install the dependencies

        cd twitter-oauth-streaming
        pip install --requirement=requirements.txt

## Register an application with Twitter
* Register an application with Twitter here: https://dev.twitter.com/apps/new
* Fill in your details. All details are mandatory.
* Your website can be fictional, but it does require a http:// prefix. Make sure you select 'Client' as the application type. You only need Read-only permissions.
* At the application settings page take note of your consumer key and consumer secret.
* Add your consumer key and secret to the top of the twitter-oauth-streaming.py script. Search for 'CHANGEME'.

## Running the script
* Start the script

    ```python twitter-oauth-streaming.py```
* You should be prompted to authorize the script with Twitter. It should open a browser for you, but if not you can visit the url printed on the console.
* Once you login to Twitter and authorize the application, you should see a Pin in the browser. This is out-of-band OAuth for Client applications like this, if it was a webapp, you would get a callback with the pin, so wouldnt need the next manual step.
* Enter the pin onto the console.
* Tweets should now be streaming out onto your console. Get down with your bad self!