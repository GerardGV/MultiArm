import time

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
    img1_gray=img1_gray.astype('float32')
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    img2_gray = img2_gray.astype('float32')
    #show_image(img1_gray, title_img_name + "Gray image 1")
    #show_image(img2_gray, title_img_name + "Gray image 2")

    # Concatenate both images in one to see both of them at the same time and work with them as a single frame.
    frame = cv2.hconcat((img1, img2))  # Building the frame with both images (in RGB, not in Gray).
    show_image(frame, title_img_name + "Frame in RGB")

    return frame, img1_gray, img2_gray


def filtrarKeypoints(keyPoints:list, DoG:list):

    pass


def assignOrientation(keyPoints:list, imgSuavizadas:list, num_scales:int, escala=2, num_bins=36):
    # ESTRUCTURAS
    # keyPoints: list[indiceImagenSuavizada, tupla(coordenadas)]
    # imgSuavizadas: list[matrizImagenSuavizada]

    #descriptorSize:si la window es de 8x8 y el descriptorSize es de 2, 2x2, esto hara que que hayan 4 descriptores
    octava=1
    orientaciones = []
    #calculo de magnitudes y orientaciones
    for infoKeypoint in keyPoints:

        # creamos un numpy array con 36 elementos, 1 por cada bin, cada bin por cada 10 grados
        orientation_histogram = np.zeros(num_bins)

        #caclulo de area alrededor del keypoint a observar, 1.5 veces sigma de la scale
        window=int(1.5*escala*octava)*3

        #controlamos que no se salga de la imagen la region
        filaIni = 0 if infoKeypoint[1][0]-window < 0 else infoKeypoint[1][0]-window
        filaFi =  imgSuavizadas[infoKeypoint[0]].shape[0] if infoKeypoint[1][0]+window > imgSuavizadas[infoKeypoint[0]].shape[0] else infoKeypoint[1][0]+window

        colIni = 0 if infoKeypoint[1][1]-window < 0 else infoKeypoint[1][1]-window
        colFi=  imgSuavizadas[infoKeypoint[0]].shape[0] if infoKeypoint[1][1]+window > imgSuavizadas[infoKeypoint[0]].shape[1] else infoKeypoint[1][1]+window

        neighborhood = imgSuavizadas[infoKeypoint[0]][filaIni:filaFi, colIni:colFi]

        # Calcular los gradientes en x e y utilizando el filtro de Sobel
        gradient_x = cv2.Sobel(neighborhood, cv2.CV_64F, 1, 0, ksize=3)
        gradient_y = cv2.Sobel(neighborhood, cv2.CV_64F, 0, 1, ksize=3)

        # Calcular la magnitud y dirección de los gradientes
        gradient_magnitude = np.sqrt(gradient_x ** 2 + gradient_y ** 2)
        gradient_orientation = np.arctan2(gradient_y, gradient_x) * (180 / np.pi)

        indices = (np.absolute(gradient_orientation) / (360 / num_bins)).astype(int)
        pesos = (1.5*escala*octava + gradient_magnitude) / 2
        #valores = pesos * ((gradient_orientation + 360) % 360) #sumamos 360 para cambiar los angulos negativos y el modulo de 360 para que ningun angulo pase de 360 grados

        orientation_histogram[indices] += pesos

        #seleccionamos el pico maximo
        maxPeakIndex=np.argmax(orientation_histogram)
        #lista donde tenemos los indices del angulo maximo y los que superan un 0,8 del maximo, multiplicados x el rango de angulos que representa cada uno
        #peaks=[maxPeakIndex*int(360/num_bins)] + list(np.where((orientation_histogram >= 0.8 * orientation_histogram[maxPeakIndex]) &
                                    #(orientation_histogram != orientation_histogram[maxPeakIndex]))[0]*int(360/num_bins))

        #orientaciones.append(peaks)
        orientaciones.append(maxPeakIndex*int(360/num_bins))
        #plt.hist(orientation_histogram, bins=num_bins)
        #plt.show()

        #cada num_scales se suma 1 octava
        octava+=infoKeypoint[0]%num_scales


    return orientaciones

