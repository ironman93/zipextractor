import os, zipfile, time, configparser
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

config = configparser.ConfigParser()
config_file_name = 'config.ini'

if not os.path.exists(config_file_name): #if the configfile doesn't exist then create one
    with open(config_file_name, 'w') as configfile:
        config['DEFAULT'] = {'Where_you_put_your_zipped_files': 'any_directory',
            'Where_they_go_after_unzipping': 'any_other_directory'}
        config.write(configfile)

config.read(config_file_name)

zip_dir = config['DEFAULT']['Where_you_put_your_zipped_files']
unzip_dir = config['DEFAULT']['Where_they_go_after_unzipping']
extension = ".zip"

def createFolder(directory):#creates folder in directory if it doesnot exist
    try:
        if not os.path.exists(directory):
            os.mkdir(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

os.chdir(zip_dir) # change directory from working dir to dir with files

def unzipall():#unzips all the items in zip_dir
    for item in os.listdir(zip_dir): # loop through items in dir
        if item.endswith(extension): # check for ".zip" extension
            file_path = os.path.abspath(item) # get full path of files
            file_name = os.path.basename(os.path.splitext(file_path)[0])#removing the .zip extension and the path to the .zip file, so file_name is just the name of the folder
            folder_directory = unzip_dir + '\\' + file_name + '\\' #creating the name of the aim directory
            createFolder(folder_directory)#create a subfolder that is named after the zip file
            copying = True
            size2 = -1
            while copying:#making sure unzipping will not begin during copy or download
                size = os.path.getsize(file_name + '.zip')
                if size == size2:
                    print('work in progress')
                    break
                else:
                    size2 = os.path.getsize(file_name + '.zip')
                    time.sleep(2)
            zip_ref = zipfile.ZipFile(file_path)
            zip_ref.extractall(folder_directory) # extract file to dir
            zip_ref.close() # close file
            os.remove(file_path) # delete zipped file


unzipall()



if __name__ == "__main__":
    patterns = "*"
    ignore_patterns = ""
    ignore_directories = True
    case_sensitive = False
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    def on_created(event):
        print('file was created')
        unzipall()
        print('created file unzipped')

    def on_deleted(event):
        print('file was deleted')

    def on_modified(event):
        print('file was modified')
        unzipall()
        print('file unzipped')

    def on_moved(event):
        print('file was moved')
        unzipall()

    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved

    path = 'C:\\Users\\finns\\Downloads\\zip'
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
