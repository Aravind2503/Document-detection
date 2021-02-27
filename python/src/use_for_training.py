import glob
import uuid
from shutil import copyfile
import utility
# import predict
import os 

l = [x[1] for x in os.walk('../resources/')]
l[2].sort()
Categories = l[2]



print(Categories)
#getting the path of the scanned image after the preprocessed input
img_path = '../resources/preprocessing_output/'
im_path = utility.mostrecentfile(img_path)

#getting the path of the output file that has the category stored
o_path = '../resources/classification_output/out.txt'
# o_path = utility.mostrecentfile(outpath)

# print(im_path)

f = open(o_path, "r")
cat = f.read() # cat stores the category of the document scanned
print (cat)

if cat in Categories:

    # finds the test and train files for the document category
    category_path_test = '../resources/ml/test/'+cat
    category_path_train = '../resources/ml/train/'+cat

    num_test = len(glob.glob(category_path_test+'/*'))
    num_train = len(glob.glob(category_path_train+'/*'))

    sum = num_test+num_train
    # print(sum)

    #create a unique file name
    unique_filename = str(uuid.uuid4())

    if sum == 0:
        copyfile(im_path,category_path_train+'/'+unique_filename)
    elif sum %5 == 0 :
        copyfile(im_path,category_path_test+'/'+unique_filename)
    else:
        copyfile(im_path,category_path_train+'/'+unique_filename)

    if sum % 10 == 0 and sum != 0:
        f = open("../resources/trainable.txt", "a")
        f.write(cat+' ')
        f.close()
else:

    # finds the test and train files for the document category
    category_path_test = '../resources/ml/buffer/test/'+cat
    category_path_train = '../resources/ml/buffer/train/'+cat

    num_test = len(glob.glob(category_path_test+'/*'))
    num_train = len(glob.glob(category_path_train+'/*'))

    sum = num_test+num_train
    # print(sum)

    #create a unique file name
    unique_filename = str(uuid.uuid4())

    if sum == 0:
        copyfile(im_path,category_path_train+'/'+unique_filename)
    elif sum %5 == 0 :
        copyfile(im_path,category_path_test+'/'+unique_filename)
    else:
        copyfile(im_path,category_path_train+'/'+unique_filename)
    
    if sum % 10 == 0 and sum !=0:
        f = open("../resources/trainable.txt", "a")
        f.write(cat+' ')
        f.close()