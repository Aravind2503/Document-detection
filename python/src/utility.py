import glob
import os


# sorting the files in the directory based on creation time
def mostrecentfile(search_dir):

    
    

    #sorting the file according to modified time
    files = glob.glob(search_dir+"*")
    files.sort(key=os.path.getmtime)
    return files[-1]



#for deleting the files after we are done with them
def cleanup(dir):
    
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)
    




if __name__ == '__main__':
    mostrecentfile()
    cleanup()