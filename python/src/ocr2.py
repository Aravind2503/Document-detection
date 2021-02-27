import os
import glob
import json
import pytesseract
from pytesseract import Output
import cv2
import utility
import re
import numpy as np










# img = cv2.imread("panamith2.jpeg")

# lower = np.array([50,50,50])  #-- Lower range --
# upper = np.array([127,127,127])  #-- Upper range --
# mask = cv2.inRange(img, lower, upper)
# res = cv2.bitwise_and(img, img, mask= mask)  #-- Contains pixels having the gray color--
# # cv2.imshow('Result',res)
# # cv2.waitKey(0)
# im,bigger1 = cv2.threshold(img,50,255,cv2.THRESH_BINARY)
# cv2.imshow('mask',bigger1)
# cv2.waitKey(0)















def processString(data):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    data1=''
    data2 = data.strip()

    for i in data2:
        if i.isalpha() == True or i in punctuations or i.isnumeric()==True or i == ' ':
            data1 += i
        else:
            data1 += ''
    return data1

# category_path = '../resources/classification_output/out.txt'
template_path = '../resources/templates/'
# image_path = '../resources/preprocessing_output/'
# ocr_out_path = '../resources/classification_output/out.json'

# im_path = utility.mostrecentfile(image_path)
im_path = 'panamith2.jpeg'
# print(im_path)

ocr_out_d = {}

# f = open(category_path, "r")
# cat = f.read()
cat = 'pan'

template_name = cat+'.json'
# print(template_name)

# print(os.listdir(template_path))
templates = os.listdir(template_path)

if template_name in templates:
    with open(template_path+template_name) as f:
        data = json.load(f)

    bigger = cv2.imread(im_path)
    # im,bigger2 = cv2.threshold(bigger,70,255,cv2.THRESH_BINARY)
    # im,bigger1 = cv2.threshold(bigger2,10,255,cv2.THRESH_BINARY)
    # gray = cv2.cvtColor(bigger1, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(bigger, (610, 388),interpolation = cv2.INTER_CUBIC)
    cv2.imshow('smaller',img)
    cv2.waitKey(0)
    print(img.shape)
    print(img.shape[1])
    # im,img = cv2.threshold(rimg,127,255,cv2.THRESH_BINARY)

    d = pytesseract.image_to_data(img, output_type = Output.DICT)
    print(len(d))
    # print(data)
    for i in data:
        
        
        points = data[i]#[[0][1]]
        y = points[0][1]
        x = points[0][0]
        x1 = points[1][0]
        y1 = points[1][1]
        w = abs(points[1][0]-points[0][0]);
        h = abs(points[1][1]-points[0][1]);

        ocr_out_d[i] = ''
        l = 0 
        for j,k in zip(d['left'],d['top']):
            
            # print(abs(x-j),abs(y-k))
            

            if (j-x) >=0 and abs(y-k) <=5 and int(d['conf'][l])>70 and (j-x1)<=15 and (k-y1)<=5: 
                
                

                ocr_out_d[i] += ' '+d['text'][l]
                # crop_img = img[y:y+h,x:w+x] #for cropping the image
                # text = pytesseract.image_to_string(crop_img,config='--psm 12 ')
                # text = text.split('\n')[0]
                # print(text)
                # with open(ocr_out_path, 'w') as fp:
                #     json.dump(ocr_out_d, fp)
                # cv2.imshow('crop_image',crop_img)
                # cv2.waitKey(0)
            # else:
            #     crop_img = img[y:y+h,x:w+x] #for cropping the image
            #     text = pytesseract.image_to_string(crop_img,config='--psm 12 ')
            #     ocr_out_d[i] = text
            # print(l)
            l += 1
            print(ocr_out_d)
    
    for i in ocr_out_d:
        # print(len(ocr_out_d[i]))
        ocr_out_d[i] = processString(ocr_out_d[i])

        if len(ocr_out_d[i]) == 0:
            points = data[i]#[[0][1]]
            y = points[0][1]
            x = points[0][0]
            w = abs(points[1][0]-points[0][0]);
            h = abs(points[1][1]-points[0][1]);
            crop_img = img[y:y+h,x:w+x] #for cropping the image
            # gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
            # im,img1 = cv2.threshold(gray,50,255,cv2.THRESH_BINARY)
            
            
            cv2.imshow('img',crop_img)
            cv2.waitKey(0)
            text = pytesseract.image_to_string(crop_img,config='--psm 12')
            
            ocr_out_d[i] = processString(text)
                # ocr_out_d[i] = (text)

    # print(ocr_out_d)
    

    for i in ocr_out_d:
        ocr_out_d[i] = processString(ocr_out_d[i])
    print(ocr_out_d)


    print('success')
else:
    print('fail')


        


            


