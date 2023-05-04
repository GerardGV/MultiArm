import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import scipy
import os


def load_images_from_folder(folder):
    image_names = []  # List where we are going to save the names of the images in the folder
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
    title_img_name = str(title_img_name[0]) + " " + str(title_img_name[1]) + " " + str(
        title_img_name[2].split(sep=".")[0]) + " | "
    print("Showing base images: ")
    img1 = read_image(image1_name)
    img2 = read_image(image2_name)
    show_image(img1, title_img_name + "Imatge1 base")
    show_image(img2, title_img_name + "Imatge2 base")

    # GRAY IMAGES:
    print("Showing gray images: ")
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    show_image(img1_gray, title_img_name + "Gray image 1")
    show_image(img2_gray, title_img_name + "Gray image 2")

    # Concatenate both images in one to see both of them at the same time and work with them as a single frame.
    frame = cv2.hconcat((img1, img2))  # Building the frame with both images (in RGB, not in Gray).
    show_image(frame, title_img_name + "Frame in RGB")

    return frame


def calculate_DoG():
    pass


def determinate_keypoints(img: np.array, scale: float, mode='same', max_scale=256):
    # Obtenemos la Gaussiana -->
    # G(x, y, sigma) = (1 / (2 * pi * sigma^2)) * e^(-(x^2+y^2)/2*sigma^2)
    G = np.random.normal(loc=0, scale=scale)

    # Convolucionamos la imagen con la Gaussiana como mascara
    # L(x, y, sigma) = G(x, y, sigma) * I(x, y) --> Donde '*' es el operador de la convolución
    # (Aplicar filtro de Gaussianas a la imagen, en este caso)
    # Como la convolución NO es commutativa,
    # haremos I '*' G, para aplicar los cambios a I (Aplicar el filtro Gaussiano a la Imagen)
    L = np.convolve(img, G, mode=mode)

    octavas= []

    # Calculamos octavas hasta el maximo especificado en el hyperparametro
    while scale <= max_scale:
        #amplitud o desviacion tipica del filtro Gaussiano
        k = pow(2, 1 / scale)

        #guardamos la convolucion anterior
        Lant = L

        #generamos la nueva Gausiana con sigma diferente
        G = np.random.normal(scale=scale*k)

        #nueva convolucion
        L = np.convolve(img, G, mode=mode)

        #calculo diferencia de Gaussianas
        D = L-Lant

        #guardamos las octavas para luego sacar los keypoints
        octavas.append(D)

        # en cada nueva octaba, el scale se duplica, uamos shift porque va mas rapido moviendo un bit
        scale = scale << 1

    keyPoints=[]

    #escogemos puntos caracteristicos entre los puntos de interes
    for i in range(1, img.shape[0]):
        for j in range(1, img.shape[1]):

            #si el pixel es el maximo o el minimo de su alrededor(area 3x3 en 3 capas) seguarda
            if img[i][j] == max(img[i-1][j-1], img[i-1][j],img[i][j+1], img[i][j-1], img[i][j+1], img[i+1][j-1], img[i+1][j], img[i+1][j+1]):
                keyPoints.append(img[i][j])

            if img[i][j] == min(img[i-1][j-1], img[i-1][j],img[i][j+1], img[i][j-1], img[i][j+1], img[i+1][j-1], img[i+1][j], img[i+1][j+1]):
                keyPoints.append(img[i][j])
    pass


def sift(img: np.array, scale=1.6):
    # Step 1: Approximate Keypoint Location

    keypoints = determinate_keypoints(img, scale)
    return 0


if __name__ == '__main__':

    folder = 'img/base/'

    # cargamos los nombres de las imagenes
    image_names = load_images_from_folder(folder)
    print(image_names)

    # ordenamos los nombres de las imagenes
    image_names = sorted(image_names)
    print(image_names)
    # ================================
    #       LOAD AND SHOW IMAGES
    # ================================
    for im1_name, im2_name in zip(image_names[0::2], image_names[1::2]):
        frame = load_and_show_images(folder + im1_name, folder + im2_name)
