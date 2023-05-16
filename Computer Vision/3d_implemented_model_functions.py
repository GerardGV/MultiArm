import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import open3d as o3d
import plotly.graph_objects as go


def show_image(img, title="Imatge", color=False):
    plt.figure()
    if color:
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    else:
        plt.imshow(img)
    plt.title(title)
    plt.show()


def load_images_from_folder(folder):
    image_names = []  # List where we are going to save the names of the images in the folder
    for path in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, path)):
            image_names.append(path)
    return image_names


def load_and_plot_images(image_name1="/img/base/img1_1_glasses_openEyes_Pol.jpeg",
                         image_name2="/img/base/img1_2_glasses_openEyes_Pol.jpeg"):
    img1 = cv2.imread(image_name1)
    img2 = cv2.imread(image_name2)

    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
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
    return SIFT_matches


# ============================================
# FUNDEMENTAL MATRIX:
# ============================================

def fundamental_matrix_find_kp_and_match(img1, img2):
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

    # Ratio test as per Lowe's paper:
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.8 * n.distance:
            pts2.append(keypt2[m.trainIdx].pt)
            pts1.append(keypt1[m.queryIdx].pt)
    pts1 = np.int32(pts1)
    pts2 = np.int32(pts2)
    return pts1, pts2


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


def least_median_squares_estimation(img1, img2, pts1, pts2):
    F, mask = cv2.findFundamentalMat(pts1, pts2, cv2.FM_LMEDS)

    final_frame_LMS = draw_epipolar_lines(img1, img2, pts1, pts2, F, mask)
    show_image(final_frame_LMS, "Least Median Squares Image: ")


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


# Full process till ransac:
def full_ransac_estimation(img1, img2):
    pts1, pts2 = fundamental_matrix_find_kp_and_match(img1, img2)
    F, mask, final_frame_RANSAC = ransac_estimation(img1, img2, pts1, pts2)
    return F, mask, final_frame_RANSAC, pts1, pts2


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
def estimate_camera_pose_and_draw(img1, img2):
    F, mask, final_frame_RANSAC, pts1, pts2 = full_ransac_estimation(img1, img2)
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
    return E, pts1, pts2, K


def checkForCheiralityCondition(E, pts1, pts2, K):
    _, R, t, mask = cv2.recoverPose(E, pts1, pts2, K)
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plotCamera(np.eye(3, 3), np.zeros((3,)), ax)
    plotCamera(R, t[:, 0], ax)
    return R, t


# ==============================
#   A FIRST RECONSTRUCTION
# ==============================

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

    fig = go.Figure(data=[go.Scatter3d(x=pts3d[:, 0], y=pts3d[:, 1], z=pts3d[:, 2], mode='markers', marker=dict(
        size=2,
        color='red',
        opacity=0.8
    ))])
    fig.update_layout(autosize=False, width=900, height=900)
    fig.show()



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
#       BUNDLE ADJUSTMENT
# ===================================
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
        texture[point_3d, 0] = cv2.cvtColor(texture_images[image_index][int(point_2d[1]), int(point_2d[0])], cv2.COLOR_BGR2RGB)

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
    return pts1, pts2, matches, [keypt1,keypt2], matchesMini

def convert_matches_to_list(matches):
    matches_list = []
    for match_tuple in matches:
        for match in match_tuple:
            matches_list.append(cv2.DMatch(match.queryIdx, match.trainIdx, match.distance))
    return matches_list
if __name__ == '__main__':
    print('Starting...')
    folder = 'img/base/'
    image_names = load_images_from_folder(folder)
    print(image_names)

    # Order names of the images because in some OS they are ordered different, so we order them alphabetically.
    image_names = sorted(image_names)
    print(image_names)
    # Use only the new images:
    image_names = image_names[18:]
    print("New images that will be used in this execution: ", image_names)
    # ================================
    #       LOAD AND SHOW IMAGES
    # ================================
    for im1_name, im2_name in zip(image_names[0::2], image_names[1::2]):
        # 1. Feature Matching and Outlier rejection using RANSAC
        img1, img2, frame = load_and_plot_images(folder + im1_name, folder + im2_name)
        # frame_SIFT = extract_keypoints_feature_descriptors_and_matching(img1, img2)
        # extract_keypoints_with_one_SIFT(img1, img2)
        # brute_force_SIFT(img1, img2)
        # 2. Estimating Fundamental Matrix
        # pts1, pts2 = fundamental_matrix_find_kp_and_match(folder + im1_name, folder + im2_name)
        # least_median_squares_estimation(img1, img2, pts1, pts2)
        # ransac_estimation(img1, img2, pts1, pts2)


        #E, pts1, pts2, K = estimate_camera_pose_and_draw(img1, img2)
        #R, t = checkForCheiralityCondition(E, pts1, pts2, K)
        #firstReconstruction(pts1, pts2, K, R, t)

        E, pts1, pts2, K = estimate_camera_pose_and_draw(img1, img2)
        R, t = checkForCheiralityCondition(E, pts1, pts2, K)
        pts3d = getTriangulatedPoints(pts1, pts2, K, R, t, cv2.triangulatePoints)

        pts1TEMP, pts2TEMP, matches, keypoints, matchesMini = TEMP_fundamental_matrix_find_kp_and_match(img1, img2)
        texture_images = [img1, img2]
        # matchList = convert_matches_to_list(matches)
        texture_mapping_sift(pts3d, matchesMini, keypoints, texture_images)



    print("End of the program.")
