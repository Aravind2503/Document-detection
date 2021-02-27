import docdetect
import cv2

image = cv2.imread('example.jpeg')

rects = docdetect.process(image)
print(rects)
img = docdetect.draw(rects,image)
cv2.imshow('image',img)
cv2.waitKey(0)