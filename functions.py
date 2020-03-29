
from IPython.display import display as ipydisplay
import cv2
import matplotlib.pyplot as plt

def bgrtorgb(image):
    return cv2.cvtColor(image.copy(), cv2.COLOR_BGR2RGB)

def show_image(name):
    #   Showing image files from directory.
    ipydisplay(Image(name))

def plot_image(image, figsize=(8,8), recolour=False):
    # Plotting image matricies.
    if recolour: image = bgrtorgb(image)
    plt.figure(figsize=figsize)
    if image.shape[-1] == 3:
        plt.imshow(image)
    elif image.shape[-1] == 1 or len(image.shape) == 2:
        plt.imshow(image, cmap='gray')
    else:
        raise Exception("Image has invalid shape.")