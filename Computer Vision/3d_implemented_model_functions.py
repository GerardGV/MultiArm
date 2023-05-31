import time
import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import open3d as o3d
import plotly.graph_objects as go


# Funció bàsica per tal de mostrar totes les imatges que s'utilitzin en aquesta implementació.
# Ens permet posar títols a les imatges que es mostrin i triar si volem la imatge en color o en grisos (Per defecte).
def show_image(img, title="Imatge", color=False):
    plt.figure()
    if color:
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    else:
        plt.imshow(img)
    plt.title(title)
    plt.show()


# Carregar tots els noms de les imatges d'un directori donat. Retorna una llista amb els noms de les imatges.
def load_images_from_folder(folder):
    image_names = []  # List where we are going to save the names of the images in the folder
    for path in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, path)):
            image_names.append(path)
    return image_names


# Donats dos noms d'imatges, les llegeix, retorna i retorna un frame amb les dues imatges concatenades i les visualitza
# per tal de veure amb quines imatges treballarem en aquesta iteració.
def load_and_plot_images(image_name1="/img/base/img1_1_glasses_openEyes_Pol.jpeg",
                         image_name2="/img/base/img1_2_glasses_openEyes_Pol.jpeg"):
    img1 = cv2.imread(image_name1)
    img2 = cv2.imread(image_name2)

    # Opcional
    # img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    # img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # cv2.imshow(img1_gray)
    # cv2.imshow(img2_gray)

    final_frame = cv2.hconcat((img1, img2))
    show_image(final_frame, "Concatenated images")
    return img1, img2, final_frame


