import matplotlib.pyplot as plt
from PIL import Image
import filters
import mosaic
from math import log10, sqrt
import cv2
import numpy as np

# mosaic.mosaic_color(Image.open('4demosaicking.bmp'), filters.get_mosaic_pixel_type_bayer).save('MosaicBayer.bmp')
# mosaic.mosaic_color(Image.open('4demosaicking.bmp'), filters.get_mosaic_pixel_type_xtrans).save('MosaicXTrans.bmp')

# plt.imshow(Image.open('MosaicBayer.bmp'))
# plt.show()
# plt.imshow(Image.open('MosaicXTrans.bmp'))
# plt.show()

# mosaic.demosaic(Image.open('MosaicBayer.bmp'), filters.get_mosaic_pixel_type_bayer, filters.get_interpolated_NN_rgb).save('DemosaicBayerNN.bmp')
# mosaic.demosaic(Image.open('MosaicXTrans.bmp'), filters.get_mosaic_pixel_type_xtrans, filters.get_interpolated_NN_rgb).save('DemosaicXTransNN.bmp')

# mosaic.demosaic(Image.open('MosaicBayer.bmp'), filters.get_mosaic_pixel_type_bayer, filters.get_interpolated_bilinear_rgb).save('DemosaicBayerBilinear2.bmp')
# mosaic.demosaic(Image.open('MosaicXTrans.bmp'), filters.get_mosaic_pixel_type_xtrans, filters.get_interpolated_bilinear_rgb).save('DemosaicXTransBilinear2.bmp')

def PSNR(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if (mse == 0):  # MSE is zero means no noise is present in the signal .
        # Therefore PSNR have no importance.
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr


# original = cv2.imread("4demosaicking.bmp")
# compressed = cv2.imread("DemosaicXTransBilinear2.bmp", 1)
# value = PSNR(original, compressed)
#
# compressed2 = cv2.imread("DemosaicXTransBilinear.bmp", 1)
# value2 = PSNR(original, compressed2)
#
# compressed3 = cv2.imread("DemosaicBayerBilinear2.bmp", 1)
# value3 = PSNR(original, compressed3)
#
# compressed4 = cv2.imread("DemosaicBayerBilinear.bmp", 1)
# value4 = PSNR(original, compressed4)
#
# print(f"PSNR value XTrans is {value} dB")
# print(f"PSNR value Bayer is {value4} dB")

mosaic.subtraction(Image.open('4demosaicking.bmp'), Image.open('DemosaicBayerNN.bmp')).save('Substracion_Bayer_NN.bmp')
