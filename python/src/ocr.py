import os
import glob
import json
import pytesseract
import cv2
import utility
import re


category_path = '../resources/classification_output/out.txt'
template_path = '../resources/templates/'
image_path = '../resources/preprocessing_output/'
ocr_out_path = '../resources/classification_output/out.json'

im_path = utility.mostrecentfile(image_path)
# print(im_path)

ocr_out_d = {}

f = open(category_path, "r")
cat = f.read()

template_name = cat+'.json'
# print(template_name)

# print(os.listdir(template_path))
templates = os.listdir(template_path)

if template_name in templates:
    with open(template_path+template_name) as f:
        data = json.load(f)

    img = cv2.imread(im_path)
    # print(data)
    for i in data:
    
        
        points = data[i]#[[0][1]]
        y = points[0][1]
        x = points[0][0]
        w = abs(points[1][0]-points[0][0]);
        h = abs(points[1][1]-points[0][1]);
            
        # print(points,y,x,w,h)

        crop_img = img[y:y+h,x:w+x] #for cropping the image
        text = pytesseract.image_to_string(crop_img,config='--psm 12 ')
        text = text.split('\n')[0]
        # print(text)
        ocr_out_d[i]=text
        # print(ocr_out_d)
        with open(ocr_out_path, 'w') as fp:
            json.dump(ocr_out_d, fp)
        # cv2.imshow('crop_image',crop_img)
        # cv2.waitKey(0)
    print('success')
else:
    print('fail')


        


            


