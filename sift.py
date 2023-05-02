import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import os

def load_images_from_folder(folder):
    image_names = [] # List where we are going to save the names of the images in the folder
    for path in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, path)):
            image_names.append(path)
    return image_names

def read_image(image_name):
    img = mpimg.imread(image_name)
    return img

def show_image(img, title="Imatge"):
    imgplot = plt.imshow(img)
    plt.title(title)
    plt.show()

def load_and_show_images(image1_name, image2_name):

    title_img_name = image1_name.split(sep="_")[2:5]
    title_img_name = str(title_img_name[0]) + " " + str(title_img_name[1]) + " "  + str(title_img_name[2].split(sep=".")[0]) + " | "
    print("Showing base images: ")
    img1 = read_image(image1_name)
    img2 = read_image(image2_name)
    show_image(img1,title_img_name + "Imatge1 base")
    show_image(img2,title_img_name + "Imatge2 base")

    # GRAY IMAGES:
    print("Showing gray images: ")
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    show_image(img1_gray,title_img_name +  "Gray image 1")
    show_image(img2_gray,title_img_name +  "Gray image 2")

    # Concatenate both images in one to see both of them at the same time and work with them as a single frame.
    frame = cv2.hconcat((img1, img2))  # Building the frame with both images (in RGB, not in Gray).
    show_image(frame, title_img_name + "Frame in RGB")

    return frame

def calculate_DoG():
    pass

def determinate_keypoints(img:np.array, k:int):
    #ocatava por la que vamos
    s=0


    k=pow(2, 1/s)
    pass

def shift():
    # Step 1: Approximate Keypoint Location

    return 0


if __name__ == '__main__':

    folder = 'img/base/'

    #cargamos los nombres de las imagenes
    image_names = load_images_from_folder(folder)
    print(image_names)

    #ordenamos los nombres de las imagenes
    image_names = sorted(image_names)
    print(image_names)
    # ================================
    #       LOAD AND SHOW IMAGES
    # ================================
    for im1_name, im2_name in zip(image_names[0::2], image_names[1::2]):
        frame = load_and_show_images(folder+im1_name, folder+im2_name)