def descriptors(keyPoints, imgSuavizadas, orientationAngles:list):
    # ESTRUCTURAS
    # keyPoints: list[indiceImagenSuavizada, tupla(coordenadas)]
    # imgSuavizadas: list[matrizImagenSuavizada]

    descriptores=[]

    #calculo de orientaciones
    for infoKeypoint in keyPoints:
        # Calcular los gradientes en x e y utilizando el filtro de Sobel
        gradient_x = cv2.Sobel(imgSuavizadas[infoKeypoint[0]], cv2.CV_64F, 1, 0, ksize=3)
        gradient_y = cv2.Sobel(imgSuavizadas[infoKeypoint[0]], cv2.CV_64F, 0, 1, ksize=3)
        gradient_orientation = np.arctan2(gradient_y, gradient_x) * (180 / np.pi)
        orientation_histogram = np.zeros(8)

        #en una vecindad de 16x16 calcularemos descriptores de 4x4 y sus histogramas de orientacion
        for i in range(0, 16, 4):
            for j in range(0, 16, 4):
                # creamos un numpy array con 8 elementos para el orientation histogram de cada bloque
                orientation_histogram = np.zeros(8)
                areaDescriptor=gradient_orientation[infoKeypoint[1][0]-i:infoKeypoint[1][0]+i, infoKeypoint[1][1]-j:infoKeypoint[1][1]+j]

    return descriptores

