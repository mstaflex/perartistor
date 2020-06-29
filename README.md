# PERsonal ARTIfact STORage

A small micro service to be able to store personal artifacts.

## Running Server

`python3 webserver.py --token="<TOKEN>" --port=9999 --path=storage`

This will run a Python webserver on port 9999
and store received artifacts under 'storage' path
in subfolders for each date and prefixed with time.

## Upload via Curl

`curl -F 'uploadfile=@<FILE>' <URL>:9999/<TOKEN>`

will upload local file FILE to the server.