def extract_keypoints_feature_descriptors_and_matching(image1, image2):
    sift1 = cv2.SIFT_create()
    sift2 = cv2.SIFT_create()

    keypoint1, descriptor1 = sift1.detectAndCompute(image1, None)
    keypoint2, descriptor2 = sift2.detectAndCompute(image2, None)

    img_SIFT_1 = cv2.drawKeypoints(image1, keypoint1, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    img_SIFT_2 = cv2.drawKeypoints(image2, keypoint2, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    final_frame = cv2.hconcat((img_SIFT_1, img_SIFT_2))
    show_image(final_frame, "Concatenated SIFT images: ")
    return final_frame


def extract_keypoints_with_one_SIFT(im1, im2):
    sift = cv2.SIFT_create()

    keypoint1, descriptor1 = sift.detectAndCompute(im1, None)
    keypoint2, descriptor2 = sift.detectAndCompute(im2, None)

    img_SIFT_1 = cv2.drawKeypoints(im1, keypoint1, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    img_SIFT_2 = cv2.drawKeypoints(im2, keypoint2, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    final_frame_BF_SIFT = cv2.hconcat((img_SIFT_1, img_SIFT_2))
    show_image(final_frame_BF_SIFT, "ONE SIFT images: ")
    return final_frame_BF_SIFT


def brute_force_SIFT(im1, im2):
    sift = cv2.SIFT_create()

    # Find keypoints
    keypoint1, descriptor1 = sift.detectAndCompute(im1, None)
    keypoint2, descriptor2 = sift.detectAndCompute(im2, None)

    # Create BF matcher object
    #   NOTE:
    #       * cv2.NORM_L2: It is good for SIFT, SURF, etc.
    #       * cv2.NORM_HAMMING: It is good for binary string-based descriptors like ORB, BRIEF, BRISK
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

    matches = bf.match(descriptor1, descriptor2)

    matches = sorted(matches, key=lambda x: x.distance)

    SIFT_matches = cv2.drawMatches(im1, keypoint1, im2, keypoint2, matches[:200], None, flags=2)
    show_image(SIFT_matches, "SIFT matches: ")
    return SIFT_matches, keypoint1, keypoint2


# ============================================
# FUNDEMENTAL MATRIX:
# ============================================

# Es tracta de la funció principal per tal d'extreure els Keypoints i descriptors de les imatges mitjançant SIFT, a
# continuació, mitjançant FLANN, es realitza un primer matching per després aplicar Lowe's per quedar-se amb els
# "good matches". Retorna els pts1 i pts2 (punts característics 2D de cada imatge)
def fundamental_matrix_find_kp_and_match(img1, img2, method="sift"):
    # Implementació més a força bruta i que no trobarà els millors resultats.
    # img1 = cv2.imread(im_name1, 0)
    # img2 = cv2.imread(im_name2, 0)
    method = method.lower()
    start_time_algorithm = time.time()
    if method == "sift":
        algorithm = cv2.SIFT_create()
    elif method == "harris":
        algorithm = cv2.cornerHarris()
    elif method == "orb":
        algorithm = cv2.ORB_create()
    else:
        print("Incorrect method, using SIFT as default")
        algorithm = cv2.SIFT_create()

    # Find Keypoints and descriptors with SIFT / the selected algorithm
    keypt1, descr1 = algorithm.detectAndCompute(img1, None)
    keypt2, descr2 = algorithm.detectAndCompute(img2, None)
    end_algorithm_time = time.time()

    print("Número de keypoints de la primera imatge: ", len(keypt1))
    print("Número de keypoints de la segona imatge: ", len(keypt2))

    # FLANN parameters:
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(descr1, descr2, k=2)
    pts1 = []
    pts2 = []
    print("Número de matches després del flann (knnMatch): ", len(matches))
    # Ratio test as per Lowe's paper:
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.8 * n.distance:
            pts2.append(keypt2[m.trainIdx].pt)
            pts1.append(keypt1[m.queryIdx].pt)
    pts1 = np.int32(pts1)
    pts2 = np.int32(pts2)
    print("Número de 'good' matches després del Lowe's ratio: ", len(pts1))
    end_algorithm_and_matching_time = time.time()

    print("Temps d'execució de l'algorisme ", method, ": ", end_algorithm_time - start_time_algorithm, " segons.")
    print("Temps d'execució de l'algorisme ", method, " i del matching (+ Lowe's): ",
          end_algorithm_and_matching_time - start_time_algorithm, " segons.")
    return pts1, pts2


# Funció que NOMÉS dibuixa en les imatges donades, les línies donades i retorna les imatges amb les línies per tal
# de visualitzar-les després. En el nostre cas l'utilitzem per visualitzar les línies epipolars.
def drawlines(img1, img2, lines, pts1, pts2):
    r, c, _ = img1.shape
    # img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
    # img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)

    for r, pt1, pt2 in zip(lines, pts1, pts2):
        color = tuple(np.random.randint(0, 255, 3).tolist())
        x0, y0 = map(int, [0, -r[2] / r[1]])
        x1, y1 = map(int, [c, -(r[2] + r[0] * c) / r[1]])
        img1 = cv2.line(img1, (x0, y0), (x1, y1), color, 1)
        img1 = cv2.circle(img1, tuple(pt1), 5, color, -1)
        img2 = cv2.circle(img2, tuple(pt2), 5, color, -1)
    return img1, img2


# =================================================
#         ESTIMATE THE FUNDAMENTAL MATRIX
# =================================================

# 2 of the most popular algorithms for OpenCV are:
#       1. Least Median Squares.
#       2. Random sample consensus (RANSAC)
# To do efficient estimations of the fundamental matrix. Both are robust
# We will have less execution time with RANSAC than with LMS


# Funció que, juntament amb la funció draw_lines(), dibuixa les línies epipolars de les dues imatges i les ajunta en un
# mateix frame el qual retorna.
def draw_epipolar_lines(img1, img2, pts1, pts2, F, mask):
    # Select only inlier points:
    pts1_filter = pts1[mask.ravel() == 1]
    pts2_filter = pts2[mask.ravel() == 1]

    # Find epilines corresponding to points in left image (img1) and drawing its lines on right imagge.
    lines2 = cv2.computeCorrespondEpilines(pts1_filter.reshape(-1, 1, 2), 1, F)
    lines2 = lines2.reshape(-1, 3)
    img3, img4 = drawlines(img2, img1, lines2, pts2_filter, pts1_filter)

    # Find epilines corresponding to points in right image (img2) and drawing its lines on left image.
    lines1 = cv2.computeCorrespondEpilines(pts2_filter.reshape(-1, 1, 2), 2, F)
    lines1 = lines1.reshape(-1, 3)
    img5, img6 = drawlines(img1, img2, lines1, pts1_filter, pts2_filter)

    # Plot the images:
    final_frame = cv2.hconcat((img3, img5))
    return final_frame


# Es realitza la Least Median Estimation donades les imatges i els punts característics. Útil tenir les estimacions
# separades per tal de poder fer les gràfiques comparatives. S'ha de tenir en compte que LMS és més lent que RANSAC.
def least_median_squares_estimation(img1, img2, pts1, pts2):
    F, mask = cv2.findFundamentalMat(pts1, pts2, cv2.FM_LMEDS)

    final_frame_LMS = draw_epipolar_lines(img1, img2, pts1, pts2, F, mask)
    show_image(final_frame_LMS, "Least Median Squares Image: ")


# De la mateixa manera que amb la funció anterior, realitzem una estimació eficient de la matriu fonamental mitjançant
# Random sample consensus (RANSAC).
def ransac_estimation(img1, img2, pts1, pts2):
    F, mask = cv2.findFundamentalMat(pts1, pts2, cv2.RANSAC)

    final_frame_RANSAC = draw_epipolar_lines(img1, img2, pts1, pts2, F, mask)
    show_image(final_frame_RANSAC, "RANSAC epipolar lines Image: ")
    return F, mask, final_frame_RANSAC


# =============================================
#       CAMERA POSE from Essential Matrix
# =============================================

# Useful functions:

def extractCameraPoses(E):
    u, d, v = np.linalg.svd(E)
    W = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])

    Rs, Cs = np.zeros((4, 3, 3)), np.zeros((4, 3))

    t = u[:, -1]
    R1 = u.dot(W.dot(v))
    R2 = u.dot(W.T.dot(v))

    if np.linalg.det(R1) < 0:
        R1 = R1 * - 1

    if np.linalg.det(R2) < 0:
        R2 = R2 * - 1
    return R1, R2, t


def plotCamera(R, t, ax, scale=0.5, depth=0.5, faceColor='grey'):
    C = -t  # Camera center (world coordinate system)

    # Generant els eixos de coordenades de la càmera.
    axes = np.zeros((3, 6))
    axes[0, 1], axes[1, 3], axes[2, 5] = 1, 1, 1

    # Transformar a sistema de coords món (world coordinate system)
    axes = R.T.dot(axes) + C[:, np.newaxis]

    # Fent el plot dels eixos
    ax.plot3D(xs=axes[0, :2], ys=axes[1, :2], zs=axes[2, :2], c='r')
    ax.plot3D(xs=axes[0, 2:4], ys=axes[1, 2:4], zs=axes[2, 2:4], c='g')
    ax.plot3D(xs=axes[0, 4:], ys=axes[1, 4:], zs=axes[2, 4:], c='b')

    # Generant 5 cantonades del polígon de la càmera (centre + 4 cantonades)
    pt1 = np.array([[0, 0, 0]]).T  # Centre de la càmera
    pt2 = np.array([[scale, -scale, depth]]).T  # A dalt a la dreta
    pt3 = np.array([[scale, scale, depth]]).T  # A baix a la dreta
    pt4 = np.array([[-scale, -scale, depth]]).T  # A dalt a l'esquerra
    pt5 = np.array([[-scale, scale, depth]]).T  # A baix a l'esquerra
    pts = np.concatenate((pt1, pt2, pt3, pt4, pt5), axis=-1)

    # Passar les coordenades càmera a coordenades món.
    pts = R.T.dot(pts) + C[:, np.newaxis]
    ax.scatter3D(xs=pts[0, :], ys=pts[1, :], zs=pts[2, :], c='k')

    # Vèrtexs pel polígon que es crearà a continuació.
    vertexs = [[pts[:, 0], pts[:, 1], pts[:, 2]], [pts[:, 0], pts[:, 2], pts[:, -1]],
               [pts[:, 0], pts[:, -1], pts[:, -2]], [pts[:, 0], pts[:, -2], pts[:, 1]]]

    # Generant el nou polígon
    ax.add_collection3d(Poly3DCollection(vertexs, facecolors=faceColor, linewidths=1, edgecolors='k', alpha=.25))


# Full process till ransac: (Funció que agrupa tot el process fet fins ara per tal de facilitar les següents proves)
def full_ransac_estimation(img1, img2, method="sift"):
    pts1, pts2 = fundamental_matrix_find_kp_and_match(img1, img2, method)
    F, mask, final_frame_RANSAC = ransac_estimation(img1, img2, pts1, pts2)
    return F, mask, final_frame_RANSAC, pts1, pts2


# Important funció en la qual generem una K sense saber cap propietat de la càmera, només basant-nos en una de
# les imatges. És útil pq ens permet continuar sense saber cap valor de la càmera.
def camera_internals_if_we_DONT_know_K(img1):
    width, height, _ = img1.shape
    focal_length = np.maximum(width, height)
    center = (height / 2, width / 2)

    K = np.array(
        [[focal_length, 0, center[0]],
         [0, focal_length, center[1]],
         [0, 0, 1]], dtype="double")
    return K


# ==============================================
# ESTIMATE CAMERA POSE FROM ESSENTIAL MATRIX
# ==============================================

# Triar quina de les 4 configuracions és la bona per al nostre moviment de càmera.
# Donades dues imatges, calcular SIFT -> MATCHING -> Estimació RANSAC, generar una estimació de K sense saber
# valors de la càmera, extreure les posicions de la càmera, mostrar les 4 configuracions de la càmera proposades a
# l'hora de realitzar les fotografies.
def estimate_camera_pose_and_draw(img1, img2, method="sift"):
    F, mask, final_frame_RANSAC, pts1, pts2 = full_ransac_estimation(img1, img2, method)
    cv2.imwrite('img/exports/final_frame_RANSAC.jpeg', final_frame_RANSAC)

    print("Número matches/punts després de full RANSAC: ", len(pts1))
    K = camera_internals_if_we_DONT_know_K(img1)
    # Estimate the Essential Matrix:
    E = K.T.dot(F.dot(K))

    R1, R2, t = extractCameraPoses(E)
    t = t[:, np.newaxis]

    # Variable axs per múltiples eixos:
    fig, axs = plt.subplots(2, 2, figsize=(20, 15))
    count = 1
    for i, R_ in enumerate([R1, R2]):
        for j, t_ in enumerate([t, -t]):
            axs[i, j] = fig.add_subplot(2, 2, count, projection='3d')
            axs[i, j].set_xlabel('X')
            axs[i, j].set_ylabel('Y')
            axs[i, j].set_zlabel('Z')
            axs[i, j].set_title('Configuració: ' + str(count))

            plotCamera(np.eye(3, 3), np.zeros((3,)), axs[i, j])
            plotCamera(R_, t_[:, 0], axs[i, j])
            count += 1
    plt.savefig("img/exports/configsPossibles.png")
    plt.show()
    return E, pts1, pts2, K


# Mitjançant aquesta funció, calculem i visualitzem quina de les 4 configuracions de càmera de la funció anterior ha
# triat l'algorisme segons els punts d'interés i característiques de la càmera introduits.
def checkForCheiralityCondition(E, pts1, pts2, K):
    _, R, t, mask = cv2.recoverPose(E, pts1, pts2, K)
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plotCamera(np.eye(3, 3), np.zeros((3,)), ax)
    plotCamera(R, t[:, 0], ax)
    plt.savefig("img/exports/confCameraTriada.png")
    plt.show()
    return R, t


# ==============================
#   A FIRST RECONSTRUCTION
# ==============================

# Funció mitjançant es fa una primera reconstrucció, obtenint un mapa de punts 3D, visualitzant per consola les
# diferents matrius calculades i finalment visualitzant una primera reconstrucció en el navegador mitjançant el mapa
# de punts calculat.
def firstReconstruction(pts1, pts2, K, R, t):
    R_t_0 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])  # First image
    R_t_1 = np.empty((3, 4))  # Second image

    R_t_1[:3, :3] = np.matmul(R, R_t_0[:3, :3])
    R_t_1[:3, :3] = R_t_0[:3, :3] + np.matmul(R_t_0[:3, :3], t.ravel())

    print("The R_t_0 \n", str(R_t_0))
    print("The R_t_1 \n", str(R_t_1))

    P1 = np.matmul(K, R_t_0)
    P2 = np.matmul(K, R_t_1)

    print("The Projection Matrix 1: \n", str(P1))
    print("The Projection Matrix 2: \n", str(P2))

    pts3d = getTriangulatedPoints(pts1, pts2, K, R, t, cv2.triangulatePoints)
    print("Número de punts3D: ", len(pts3d))
    fig = go.Figure(data=[go.Scatter3d(x=pts3d[:, 0], y=pts3d[:, 1], z=pts3d[:, 2], mode='markers', marker=dict(
        size=2,
        color='red',
        opacity=0.8
    ))])
    fig.update_layout(autosize=False, width=900, height=900)
    fig.show()
    return pts3d


