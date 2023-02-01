from math import floor
from PIL import Image
import math
from math import log10, sqrt
import numpy as np
import cv2


def inter_line(f1, f2, d):
    return f1 * (1 - d) + f2 * d


def inter_cubic(f1, f2, f3, d):
    return f2 + (f3 - f1) * d + (f1 - 2 * f2 + f3) * d * d


def inter_cubic_norm(f1, f2, f3, d):
    inter_val = f2 + (f3 - f1) * d + (f1 - 2 * f2 + f3) * d * d
    if inter_val > 255:
        return 255
    elif inter_val < 0:
        return 0
    else:
        return round(inter_val)


# intrpolation_type == 0/1/2 (nearest/bilinear/bicubic)
def interpolation(intrpolation_type, image_src, image_dest):
    width_src, height_src = image_src.size
    width_dest, height_dest = image_dest.size
    ratio_x = width_src / width_dest
    ratio_y = height_src / height_dest
    pixels_dest = image_dest.load()
    for j in range(height_dest):
        for i in range(width_dest):
            if intrpolation_type in (0, 1):
                x = i * ratio_x
                y = j * ratio_y
                x0 = floor(x)
                y0 = floor(y)
                dx = x - x0
                dy = y - y0
                if x0 + 1 > width_src - 1:
                    x0_1 = x0
                else:
                    x0_1 = x0 + 1
                if y0 + 1 > height_src - 1:
                    y0_1 = y0
                else:
                    y0_1 = y0 + 1
                r00, g00, b00 = image_src.getpixel((x0, y0))
                r01, g01, b01 = image_src.getpixel((x0, y0_1))
                r10, g10, b10 = image_src.getpixel((x0_1, y0))
                r11, g11, b11 = image_src.getpixel((x0_1, y0_1))
                if intrpolation_type == 0:  # nearest
                    if dx < 0.5 and dy < 0.5:
                        pixels_dest[i, j] = (r00, g00, b00)
                    elif dx < 0.5 and dy >= 0.5:
                        pixels_dest[i, j] = (r01, g01, b01)
                    elif dx >= 0.5 and dy < 0.5:
                        pixels_dest[i, j] = (r10, g10, b10)
                    else:
                        pixels_dest[i, j] = (r11, g11, b11)
                elif intrpolation_type == 1:  # bilinear
                    pixels_dest[i, j] = (round(inter_line(inter_line(r00, r10, dx), inter_line(r01, r11, dx), dy)),
                                         round(inter_line(inter_line(g00, g10, dx), inter_line(g01, g11, dx), dy)),
                                         round(inter_line(inter_line(b00, b10, dx), inter_line(b01, b11, dx), dy)))
            elif intrpolation_type == 2:  # bicubic
                x = i * ratio_x
                y = j * ratio_y
                x1 = floor(x)
                y1 = floor(y)
                dx = x - x1
                dy = y - y1
                if x1 + 1 > width_src - 1:
                    x2 = x1
                else:
                    x2 = x1 + 1
                if x1 - 1 < 0:
                    x0 = x1
                else:
                    x0 = x1 - 1
                if y1 + 1 > height_src - 1:
                    y2 = y1
                else:
                    y2 = y1 + 1
                if y1 - 1 < 0:
                    y0 = y1
                else:
                    y0 = y1 - 1
                r00, g00, b00 = image_src.getpixel((x0, y0))
                r01, g01, b01 = image_src.getpixel((x0, y1))
                r02, g02, b02 = image_src.getpixel((x0, y2))
                r10, g10, b10 = image_src.getpixel((x1, y0))
                r11, g11, b11 = image_src.getpixel((x1, y1))
                r12, g12, b12 = image_src.getpixel((x1, y2))
                r20, g20, b20 = image_src.getpixel((x2, y0))
                r21, g21, b21 = image_src.getpixel((x2, y1))
                r22, g22, b22 = image_src.getpixel((x2, y2))
                pixels_dest[i, j] = (inter_cubic_norm(inter_cubic(r00, r10, r20, dx),
                                                      inter_cubic(r01, r11, r21, dx),
                                                      inter_cubic(r02, r12, r22, dx),
                                                      dy),
                                     inter_cubic_norm(inter_cubic(g00, g10, g20, dx),
                                                      inter_cubic(g01, g11, g21, dx),
                                                      inter_cubic(g02, g12, g22, dx),
                                                      dy),
                                     inter_cubic_norm(inter_cubic(b00, b10, b20, dx),
                                                      inter_cubic(b01, b11, b21, dx),
                                                      inter_cubic(b02, b12, b22, dx),
                                                      dy))





