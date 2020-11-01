import numpy as np
import PIL


def validate(value: int) -> int:
    if value > 255:
        return 255
    elif value < 0:
        return 0
    else:
        return value


def additive(img: PIL.Image.Image, value: int) -> PIL.Image.Image:
    image = np.array(img)
    height, width, _ = image.shape
    for i in range(height):
        for j in range(width):
            r, g, b = image[i, j, :].tolist()
            r = r + value
            g = g + value
            b = b + value
            r = validate(r)
            g = validate(g)
            b = validate(b)
            image[i, j, :] = np.array([r, g, b])
    return PIL.Image.fromarray(image.astype('uint8'), 'RGB')


def multiplicative(img: PIL.Image.Image, value: float) -> PIL.Image.Image:
    image = np.array(img)
    height, width, _ = image.shape
    for i in range(height):
        for j in range(width):
            r, g, b = image[i, j, :].tolist()
            r = r * value
            g = g * value
            b = b * value
            r = validate(r)
            g = validate(g)
            b = validate(b)
            image[i, j, :] = np.array([r, g, b])
    return PIL.Image.fromarray(image.astype('uint8'), 'RGB')


def luminosity_grayscale(img: PIL.Image.Image) -> PIL.Image.Image:
    image = np.array(img)
    height, width, _ = image.shape
    for i in range(height):
        for j in range(width):
            r, g, b = image[i, j, :].tolist()
            value = int(0.299*r + 0.587*g + 0.114*b)
            value = validate(value)
            image[i, j, :] = np.array([value, value, value])
    return PIL.Image.fromarray(image.astype('uint8'), 'RGB')


def lightness_grayscale(img: PIL.Image.Image) -> PIL.Image.Image:
    image = np.array(img)
    height, width, _ = image.shape
    for i in range(height):
        for j in range(width):
            r, g, b = image[i, j, :].tolist()
            value = (min([r, g, b]) + max([r, g, b]))/2
            value = validate(value)
            image[i, j, :] = np.array([value, value, value])
    return PIL.Image.fromarray(image.astype('uint8'), 'RGB')


def average_grayscale(img: PIL.Image.Image) -> PIL.Image.Image:
    image = np.array(img)
    height, width, _ = image.shape
    for i in range(height):
        for j in range(width):
            r, g, b = image[i, j, :].tolist()
            value = (r + g + b)/3
            value = validate(value)
            image[i, j, :] = np.array([value, value, value])
    return PIL.Image.fromarray(image.astype('uint8'), 'RGB')


def brightness(img: PIL.Image.Image, value: float) -> PIL.Image.Image:
    image = np.array(img)
    height, width, _ = image.shape
    for i in range(height):
        for j in range(width):
            r, g, b = image[i, j, :].tolist()
            r = (r/255)**value * 255
            g = (g/255)**value * 255
            b = (b/255)**value * 255
            r = validate(r)
            g = validate(g)
            b = validate(b)
            image[i, j, :] = np.array([r, g, b])
    return PIL.Image.fromarray(image.astype('uint8'), 'RGB')
