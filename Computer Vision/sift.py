import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import math
import os
import statistics


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
    #print("Showing base images: ")
    img1 = read_image(image1_name)
    img2 = read_image(image2_name)
    #show_image(img1, title_img_name + "Imatge1 base")
    #show_image(img2, title_img_name + "Imatge2 base")

    # GRAY IMAGES:
    #print("Showing gray images: ")
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    #show_image(img1_gray, title_img_name + "Gray image 1")
    #show_image(img2_gray, title_img_name + "Gray image 2")

    # Concatenate both images in one to see both of them at the same time and work with them as a single frame.
    frame = cv2.hconcat((img1, img2))  # Building the frame with both images (in RGB, not in Gray).
    show_image(frame, title_img_name + "Frame in RGB")

    return frame, img1_gray, img2_gray


def filtrarKeypoints(keyPoints:list, DoG:list):

    pass

#ESTRUCTURAS
#keyPoints: list[capaDog, tupla(coordenadas)]
#scales: list[sigma, imagenSuavizada]
#DoG: list[dict{'D':matrizDoG, 'scales':tupla(indicesScalesProgenitoras)}]
def assignOrientation(keyPoints:list, scales:list, num_bins=36):

    scale = 1

    #calculo de magnitudes y orientaciones
    for infoKeypoint in keyPoints:

        # creamos un numpy array con 36 ellementos, 1 por cada bin, cada bin por cada 10 grados
        orientation_histogram = np.zeros(num_bins)

        #NO HACE FALTA GUARDAR LA TUPLA DE LAS SCALES GENERADORAS DE LA DoG, en su lugar guardar en lista de keypoints el scale al que pertenece, no el DoG

        #si el valor del keypoint es superior que los valores del mismo en DoG superior y inferior, escogemos la imagen suavizada, scale con k inferior
        #if DoG[infoKeypoint[0]]['D'][infoKeypoint[1][0]][infoKeypoint[1][1]] == max(DoG[infoKeypoint[0]]['D'][infoKeypoint[1][0]][infoKeypoint[1][1]], DoG[infoKeypoint[0]-1]['D'][infoKeypoint[1][0]][infoKeypoint[1][1]], DoG[infoKeypoint[0]+1]['D'][infoKeypoint[1][0]][infoKeypoint[1][1]]):
            #scale=1
        #else:
            #scale=0

        #caclulode vecinos que observar segun la scala del keypoint, 1.5 veces sigma de la scale
        radio=int(1.5*infoKeypoint[0])

        for i in range(infoKeypoint[1][1]-radio, infoKeypoint[1][1]+radio):
            for j in range(infoKeypoint[1][1]-radio, infoKeypoint[1][1]+radio):

                magnitud=math.sqrt(pow(scales[DoG[infoKeypoint[0]]['scales'][scale]][1][i+1][j]-scales[DoG[infoKeypoint[0]]['scales'][scale]][1][i-1][j], 2) + pow(scales[DoG[infoKeypoint[0]]['scales'][scale]][1][i][j+1]-scales[DoG[infoKeypoint[0]]['scales'][scale]][1][i][j-1], 2))
                orientacio=math.atan(pow(scales[DoG[infoKeypoint[0]]['scales'][scale]][1][i][j+1]-scales[DoG[infoKeypoint[0]]['scales'][scale]][1][i][j-1], 2) / pow(scales[DoG[infoKeypoint[0]]['scales'][scale]][1][i+1][j]-scales[DoG[infoKeypoint[0]]['scales'][scale]][1][i-1][j], 2))

                #ponemos valor absoluto a la orientacion en caso de que de un angulo negativo y dividimos entre el numero de bins para que no salga de este rango
                if orientacio != 0:
                    bin_index = int(abs(orientacio) / (360 / num_bins))
                else:
                    bin_index = int(360/ (360 / num_bins))#si la orientacion es 0 equivale a 360 grados, subtituimos para evitar dividir 0, error

                #añadimos la orientacion ponderada segun la media de la sigma de la scale de esta y su magnitud
                orientation_histogram[bin_index] += statistics.mean([1.5 * scales[DoG[infoKeypoint[0]]['scales'][scale]][0], magnitud]) * orientacio

        plt.hist(orientation_histogram, bins=num_bins)
        plt.show()

        #creacion nuevo keypoint con la orientacion que en el histograma tiene mas de 80%, mismas coordenadas, diferente angulo

        #creacion descriptor

    pass

