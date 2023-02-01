from PIL import Image

# mozaikowanie
# get_mosaic_pixel_type_fn - rodzaj mozaiki (bayer, x-trans)
def mosaic_color(image, get_mosaic_pixel_type_fn):
    ret = Image.new("RGB", image.size)
    width, height = image.size
    pixel = ret.load()
    for i in range(height):
        for j in range(width):
            pt = get_mosaic_pixel_type_fn(j, i)
            r, g, b = image.getpixel((j, i))
            if pt == 0:
                pixel[j, i] = (r, 0, 0)
            elif pt == 1:
                pixel[j, i] = (0, g, 0)
            else:
                pixel[j, i] = (0, 0, b)
    return ret

# demozaikowanie
# get_mosaic_pixel_type_fn - rodzaj mozaiki (bayer, x-trans)
# get_interpolated_rgb_fn - nazwa funkcji interpolującej, która ma być użyta do odtworzenia kolorów
def demosaic(image, get_mosaic_pixel_type_fn, get_interpolated_rgb_fn):
    ret = Image.new("RGB", image.size)
    width, height = image.size
    pixel = ret.load()
    for i in range(height):
        for j in range(width):
            pixel[j, i] = get_interpolated_rgb_fn(image, j, i, get_mosaic_pixel_type_fn)
    return ret

def subtraction(image1, image2):
    width, height = image1.size
    image3 = Image.new("RGB", [width, height], (255, 255, 255))
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