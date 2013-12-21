import webbrowser 
import pickle 
import os 
import errno
import time
import datetime 
from dropbox import session, rest, client
from config import Config 

class transferScript():

    def __init__(self):
        
        with open ('tokens.cfg','a+') as token_file:
            tokens = Config(token_file)
            print "reading token file........."
            print tokens.key
            
        self.mSession = session.DropboxSession(tokens.key,tokens.secret,'dropbox')
        print "creating session........"

        try :
		    
            self.mSession.set_token(tokens.token_key,tokens.token_secret)
            print "loading access tokens......"
            
        except:
            access_token = self.mSession.obtain_request_token()
            
            webbrowser.open_new_tab(self.mSession.build_authorize_url(access_token))
            raw_input()
            self.mSession.obtain_access_token(access_token)
            print "loading access tokens......"
            tokens.token_key = self.mSession.token.key
            tokens.token_secret = self.mSession.token.secret
            with open ('tokens.cfg','w') as token_file :
                tokens.save(token_file)
                
        self.mClient = client.DropboxClient(self.mSession)
        
    def init_download(self):
        self._target_folder = 'DropBox Images'
        print "Creating backup folder......."
        self.download_folder('')


    def check_dir(self,path):
        if path !='':
            
            try:
                # try to create it
                os.makedirs(path)
            except OSError as exception:
                # raise all errors except of the error that shows us that the dir already exists already
                if exception.errno != errno.EEXIST: 
                    raise
            
    def download_file(self,source_path,target_path):
        print 'Downloading %s' % source_path
        file_path = os.path.expanduser(target_path)
        (dir_path,tail) = os.path.split(target_path)
        self.check_dir(dir_path)
        to_file = open(file_path,"wb")
        s,p = os.path.split(source_path)
        source_path = s+"/"+p
        f= self.mClient.get_file(source_path)
        to_file.write(f.read())
        return
    def download_folder(self, folderPath):
        

        # try to download 5 times to handle http 5xx errors from dropbox
        
        try:
            response = self.mClient.metadata(folderPath)
                # also ensure that response includes content
            if 'contents' in response:
                for f in response['contents']:
                    name = os.path.basename(f['path'])
                    complete_path = os.path.join(folderPath, name)
                    if f['is_dir']:            
                        # do recursion to also download this folder
                        self.download_folder(complete_path)
                    else:
                        # download the file
                        self.download_file(complete_path, os.path.join(self._target_folder, complete_path))
            else:
                raise ValueError
        except (rest.ErrorResponse, rest.RESTSocketError, ValueError) as error:
                print 'An error occured while listing a directory. Will try again in some seconds.'
                print "Error occured "+ str(error)
def main():
    data_exchange_obj = transferScript()
    data_exchange_obj.init_download()
	

if __name__ == '__main__':
    main()