def generateDescriptors(keypoints, angulos, gaussian_images, window_width=4, num_bins=8, scale_multiplier=3, descriptor_max_value=0.2, maxEscalas=3):
    """Generate descriptors for each keypoint
    """
    # keyPoints: list[indiceImagenSuavizada, tupla(coordenadas)]
    # gaussian_images: list[matrizImagenSuavizada]
    descriptors = []
    octava=1
    float_tolerance=0.000001

    for keypoint, angulo in zip(keypoints, angulos):
        octava += keypoints[0] % maxEscalas

        #octave, layer, scale = unpackOctave(keypoint)
        #gaussian_image = gaussian_images[octave + 1, layer]
        num_rows, num_cols = gaussian_images[keypoints[0]].shape

        scale = 2 * octava

        point = round(scale * np.array(keypoint[1])).astype('int')
        bins_per_degree = num_bins / 360.
        angle = 360. - angulo
        cos_angle = math.cos(math.deg2rad(angle))
        sin_angle = math.sin(math.deg2rad(angle))
        weight_multiplier = -0.5 / ((0.5 * window_width) ** 2)
        row_bin_list = []
        col_bin_list = []
        magnitude_list = []
        orientation_bin_list = []
        histogram_tensor = np.zeros((window_width + 2, window_width + 2, num_bins))   # first two dimensions are increased by 2 to account for border effects

        # Descriptor window size (described by half_width) follows OpenCV convention
        hist_width = scale_multiplier * 0.5 * scale * keypoint.size
        half_width = int(round(hist_width * math.sqrt(2) * (window_width + 1) * 0.5))   # sqrt(2) corresponds to diagonal length of a pixel
        half_width = int(min(half_width, math.sqrt(num_rows ** 2 + num_cols ** 2)))     # ensure half_width lies within image

        for row in range(-half_width, half_width + 1):
            for col in range(-half_width, half_width + 1):
                row_rot = col * sin_angle + row * cos_angle
                col_rot = col * cos_angle - row * sin_angle
                row_bin = (row_rot / hist_width) + 0.5 * window_width - 0.5
                col_bin = (col_rot / hist_width) + 0.5 * window_width - 0.5
                if row_bin > -1 and row_bin < window_width and col_bin > -1 and col_bin < window_width:
                    window_row = int(round(point[1] + row))
                    window_col = int(round(point[0] + col))
                    if window_row > 0 and window_row < num_rows - 1 and window_col > 0 and window_col < num_cols - 1:
                        dx = gaussian_images[keypoints[0]][window_row, window_col + 1] - gaussian_images[keypoints[0]][window_row, window_col - 1]
                        dy = gaussian_images[keypoints[0]][window_row - 1, window_col] - gaussian_images[keypoints[0]][window_row + 1, window_col]
                        gradient_magnitude = math.sqrt(dx * dx + dy * dy)
                        gradient_orientation = math.rad2deg(math.arctan2(dy, dx)) % 360
                        weight = math.exp(weight_multiplier * ((row_rot / hist_width) ** 2 + (col_rot / hist_width) ** 2))
                        row_bin_list.append(row_bin)
                        col_bin_list.append(col_bin)
                        magnitude_list.append(weight * gradient_magnitude)
                        orientation_bin_list.append((gradient_orientation - angle) * bins_per_degree)

        for row_bin, col_bin, magnitude, orientation_bin in zip(row_bin_list, col_bin_list, magnitude_list, orientation_bin_list):
            # Smoothing via trilinear interpolation
            # Notations follows https://en.wikipedia.org/wiki/Trilinear_interpolation
            # Note that we are really doing the inverse of trilinear interpolation here (we take the center value of the cube and distribute it among its eight neighbors)
            row_bin_floor, col_bin_floor, orientation_bin_floor = np.floor([row_bin, col_bin, orientation_bin]).astype(int)
            row_fraction, col_fraction, orientation_fraction = row_bin - row_bin_floor, col_bin - col_bin_floor, orientation_bin - orientation_bin_floor
            if orientation_bin_floor < 0:
                orientation_bin_floor += num_bins
            if orientation_bin_floor >= num_bins:
                orientation_bin_floor -= num_bins

            c1 = magnitude * row_fraction
            c0 = magnitude * (1 - row_fraction)
            c11 = c1 * col_fraction
            c10 = c1 * (1 - col_fraction)
            c01 = c0 * col_fraction
            c00 = c0 * (1 - col_fraction)
            c111 = c11 * orientation_fraction
            c110 = c11 * (1 - orientation_fraction)
            c101 = c10 * orientation_fraction
            c100 = c10 * (1 - orientation_fraction)
            c011 = c01 * orientation_fraction
            c010 = c01 * (1 - orientation_fraction)
            c001 = c00 * orientation_fraction
            c000 = c00 * (1 - orientation_fraction)

            histogram_tensor[row_bin_floor + 1, col_bin_floor + 1, orientation_bin_floor] += c000
            histogram_tensor[row_bin_floor + 1, col_bin_floor + 1, (orientation_bin_floor + 1) % num_bins] += c001
            histogram_tensor[row_bin_floor + 1, col_bin_floor + 2, orientation_bin_floor] += c010
            histogram_tensor[row_bin_floor + 1, col_bin_floor + 2, (orientation_bin_floor + 1) % num_bins] += c011
            histogram_tensor[row_bin_floor + 2, col_bin_floor + 1, orientation_bin_floor] += c100
            histogram_tensor[row_bin_floor + 2, col_bin_floor + 1, (orientation_bin_floor + 1) % num_bins] += c101
            histogram_tensor[row_bin_floor + 2, col_bin_floor + 2, orientation_bin_floor] += c110
            histogram_tensor[row_bin_floor + 2, col_bin_floor + 2, (orientation_bin_floor + 1) % num_bins] += c111

        descriptor_vector = histogram_tensor[1:-1, 1:-1, :].flatten()  # Remove histogram borders
        # Threshold and normalize descriptor_vector
        threshold = np.linalg.norm(descriptor_vector) * descriptor_max_value
        descriptor_vector[descriptor_vector > threshold] = threshold
        descriptor_vector /= max(np.linalg.norm(descriptor_vector), float_tolerance)
        # Multiply by 512, round, and saturate between 0 and 255 to convert from float32 to unsigned char (OpenCV convention)
        descriptor_vector = round(512 * descriptor_vector)
        descriptor_vector[descriptor_vector < 0] = 0
        descriptor_vector[descriptor_vector > 255] = 255
        descriptors.append(descriptor_vector)
    return np.array(descriptors, dtype='float32')
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
            for j in range(1, img.shape[1] - 1):

                maxUtil=0
                minUtil=math.inf

                if DoG[1][i, j] != 0:#valor 0 no esta admintido como keypoint

                    subMatrizAnterior = DoG[0][i - 1:i + 2, j - 1:j + 2]
                    subMatrizActual = DoG[1][i - 1:i + 2, j - 1:j + 2]
                    subMatrizPosterior = DoG[2][i - 1:i + 2, j - 1:j + 2]


                    #esta comparacion tiene utilidad para ahorrar una comparacion con las DoG 1,2,3 ya tendremos la comparacion de 1 con 2
                    maxUtil= max(np.max(subMatrizActual), np.max(subMatrizPosterior))

                    #si no cumple ser el maximo entre las 2 capas no hace falta continuar porque no sera el max
                    if maxUtil == DoG[1][i, j] and DoG[1][i,j] == max(np.max(subMatrizActual), np.max(subMatrizAnterior)):

                            # concatenar las submatrizes
                            subMatriz = np.concatenate((subMatrizActual, subMatrizAnterior, subMatrizPosterior), axis=0)

                            # si el pixel es un maximo unico, no aparace el valor de nuevo en la submatriz, se considera key point
                            if np.count_nonzero(subMatriz == DoG[1][i, j]) == 1:
                                keyPoints.append(((0, 1), (i,j)))  # añadimos en que scala se encuentra para luego las orientaciones, sabemos que si es la DoG 1, estara entre las escalas 0 y 2

                    elif np.count_nonzero(subMatrizPosterior) == len(subMatrizPosterior):#si haya lgun 0 en la siguiente DoG scale se pondra como valor min, asi que no la queremos ni ver
                        minUtil = min(np.min(subMatrizActual), np.min(subMatrizPosterior))

                        if minUtil == DoG[1][i, j]:
                            if DoG[1][i,j] == min(np.max(subMatrizActual), np.min(subMatrizAnterior)):
                                # concatenar las submatrizes
                                subMatriz = np.concatenate((subMatrizActual, subMatrizAnterior, subMatrizPosterior), axis=0)

                                # si el pixel es un maximo unico, no aparace el valor de nuevo en la submatriz, se considera key point
                                if np.count_nonzero(subMatriz == DoG[1][i, j]) == 1:
                                    keyPoints.append(((0, 1), (i, j)))  # añadimos en que scala se encuentra para luego las orientaciones, sabemos que si es la DoG 1, estara entre las escalas 0 y 2

                #se compara con la siguiente scale de las DoG
                for scaleDoG in range(2, len(DoG)-1):
                     if DoG[1][i, j] != 0:#valor 0 no esta admintido como keypoint
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
                        elif np.count_nonzero(subMatrizPosterior) == len(subMatrizPosterior):

                            minUtil = min(minUtil, np.min(subMatrizPosterior))

                            if minUtil == DoG[scaleDoG][i, j] :

                                subMatrizActual = DoG[scaleDoG][i - 1:i + 2, j - 1:j + 2]
                                subMatrizAnterior = DoG[scaleDoG][i - 1:i + 2, j - 1:j + 2]

                                # concatenar las submatrizes
                                subMatriz = np.concatenate((subMatrizActual, subMatrizAnterior, subMatrizPosterior), axis=0)

                                # si el pixel es un maximo unico, no aparace el valor de nuevo en la submatriz, se considera key point
                                if np.count_nonzero(subMatriz == DoG[scaleDoG][i, j]) == 1:
                                    keyPoints.append(((0, 1), (i, j)))  # añadimos en que scala se encuentra para luego las orientaciones, sabemos que si es la DoG 1, estara entre las escalas 0 y 2

        # se reduce la resolucion a la mitad de la octava anterior, para esto se necesita mantener la informacion original, imgFaces
        # se subtituye los valores de los pixeles de n columnas, cada octava tiene la mitad de innfromacion de la aterior,
        # esto significa el doble de columnas son subtituidas en cada octava
        imgCopy[:, 1::pow(2, ocatavActual + 1)] = img[:, 0::pow(2, ocatavActual + 1)]

    return keyPoints, scales



