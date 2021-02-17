from python.src.utility import cleanup
import utility
import predict
import image_preprocessing


path_to_uploads = '../../uploads/'
path_to_preprocessing_output = '../resources/preprocessing_output/'

#get the path of the most recently added file
filepath= utility.mostrecentfile()
print(filepath)


#apply the necessary preprocessing
outpath = image_preprocessing.persp_trans(filepath) #return output path of the file



#predict the model
category = predict.predict(filepath) #take path of the file as input and return the classification
print("document is: "+category)


#clean the  uploads and preprocessing_output directories
# utility.cleanup(path_to_uploads)
# utility.cleanup(path_to_preprocessing_output);
