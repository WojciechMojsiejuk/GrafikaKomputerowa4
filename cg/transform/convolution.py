from abc import abstractmethod

import PIL
import numpy as np
from cg.transform.point import validate

class Filters:
    box_blur = np.ones((3, 3), dtype=int)
    sharpen = np.array([[0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]])

    gaussian_blur = np.array([[1, 2, 1],
                              [2, 4, 2],
                              [1, 2, 1]])

    sobel_vertical = np.array([
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]
        ])

    sobel_horizontal = np.array([
        [1, 2, 1],
        [0, 0, 0],
        [-1, -2, -1]
    ])


class Convolution:
    def __init__(self, kernel: np.ndarray, image: np.ndarray) -> None:
        self.kernel = kernel
        self.kernel_weight = self.calculate_kernel_weight()
        self.img = np.array(image)
        self.h_ext, self.w_ext = self.calculate_border_extension()
        self.height, self.width, self.channel = self.img.shape
        self.expand_img_dim()

    def calculate_border_extension(self) -> (int, int):
        return int((self.kernel.shape[0]-1)/2), int((self.kernel.shape[1]-1)/2)

    def expand_img_dim(self) -> None:
        expanded_img = np.zeros((self.height+2*self.h_ext, self.width+2*self.w_ext, self.channel), dtype=int)
        expanded_img[self.h_ext:self.height+self.h_ext, self.w_ext:self.width+self.w_ext, :] = self.img
        self.img = expanded_img

    def calculate_kernel_weight(self) -> int:
        kernel_weight = int(np.sum(self.kernel, dtype=int))
        if kernel_weight == 0:
            kernel_weight = 1
        return kernel_weight

    @abstractmethod
    def apply_filter(self):
        pass

    def return_img(self) -> PIL.Image.Image:
        image = self.img[self.h_ext:self.height+self.h_ext, self.w_ext:self.width+self.w_ext, :]
        return PIL.Image.fromarray(image.astype('uint8'), 'RGB')


class FilterConvolution(Convolution):
    def apply_filter(self):
        for y in range(self.h_ext, self.height+self.h_ext):
            for x in range(self.w_ext, self.width+self.w_ext):
                window_0 = self.img[y-self.h_ext:y+self.h_ext+1, x-self.w_ext:x+self.w_ext+1, 0]
                applied_window_0 = window_0 * self.kernel
                window_value_0 = round(np.sum(applied_window_0)/self.kernel_weight)

                window_1 = self.img[y - self.h_ext:y + self.h_ext+1, x - self.w_ext:x + self.w_ext+1, 1]
                applied_window_1 = window_1 * self.kernel
                window_value_1 = round(np.sum(applied_window_1) / self.kernel_weight)

                window_2 = self.img[y - self.h_ext:y + self.h_ext+1, x - self.w_ext:x + self.w_ext+1, 2]
                applied_window_2 = window_2 * self.kernel
                window_value_2 = round(np.sum(applied_window_2) / self.kernel_weight)

                self.img[y, x, 0] = validate(window_value_0)
                self.img[y, x, 1] = validate(window_value_1)
                self.img[y, x, 2] = validate(window_value_2)


class MedianFilterConvolution(Convolution):
    def apply_filter(self):
        for y in range(self.h_ext, self.height+self.h_ext):
            for x in range(self.w_ext, self.width+self.w_ext):
                window_0 = self.img[y - self.h_ext:y + self.h_ext+1, x - self.w_ext:x + self.w_ext+1, 0]
                window_value_0 = validate(int(np.median(window_0)))

                window_1 = self.img[y - self.h_ext:y + self.h_ext+1, x - self.w_ext:x + self.w_ext+1, 1]
                window_value_1 = validate(int(np.median(window_1)))

                window_2 = self.img[y - self.h_ext:y + self.h_ext+1, x - self.w_ext:x + self.w_ext+1, 2]
                window_value_2 = validate(int(np.median(window_2)))

                self.img[y, x, 0] = window_value_0
                self.img[y, x, 1] = window_value_1
                self.img[y, x, 2] = window_value_2