# Funció necessaria per tal de calcular els punts 3d donats uns punts 2d, conf de la càmera i una funció de
# triangulació.
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


# ===================================
#       BUNDLE ADJUSTMENT / DEBUGGING ZONE
# ===================================

"""
 A partir d'aquí comença la zona de codi perillós. Entrar sota la teva responsabilitat.
 Són intents de texturitzar / crear una mesh / algo per tal de generar un model 3D texturitzat.
 També s'han copiat funcions existents i modificat per tal de debugar sense petar el codi que ja funciona. Permetint 
 afegir returns extres, modificar els tipus de variables etc per tal d'intentar que funcioni la texturització.
 Aquestes funcions tenen com a prefix TEMP (temporal).
"""


def lowes(keypt1, keypt2, matches):
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


def texture_mapping_sift(model_3d, matches, keypoints, texture_images):
    # Crear una malla 3D a partir del modelo 3D reconstruido
    vertices = np.array(model_3d)
    triangles = np.array([[0, 1, 2]])  # Define los índices de los vértices que forman los triángulos
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(vertices)
    mesh.triangles = o3d.utility.Vector3iVector(triangles)

    # Convertir mesh.vertices a un array NumPy para obtener las dimensiones
    vertices_np = np.asarray(mesh.vertices)
    num_vertices = vertices_np.shape[0]

    # Crear la textura de la malla utilizando las imágenes de textura
    texture_coords = []
    for match in matches:
        query_idx = match.queryIdx
        train_idx = match.trainIdx
        point_2d = keypoints[0][query_idx].pt
        texture_coords.append([point_2d[0], point_2d[1]])
    texture_coords = np.array(texture_coords)

    # Alinear las coordenadas de textura al rango [0, 1]
    texture_coords[:, 0] /= max(texture_images[0].shape[1], texture_images[1].shape[1])
    texture_coords[:, 1] /= max(texture_images[0].shape[0], texture_images[1].shape[0])

    # Crear una imagen de textura combinando las imágenes de textura
    texture = np.zeros((num_vertices, 1, 3), dtype=np.uint8)
    for match in matches:
        query_idx = match.queryIdx
        train_idx = match.trainIdx
        point_3d = int(round(match.distance))  # Utiliza la distancia del match como índice 3D
        if point_3d > texture.shape[0]:
            continue
        point_2d = keypoints[0][query_idx].pt
        image_index = 0 if point_2d[0] < texture_images[0].shape[1] else 1
        texture[point_3d, 0] = cv2.cvtColor(texture_images[image_index][int(point_2d[1]), int(point_2d[0])],
                                            cv2.COLOR_BGR2RGB)

    # Asignar la textura a la malla
    mesh.texture = o3d.geometry.Image(texture)

    # Crear el visor 3D para visualizar el modelo texturizado
    vis = o3d.visualization.VisualizerWithKeyCallback()
    vis.create_window()
    vis.add_geometry(mesh)
    vis.run()
    vis.destroy_window()


