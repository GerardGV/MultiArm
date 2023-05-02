# ==========================================================================
# MultiRobot project. A robot developed in SM, VC and RLP.
# Owners: Pol Colomer Campoy (SM, VC and RLP), Jan Rubio Rico (SM, VC and RLP),
# Gerard Josep Guarin Velez (SM, VC and RLP), Rubén Simó (RLP)
# ==========================================================================
import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import os
from PIL import Image

# =======================================================================

import cv2
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def reconstruct_3d(images, calibration_matrices):
    # Convertir las imágenes a escala de grises
    gray_images = [cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) for image in images]

    # Crear un objeto SIFT
    sift = cv2.xfeatures2d.SIFT_create()

    # Detectar los puntos característicos y calcular los descriptores para todas las imágenes
    keypoints = []
    descriptors = []
    for image in gray_images:
        kp, des = sift.detectAndCompute(image, None)
        keypoints.append(kp)
        descriptors.append(des)

    # Emparejar los descriptores utilizando el algoritmo de fuerza bruta
    bf = cv2.BFMatcher()
    matches = []
    for i in range(len(images)-1):
        for j in range(i+1, len(images)):
            # Emparejar los descriptores de los puntos característicos en las dos imágenes
            matches_ij = bf.match(descriptors[i], descriptors[j])
            # Seleccionar los mejores emparejamientos
            matches_ij = sorted(matches_ij, key=lambda x: x.distance)[:100]
            # Añadir las correspondencias a la lista global de correspondencias
            matches.append((i, j, matches_ij))

    # Calcular las matrices fundamentales para cada par de imágenes
    F_matrices = []
    for match in matches:
        i, j, matches_ij = match
        pts_i = np.float32([keypoints[i][m.queryIdx].pt for m in matches_ij])
        pts_j = np.float32([keypoints[j][m.trainIdx].pt for m in matches_ij])
        F, _ = cv2.findFundamentalMat(pts_i, pts_j, cv2.FM_RANSAC, 0.1, 0.99)
        F_matrices.append(F)

    # Calcular la matriz de homografía para cada imagen
    H_matrices = []
    for i in range(len(images)):
        H, _ = cv2.findHomography(np.float32(keypoints[i]), np.float32(keypoints[0]), cv2.RANSAC, 5.0)
        H_matrices.append(H)

    # Obtener las coordenadas 3D de los puntos
    points3d = []
    for i in range(len(keypoints[0])):
        x, y = keypoints[0][i].pt
        points2d = []
        for j in range(len(images)):
            if i < len(keypoints[j]):
                x_j, y_j = keypoints[j][i].pt
                points2d.append((x_j, y_j))
        points2d = np.float32(points2d).reshape(-1, 1, 2)
        points3d_homogeneous = cv2.triangulatePoints(calibration_matrices[0], calibration_matrices[1], points2d[0], points2d[1])
        points3d_cartesian = cv2.convertPointsFromHomogeneous(points3d_homogeneous.T)
        points



# =======================================================================

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

    frameORB = calculate_keypoints(img1, img2, title_img_name)
    matchesORB = calculate_keypoints_ORB_matching(img1,img2,title_img_name)

    return frame, frameORB, matchesORB

def calculate_keypoints(img1, img2, title=""):
    orb1 = cv2.ORB_create(500)
    orb2 = cv2.ORB_create(500)

    key_pt1, descr1 = orb1.detectAndCompute(img1, None)
    key_pt2, descr2 = orb2.detectAndCompute(img2, None)
    img_orb1 = cv2.drawKeypoints(img1, key_pt1, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    img_orb2 = cv2.drawKeypoints(img2, key_pt2, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    final_frame_ORB = cv2.hconcat((img_orb1,img_orb2))
    show_image(final_frame_ORB, title + "Final Frame with ORB")

    return final_frame_ORB

def calculate_keypoints_ORB_matching(img1, img2, title =""):
    orb = cv2.ORB_create(nfeatures= 800)

    key_pt1, descr1 = orb.detectAndCompute(img1, None)
    key_pt2, descr2 = orb.detectAndCompute(img2, None)

    # BF MATCHER (Brute Force Matcher)
    bf = cv2.BFMatcher_create(cv2.NORM_HAMMING, crossCheck=True)

    matches = bf.match(descr1,descr2)

    orb_matches = cv2.drawMatches(img1, key_pt1, img2, key_pt2, matches[:500], None, flags=2)

    show_image(orb_matches, title+"Final Frame Matches using BF Matching (ORB)")

if __name__ == '__main__':
    print('Starting...')
    folder = 'img/base/'
    image_names = load_images_from_folder(folder)
    print(image_names)
    # ================================
    #       LOAD AND SHOW IMAGES
    # ================================
    for im1_name, im2_name in zip(image_names[0::2], image_names[1::2]):
        frame, frameORB, matchesORB = load_and_show_images(folder+im1_name, folder+im2_name)



    print("End of the program.")