def determinateKeypoints(img:np.array, k:float, mode:str, max_scale:int, num_ocatavas:int, kernelSize:int):

    imgCopy=np.copy(img)

    # Obtenemos la Gaussiana con sigma inicial de 0.7071876 por el video
    sigmaInicial=0.7071876
    nuevaSigma=0.7071876

    DoG = []
    scales = []
    keyPoints = []
    #creamos diferentes octavas con diferentes scales para obtener las diferencias de Gaussianas
    for ocatavActual in range(num_ocatavas):

        exponenteK=ocatavActual+1

        # generamos Gausian KERNEL de 1 dimension
        G = cv2.getGaussianKernel(kernelSize, sigmaInicial * pow(k, exponenteK))
        G = np.outer(G, G)  # genera Gaussian Kernel de 2 dimensiones

        # convolucionamos, -1 indica queremos un resultado del mismo tamaño de la imagen
        L = cv2.filter2D(imgCopy, -1, G)

        # guardamos la imagent suavizada, L, con sus sigma para luego calcular orientacion
        scales.append(L)

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
            scales.append(L)

            #calculo diferencia de Gaussianas
            D = L-Lant

            #guardamos las octavas para luego sacar los keypoints y los indices de las escalas de donde las obtenemos
            DoG.append(D)

            #nueva sigma, se pone +1 porque se necesita el numeron de scales, en scale 0 llevamos 1 scale
            nuevaSigma *= pow(k, exponenteK+1)


        #se reduce la resolucion a la mitad de la octava anterior, para esto se necesita mantener la informacion original, imgFaces
        #se subtituye los valores de los pixeles de n columnas, cada octava tiene la mitad de innfromacion de la aterior,
        #esto significa el doble de columnas son subtituidas en cada octava
        imgCopy[:, 1::pow(2, ocatavActual+1)]=img[:, 0::pow(2, ocatavActual+1)]

    contrast_threshold=0.04
    threshold = math.floor(0.5 * contrast_threshold / max_scale * 255)
    #valors= []
    #ahora iremos mirando los puntos caracteristicos de cada capa segun su capa anterior y posterir, por ello no miramos la primera ni la ultima
    for capaDoG in range(1, len(DoG)-1):
        #iteramos pixel a pixel miranod 3(x)x3(y)x3(capa, z)-1(pixel que escogemos para mirar a su alrededor) pixeles
        for i in range(1, DoG[capaDoG].shape[0]-1):
            for j in range(1, DoG[capaDoG].shape[1]-1):

                if DoG[capaDoG][i, j] != 0 and abs(DoG[capaDoG][i, j]) > threshold:#0 no puede ser un keypoint porque significa que no hay diferencia entre escalas
                    subMatrizActual=DoG[capaDoG][i-1:i+2, j-1:j+2]
                    subMatrizAnterior = DoG[capaDoG - 1][i - 1:i + 2, j - 1:j + 2]
                    subMatrizPosterior = DoG[capaDoG + 1][i - 1:i + 2, j - 1:j + 2]

                    #si el pixel es el maximo o el minimo de su alrededor en la capa o SCALA ACTUAL
                    if max(np.max(subMatrizActual), np.max(subMatrizAnterior),np.max(subMatrizPosterior)) == DoG[capaDoG][i,j]:
                        #concatenar las submatrizes
                        subMatriz = np.concatenate((subMatrizActual, subMatrizAnterior, subMatrizPosterior), axis=0)

                        #si el pixel es un maximo unico, no aparace el valor de nuevo en la submatriz, se considera key point
                        if np.count_nonzero(subMatriz == DoG[capaDoG][i,j]) == 1:
                            keyPoints.append((capaDoG-1, (i, j))) # añadimos en que scala se encuentra para luego las orientaciones, sabemos que si es la DoG 5, estara entre las escalas 5 y 6
                            #valors.append(DoG[capaDoG][i, j] )
                    elif min(np.min(subMatrizActual), np.min(subMatrizAnterior), np.min(subMatrizPosterior)) == DoG[capaDoG][i, j]:
                        # concatenar las submatrizes
                        subMatriz = np.concatenate((subMatrizActual, subMatrizAnterior, subMatrizPosterior), axis=0)

                        # si el pixel es un maximo unico, no aparace el valor de nuevo en la submatriz, se considera key point
                        if np.count_nonzero(subMatriz == DoG[capaDoG][i, j]) == 1:
                            keyPoints.append((capaDoG-1, (i, j))) # añadimos en que scala se encuntra para luego las orientaciones, sabemos que si es la DoG 5, estara entre las escalas 5 y 6, consideramos que l 5
                            #valors.append(DoG[capaDoG][i, j])
    return keyPoints, scales


