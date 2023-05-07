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


def filtrarKeypoints(keypoints:list):

    pass


def determinateKeypoints(img:np.array, k=1.6, mode='same', max_scale=3, num_ocatavas=4):

    imgCopy=np.copy(img)

    # Obtenemos la Gaussiana con sigma inicial de 0.7071876 por el video
    ultimoSigma=0.7071876
    #G = np.random.normal(loc=0, scale=ultimoSigma)

    # Convolucionamos la imagen con la Gaussiana como mascara
    # L(x, y, sigma) = G(x, y, sigma) * I(x, y) --> Donde '*' es el operador de la convolución
    # (Aplicar filtro de Gaussianas a la imagen, en este caso)
    # Como la convolución NO es commutativa,
    # haremos I '*' G, para aplicar los cambios a I (Aplicar el filtro Gaussiano a la Imagen)
    #L = np.convolve(img, G, mode=mode)

    DoG = []

    for ocatavActual in range(num_ocatavas):

        #generamos Gausiana
        G = np.random.normal(loc=0, scale=ultimoSigma)

        # haremos I '*' G, para aplicar los cambios a I (Aplicar el filtro Gaussiano a la Imagen)
        L = np.convolve(imgCopy, G, mode=mode)

        # Calculamos octavas hasta el maximo especificado en el hyperparametro
        for scale in range(max_scale):
            #amplitud o desviacion tipica del filtro Gaussiano
            #k = pow(2, 1 / scale)

            #guardamos la convolucion anterior
            Lant = L

            #generamos la nueva Gausiana con el anterior sigma por k, como cada iteracion se hace kAnterior*k, es com estar haciendo k^2->k^3...
            G = np.random.normal(scale=ultimoSigma*k)

            #nueva convolucion
            L = np.convolve(imgCopy, G, mode=mode)

            #calculo diferencia de Gaussianas
            D = L-Lant

            #guardamos las octavas para luego sacar los keypoints
            DoG.append(D)

            # en cada nueva octaba, el scale se duplica, uamos shift porque va mas rapido moviendo un bit
            #scale = scale << 1

        #se reduce la resolucion a la mitad
        imgCopy=imgCopy[int(imgCopy.shape[0]/2), int(imgCopy.shape[1]/2)]

        #cuando terminamos una octava, la siguiente empieza con k multiplicada por numero de octava, por tema de que se ha reducido la resolucion de la imagen a la mitad
        ultimoSigma=pow(k, ocatavActual)



    keyPoints=[]

    #ahora iremos mirando los puntos caracteristicos de cada capa segun su capa anterior y posterir, por ello no miramos la primera ni la ultima
    for capaDoG in range(1, len(DoG)):
        #iteramos pixel a pixel miranod 3(x)x3(y)x3(capa, z)-1(pixel que escogemos para mirar a su alrededor) pixeles
        for i in range(1, capaDoG.shape[0]):
            for j in range(1, capaDoG.shape[1]):

                #los prints son TEMPORALES PORQUE LOS IF SE UNIRAN EN UNO UNA VEZ COMPROBADO QUE TODO VA, todos los condicionales max y min se uniran en uno max y otro min


                #si el pixel es el maximo o el minimo de su alrededor en la capa o SCALA ACTUAL
                if img[i][j] == max(DoG[capaDoG][i-1][j-1], DoG[capaDoG][i-1][j], DoG[capaDoG][i][j+1],
                                    DoG[capaDoG][i][j-1], DoG[capaDoG][i][j+1], DoG[capaDoG][i+1][j-1],
                                    DoG[capaDoG][i+1][j], DoG[capaDoG][i+1][j+1]):
                    print("max de la capa ACTUAL")
                    #keyPoints.append((i, j))

                if img[i][j] == min(DoG[capaDoG][i-1][j-1], DoG[capaDoG][i-1][j], DoG[capaDoG][i][j+1], DoG[capaDoG][i][j-1],
                                    DoG[capaDoG][i][j+1], DoG[capaDoG][i+1][j-1], DoG[capaDoG][i+1][j],
                                    DoG[capaDoG][i+1][j+1]):
                    print("min de la capa ACTUAL")
                    #keyPoints.append((i, j))

                # si el pixel es el maximo o el minimo de su alrededor en la capa o SCALA ANTERIOR
                if img[i][j] == max(DoG[capaDoG-1][i - 1][j - 1], DoG[capaDoG-1][i - 1][j], DoG[capaDoG-1][i][j + 1],
                                    DoG[capaDoG-1][i][j - 1], DoG[capaDoG-1][i][j + 1], DoG[capaDoG-1][i + 1][j - 1],
                                    DoG[capaDoG-1][i + 1][j], DoG[capaDoG-1][i + 1][j + 1], DoG[capaDoG-1][i][j]):
                    print("max de la capa ANTERIOR")

                if img[i][j] == min(DoG[capaDoG-1][i - 1][j - 1], DoG[capaDoG-1][i - 1][j], DoG[capaDoG-1][i][j + 1], DoG[capaDoG-1][i][j - 1],
                                    DoG[capaDoG-1][i][j + 1], DoG[capaDoG-1][i + 1][j - 1], DoG[capaDoG-1][i + 1][j],
                                    DoG[capaDoG-1][i + 1][j + 1], DoG[capaDoG-1][i][j]):
                    print("min de la capa ANTERIOR")

                # si el pixel es el maximo o el minimo de su alrededor en la capa o SCALA POSTERIOR
                if img[i][j] == max(DoG[capaDoG + 1][i - 1][j - 1], DoG[capaDoG + 1][i - 1][j],
                                    DoG[capaDoG + 1][i][j + 1], DoG[capaDoG + 1][i][j - 1], DoG[capaDoG + 1][i][j + 1],
                                    DoG[capaDoG + 1][i + 1][j - 1], DoG[capaDoG + 1][i + 1][j],
                                    DoG[capaDoG + 1][i + 1][j + 1], DoG[capaDoG + 1][i][j]):
                    print("max de la capa POSTERIROR")

                if img[i][j] == min(DoG[capaDoG + 1][i - 1][j - 1], DoG[capaDoG + 1][i - 1][j],
                                    DoG[capaDoG + 1][i][j + 1], DoG[capaDoG + 1][i][j - 1],
                                    DoG[capaDoG + 1][i][j + 1], DoG[capaDoG + 1][i + 1][j - 1],
                                    DoG[capaDoG + 1][i + 1][j],
                                    DoG[capaDoG + 1][i + 1][j + 1], DoG[capaDoG + 1][i][j]):
                    print("min de la capa POSTERIOR")

    return keyPoints


def sift(img: np.array, scale=1.6):
    # Step 1: Approximate Keypoint Location

    keypoints = determinateKeypoints(img, scale)

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