def TEMP_fundamental_matrix_find_kp_and_match(img1, img2):
    # Implementació més a força bruta i que no trobarà els millors resultats.
    # img1 = cv2.imread(im_name1, 0)
    # img2 = cv2.imread(im_name2, 0)

    sift = cv2.SIFT_create()

    # Find Keypoints and descriptors with SIFT
    keypt1, descr1 = sift.detectAndCompute(img1, None)
    keypt2, descr2 = sift.detectAndCompute(img2, None)

    # FLANN parameters:
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(descr1, descr2, k=2)
    pts1 = []
    pts2 = []
    matchesMini = []
    # Ratio test as per Lowe's paper:
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.8 * n.distance:
            pts2.append(keypt2[m.trainIdx].pt)
            pts1.append(keypt1[m.queryIdx].pt)
            matchesMini.append(m)
            matchesMini.append(n)
    pts1 = np.int32(pts1)
    pts2 = np.int32(pts2)
    return pts1, pts2, matches, [keypt1, keypt2], matchesMini


# Funció per convertir els matches donats per FLANN amb la seva estructura característica de tuples a una feta de
# llistes. Utilitzada a l'hora de debugar i anar provant altres funcions que necessitaves com a input una llista de
# matches en comptes d'una tupla de tuples
def convert_matches_to_list(matches):
    matches_list = []
    for match_tuple in matches:
        for match in match_tuple:
            matches_list.append(cv2.DMatch(match.queryIdx, match.trainIdx, match.distance))
    return matches_list


