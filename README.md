transferScript
==============
A Python script to download and upload content from/to your Dropbox.


##Features :


1. Can traverse user's Dropbox directories recursively thus the script works even if there is any level of nesting of folders.

2. Authentication from Dropbox is required only once.

3. You can manually edit the tokens.cfg file to put your own app keys.

4. For first time users, browser is opened automatically with required URL.


##Dependencies :

Install [config module](https://pypi.python.org/pypi/config/0.3.7), which doesn't comes preloaded with the default python modules with IDLE on windows or with Ubuntu.

##How to use :

1. Install dependencies.

2. Put your app keys and app secret in tokens.cfg.

3. You will need to authenticate in the browser for the first time.

##TODO :

1. Use Dropbox Delta function to provide an option to downloading only changed files.
2. Analyse response to download only images.
3. Use chunked upload.
4. Support for checking version history of a file. 

[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/shubhamd/transferscript/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

