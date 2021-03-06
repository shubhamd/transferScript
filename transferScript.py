import webbrowser 
import os 
import errno 
from dropbox import session, rest, client
from config import Config  # TODO :  Use pickle module instead, as it comes preloaded with the Python modules.
# other modules that can be used instead of config : configobj , pickle, jsonlib

class transferScript():
    
    def __init__(self): # constructor
        
        """open tokens.cfg in append mode ,as we need to read 
		the app key,app secret also store access tokens to avoid future logins""" 
        with open ('tokens.cfg','a+') as token_file:  # good practice to use context managers, no need to close the file manually.
            tokens = Config(token_file)
            print "reading token file........."
            print tokens.key
            
        self.mSession = session.DropboxSession(tokens.key,tokens.secret,'dropbox')
		# Here 'dropbox' is the access type, it could also be 'app folder'
        print "creating session........"

        try :
		    # If possible, avoid login.
            self.mSession.set_token(tokens.token_key,tokens.token_secret)
            print "loading access tokens......"
            # Otherwise, prompt user to grant access. 
        except:
            access_token = self.mSession.obtain_request_token()
			
            #Open new tab in browser to authenticate.
	    print "Once authenticated in browser, Press Enter."
            webbrowser.open_new_tab(self.mSession.build_authorize_url(access_token))
			
            raw_input()
            self.mSession.obtain_access_token(access_token)
            print "loading access tokens......"
            tokens.token_key = self.mSession.token.key
            tokens.token_secret = self.mSession.token.secret
			# Save the access tokens, to avoid future logins.
            with open ('tokens.cfg','w') as token_file :
                tokens.save(token_file)
        #Create a Dropbox client  to download and upload files.        
        self.mClient = client.DropboxClient(self.mSession)
        
    def init_download(self):
        self._target_folder = 'DropBox Images'
        print "Creating backup folder......."
        self.download_folder('')
		# Initiate downlaod by specifying the Dropbox directory of the user.
		# '' denotes the default directory of user on dropbox server


    def check_dir(self,path):
        if not os.path.exists(path):   # reference : http://stackoverflow.com/questions/273192/create-directory-if-it-doesnt-exist-for-file-write
            #check if the directory exists, if not
            try:
                # try to create it
                os.makedirs(path)
		
            except OSError as exception:
                # raise all errors except of the error that shows us that the dir already exists already
                if exception.errno != errno.EEXIST: 
                    raise
    
    # Dropbox's server follow path convention of Unix. So I used mString.replace(args) to correct the path
	# issue confirmation : https://github.com/michaeldewildt/WordPress-Backup-to-Dropbox/issues/123
        
            
    def download_file(self,source_path,target_path):
        print 'Downloading %s' % source_path
        file_path = os.path.expanduser(target_path)
        (dir_path,tail) = os.path.split(target_path)
        self.check_dir(dir_path)
	print "file path is :",file_path
        to_file = open(file_path,"wb")
		# wb for binary files .
        
	source_path = source_path.replace("\\","/")  # replace() the backslashes with forward slashes.
        # Unix convention 
	print "source path is : ",source_path	
        f= self.mClient.get_file(source_path) # Code USED TO CRASH at this line for deeper directories. As it was't following same path convention as Dropbox Servers.
        to_file.write(f.read())
        return
    def download_folder(self, folderPath):
        # Scan the response each time to get the info about direcory hierarchy.
        # SCOPE : To filter out the images, we just need to check the mime type in the response.
        try:
            response = self.mClient.metadata(folderPath)
                # Download has been initiated from the default dropbox directory in folderpath.
	    
            if 'contents' in response:
                for f in response['contents']:
                    name = os.path.basename(f['path'])
                    
                    complete_path = os.path.join(folderPath, name)
                    complete_path = complete_path.replace("\\","/")
		    print "complete path is :",complete_path 
                    if f['is_dir']:            
                        # call download_folder() recursively
                        self.download_folder(complete_path)
                    else:
                        # if it is not a directory, it is a file, so download.
                        self.download_file(complete_path, os.path.join(self._target_folder, complete_path))
            else:
                raise ValueError
        except (rest.ErrorResponse, rest.RESTSocketError, ValueError) as error:
                print 'An error occured while listing a directory.'
                print "Error occured "+ str(error)
    def upload_file(self):
        with open('./dtu.jpg','rb') as f:
            
            response = self.mClient.put_file('/name_after_uploading.jpg', f)
			#put_file takes a path pointing to where we want the file, a file-like object to be uploaded there.
            print "The file has been uploaded successfully !"
        
def main():
    data_exchange_obj = transferScript() # create instance
    data_exchange_obj.init_download() # start download 
#   data_exchange_obj.upload_file()                   # Ensure that  dtu.jpg exists in the same directory as this python program. 
	                                                # Only images can be uploaded to the server. ( as per my app permissions, if you use my app keys) 

if __name__ == '__main__':
    main()