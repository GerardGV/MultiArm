%matplotlib notebook

import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import ipywidgets as widgets


def find_keypoints_and_matches(img1, img2):
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    return src_pts, dst_pts

def create_3d_model(img1, img2):
    src_pts, dst_pts = find_keypoints_and_matches(img1, img2)
    F, mask = cv2.findFundamentalMat(src_pts, dst_pts, cv2.FM_RANSAC)

    # Seleccione solo los puntos enmascarados
    src_pts = src_pts[mask.ravel() == 1]
    dst_pts = dst_pts[mask.ravel() == 1]

    # Parámetros de cámara ficticios, reemplace con los valores correctos de la calibración de la cámara
    K = np.array([[1, 0, 0],
                  [0, 1, 0],
                  [0, 0, 1]])

    # Rectifique las imágenes
    retval, H1, H2 = cv2.stereoRectifyUncalibrated(src_pts, dst_pts, F, img1.shape[::-1])
    map1x, map1y = cv2.initUndistortRectifyMap(K, np.zeros(5), H1, K, img1.shape[::-1], cv2.CV_32FC1)
    map2x, map2y = cv2.initUndistortRectifyMap(K, np.zeros(5), H2, K, img2.shape[::-1], cv2.CV_32FC1)
    img1_rectified = cv2.remap(img1, map1x, map1y, cv2.INTER_LINEAR)
    img2_rectified = cv2.remap(img2, map2x, map2y, cv2.INTER_LINEAR)

    # Genere el mapa de disparidad
    window_size = 5
    stereo = cv2.StereoSGBM_create(minDisparity=0,
                                   numDisparities=16,
                                   blockSize=window_size,
                                   uniquenessRatio=10,
                                   speckleWindowSize=100,
                                   speckleRange=32,
                                   disp12MaxDiff=1,
                                   P1=8 * 3 * window_size ** 2,
                                   P2=32 * 3 * window_size ** 2)
    disparity = stereo.compute(img1_rectified, img2_rectified).astype(np.float32) / 16.0

    # Generar el modelo 3D
    h, w = img1.shape[:2]
    f = 1  # Distancia focal ficticia, reemplazar con valor real
    Q = np.float32([[1, 0, 0, -0.5 * w],
                    [0, -1, 0, 0.5 * h],
                    [0, 0, 0, -f],
                    [0, 0, 1, 0]])
    points_3d = cv2.reprojectImageTo3D(disparity, Q)

    return points_3d

def visualize_3d_model(points_3d, threshold=5.0):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    mask = (np.abs(points_3d[..., 2]) < threshold)
    x = points_3d[..., 0][mask]
    y = points_3d[..., 1][mask]
    z = points_3d[..., 2][mask]

    ax.scatter(x, y, z, s=1, c=z, cmap='jet', marker='o', alpha=0.5)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()


img1 = cv2.imread('img/base/img10_1_rotated_only_face.jpeg', 0)
img2 = cv2.imread('img/base/img10_2_rotated_only_face.jpeg', 0)

points_3d = create_3d_model(img1, img2)
visualize_3d_model(points_3d)
print(points_3d)

