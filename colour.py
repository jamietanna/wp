from colorz import colorz
from math   import sqrt
import colorsys

from array import array
from generic import output

def torgb(hexv):
    hexv = hexv[1:]
    r, g, b = (
        int(hexv[0:2], 16) / 256.0,
        int(hexv[2:4], 16) / 256.0,
        int(hexv[4:6], 16) / 256.0,
    )
    return r, g, b

def normalize(hexv, minv=128, maxv=256):
    r, g, b = torgb(hexv)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    minv = minv / 256.0
    maxv = maxv / 256.0
    if v < minv:
        v = minv
    if v > maxv:
        v = maxv
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return '#{:02x}{:02x}{:02x}'.format(int(r * 256), int(g * 256), int(b * 256))

def darkness(hexv):
  r, g, b = torgb(hexv)
  darkness = sqrt((255 - r) ** 2 + (255 - g) ** 2 + (255 - b) ** 2)
  return darkness

def to_hsv(c):
    r, g, b = torgb(c)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return h, s, v

def get_colours(path):
    colours = colorz(path, 16)
    # ####### HACK! !!!!!!!!!!!!!!!!!!!!!!!!
    # colours = ['#774d38', '#4a3a2b', '#f1ae39', '#d37837', '#182220', '#a15330', '#0e1211', '#212e2c', '#5e4534', '#f6f5b6', '#28271f', '#f4de5b', '#434338', '#34352d', '#030201', '#649386']

    colours_sort = list(colours)
    colours_sort.sort(key=lambda  x:darkness(x), reverse=True)

    colours_normalised = []
    ret = []

    indexes = array('i', [0] * 16)
    for idx, c in enumerate(colours_sort):
        indexes[colours.index(c)] = idx

    for i, c in enumerate(colours_sort):
        if i == 0:
            c = normalize(c, minv=0, maxv=32)
        elif i == 8:
            c = normalize(c, minv=128, maxv=192)
        elif i < 8:
            c = normalize(c, minv=160, maxv=224)
        else:
            c = normalize(c, minv=200, maxv=256)
        c = normalize(c, minv=32, maxv=224)
        colours_normalised.append(c)

    # for c in colours_normalised:

    for idx, val in enumerate(indexes):
        ret.append(colours_normalised[val])

    return ret

