import numpy as np
import PIL


def validate(value: int) -> int:
    if value > 255:
        return 255
    elif value < 0:
        return 0
    else:
        return value


def additive(img: PIL.Image.Image, value: int) -> np.ndarray:
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
    return image