def determinateKeypoints2(img:np.array, k:float, mode:str, max_scale:int, num_ocatavas:int, kernelSize:int):
    imgCopy=np.copy(img)

    # Obtenemos la Gaussiana con sigma inicial de 0.7071876 por el video
    sigmaInicial=0.7071876
    nuevaSigma=0.7071876


    scales = []
    keyPoints = []

    #creamos diferentes octavas con diferentes scales para obtener las diferencias de Gaussianas
    for ocatavActual in range(num_ocatavas):

        DoG = []

        exponenteK=ocatavActual+1

        # generamos Gausian KERNEL de 1 dimension
        G = cv2.getGaussianKernel(kernelSize, sigmaInicial * pow(k, exponenteK))
        G = np.outer(G, G)  # genera Gaussian Kernel de 2 dimensiones

        # convolucionamos, -1 indica queremos un resultado del mismo tamaño de la imagen
        L0 = cv2.filter2D(imgCopy, -1, G)

        # guardamos la imagent suavizada, L, con sus sigma para luego calcular orientacion
        scales.append((nuevaSigma, L0))

        exponenteK += 1

        # nueva sigma, se pone +1 porque se necesita el numeron de scales, en scale 0 llevamos 1 scale
        nuevaSigma *= pow(k, exponenteK)

        # Calculamos escalas hasta el maximo especificado en el hyperparametro
        for scale in range(max_scale):

            # generamos la nueva Gausiana con el anterior sigma por k
            G = cv2.getGaussianKernel(kernelSize, nuevaSigma)
            G = np.outer(G, G)  # genera Gaussian Kernel de 2 dimensiones

            # convolucionamos, -1 indica que queremos un resultado del mismo tamaño de la imagen
            L1 = cv2.filter2D(imgCopy, -1, G)
            scales.append((nuevaSigma, L1))

            exponenteK += 1

            # nueva sigma, se pone +1 porque se necesita el numeron de scales, en scale 0 llevamos 1 scale
            nuevaSigma *= pow(k, exponenteK)

            G = cv2.getGaussianKernel(kernelSize, nuevaSigma)
            G = np.outer(G, G)  # genera Gaussian Kernel de 2 dimensiones

            L2 = cv2.filter2D(imgCopy, -1, G)
            scales.append((nuevaSigma, L2))

            exponenteK += 1

            # nueva sigma, se pone +1 porque se necesita el numeron de scales, en scale 0 llevamos 1 scale
            nuevaSigma *= pow(k, exponenteK)

            G = cv2.getGaussianKernel(kernelSize, nuevaSigma)
            G = np.outer(G, G)  # genera Gaussian Kernel de 2 dimensiones

            L3 = cv2.filter2D(imgCopy, -1, G)
            scales.append((nuevaSigma, L3))

            #calculo diferencia de Gaussianas
            D0 = L1 - L0
            D1 = L2 - L1
            D2 = L3 - L2

            #guardamos diferencias para luego busacar keypoints eficientemente
            DoG.append(D0)
            DoG.append(D1)
            DoG.append(D2)

            #Guardamos la ultima imagen suavizada para calculo de la siguiente D
            L0 = L3


        # para mirar vecindad evitaremos los bordes, fila 0 y n, col 0 y n
        for i in range(1, img.shape[0] - 1):
            for j in range(1, img.shape[1]  - 1):

                subMatrizActual = DoG[0][i - 1:i + 2, j - 1:j + 2]
                subMatrizAnterior = DoG[1][i - 1:i + 2, j - 1:j + 2]
                subMatrizPosterior = DoG[2][i - 1:i + 2, j - 1:j + 2]


                #esta comparacion tiene utilidad para ahorrar una comparacion con las DoG 1,2,3 ya tendremos la comparacion de 1 con 2
                maxUtil= max(np.max(subMatrizActual), np.max(subMatrizPosterior))

                #si no cumple ser el maximo entre las 2 capas no hace falta continuar porque no sera el max
                if maxUtil == DoG[1][i,j]:
                    if DoG[1][i,j] == max(np.max(subMatrizActual), np.max(subMatrizAnterior)):

                        # concatenar las submatrizes
                        subMatriz = np.concatenate((subMatrizActual, subMatrizAnterior, subMatrizPosterior), axis=0)

                        # si el pixel es un maximo unico, no aparace el valor de nuevo en la submatriz, se considera key point
                        if np.count_nonzero(subMatriz == DoG[1][i, j]) == 1:
                            keyPoints.append(((0, 1), (i,j)))  # añadimos en que scala se encuentra para luego las orientaciones, sabemos que si es la DoG 1, estara entre las escalas 0 y 2
                else:
                    minUtil = min(np.min(subMatrizActual), np.min(subMatrizPosterior))

                    if minUtil == DoG[1][i,j]:
                        if DoG[1][i,j] == min(np.max(subMatrizActual), np.min(subMatrizAnterior)):
                            # concatenar las submatrizes
                            subMatriz = np.concatenate((subMatrizActual, subMatrizAnterior, subMatrizPosterior), axis=0)

                            # si el pixel es un maximo unico, no aparace el valor de nuevo en la submatriz, se considera key point
                            if np.count_nonzero(subMatriz == DoG[1][i, j]) == 1:
                                keyPoints.append(((0, 1), (i, j)))  # añadimos en que scala se encuentra para luego las orientaciones, sabemos que si es la DoG 1, estara entre las escalas 0 y 2

                #se compara con la siguiente scale de las DoG
                for scaleDoG in range(2, len(DoG)-1):

                    subMatrizPosterior = DoG[scaleDoG + 1][i - 1:i + 2, j - 1:j + 2]
                    maxUtil = max(maxUtil, np.max(subMatrizPosterior))

                    if maxUtil == DoG[scaleDoG][i, j]:

                        subMatrizActual = DoG[scaleDoG][i - 1:i + 2, j - 1:j + 2]
                        subMatrizAnterior = DoG[scaleDoG][i - 1:i + 2, j - 1:j + 2]

                        # concatenar las submatrizes
                        subMatriz = np.concatenate((subMatrizActual, subMatrizAnterior, subMatrizPosterior), axis=0)

                        # si el pixel es un maximo unico, no aparace el valor de nuevo en la submatriz, se considera key point
                        if np.count_nonzero(subMatriz == DoG[scaleDoG][i, j]) == 1:
                            keyPoints.append(((0, 1), (i, j)))  # añadimos en que scala se encuentra para luego las orientaciones, sabemos que si es la DoG 1, estara entre las escalas 0 y 2
                    else:

                        minUtil = min(minUtil, np.min(subMatrizPosterior))

                        if minUtil == DoG[scaleDoG][i, j]:

                            subMatrizActual = DoG[scaleDoG][i - 1:i + 2, j - 1:j + 2]
                            subMatrizAnterior = DoG[scaleDoG][i - 1:i + 2, j - 1:j + 2]

                            # concatenar las submatrizes
                            subMatriz = np.concatenate((subMatrizActual, subMatrizAnterior, subMatrizPosterior), axis=0)

                            # si el pixel es un maximo unico, no aparace el valor de nuevo en la submatriz, se considera key point
                            if np.count_nonzero(subMatriz == DoG[scaleDoG][i, j]) == 1:
                                keyPoints.append(((0, 1), (i, j)))  # añadimos en que scala se encuentra para luego las orientaciones, sabemos que si es la DoG 1, estara entre las escalas 0 y 2

        # se reduce la resolucion a la mitad de la octava anterior, para esto se necesita mantener la informacion original, img
        # se subtituye los valores de los pixeles de n columnas, cada octava tiene la mitad de innfromacion de la aterior,
        # esto significa el doble de columnas son subtituidas en cada octava
        imgCopy[:, 1::pow(2, ocatavActual + 1)] = img[:, 0::pow(2, ocatavActual + 1)]