def brute_force_Harris(im1):
    gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    # find Harris corners
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, 2, 3, 0.04)
    print("Corner harris dist: ", len(dst))
    dst = cv2.dilate(dst, None)
    print("Corner harris dist després dilate: ", len(dst))
    ret, dst = cv2.threshold(dst, 0.01 * dst.max(), 255, 0)
    dst = np.uint8(dst)
    # find centroids
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
    # define the criteria to stop and refine the corners
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(gray, np.float32(centroids), (5, 5), (-1, -1), criteria)
    # Now draw them
    res = np.hstack((centroids, corners))
    res = np.intp(res)
    print("Res Hariis: ", len(res))
    im1[res[:, 1], res[:, 0]] = [0, 0, 255]
    im1[res[:, 3], res[:, 2]] = [0, 255, 0]

    show_image(im1, "Harris image: ", False)
    # show_image(im1, "Harris image COLOR: ", True)
    return im1


def brute_force_ORB(im1, im2):
    sift = cv2.ORB_create()

    # Find keypoints
    keypoint1, descriptor1 = sift.detectAndCompute(im1, None)
    keypoint2, descriptor2 = sift.detectAndCompute(im2, None)

    # Create BF matcher object
    #   NOTE:
    #       * cv2.NORM_L2: It is good for SIFT, SURF, etc.
    #       * cv2.NORM_HAMMING: It is good for binary string-based descriptors like ORB, BRIEF, BRISK
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    matches = bf.match(descriptor1, descriptor2)

    matches = sorted(matches, key=lambda x: x.distance)

    SIFT_matches = cv2.drawMatches(im1, keypoint1, im2, keypoint2, matches[:200], None, flags=2)
    show_image(SIFT_matches, "ORB matches: ")
    return keypoint1, keypoint2, matches


