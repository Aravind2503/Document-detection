#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
import numpy as np


def biggestContour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 5000:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return (biggest, max_area)


def order_points(pts):
    pts = pts.reshape((4, 2))
    newpts = np.zeros((4, 1, 2), dtype=np.int32)
    add = pts.sum(1)

    newpts[0] = pts[np.argmin(add)]
    newpts[3] = pts[np.argmax(add)]
    diff = np.diff(pts, axis=1)
    newpts[1] = pts[np.argmin(diff)]
    newpts[2] = pts[np.argmax(diff)]
    return newpts


def persp_trans(filepath):

        # Load image, convert to grayscale, and find edges

    image = cv2.imread(filepath)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU
    #                        + cv2.THRESH_BINARY)[1]
    # (width, height) = (600, 350)

    # # Find contour and sort by contour area

    # cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
    #                         cv2.CHAIN_APPROX_SIMPLE)
    # cnts = (cnts[0] if len(cnts) == 2 else cnts[1])
    # cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    # # perceptive transform

    # (b, m) = biggestContour(cnts)
    # a = order_points(b)
    # pts1 = np.float32(a)
    # pts2 = np.float32([[0, 0], [width, 0], [0, height], [width,
    #                   height]])
    # matrix = cv2.getPerspectiveTransform(pts1, pts2)
    # output = cv2.warpPerspective(image, matrix, (width, height))
    output = image
    outpath = '../resources/preprocessing_output/out.jpeg'
    cv2.imwrite(outpath, output)
    return outpath


if __name__ == '__main__':
    # biggestContour()
    # order_points()
    persp_trans('example3.jpeg')