# scale_to - krotnosc powiekszenia (dla ujmenych pomniejszenia)
# intrpolation_type == 0/1/2 (nearest/bilinear/bicubic)
def scale_image(image, scale_to, interpolation_type):
    width_src, height_src = image.size
    if scale_to > 0:
        width_dest = scale_to * width_src
        height_dest = scale_to * height_src
    elif scale_to < 0:
        width_dest = round(width_src / abs(scale_to))
        height_dest = round(height_src / abs(scale_to))
    else:
        print('Error')
        quit()
    image_dest = Image.new("RGB", (width_dest, height_dest))
    interpolation(interpolation_type, image, image_dest)
    return image_dest

# pi/degree = kat obrocenia
def rotation(image_src, degree):
    width, height = image_src.size
    # kat obrocenia obrazka (pi == 180 stopni)
    M = math.pi / degree
    newimg = Image.new("RGB", [width, height])
    # środkowy pixel
    ctrX = width / 2
    ctrY = height / 2

    for i in range(0, height):
        for j in range(0, width):
            x = int(i - ctrX)
            y = int(ctrY - j)
            if x == 0:
                newimg.putpixel((x, y), image_src.getpixel((i, j)))
                newimg.putpixel((x + 1, y), image_src.getpixel((i, j)))
                newimg.putpixel((x, y + 1), image_src.getpixel((i, j)))
                newimg.putpixel((x + 1, y + 1), image_src.getpixel((i, j)))
            else:
                newx = x * math.cos(M) - y * math.sin(M)
                newy = x * math.sin(M) + y * math.cos(M)
                x = int(int(newx) + ctrX)
                y = int(ctrY - int(newy))
                if x < 0 or x >= width - 1 or y < 0 or y >= height - 1:
                    continue
                else:
                    newimg.putpixel((x, y), image_src.getpixel((i, j)))
                    newimg.putpixel((x + 1, y), image_src.getpixel((i, j)))
                    newimg.putpixel((x, y + 1), image_src.getpixel((i, j)))
                    newimg.putpixel((x + 1, y + 1), image_src.getpixel((i, j)))

    return newimg

def PSNR(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if (mse == 0):  # MSE is zero means no noise is present in the signal .
        # Therefore PSNR have no importance.
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr

# ----------Main------------



# scale_image(Image.open('interpolation.png'), -2, 0).save('down_Nearest.png')
# scale_image(Image.open('down_Nearest.png'), 2, 0).save('down_up_Nearest.png')
# #
# scale_image(Image.open('interpolation.png'), -2, 1).save('down_Bilinear.png')
# scale_image(Image.open('down_Bilinear.png'), 2, 1).save('down_up_Bilinear.png')
# #
# scale_image(Image.open('interpolation.png'), -2, 2).save('down_Bicubic.png')
# scale_image(Image.open('down_Bicubic.png'), 2, 2).save('down_up_Bicubic.png')

# rotation(Image.open('interpolation.png'), 3).save('rotated3.png')
# rotation(Image.open('interpolation.png'), 2).save('rotated2.png')

# original = cv2.imread("interpolation.png")
# compressed = cv2.imread("down_up_Nearest.png", 1)
#
# original2 = Image.open('interpolation.png')
# compressedx = Image.open('down_up_Bilinear.png')
#
# value = PSNR(original2, compressedx)
#
# compressed2 = cv2.imread('down_up_Bilinear.png')
# value2 = PSNR(original, compressed2)
#
# compressed3 = cv2.imread('down_up_Bicubic.png')
# value3 = PSNR(original, compressed3)
#
#
#
# print(f"PSNR value nearest is {value} dB")
# print(f"PSNR value bilinear is {value2} dB")
# print(f"PSNR value bicubic is {value3} dB")

scale_image(Image.open('interpolation.png'), 3, 1).save('up_Bilinear.png')