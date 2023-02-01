# mapowanie filtru bayer (x,y) -> 0|1|2
# gdzie r == 0, g == 1, b == 2
def get_mosaic_pixel_type_bayer(x, y):
    ret = 1
    if (x % 2 == 1) and (y % 2 == 0):
        ret = 0
    if (x % 2 == 0) and (y % 2 == 1):
        ret = 2
    return ret

# mapowanie filtru x-trans (x,y) -> 0|1|2
# gdzie r == 0, g == 1, b == 2
def get_mosaic_pixel_type_xtrans(x, y):
    if x % 6 in (0, 3) and y % 6 in (0, 3) \
            or x % 6 in (1, 2, 4, 5) and y % 6 in (1, 2, 4, 5):
        ret = 1
    elif x % 6 == 0 and y % 6 in (1, 5) \
            or x % 6 in (1, 5) and y % 6 == 3 \
            or x % 6 in (2, 4) and y % 6 == 0 \
            or x % 6 == 3 and y % 6 in (2, 4):
        ret = 0
    elif x % 6 == 0 and y % 6 in (2, 4) \
            or x % 6 in (1, 5) and y % 6 == 0 \
            or x % 6 in (2, 4) and y % 6 == 3 \
            or x % 6 == 3 and y % 6 in (1, 5):
        ret = 2
    return ret

# interpolacja bilinear
def get_interpolated_bilinear_rgb(image, x, y, get_mosaic_pixel_type_fn):
    r_sum, g_sum, b_sum = (0, 0, 0) # sumy kolorow
    r_cnt, g_cnt, b_cnt = (0, 0, 0) # ilości pixeli danego koloru
    r_value, b_value, g_value = (0, 0, 0) # średnie kolorow
    r_val0, g_val0, b_val0 = image.getpixel((x, y))
    w, h = image.size
    for i in range(-1, 2): # petle zbierajace wartosci z 9 pikseli
        for j in range(-1, 2):
            if x + j in range(0, w) and y + i in range(0, h):
                pixel_type = get_mosaic_pixel_type_fn(x + j, y + i) # funkcja zwracajaca kolor piksela
                r_val, g_val, b_val = image.getpixel((x + j, y + i))
                if pixel_type == 0:
                    r_sum += r_val
                    r_cnt += 1
                if pixel_type == 1:
                    g_sum += g_val
                    g_cnt += 1
                if pixel_type == 2:
                    b_sum += b_val
                    b_cnt += 1
    if r_cnt > 0:
        r_value = r_sum // r_cnt
    if g_cnt > 0:
        g_value = g_sum // g_cnt
    if b_cnt > 0:
        b_value = b_sum // b_cnt

    if get_mosaic_pixel_type_fn(x, y) == 0:
        r_value = r_val0
    elif get_mosaic_pixel_type_fn(x, y) == 1:
        g_value = g_val0
    elif get_mosaic_pixel_type_fn(x, y) == 2:
        b_value = b_val0

    return r_value, g_value, b_value

# interpolacja najblizszego sasiada
def get_interpolated_NN_rgb(image, x, y, get_mosaic_pixel_type_fn):
    r_sum, g_sum, b_sum = (0, 0, 0) # tu będą sumy
    r_cnt, g_cnt, b_cnt = (0, 0, 0) # tu będą ilości pixeli
    r_value, b_value, g_value = (0, 0, 0) # tu będą średnie
    w, h = image.size

    for i in range(2):  # zbieramy wartości z max 4 pixeli
        for j in range(2):
            if x + j in range(0, w) and y + i in range(0, h):  # ogarniamy krawędzie i narożniki
                pixel_type = get_mosaic_pixel_type_fn(x + j, y + i)
                r_val, g_val, b_val = image.getpixel((x + j, y + i))
                if pixel_type == 0:
                    r_sum += r_val
                    r_cnt += 1
                if pixel_type == 1:
                    g_sum += g_val
                    g_cnt += 1
                if pixel_type == 2:
                    b_sum += b_val
                    b_cnt += 1
    if r_cnt > 0:
        r_value = r_sum // r_cnt
    if g_cnt > 0:
        g_value = g_sum // g_cnt
    if b_cnt > 0:
        b_value = b_sum // b_cnt
    return r_value, g_value, b_value