def full_ransac_estimation_ORB(img1, img2):
    # kp1, kp2, matches = brute_force_ORB(img1, img2)
    # pts1, pts2 = lowes(kp1, kp2, matches)
    pts1, pts2 = fundamental_matrix_find_kp_and_match_ORB(img1, img2)
    F, mask, final_frame_RANSAC = ransac_estimation(img1, img2, pts1, pts2)
    return F, mask, final_frame_RANSAC, pts1, pts2


def estimate_camera_pose_and_draw_ORB(img1, img2):
    F, mask, final_frame_RANSAC, pts1, pts2 = full_ransac_estimation_ORB(img1, img2)
    K = camera_internals_if_we_DONT_know_K(img1)
    # Estimate the Essential Matrix:
    E = K.T.dot(F.dot(K))

    R1, R2, t = extractCameraPoses(E)
    t = t[:, np.newaxis]

    # Variable axs per múltiples eixos:
    fig, axs = plt.subplots(2, 2, figsize=(20, 15))
    count = 1
    for i, R_ in enumerate([R1, R2]):
        for j, t_ in enumerate([t, -t]):
            axs[i, j] = fig.add_subplot(2, 2, count, projection='3d')
            axs[i, j].set_xlabel('X')
            axs[i, j].set_ylabel('Y')
            axs[i, j].set_zlabel('Z')
            axs[i, j].set_title('Configuració: ' + str(count))

            plotCamera(np.eye(3, 3), np.zeros((3,)), axs[i, j])
            plotCamera(R_, t_[:, 0], axs[i, j])
            count += 1
    plt.show()
    return E, pts1, pts2, K


