import tensorflow as tf
import cv2
# from google.colab import files
# import pytesseract


Categories = ['Aadhar','PAN']

img = cv2.imread('../../uploads/example_aadhar.jpeg')
print(img.shape)
img2 = cv2.resize(img,(224,224))
print(img2.shape)

def prepare(filepath):
  IMG_SIZE = 224
  img_array = cv2.imread(filepath)
  new_array = cv2.resize(img_array,(IMG_SIZE,IMG_SIZE))
  return new_array.reshape(-1,IMG_SIZE,IMG_SIZE,3,1)


model = tf.keras.models.load_model('../model/model1')

# print(img2.shape)
prediction = model.predict([prepare('../../uploads/example_aadhar.jpeg')])
print(prediction)
print(int(prediction[0][0]))
print( Categories[int(prediction[0][1])] )

# st = pytesseract.image_to_string(img)
# print(st)