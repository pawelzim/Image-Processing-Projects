from PIL import Image
import statistics as stat
import cv2
import numpy as np

def median_filter(img, x, y):
    w, h = img.size
    r_val = []
    g_val = []
    b_val = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if x + j in range(0, w) and y + i in range(0, h):
                r, g, b = img.getpixel((x+j, y+i))
                r_val.append(r)
                g_val.append(g)
                b_val.append(b)

    r_ret = int(stat.median(r_val))
    b_ret = int(stat.median(b_val))
    g_ret = int(stat.median(g_val))

    return r_ret, g_ret, b_ret

def moving_average(img):
    kernel1 = np.ones((5, 5), np.float32) / 25  #jednorodny
    kernel2 = np.array([[0, 0, 1, 0, 0],
                       [0, 2, 2, 2, 0],
                       [1, 2, 5, 2, 1],
                       [0, 2, 2, 2, 0],
                       [0, 0, 1, 0, 0]])/25 #trojkatny
    org = cv2.filter2D(img, -1, kernel1)

    return org

def bilateral_filter(img):
    bilateral = cv2.bilateralFilter(img, 25, 100, 100)

    return bilateral

def subtraction(image1, image2):
    width, height = image1.size
    image3 = Image.new("RGB", [1024, 1024], (255, 255, 255))
    pixel = image3.load()
    for i in range(0, height):
        for j in range(0, width):
            r1, g1, b1 = image1.getpixel((j, i))
            r2, g2, b2 = image2.getpixel((j, i))
            r3 = r2-r1
            g3 = g2-g1
            b3 = b2-b1
            if r3 < 0:
                r3 = 0
            if g3 < 0:
                g3 = 0
            if b3 < 0:
                b3 = 0
            pixel[j, i] = (r3, g3, b3)

    return image3

def MSE(original_img, img):
    Y = np.square(np.subtract(original_img, img)).mean()
    print("MSE:", Y)