def determinateKeypoints(img:np.array, k:float, mode:str, max_scale:int, num_ocatavas:int, kernelSize:int):

    imgCopy=np.copy(img)

    # Obtenemos la Gaussiana con sigma inicial de 0.7071876 por el video
    sigmaInicial=0.7071876
    nuevaSigma=0.7071876

    DoG = []
    scales = []
    #creamos diferentes octavas con diferentes scales para obtener las diferencias de Gaussianas
    for ocatavActual in range(num_ocatavas):

        exponenteK=ocatavActual+1

        # generamos Gausian KERNEL de 1 dimension
        G = cv2.getGaussianKernel(kernelSize, sigmaInicial * pow(k, exponenteK))
        G = np.outer(G, G)  # genera Gaussian Kernel de 2 dimensiones

        # convolucionamos, -1 indica queremos un resultado del mismo tamaño de la imagen
        L = cv2.filter2D(imgCopy, -1, G)

        # guardamos la imagent suavizada, L, con sus sigma para luego calcular orientacion
        scales.append((nuevaSigma, L))

        # nueva sigma, se pone +1 porque se necesita el numeron de scales, en scale 0 llevamos 1 scale
        nuevaSigma *= pow(k, exponenteK+1)

        # Calculamos escalas hasta el maximo especificado en el hyperparametro
        for scale in range(max_scale):


            #guardamos la convolucion anterior
            Lant = L

            #generamos la nueva Gausiana con el anterior sigma por k
            G = cv2.getGaussianKernel(kernelSize, nuevaSigma)
            G = np.outer(G, G)  # genera Gaussian Kernel de 2 dimensiones

            # convolucionamos, -1 indica que queremos un resultado del mismo tamaño de la imagen
            L = cv2.filter2D(imgCopy, -1, G)
            scales.append((nuevaSigma, L))

            #calculo diferencia de Gaussianas
            D = L-Lant

            #guardamos las octavas para luego sacar los keypoints y los indices de las escalas de donde las obtenemos
            DoG.append(D)

            #nueva sigma, se pone +1 porque se necesita el numeron de scales, en scale 0 llevamos 1 scale
            nuevaSigma *= pow(k, exponenteK+1)


        #se reduce la resolucion a la mitad de la octava anterior, para esto se necesita mantener la informacion original, img
        #se subtituye los valores de los pixeles de n columnas, cada octava tiene la mitad de innfromacion de la aterior,
        #esto significa el doble de columnas son subtituidas en cada octava
        imgCopy[:, 1::pow(2, ocatavActual+1)]=img[:, 0::pow(2, ocatavActual+1)]


    keyPoints=[]

    #ahora iremos mirando los puntos caracteristicos de cada capa segun su capa anterior y posterir, por ello no miramos la primera ni la ultima
    for capaDoG in range(1, len(DoG)-1):
        #iteramos pixel a pixel miranod 3(x)x3(y)x3(capa, z)-1(pixel que escogemos para mirar a su alrededor) pixeles
        for i in range(1, DoG[capaDoG].shape[0]-1):
            for j in range(1, DoG[capaDoG].shape[1]-1):

                subMatrizActual=DoG[capaDoG][i-1:i+2, j-1:j+2]
                subMatrizAnterior = DoG[capaDoG - 1][i - 1:i + 2, j - 1:j + 2]
                subMatrizPosterior = DoG[capaDoG + 1][i - 1:i + 2, j - 1:j + 2]

                #si el pixel es el maximo o el minimo de su alrededor en la capa o SCALA ACTUAL
                if DoG[capaDoG][i, j] != 0 and max(np.max(subMatrizActual), np.max(subMatrizAnterior),np.max(subMatrizPosterior)) == DoG[capaDoG][i,j]:
                    #concatenar las submatrizes
                    subMatriz = np.concatenate((subMatrizActual, subMatrizAnterior, subMatrizPosterior), axis=0)

                    #si el pixel es un maximo unico, no aparace el valor de nuevo en la submatriz, se considera key point
                    if np.count_nonzero(subMatriz == DoG[capaDoG][i,j]) == 1:
                        keyPoints.append(((capaDoG, capaDoG+1), (i, j))) # añadimos en que scala se encuntra para luego las orientaciones, sabemos que si es la DoG 5, estara entre las escalas 5 y 6

                elif DoG[capaDoG][i, j] != 0 and min(np.min(subMatrizActual), np.min(subMatrizAnterior), np.min(subMatrizPosterior)) == DoG[capaDoG][i, j]:
                    # concatenar las submatrizes
                    subMatriz = np.concatenate((subMatrizActual, subMatrizAnterior, subMatrizPosterior), axis=0)

                    # si el pixel es un maximo unico, no aparace el valor de nuevo en la submatriz, se considera key point
                    if np.count_nonzero(subMatriz == DoG[capaDoG][i, j]) == 1:
                        keyPoints.append(((capaDoG, capaDoG+1), (i, j))) # añadimos en que scala se encuntra para luego las orientaciones, sabemos que si es la DoG 5, estara entre las escalas 5 y 6

    return keyPoints, scales


def sift(img: np.array, k=1.6, mode='same', max_scale=3, num_ocatavas=4, kernelSize=3):
    # Step 1: Approximate Keypoint Location

    keyPoints, scales = determinateKeypoints(img, k, mode, max_scale, num_ocatavas, kernelSize)

    #reducir los outliers en los keypoints
    #keypoints = filtrarKeypoints(keyPoints, DoG)

    #asignar orientacion a los keypoints
    assignOrientation(keyPoints, scales)

    return 0


if __name__ == '__main__':

    folder = 'Computer Vision/img/base/'

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
        #devuelve un frame con las 2 imagenes unidas y carga las 2 imagenes en gris
        frame, imgGray1, imgGray2 = load_and_show_images((folder + im1_name), (folder + im2_name))
        sift(imgGray1)
        sift(imgGray2)