def sift(img: np.array, k=1.6, mode='same', max_scale=3, num_ocatavas=4, kernelSize=3):
    # Step 1: Approximate Keypoint Location

    t0 = time.time()
    keyPoints, scales = determinateKeypoints(img, k, mode, max_scale, num_ocatavas, kernelSize)
    print(time.time() - t0)

    #t0=time.time()
    #keyPoints2, scales2 = determinateKeypoints2(imgFaces, k, mode, max_scale, num_ocatavas, kernelSize)
    #print(time.time()-t0)

    #reducir los outliers en los keypoints
    #keypoints = filtrarKeypoints(keyPoints, DoG)

    #asignar orientacion a los keypoints
    orientaciones = assignOrientation(keyPoints, scales, max_scale)
    descriptores = generateDescriptors(keyPoints,orientaciones, scales, max_scale=max_scale)
    return 0


if __name__ == '__main__':

    folder = 'Computer Vision/imgFaces/base/'

    # cargamos los nombres de las imagenes
    image_names = load_images_from_folder(folder)
    #print(image_names)

    # ordenamos los nombres de las imagenes
    image_names = sorted(image_names)
    #print(image_names)
    # ================================
    #       LOAD AND SHOW IMAGES
    # ================================
    for im1_name, im2_name in zip(image_names[0::2], image_names[1::2]):
        #devuelve un frame con las 2 imagenes unidas y carga las 2 imagenes en gris
        frame, imgGray1, imgGray2 = load_and_show_images((folder + im1_name), (folder + im2_name))
        sift(imgGray1)
        sift(imgGray2)