def fundamental_matrix_find_kp_and_match_ORB(img1, img2):
    # Implementació més a força bruta i que no trobarà els millors resultats.
    # img1 = cv2.imread(im_name1, 0)
    # img2 = cv2.imread(im_name2, 0)
    start_orb = time.time()
    algorithm = cv2.ORB_create()

    # Find Keypoints and descriptors with SIFT / the selected algorithm
    keypt1, descr1 = algorithm.detectAndCompute(img1, None)
    keypt2, descr2 = algorithm.detectAndCompute(img2, None)
    print("Time ORB: ", time.time() - start_orb)
    print("Keypoints 1 ORB: ", len(keypt1))
    print("Keypoints 2 ORB: ", len(keypt2))
    showKeyPoints(img1, keypt1, 'img/exports/', 'orb_img1_keypoints.jpeg')
    showKeyPoints(img2, keypt2, 'img/exports/', 'orb_img2_keypoints.jpeg')
    # FLANN parameters:
    FLANN_INDEX_LSH = 6
    index_params = dict(algorithm=FLANN_INDEX_LSH,
                        table_number=6,  # was 12
                        key_size=12,  # was 20
                        multi_probe_level=1)  # was 2
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(descr1, descr2, k=2)
    pts1 = []
    pts2 = []
    print("MATCHES  ORB: ", len(matches))

    # Ratio test as per Lowe's paper:
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.8 * n.distance:
            pts2.append(keypt2[m.trainIdx].pt)
            pts1.append(keypt1[m.queryIdx].pt)
    pts1 = np.int32(pts1)
    pts2 = np.int32(pts2)

    print("Good matches: ", len(pts2))

    return pts1, pts2


def harrisImplementation(inputFolder, img_name, expFolder):
    # path to input image specified and
    # image is loaded with imread command
    image = cv2.imread(inputFolder + img_name)

    # convert the input image into
    # grayscale color space
    operatedImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # modify the data type
    # setting to 32-bit floating point
    operatedImage = np.float32(operatedImage)

    # apply the cv2.cornerHarris method
    # to detect the corners with appropriate
    # values as input parameters
    dest = cv2.cornerHarris(operatedImage, 2, 5, 0.07)

    # Results are marked through the dilated corners
    dest = cv2.dilate(dest, None)
    print("Longitud de dest Harris img -> ", img_name, ": ", len(dest))
    temp = dest > 0.01 * dest.max()
    print("Operació rara: ", np.count_nonzero(temp))
    # Reverting back to the original image,
    # with optimal threshold value
    temp = image
    image[dest > 0.01 * dest.max()] = [0, 0, 255]
    resta = image[:,:, 2] - temp[:,:,2]
    print("Resta img: ",(image.shape[0] * image.shape[1]) - (np.count_nonzero(image[:,:,2] -255)))
    cv2.imwrite(expFolder + img_name, image)
    # the window showing output image with corners
    cv2.imshow('Image with Borders', image)

    # De-allocate any associated memory usage
    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()

