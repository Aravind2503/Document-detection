import tensorflow as tf
import cv2
import os

# Categories = ['Aadhar','PAN']
l = [x[1] for x in os.walk('../resources/')]
l[2].sort()
Categories = l[2]
numcat = len(Categories)
threshold = 1/numcat

llll = [x[1] for x in os.walk('../model/')]
lll = llll[0]
# print(lll)


def prepare(filepath):
  IMG_SIZE = 224
  img_array = cv2.imread(filepath)
  new_array = cv2.resize(img_array,(IMG_SIZE,IMG_SIZE))
  return new_array.reshape(-1,IMG_SIZE,IMG_SIZE,3,1)


# model = tf.keras.models.load_model('../model/model1')

# # print(img2.shape)
# prediction = model.predict([prepare('../../uploads/example.jpeg')])
# print(prediction)
# print(int(prediction[0][0]))
# print( Categories[int(prediction[0][1])] )

# st = pytesseract.image_to_string(img)
# print(st)


def predict(filepath):
    img = cv2.imread(filepath)
    model_path =''
    
    if 'model2' in lll:
      model_path = '../model/model2'
    else:
      model_path = '../model/model1'


    #loading the trained model
    model = tf.keras.models.load_model(model_path) #make this dynamic later

    
    prediction = model.predict([prepare(filepath)])
    
    ll = list(prediction[0]) # converting numpy array to list 
    pos = ll.index(max(ll))
    

    if(ll[pos]>threshold):
      f = open("../resources/classification_output/out.txt", "w")
      f.write(Categories[pos])
      f.close()
      return ( Categories[pos] )
  
    else:
      return ('new')


    # return ( Categories[int(prediction[0][1])] )
      


    