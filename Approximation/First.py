from PIL import Image
import statistics as stat
import cv2
import Second

def median(img):
    w, h = img.size
    pixel = img.load()
    for i in range(1, h-1):
        for j in range(1, w-1):
            pixel[j, i] = Second.median_filter(img, j, i)

    return img


# --------MAIN----------

# filtr medianowy
# median(Image.open('Leopard-with-noise.jpg')).save('Median_filter.jpg')

# filtr splotowy (ruchoma srednia)
# cv2.imwrite('MovingAverage_filter_openCv_trianular.jpg', Second.moving_average(img = cv2.imread('Leopard-with-noise.jpg')))

# filtr bilateralny
cv2.imwrite('Bilateral_filter_openCv_2.jpg', Second.bilateral_filter(img = cv2.imread('Leopard-with-noise.jpg')))

# odejmowanie obrazow
# Second.subtraction(Image.open('Leopard-1.jpg'), Image.open('Median_filter.jpg')).save('Median_substraction.jpg')
# Second.subtraction(Image.open('Leopard-1.jpg'), Image.open('Bilateral_filter_openCv.jpg')).save('Bilateral_substraction.jpg')
# Second.subtraction(Image.open('Leopard-1.jpg'), Image.open('MovingAverage_filter_openCv.jpg')).save('MovingAverage_substraction.jpg')

# MSE
Second.MSE(Image.open('Leopard-1.jpg'), Image.open('Median_filter.jpg'))
Second.MSE(Image.open('Leopard-1.jpg'), Image.open('Bilateral_filter_openCv.jpg'))
Second.MSE(Image.open('Leopard-1.jpg'), Image.open('MovingAverage_filter_openCv.jpg'))
Second.MSE(Image.open('Leopard-1.jpg'), Image.open('MovingAverage_filter_openCv_trianular.jpg'))