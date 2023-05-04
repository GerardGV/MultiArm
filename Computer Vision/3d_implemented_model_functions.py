import cv2
import numpy as np
from matplotlib import pyplot as plt
import os


def show_image(img, title="Imatge"):
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

def fundamental_matrix_find_kp_and_match(im_name1, im_name2):
    img1 = cv2.imread(im_name1, 0)
    img2 = cv2.imread(im_name2, 0)

    sift = cv2.SIFT_create()

    # Find Keypoints and descriptors with SIFT
    keypt1, descr1 = sift.detectAndCompute(img1, None)
    keypt2, descr2 = sift.detectAndCompute(img2, None)

    # FLANN parameters:
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(descr1, descr2)
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
    r, c = img1.shape
    img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
    img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)

    for r, pt1, pt2 in zip(lines, pts1, pts2):
        color = tuple(np.random.randint(0, 255, 3).tolist())
        x0, y0 = map(int, [0, -r[2] / r[1]])
        x1, y1 = map(int, [c, -(r[2] + r[0] * c) / r[1]])
        img1 = cv2.line(img1, (x0, y0), (x1, y1), color, 1)
        img1 = cv2.circle(img1, tuple(pt1), 5, color, -1)
        img2 = cv2.circle(img2, tuple(pt2), 5, color, -1)
    return img1, img2


if __name__ == '__main__':
    print('Starting...')
    folder = 'img/base/'
    image_names = load_images_from_folder(folder)
    print(image_names)

    # Order names of the images because in some OS they are ordered different, so we order them alphabetically.
    image_names = sorted(image_names)
    print(image_names)
    # ================================
    #       LOAD AND SHOW IMAGES
    # ================================
    for im1_name, im2_name in zip(image_names[0::2], image_names[1::2]):
        # 1. Feature Matching and Outlier rejection using RANSAC
        img1, img2, frame = load_and_plot_images(folder + im1_name, folder + im2_name)
        frame_SIFT = extract_keypoints_feature_descriptors_and_matching(img1, img2)
        extract_keypoints_with_one_SIFT(img1, img2)
        brute_force_SIFT(img1, img2)
        # 2. Estimating Fundamental Matrix

    print("End of the program.")
