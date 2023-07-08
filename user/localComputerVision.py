import time

import cv2
import numpy as np
import json
import plotly.graph_objects as go

# ===========================================================
#            FUNCIONS ÚTILS PER ELS MÒDULS PRINCIPALS
#              USEFUL FUNCTIONS FOR THE MAIN MODULES
# ===========================================================
# Calcula el valor K donat una imatge si no coneixem cap valor de la càmera.

# Calculate the K value given an image if we don't know any values of the camera.
def camera_internals_if_we_DONT_know_K(img1):
    width, height, _ = img1.shape
    focal_length = np.maximum(width, height)
    center = (height / 2, width / 2)

    K = np.array(
        [[focal_length, 0, center[0]],
         [0, focal_length, center[1]],
         [0, 0, 1]], dtype="double")
    return K


# Funció necessaria per tal de calcular els punts 3d donats uns punts 2D, conf de la càmera i una funció de
# triangulació.

# Function needed to calculate 3d points given 2d points, camera conf and a triangulation function.
def getTriangulatedPoints(img1pts, img2pts, K, R, t, triangulateFunc):
    img1ptsHom = cv2.convertPointsToHomogeneous(img1pts)[:, 0, :]
    img2ptsHom = cv2.convertPointsToHomogeneous(img2pts)[:, 0, :]

    img1ptsNorm = (np.linalg.inv(K).dot(img1ptsHom.T)).T
    img2ptsNorm = (np.linalg.inv(K).dot(img2ptsHom.T)).T

    img1ptsNorm = cv2.convertPointsFromHomogeneous(img1ptsNorm)[:, 0, :]
    img2ptsNorm = cv2.convertPointsFromHomogeneous(img2ptsNorm)[:, 0, :]

    pts4d = triangulateFunc(np.eye(3, 4), np.hstack((R, t)), img1ptsNorm.T, img2ptsNorm.T)
    pts3d = cv2.convertPointsFromHomogeneous(pts4d.T)[:, 0, :]

    return pts3d


# ================================================================
#                  MÒDULS DE SOFTWARE PRINCIPALS:
#                   PRINCIPAL SOFTWARE MODULES:
# ================================================================

# Aplicar l'algorisme SIFT donades dues imatges per tal de poder trobar els punts característics i descriptors els
# quals retornarem (útils per a fer el matching).

# Apply the SIFT algorithm given two images in order to find the key points and descriptors
# which we will return (useful for matching).
def sift(img1, img2):
    algorithm = cv2.SIFT_create()

    # Find Keypoints and descriptors with SIFT
    keypt1, descr1 = algorithm.detectAndCompute(img1, None)
    keypt2, descr2 = algorithm.detectAndCompute(img2, None)

    return keypt1, descr1, keypt2, descr2


# Donats els resultats del SIFT, és a dir els keypoints i els descriptors de cada imatge, es realitza el matching
# mitjançant FLANN (utilitzat per fer cerques ràpides entre veïns (coincidència de descriptors -> match)). Com que hi
# ha molts matches amb valors incorrectes, es fa el Lowe's ratio test per filtrar els matches i quedar-nos amb
# els matches confiables o "good matches", els quals retornem.

# Given the SIFT results, i.e. the keypoints and descriptors of each image, the matching is performed via FLANN (used
# to do fast neighbor searches (descriptor match -> match)). As there there are many matches with incorrect values,
# the Lowe's ratio test is performed to filter the matches and leave us with the reliable matches or "good matches",
# which we return.
def matching(keypt1, descr1, keypt2, descr2):
    # FLANN parameters:
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(descr1, descr2, k=2)
    pts1 = []
    pts2 = []

    # Ratio test as per Lowe's paper:
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.8 * n.distance:
            pts2.append(keypt2[m.trainIdx].pt)
            pts1.append(keypt1[m.queryIdx].pt)
    pts1 = np.int32(pts1)
    pts2 = np.int32(pts2)

    return pts1, pts2


# Funció mitjançant la qual es fa una primera reconstrucció, obtenint un mapa de punts 3D (""" finalment visualitzant
# una primera reconstrucció en el navegador mitjançant el mapa de punts calculat"""). Retorna un array amb els punts 3D.

# Function through which a first reconstruction is made, obtaining a 3D point map, ("""finally viewing
# a first reconstruction in the browser using the calculated point map. """). Returns an array with the 3D points.
def firstReconstruction(img1, pts1, pts2):
    # RANSAC
    F, mask = cv2.findFundamentalMat(pts1, pts2, cv2.RANSAC)

    # CAMERA PARAMETERS
    K = camera_internals_if_we_DONT_know_K(img1)
    # Estimate the Essential Matrix:
    E = K.T.dot(F.dot(K))

    # Check for cheirality condition
    _, R, t, mask = cv2.recoverPose(E, pts1, pts2, K)

    pts3d = getTriangulatedPoints(pts1, pts2, K, R, t, cv2.triangulatePoints)

    # REMINDER: If you want to visualize the points, you must uncomment the third import (plotly.graph_objects as go)
    # Visualitzar els punts 3D
    fig = go.Figure(data=[go.Scatter3d(x=pts3d[:, 0], y=pts3d[:, 1], z=pts3d[:, 2], mode='markers', marker=dict(
        size=2,
        color='red',
        opacity=0.8
    ))])
    fig.update_layout(autosize=False, width=900, height=900)
    fig.show()

    return pts3d

def img_to_3d_points():
    img1 = cv2.imread('../cloudServer/imgFaces/VC Part/imgTest1.png')
    img2 = cv2.imread('../cloudServer/imgFaces/VC Part/imgTest2.png')

    keypoints1, descriptors1, keypoints2, descriptors2 = sift(img1, img2)
    pts1, pts2 = matching(keypoints1, descriptors1, keypoints2, descriptors2)
    pts3D = firstReconstruction(img1, pts1, pts2)
    return pts3D

if __name__ == '__main__':
    for i in range(0,10):
        pts3D = img_to_3d_points()
        print("Len pts3D: ", len(pts3D))
        print(pts3D)
        """
        coords = pts3D.tolist()
        coordenadas = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]
        coords_json = json.dumps(coords)
        # print(coords_json)
        # return pts3D
        """
        time.sleep(5)
