import utility
import predict
import perspective_transform


path_to_uploads = '../../uploads/'
path_to_preprocessing_output = '../resources/preprocessing_output/'

#get the path of the most recently added file
filepath= utility.mostrecentfile(path_to_uploads)
# print(filepath)


#apply the necessary preprocessing
outpath = perspective_transform.persp_trans(filepath) #return output path of the file



#predict the model
category = predict.predict(outpath) #take path of the file as input and return the classification
print(category)


#clean the  uploads and preprocessing_output directories
# utility.cleanup(path_to_uploads)
# utility.cleanup(path_to_preprocessing_output);
