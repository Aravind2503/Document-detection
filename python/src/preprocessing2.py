import cv2
import numpy as np
import math
from sklearn.cluster import KMeans
from itertools import combinations
import warnings


def get_angle_between_lines(line_1, line_2):
    warnings.filterwarnings('ignore')
    rho1, theta1 = line_1
    rho2, theta2 = line_2

    m1 = -(np.cos(theta1) / np.sin(theta1))
    m2 = -(np.cos(theta2) / np.sin(theta2))
    return abs(math.atan(abs(m2 - m1) / (1 + m2 * m1))) * (180 / np.pi)


def intersection(line1, line2):
    rho1, theta1 = line1
    rho2, theta2 = line2

    A = np.array([[np.cos(theta1), np.sin(theta1)], [np.cos(theta2), np.sin(theta2)]])
    b = np.array([[rho1], [rho2]])
    x0, y0 = np.linalg.solve(A, b)
    x0, y0 = int(np.round(x0)), int(np.round(y0))
    return [[x0, y0]]


def draw_intersections(intersections, image, lines):
    intersection_point_output = image

    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        n = 5000
        x1 = int(x0 + n * (-b))
        y1 = int(y0 + n * (a))
        x2 = int(x0 - n * (-b))
        y2 = int(y0 - n * (a))

        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

        for point in intersections:
            x, y = point[0]
            cv2.circle(intersection_point_output, (x, y), 5, (255, 255, 127), 5)


def find_quadrilaterals(intersections):
    X = np.array([[point[0][0], point[0][1]] for point in intersections])
    kmeans = KMeans(n_clusters=4, init='k-means++', max_iter=100, n_init=10, random_state=0).fit(X)

    return [[center.tolist()] for center in kmeans.cluster_centers_]


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect


def extract_page(intersections, image):
    pts = np.array([(x, y) for intersection in intersections for x, y in intersection])
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped


def preprocess(image):
    copy = image.copy()

    temp = cv2.fastNlMeansDenoising(image, h=7)

    gray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)

    T_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=10)

    edges = cv2.Canny(closed, 50, 150, apertureSize=3)

    lines = cv2.HoughLines(edges, 2, np.pi / 180, 100)

    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            n = 1000
            pt1 = (int(x0 + (n * -b)), int(y0 + (n * a)))
            pt2 = (int(x0 - (n * -b)), int(y0 - (n * a)))
            cv2.line(image, pt1, pt2, (0, 0, 255), 3, cv2.LINE_AA)

    intersections = []
    group_lines = combinations(range(len(lines)), 2)
    x_in_range = lambda x: 0 <= x <= image.shape[1]
    y_in_range = lambda y: 0 <= y <= image.shape[0]

    for i, j in group_lines:
        line_i, line_j = lines[i][0], lines[j][0]

        if 80.0 < get_angle_between_lines(line_i, line_j) < 100.0:
            int_point = intersection(line_i, line_j)

            if x_in_range(int_point[0][0]) and y_in_range(int_point[0][1]):
                intersections.append(int_point)

    draw_intersections(intersections, image, lines)

    quad = find_quadrilaterals(intersections)

    extracted = extract_page(quad, copy)

    return extracted


def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img


# **Sharpen the image using Kernel Sharpening Technique**


def final_image(rotated):
    # Create our shapening kernel, it must equal to one eventually
    kernel_sharpening = np.array([[0, -1, 0],
                                  [-1, 5, -1],
                                  [0, -1, 0]])
    # applying the sharpening kernel to the input image & displaying it.
    sharpened = cv2.filter2D(rotated, -1, kernel_sharpening)
    sharpened = increase_brightness(sharpened, 30)
    return sharpened


image = cv2.imread('example2.jpeg')

cv2.imshow('image', final_image(preprocess(image)))

cv2.waitKey(0)