def showKeyPoints(img, keypoints, expfolder, im_name):

    img_SIFT_1 = cv2.drawKeypoints(img, keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imwrite(expfolder + im_name, img_SIFT_1)
# ====================================================
#           MAIN - EXECUCIÓ PRINCIPAL
# ====================================================

if __name__ == '__main__':
    print('Starting...')
    folder = 'img/base/'
    expFolder = 'img/exports/'
    method = "sift"
    image_names = load_images_from_folder(folder)
    print(image_names)

    # Order names of the images because in some OS they are ordered different, so we order them alphabetically.
    image_names = sorted(image_names)
    print(image_names)

    # Use only the new images: -- Triar quines imatges voldrem fer servir en aquesta execució
    image_names = image_names[16:18]
    print("New images that will be used in this execution: ", image_names)
    # ================================
    #       LOAD AND SHOW IMAGES
    # ================================

    for im1_name, im2_name in zip(image_names[0::2], image_names[1::2]):
        # 1. Feature Matching and Outlier rejection using RANSAC
        img1, img2, frame = load_and_plot_images(folder + im1_name, folder + im2_name)
        """
        frame_SIFT = extract_keypoints_feature_descriptors_and_matching(img1, img2)
        cv2.imwrite(expFolder+'frameSIFT_imgs.jpeg', frame_SIFT)
        extract_keypoints_with_one_SIFT(img1, img2)
        a, kp1_sift, kp2_sift = brute_force_SIFT(img1, img2)
        showKeyPoints(img1, kp1_sift, expFolder, 'keypoints_RAW_SIFT_'+im1_name)
        showKeyPoints(img2, kp2_sift, expFolder, 'keypoints_RAW_SIFT_'+im2_name)
        """
        # 2. Estimating Fundamental Matrix
        # pts1, pts2 = fundamental_matrix_find_kp_and_match(folder + im1_name, folder + im2_name)
        # least_median_squares_estimation(img1, img2, pts1, pts2)
        # ransac_estimation(img1, img2, pts1, pts2)
        # harrisImplementation(folder, im1_name, expFolder)
        # harrisImplementation(folder, im2_name, expFolder)
        # img1_harris = brute_force_Harris(img1)
        # img2_harris = brute_force_Harris(img2)
        # HARRIS_matches = cv2.drawMatches(img1_harris, keypoint1, img2_harris, keypoint2, matches[:200], None, flags=2)
        # show_image(SIFT_matches, "SIFT matches: ")
        # ====================== INICI SIFT -> Mapa de punts 3D ==============================
        # A "Estimate_camera_pose_and_draw() ja es realitza full_ransac_estimation(SIFT->Matching->RANSAC)
        start_time = time.time()
        #E, pts1, pts2, K = estimate_camera_pose_and_draw_ORB(img1, img2)
        E, pts1, pts2, K = estimate_camera_pose_and_draw(img1, img2, method)
        R, t = checkForCheiralityCondition(E, pts1, pts2, K)
        firstReconstruction(pts1, pts2, K, R, t)
        end_time = time.time()
        
        print("Temps d'execució del SIFT + Matching + Reconstrucció: ", end_time-start_time, " segons")
        

        # ====================== FI INICI SIFT -> Mapa de punts 3D ===========================
        """
        # FALTA DEBUGAR CORRECTAMENT: 
        E, pts1, pts2, K = estimate_camera_pose_and_draw(img1, img2)
        R, t = checkForCheiralityCondition(E, pts1, pts2, K)
        pts3d = getTriangulatedPoints(pts1, pts2, K, R, t, cv2.triangulatePoints)

        pts1TEMP, pts2TEMP, matches, keypoints, matchesMini = TEMP_fundamental_matrix_find_kp_and_match(img1, img2)
        texture_images = [img1, img2]
        # matchList = convert_matches_to_list(matches)
        texture_mapping_sift(pts3d, matchesMini, keypoints, texture_images)
        """
    print("End of the program.")
    # Si es veu aquest print és que tot ha anat bé :) (igual que si es veu Process finished with exit code 0.


